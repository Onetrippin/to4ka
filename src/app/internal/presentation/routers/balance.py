from http import HTTPStatus

from ninja import Router

from app.internal.domain.entities.balance import Balance
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

    return router