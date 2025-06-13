from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from django.db import transaction
from django.db.models import Q, Subquery
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

    def update_order_status(
        self, order_id: UUID, status: str, filled: Optional[int], closed_at: Optional[datetime]
    ) -> None:
        update_fields: Dict[str, Any] = {'status': status}
        if filled is not None:
            update_fields['filled'] = filled
        if closed_at is not None:
            update_fields['closed_at'] = closed_at

        return Order.objects.filter(id=order_id).update(**update_fields)

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

    def cancel_order(self, user_id: UUID, order_id: UUID) -> None:
        updated_order = Order.objects.filter(user_id=user_id, id=order_id).update(
            status='CANCELLED',
            closed_at=timezone.now(),
        )

        if updated_order:
            Order.objects.filter(user_id=user_id, id=order_id).delete()

    def get_levels_info(self, ticker: str, limit: int) -> tuple:
        statuses = ['NEW', 'PARTIALLY_EXECUTED']

        bid_orders = Order.objects.filter(tool__ticker=ticker, direction='BUY', status__in=statuses, type='limit')[
            :limit
        ].values('price', 'quantity')

        ask_orders = Order.objects.filter(tool__ticker=ticker, direction='SELL', status__in=statuses, type='limit')[
            :limit
        ].values('price', 'quantity')

        return bid_orders, ask_orders

    def get_trans_list(self, ticker: str, limit: int) -> list:
        return list(Trade.objects.filter(tool__ticker=ticker).values('tool__ticker', 'quantity', 'price', 'date'))

    def get_opposite_limit_orders_for_market(
        self, direction: Literal['BUY', 'SELL'], ticker: str
    ) -> List[Dict[str, Any]]:
        return list(
            Order.objects.filter(
                tool__ticker=ticker,
                direction='SELL' if direction == 'BUY' else 'BUY',
                status__in=['NEW', 'PARTIALLY_EXECUTED'],
                type='limit',
            )
            .order_by('price' if direction == 'BUY' else '-price')
            .values('id', 'price', 'quantity', 'filled', 'tool_id', 'user_id')
        )

    def get_opposite_limit_orders_for_limit(
        self, direction: Literal['BUY', 'SELL'], ticker: str, price: float
    ) -> List[Dict[str, Any]]:
        return list(
            Order.objects.filter(
                tool__ticker=ticker,
                direction='SELL' if direction == 'BUY' else 'BUY',
                status__in=['NEW', 'PARTIALLY_EXECUTED'],
                type='limit',
            )
            .filter(Q(price__lte=price) if direction == 'BUY' else Q(price__gte=price))
            .order_by('price' if direction == 'BUY' else '-price')
            .values('id', 'price', 'quantity', 'filled', 'tool_id')
        )

    def create_market_order(
        self,
        user_id: UUID,
        order_data: MarketOrderListBody,
        status: str,
    ) -> UUID:
        return Order.objects.create(
            user_id=user_id,
            tool_id=Subquery(Tool.objects.filter(ticker=order_data.ticker).values('id')[:1]),
            direction=order_data.direction,
            type='market',
            quantity=order_data.qty,
            status=status,
            closed_at=timezone.now(),
        ).id

    def execute_market_order(self, trades_info: dict, order_data: MarketOrderListBody) -> UUID:
        with transaction.atomic:
            self.create_trades(trades_info=trades_info)
            self.update_balances(trades_info=trades_info)
            return self.create_market_order(trades_info['user_id'], order_data, 'EXECUTED')

    def create_trades(self, trades_info: dict) -> None:
        Trade.objects.bulk_create(
            [
                Trade(
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
        for trade in trades_info['trades']:
            cost = trade['quantity'] * trade['price']
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
            deltas.setdefault((trades_info['user_id'], rub_tool_id), [0, 0])[0] += net_rub_change
        if net_tool_change != 0:
            tool_id = trades_info['trades'][0]['tool_id']
            deltas.setdefault((trades_info['user_id'], tool_id), [0, 0])[0] += net_tool_change
        keys = list(deltas.keys())
        user_ids = list({uid for uid, _ in keys})
        tool_ids = list({tid for _, tid in keys})
        balances = list(
            Balance.objects.filter(
                user_id__in=user_ids,
                tool_id__in=tool_ids,
            )
        )
        balance_map = {(b.user_id, b.tool_id): b for b in balances}
        for (uid, tid), (amount_delta, reserved_delta) in deltas.items():
            balance = balance_map.get((uid, tid))
            if not balance:
                balance = Balance(user_id=uid, tool_id=tid, amount=0, reserved_amount=0)
                balances.append(balance)
                balance_map[(uid, tid)] = balance
            balance.amount += amount_delta
            balance.reserved_amount += reserved_delta
        Balance.objects.bulk_update(balances, ['amount', 'reserved_amount'])

    def create_limit_order(
        self,
        user_id: UUID,
        order_data: LimitOrderListBody,
        status: str,
        filled: int = 0,
        closed_at: Optional[datetime] = None,
    ) -> Order:
        tool = Tool.objects.only("id").get(ticker=order_data.ticker)

        return Order.objects.create(
            user_id=user_id,
            tool_id=tool.id,
            direction=order_data.direction,
            type="limit",
            price=order_data.price,
            quantity=order_data.qty,
            status=status,
            filled=filled,
            closed_at=closed_at,
        )
