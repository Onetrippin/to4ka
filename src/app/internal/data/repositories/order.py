from typing import Any, Dict, List

from app.internal.data.models.order import Order
from app.internal.domain.interfaces.order import IOrderRepository


class OrderRepository(IOrderRepository):
    def get_order_list(self, user_id: int) -> List[Dict[str, Any]]:
        orders = Order.objects.filter(user_id_id=user_id).values(
            'id',
            'status',
            'user_id_id',
            'created_at',
            'side',
            'tool_id__ticker',
            'tool_quantity',
            'price',
            'filled',
            'type',
        )

        return list(orders)
