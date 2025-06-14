from http import HTTPStatus

from ninja import Body

from app.internal.common.response_entities import ErrorResponse, SuccessResponse
from app.internal.domain.entities.balance import Deposit, Withdraw
from app.internal.domain.services.balance import BalanceService


class BalanceHandlers:
    def __init__(self, balance_service: BalanceService) -> None:
        self.balance_service = balance_service

    def get_balances(self, request):
        user_id = request.user_id
        return HTTPStatus.OK, self.balance_service.get_balances(user_id)

    def make_deposit(self, request, deposit_data: Deposit = Body(...)):
        is_success = self.balance_service.make_deposit(deposit_data, request.user_role)
        if is_success is None:
            return HTTPStatus.FORBIDDEN, ErrorResponse(detail='You are not admin user')
        if is_success:
            return HTTPStatus.OK, SuccessResponse
        return HTTPStatus.BAD_REQUEST, ErrorResponse(detail='User or ticker doesn\'t exist')

    def make_withdraw(self, request, withdraw_data: Withdraw = Body(...)):
        is_success = self.balance_service.make_withdraw(withdraw_data, request.user_role)
        if is_success is None:
            return HTTPStatus.FORBIDDEN, ErrorResponse(detail='You are not admin user')
        if is_success:
            return HTTPStatus.OK, SuccessResponse
        return HTTPStatus.BAD_REQUEST, ErrorResponse(detail='User or ticker doesn\'t exist')
