from http import HTTPStatus
from typing import List

from ninja import Router

from app.internal.common.response_entities import SuccessResponse
from app.internal.domain.entities.order import LimitOrderListOut, MarketOrderListOut
from app.internal.presentation.handlers.order import OrderHandlers


def get_orders_routers(order_handlers: OrderHandlers) -> Router:
    router = Router(tags=['orders'])

    @router.get(
        '/order',
        response={HTTPStatus.OK: List[LimitOrderListOut | MarketOrderListOut]},
        summary='List Orders',
    )
    def get_order_list(request):
        return order_handlers.get_order_list(request)

    @router.get(
        '/order/{order_id}',
        response={HTTPStatus.OK: LimitOrderListOut | MarketOrderListOut},
        summary='Get Order',
    )
    def get_order(request, order_id: str):
        return order_handlers.get_order(request, order_id)

    @router.delete(
        '/order/{order_id}',
        response={HTTPStatus.OK: SuccessResponse},
        summary='Cancel Order',
    )
    def cancel_order(request, order_id: str):
        return order_handlers.cancel_order(request, order_id)

    return router
