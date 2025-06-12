from typing import Any, Dict, List

from django.utils import timezone

from app.internal.data.models.order import Order
from app.internal.data.models.trade import Trade
from app.internal.domain.interfaces.order import IOrderRepository


class OrderRepository(IOrderRepository):
    def get_order_list(self, user_id: int) -> List[Dict[str, Any]]:
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

    def create_order(self):
        ...

    def get_order(self, user_id: int, order_id: str) -> Dict[str, Any]:
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

    def cancel_order(self, user_id: int, order_id: str) -> None:
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
