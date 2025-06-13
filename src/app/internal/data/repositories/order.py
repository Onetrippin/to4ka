from datetime import datetime
from typing import Any, Dict, List, Optional, Literal
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

    def update_order_status(self, order_id: UUID, status: str, filled: Optional[int], closed_at: Optional[datetime]) -> None:
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

    def get_opposite_limit_orders_for_market(self, direction: Literal['BUY', 'SELL'], ticker: str) -> List[Dict[str, Any]]:
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

    def get_opposite_limit_orders_for_limit(self, direction: Literal['BUY', 'SELL'], ticker: str, price: float) -> List[Dict[str, Any]]:
        return list(
            Order.objects.filter(
                tool__ticker=ticker,
                direction='SELL' if direction == 'BUY' else 'BUY',
                status__in=['NEW', 'PARTIALLY_EXECUTED'],
                type='limit',
            ).filter(Q(price__lte=price) if direction == 'BUY' else Q(price__gte=price))
            .order_by('price' if direction == 'BUY' else '-price')
            .values('id', 'price', 'quantity', 'filled', 'tool_id')
        )

    def create_trade_from_match(
            self,
            user_id: UUID,
            direction: Literal['BUY', 'SELL'],
            match_order_id: UUID,
            tool_id: UUID,
            price: int,
            quantity: int,
    ) -> Trade:
        match_order = Order.objects.get(id=match_order_id)

        return Trade.objects.create(
            buyer_id=user_id if direction == 'BUY' else match_order.user_id,
            seller_id=match_order.user_id if direction == 'BUY' else user_id,
            tool_id=tool_id,
            quantity=quantity,
            price=price,
            date=timezone.now(),
        )

    def create_market_order(
            self,
            user_id: UUID,
            order_data: MarketOrderListBody,
            status: str,
    ) -> Order:
        return Order.objects.create(
            user_id=user_id,
            tool_id=Subquery(Tool.objects.filter(ticker=order_data.ticker).values('id')[:1]),
            direction=order_data.direction,
            type='market',
            quantity=order_data.qty,
            status=status,
            closed_at=timezone.now(),
        )

    def execute_market_order(self, trades_info: dict) -> None:
        with transaction.atomic:
            Trade.objects.bulk_create(
                [
                    Trade(
                        buyer_id=trades_info['user_id'] if trades_info['direction'] == 'BUY' else trade['user_id'],
                        seller_id=trade['user_id'] if trades_info['direction'] == 'BUY' else trades_info['user_id'],
                        tool_id=trade['tool_id'],
                        quantity=trade['quantity'],
                        price=trade['price'],
                        date=timezone.now(),
                    ) for trade in trades_info['trades']
                ]
            )
            # тут я начал делать изменение балансов, но вспомнил про перевод в рубли и поэтому тут надо переделать
            # то есть для рублей надо везде сделать перевод quantity * price
            # менять также надо с bulk_update
            # просто в случае если BUY, то прибавлять то, что купил, вычитать можно в конце 1 раз всю сумму рублей
            # у чела же убавлять с резерв счёта то, что покупаешь и прибавлять рубли на счёт
            # в случае SELL наоборот - ты минусуешь со своего счёта того, что продаёшь и прибавляешь на рублёвый
            # а у чела минусуешь с резерва рублёвого и прибавляешь то, что покупаешь на обычный
            keys = {(t['user_id'], t['tool_id']) for t in trades_info['trades']}
            balance_map = {
                (b.user_id, b.tool_id): b for b in list(
                    Balance.objects.filter(
                        Q(user_id__in=[k[0] for k in keys]),
                        Q(tool_id__in=[k[1] for k in keys]),
                    )
                )
            }
            delta_amounts = {}
            delta_reserved = {}
            for trade in trades_info['trades']:
                key = (trade['user_id'], trade['tool_id'])
                qty = trade['quantity']

                if trades_info['direction'] == 'BUY':
                    if key in delta_amounts:
                        delta_amounts[key] += qty
                    else:
                        delta_amounts[key] = qty
                else:
                    if key in delta_reserved:
                        delta_reserved[key] -= qty
                    else:
                        delta_reserved[key] = -qty
            Balance.objects.bulk_update(

            )

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
