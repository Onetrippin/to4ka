from uuid import UUID

from app.internal.domain.entities.balance import Balance, Deposit, Withdraw
from app.internal.domain.interfaces.balance import IBalanceRepository


class BalanceService:
    def __init__(self, balance_repo: IBalanceRepository) -> None:
        self.balance_repo = balance_repo

    def get_balances(self, user_id: UUID) -> Balance:
        return Balance({bal['tool__name']: bal['amount'] + bal['reserved_amount'] for bal in self.balance_repo.get_balances(user_id)})

    def make_deposit(self, deposit_data: Deposit, user_role: str) -> bool:
        if user_role == 'ADMIN':
            self.balance_repo.make_deposit(
                user_id=deposit_data.user_id, ticker=deposit_data.ticker, amount=deposit_data.amount
            )
            return True
        return False

    def make_withdraw(self, withdraw_data: Withdraw, user_role: str) -> bool:
        if user_role == 'ADMIN':
            self.balance_repo.make_withdraw(
                user_id=withdraw_data.user_id, ticker=withdraw_data.ticker, amount=withdraw_data.amount
            )
            return True
        return False
