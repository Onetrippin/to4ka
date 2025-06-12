from http import HTTPStatus
from typing import List
from uuid import UUID

from ninja import Path, Query, Router

from app.internal.common.response_entities import SuccessResponse, ValidationErrorResponse
from app.internal.domain.entities.order import (
    OrderBook,
    Transaction,
    CreateOrderOut,
    LimitOrderListBody,
    MarketOrderListBody,
    LimitOrderListOut,
    MarketOrderListOut
)
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
    def get_order(request, order_id: UUID = Path(...)):
        return order_handlers.get_order(request, order_id)

    @router.delete(
        '/order/{order_id}',
        response={HTTPStatus.OK: SuccessResponse},
        summary='Cancel Order',
    )
    def cancel_order(request, order_id: UUID = Path(...)):
        return order_handlers.cancel_order(request, order_id)

    @router.get(
        '/public/orderbook/{ticker}',
        response={HTTPStatus.OK: OrderBook},
        summary='Get Orderbook',
        auth=None,
    )
    def get_orderbook(request, ticker: str = Path(...), limit: int = Query(10)):
        return order_handlers.get_orderbook(request, ticker, limit)

    @router.get(
        '/public/transactions/{ticker}',
        response={HTTPStatus.OK: list[Transaction]},
        summary='Get Transaction History',
        auth=None,
    )
    def get_trans_history(request, ticker: str = Path(...), limit: int = Query(10)):
        return order_handlers.get_trans_history(request, ticker, limit)

    @router.post(
        '/order',
        response={HTTPStatus.OK: CreateOrderOut, HTTPStatus.UNPROCESSABLE_ENTITY: ValidationErrorResponse},
        summary='Create Order',
    )
    def create_order(request, order_data: LimitOrderListBody | MarketOrderListBody):
        return order_handlers.create_order(request, order_data)

    return router
