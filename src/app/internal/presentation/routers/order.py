from http import HTTPStatus
from typing import List

from ninja import Router

from app.internal.domain.entities.order import OrderListOut
from app.internal.presentation.handlers.order import OrderHandlers


def get_orders_routers(order_handlers: OrderHandlers) -> Router:
    router = Router(tags=['orders'])

    @router.get(
        '/order',
        response={HTTPStatus.OK: List[OrderListOut]},
        summary='List Orders',
    )
    def get_order_list(request):
        return order_handlers.get_order_list(request)

    return router
