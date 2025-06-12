from datetime import datetime
from typing import Any, Dict, List, Optional, Literal
from uuid import UUID

from django.db.models import Q
from django.utils import timezone

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
            .values('id', 'price', 'quantity', 'filled', 'tool_id')
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
            direction: Literal["BUY", "SELL"],
            match_order_id: UUID,
            tool_id: UUID,
            price: float,
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
            filled: int = 0,
            closed_at: Optional[datetime] = None,
    ) -> Order:
        tool = Tool.objects.only('id').get(ticker=order_data.ticker)

        return Order.objects.create(
            user_id=user_id,
            tool_id=tool.id,
            direction=order_data.direction,
            type="market",
            quantity=order_data.qty,
            status=status,
            filled=filled,
            closed_at=closed_at,
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
