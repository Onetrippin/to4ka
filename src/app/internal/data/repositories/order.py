from typing import Any, Dict, List

from app.internal.data.models.order import Order
from app.internal.domain.interfaces.order import IOrderRepository


class OrderRepository(IOrderRepository):
    def get_order_list(self, user_id: int) -> List[Dict[str, Any]]:
        return list(Order.objects.filter(user_id=user_id).values(
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
        ))

    def create_order(self):
        ...

    def get_order(self, user_id: int, order_id: str) -> Dict[str, Any]:
        return Order.objects.filter(id=order_id).values(
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
        ).first()

    def cancel_order(self):
        ...