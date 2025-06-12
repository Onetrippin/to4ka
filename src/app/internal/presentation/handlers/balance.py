from http import HTTPStatus

from app.internal.domain.services.balance import BalanceService


class BalanceHandlers:
    def __init__(self, balance_service: BalanceService) -> None:
        self.balance_service = balance_service

    def get_balances(self, request):
        user_id = request.user_id
        return HTTPStatus.OK, self.balance_service.get_balances(user_id)
