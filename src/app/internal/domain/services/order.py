from typing import List

from app.internal.domain.entities.order import LimitOrderListBody, MarketOrderListBody, OrderListOut
from app.internal.domain.interfaces.order import IOrderRepository


class OrderService:
    def __init__(self, order_repo: IOrderRepository) -> None:
        self.order_repo = order_repo

    def get_order_list(self, user_id: int) -> List[OrderListOut]:
        raw_orders = self.order_repo.get_order_list(user_id)
        result = []

        for order in raw_orders:
            if order['type'] == 'limit':
                body = LimitOrderListBody(
                    direction=order['side'].upper(),
                    ticker=order['tool_id__ticker'],
                    qty=order['tool_quantity'],
                    price=order['price'],
                )
            else:
                body = MarketOrderListBody(
                    direction=order['side'].upper(),
                    ticker=order['tool_id__ticker'],
                    qty=order['tool_quantity'],
                )

            order_out = OrderListOut(
                id=str(order['id']),
                status=order['status'].upper(),
                user_id=str(order['user_id_id']),
                timestamp=order['created_at'],
                body=body,
                filled=order['filled'],
            )

            result.append(order_out)

        return result
