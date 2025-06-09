from http import HTTPStatus

from app.internal.domain.services.order import OrderService


class OrderHandlers:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def get_order_list(self, request):
        user_id = request.user.id
        order_list = self.order_service.get_order_list(user_id)
        return HTTPStatus.OK, order_list
