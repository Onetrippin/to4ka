from uuid import UUID

from app.internal.data.repositories.balance import BalanceRepository
from app.internal.domain.entities.balance import Balance, Deposit


class BalanceService:
    def __init__(self, balance_repo: BalanceRepository) -> None:
        self.balance_repo = balance_repo

    def get_balances(self, user_id: UUID) -> Balance:
        return Balance({bal['tool__name']: bal['amount'] for bal in self.balance_repo.get_balances(user_id)})

    def make_deposit(self, deposit_data: Deposit, user_role: str) -> bool:
        if user_role == 'ADMIN':
            self.balance_repo.make_deposit(deposit_data.user_id, deposit_data.ticker, deposit_data.amount)
            return True
        return False

