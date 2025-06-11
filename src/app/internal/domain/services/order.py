from typing import List

from app.internal.domain.entities.order import LimitOrderListBody, MarketOrderListBody, MarketOrderListOut, \
    LimitOrderListOut
from app.internal.domain.interfaces.order import IOrderRepository


class OrderService:
    def __init__(self, order_repo: IOrderRepository) -> None:
        self.order_repo = order_repo

    def _build_order_out(self, raw_order: dict) -> LimitOrderListOut | MarketOrderListOut:
        if raw_order['type'] == 'limit':
            return LimitOrderListOut(
                id=raw_order['id'],
                status=raw_order['status'].upper(),
                user_id=raw_order['user_id'],
                timestamp=raw_order['created_at'],
                body=LimitOrderListBody(
                    direction=raw_order['direction'].upper(),
                    ticker=raw_order['tool__ticker'],
                    qty=raw_order['quantity'],
                    price=raw_order['price'],
                ),
                filled=raw_order['filled'],
            )

        return MarketOrderListOut(
            id=raw_order['id'],
            status=raw_order['status'].upper(),
            user_id=raw_order['user_id'],
            timestamp=raw_order['created_at'],
            body=MarketOrderListBody(
                direction=raw_order['direction'].upper(),
                ticker=raw_order['tool__ticker'],
                qty=raw_order['quantity'],
            ),
        )

    def get_order_list(self, user_id: int) -> List[LimitOrderListOut | MarketOrderListOut]:
        raw_orders = self.order_repo.get_order_list(user_id)

        return [self._build_order_out(raw_order) for raw_order in raw_orders]

    def get_order(self, user_id: int, order_id: str) -> LimitOrderListOut | MarketOrderListOut:
        raw_order = self.order_repo.get_order(user_id, order_id)

        return self._build_order_out(raw_order)