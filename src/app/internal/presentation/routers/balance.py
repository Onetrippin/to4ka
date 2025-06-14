from http import HTTPStatus

from ninja import Body, Router

from app.internal.common.response_entities import ErrorResponse, SuccessResponse
from app.internal.domain.entities.balance import Balance, Deposit, Withdraw
from app.internal.presentation.handlers.balance import BalanceHandlers


def get_balance_router(balance_handlers: BalanceHandlers) -> Router:
    router = Router(tags=['balance'])

    @router.get(
        '/balance',
        response={HTTPStatus.OK: Balance},
        summary='Get Balances',
    )
    def get_balances(request):
        return balance_handlers.get_balances(request)

    @router.post(
        '/admin/balance/deposit',
        response={
            HTTPStatus.OK: SuccessResponse,
            HTTPStatus.FORBIDDEN: ErrorResponse,
            HTTPStatus.BAD_REQUEST: ErrorResponse,
        },
        summary='Deposit',
    )
    def make_deposit(request, deposit_data: Deposit = Body(...)):
        return balance_handlers.make_deposit(request, deposit_data)

    @router.post(
        '/admin/balance/withdraw',
        response={
            HTTPStatus.OK: SuccessResponse,
            HTTPStatus.FORBIDDEN: ErrorResponse,
            HTTPStatus.BAD_REQUEST: ErrorResponse,
        },
        summary='Withdraw',
    )
    def make_withdraw(request, withdraw_data: Withdraw = Body(...)):
        return balance_handlers.make_withdraw(request, withdraw_data)

    return router
