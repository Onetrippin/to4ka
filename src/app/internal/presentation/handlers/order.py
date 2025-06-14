from http import HTTPStatus
from uuid import UUID

from ninja import Path, Query

from app.internal.common.response_entities import ErrorResponse, SuccessResponse
from app.internal.domain.entities.order import CreateOrderOut, LimitOrderListBody, MarketOrderListBody
from app.internal.domain.services.order import OrderService


class OrderHandlers:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def get_order_list(self, request):
        user_id = request.user_id
        order_list = self.order_service.get_order_list(user_id)
        return HTTPStatus.OK, order_list

    def get_order(self, request, order_id: UUID = Path(...)):
        user_id = request.user_id
        order = self.order_service.get_order(user_id, order_id)
        return HTTPStatus.OK, order

    def cancel_order(self, request, order_id: UUID = Path(...)):
        user_id = request.user_id
        if self.order_service.cancel_order(user_id, order_id):
            return HTTPStatus.OK, SuccessResponse
        return HTTPStatus.BAD_REQUEST, ErrorResponse(detail='Can\'t cancel order')

    def get_orderbook(self, request, ticker: str = Path(...), limit: int = Query(10)):
        return HTTPStatus.OK, self.order_service.get_orderbook(ticker, limit)

    def get_trans_history(self, request, ticker: str = Path(...), limit: int = Query(10)):
        return HTTPStatus.OK, self.order_service.get_trans_history(ticker, limit)

    def create_order(self, request, order_data: LimitOrderListBody | MarketOrderListBody):
        user_id = request.user_id
        if isinstance(order_data, LimitOrderListBody):
            order_id, text = self.order_service.create_limit_order(user_id, order_data)
            order = 'limit'
        else:
            order_id, text = self.order_service.create_market_order(user_id, order_data)
            order = 'market'
        if not order_id:
            return HTTPStatus.BAD_REQUEST, ErrorResponse(detail=f'Can\'t create order ({order}): {text}')
        return HTTPStatus.OK, CreateOrderOut(order_id=order_id)
