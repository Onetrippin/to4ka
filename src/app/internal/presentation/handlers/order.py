from http import HTTPStatus

from app.internal.domain.services.order import OrderService


class OrderHandlers:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def get_order_list(self, request):
        user_id = request.user_id
        order_list = self.order_service.get_order_list(user_id)
        return HTTPStatus.OK, order_list

    def get_order(self, request, order_id: str):
        user_id = request.user_id
        order = self.order_service.get_order(user_id, order_id)
        return HTTPStatus.OK, order
