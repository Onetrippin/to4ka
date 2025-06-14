from datetime import datetime
from typing import Any, Dict, List, Literal
from uuid import UUID

from django.db import IntegrityError, transaction
from django.db.models import F, Q, Subquery
from django.utils import timezone

from app.internal.data.models.balance import Balance
from app.internal.data.models.order import Order
from app.internal.data.models.tool import Tool
from app.internal.data.models.trade import Trade
from app.internal.domain.entities.order import LimitOrderListBody, MarketOrderListBody
from app.internal.domain.interfaces.order import IOrderRepository


class OrderRepository(IOrderRepository):
    def get_order_list(self, user_id: UUID) -> List[Dict[str, Any]]:
        return list(
            Order.objects.filter(user_id=user_id).values(
                'id',
                'status',
                'user_id',
                'created_at',
                'direction',
                'tool__ticker',
                'quantity',
                'price',
                'filled',
                'type',
            )
        )

    def get_order(self, user_id: UUID, order_id: UUID) -> Dict[str, Any]:
        return (
            Order.objects.filter(user_id=user_id, id=order_id)
            .values(
                'id',
                'status',
                'user_id',
                'created_at',
                'direction',
                'tool__ticker',
                'quantity',
                'price',
                'filled',
                'type',
            )
            .first()
        )

    def cancel_order(self, user_id: UUID, order_id: UUID) -> bool:
        updated_order = Order.objects.filter(
            user_id=user_id, id=order_id, status__in=['NEW', 'PARTIALLY_EXECUTED']
        ).update(
            status='CANCELLED',
            closed_at=timezone.now(),
        )
        try:
            ticker, qty, filled, direction, price = (
                Order.objects.filter(id=order_id)
                .values_list(
                    'tool__ticker',
                    'quantity',
                    'filled',
                    'direction',
                    'price',
                )
                .first()
            )
            remaining_reserved = qty - filled
        except TypeError:
            return False

        if updated_order:
            if direction == 'BUY':
                ticker = 'RUB'
                remaining_reserved = remaining_reserved * price
            Balance.objects.filter(user_id=user_id, tool__ticker=ticker).update(
                amount=F('amount') + remaining_reserved, reserved_amount=F('reserved_amount') - remaining_reserved
            )
            return True
        return False

    def get_levels_info(self, ticker: str, limit: int) -> tuple:
        statuses = ['NEW', 'PARTIALLY_EXECUTED']

        bid_orders = Order.objects.filter(tool__ticker=ticker, direction='BUY', status__in=statuses, type='limit')[
            :limit
        ].values('price', 'quantity', 'filled')

        ask_orders = Order.objects.filter(tool__ticker=ticker, direction='SELL', status__in=statuses, type='limit')[
            :limit
        ].values('price', 'quantity', 'filled')

        return bid_orders, ask_orders

    def get_trans_list(self, ticker: str, limit: int) -> list:
        return list(
            Trade.objects.filter(tool__ticker=ticker)[:limit].values('tool__ticker', 'quantity', 'price', 'date')
        )

    def get_opposite_limit_orders_for_market(
        self, direction: Literal['BUY', 'SELL'], ticker: str, user_id: UUID
    ) -> List[Dict[str, Any]]:
        return list(
            Order.objects.filter(
                tool__ticker=ticker,
                direction='SELL' if direction == 'BUY' else 'BUY',
                status__in=['NEW', 'PARTIALLY_EXECUTED'],
                type='limit',
            )
            .exclude(user_id=user_id)
            .order_by('price' if direction == 'BUY' else '-price')
            .values('id', 'price', 'quantity', 'filled', 'tool_id', 'user_id')
        )

    def get_opposite_limit_orders_for_limit(
        self, direction: Literal['BUY', 'SELL'], ticker: str, price: int, user_id: UUID
    ) -> List[Dict[str, Any]]:
        return list(
            Order.objects.filter(
                tool__ticker=ticker,
                direction='SELL' if direction == 'BUY' else 'BUY',
                status__in=['NEW', 'PARTIALLY_EXECUTED'],
                type='limit',
            )
            .filter(Q(price__lte=price) if direction == 'BUY' else Q(price__gte=price))
            .exclude(user_id=user_id)
            .order_by('price' if direction == 'BUY' else '-price')
            .values('id', 'price', 'quantity', 'filled', 'tool_id', 'user_id')
        )

    def create_market_order(
        self,
        user_id: UUID,
        order_data: MarketOrderListBody,
        status: str,
    ) -> UUID | None:
        try:
            return Order.objects.create(
                user_id=user_id,
                tool_id=Subquery(Tool.objects.filter(ticker=order_data.ticker).values('id')[:1]),
                direction=order_data.direction,
                type='market',
                quantity=order_data.qty,
                status=status,
                closed_at=timezone.now(),
            ).id
        except IntegrityError:
            return

    def execute_market_order(self, trades_info: dict, order_data: MarketOrderListBody) -> UUID | None:
        with transaction.atomic():
            order_id = self.create_market_order(trades_info['user_id'], order_data, 'EXECUTED')
            if not order_id:
                return
            trades_info['order_id'] = order_id
            self.create_trades(trades_info=trades_info)
            self.update_balances(trades_info=trades_info)
            self.update_order_status(trades_info=trades_info)
            return order_id

    def execute_limit_order(
        self, trades_info: dict, order_data: LimitOrderListBody, status: str = None, filled: int = 0
    ) -> UUID | None:
        with transaction.atomic():
            if trades_info['trades']:
                order_id = self.create_limit_order(
                    trades_info['user_id'], order_data, status, filled, timezone.now() if status == 'EXECUTED' else None
                )
                if not order_id:
                    return
                trades_info['order_id'] = order_id
                self.create_trades(trades_info=trades_info)
                self.update_balances(trades_info=trades_info)
                self.update_order_status(trades_info=trades_info)
                return order_id
            else:
                if order_data.direction == 'BUY':
                    ticker = 'RUB'
                    amount = order_data.price * order_data.qty
                else:
                    ticker = order_data.ticker
                    amount = order_data.qty
                Balance.objects.filter(user_id=trades_info['user_id'], tool__ticker=ticker).update(
                    amount=F('amount') - amount, reserved_amount=F('reserved_amount') + amount
                )
                order_id = self.create_limit_order(trades_info['user_id'], order_data, 'NEW', closed_at=None)
                if order_id:
                    return order_id
                return

    def update_order_status(self, trades_info: dict) -> None:
        orders_info = []
        for trade in trades_info['trades']:
            filled = trade['init_filled'] + trade['quantity']
            status = 'EXECUTED' if trade['init_quantity'] == filled else 'PARTIALLY_EXECUTED'
            orders_info.append(
                {
                    'order_id': trade['match_order_id'],
                    'filled': filled,
                    'status': status,
                    'closed_at': timezone.now() if status == 'EXECUTED' else None,
                }
            )
        orders = list(Order.objects.filter(id__in=[trade['match_order_id'] for trade in trades_info['trades']]))
        order_map = {order.id: order for order in orders}
        for order_info in orders_info:
            order = order_map.get(order_info['order_id'])
            if order:
                order.filled = order_info['filled']
                order.status = order_info['status']
                order.closed_at = order_info['closed_at']

        Order.objects.bulk_update(orders, ['filled', 'status', 'closed_at'])

    def create_trades(self, trades_info: dict) -> None:
        Trade.objects.bulk_create(
            [
                Trade(
                    bid_id=trades_info['order_id'] if trades_info['direction'] == 'BUY' else trade['match_order_id'],
                    ask_id=trade['match_order_id'] if trades_info['direction'] == 'BUY' else trades_info['order_id'],
                    buyer_id=trades_info['user_id'] if trades_info['direction'] == 'BUY' else trade['user_id'],
                    seller_id=trade['user_id'] if trades_info['direction'] == 'BUY' else trades_info['user_id'],
                    tool_id=trade['tool_id'],
                    quantity=trade['quantity'],
                    price=trade['price'],
                    date=timezone.now(),
                )
                for trade in trades_info['trades']
            ]
        )

    def update_balances(self, trades_info: dict) -> None:
        rub_tool_id = Tool.objects.filter(ticker='RUB').values_list('id', flat=True).first()
        deltas = {}
        net_rub_change = 0
        net_tool_change = 0
        quantities = 0
        for trade in trades_info['trades']:
            cost = trade['quantity'] * trade['price']
            quantities += trade['quantity']
            if trades_info['direction'] == 'BUY':
                deltas.setdefault((trade['user_id'], rub_tool_id), [0, 0])[0] += cost
                deltas.setdefault((trade['user_id'], trade['tool_id']), [0, 0])[1] -= trade['quantity']
                net_rub_change -= cost
                net_tool_change += trade['quantity']
            else:
                deltas.setdefault((trade['user_id'], rub_tool_id), [0, 0])[1] -= cost
                deltas.setdefault((trade['user_id'], trade['tool_id']), [0, 0])[0] += trade['quantity']
                net_rub_change += cost
                net_tool_change -= trade['quantity']
        if net_rub_change != 0:
            if net_rub_change < 0 and quantities < trades_info['quantity']:
                diff = trades_info['quantity'] - quantities
                deltas.setdefault((trades_info['user_id'], rub_tool_id), [0, 0])[1] += diff * trades_info['price']
            deltas.setdefault((trades_info['user_id'], rub_tool_id), [0, 0])[0] += net_rub_change
        if net_tool_change != 0:
            tool_id = trades_info['trades'][0]['tool_id']
            if net_tool_change < 0 and quantities < trades_info['quantity']:
                reserved_tool = trades_info['quantity'] + net_tool_change
                deltas.setdefault((trades_info['user_id'], tool_id), [0, 0])[0] -= trades_info['quantity']
                deltas.setdefault((trades_info['user_id'], tool_id), [0, 0])[1] += reserved_tool
            else:
                deltas.setdefault((trades_info['user_id'], tool_id), [0, 0])[0] += net_tool_change
        q_objects = Q()
        for (uid, tid) in deltas:
            q_objects |= Q(user_id=uid, tool_id=tid)
        balances = list(Balance.objects.filter(q_objects))
        balance_map = {(b.user_id, b.tool_id): b for b in balances}
        existing_balances = []
        new_balances = []
        for (uid, tid), (amount_delta, reserved_delta) in deltas.items():
            balance = balance_map.get((uid, tid))
            if not balance:
                balance = Balance(user_id=uid, tool_id=tid, amount=0, reserved_amount=0)
                new_balances.append(balance)
                balance_map[(uid, tid)] = balance
            else:
                existing_balances.append(balance)
            balance.amount += amount_delta
            balance.reserved_amount += reserved_delta
        if new_balances:
            Balance.objects.bulk_create(new_balances)
        Balance.objects.bulk_update(existing_balances + new_balances, ['amount', 'reserved_amount'])

    def create_limit_order(
        self,
        user_id: UUID,
        order_data: LimitOrderListBody,
        status: str,
        filled: int = 0,
        closed_at: datetime | None = timezone.now(),
    ) -> UUID | None:
        try:
            return Order.objects.create(
                user_id=user_id,
                tool_id=Subquery(Tool.objects.filter(ticker=order_data.ticker).values('id')[:1]),
                direction=order_data.direction,
                type='limit',
                price=order_data.price,
                quantity=order_data.qty,
                status=status,
                filled=filled,
                closed_at=closed_at,
            ).id
        except IntegrityError:
            return
