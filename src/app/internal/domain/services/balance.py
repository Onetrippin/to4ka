from uuid import UUID

from app.internal.data.repositories.balance import BalanceRepository
from app.internal.domain.entities.balance import Balance


class BalanceService:
    def __init__(self, balance_repo: BalanceRepository) -> None:
        self.balance_repo = balance_repo

    def get_balances(self, user_id: UUID) -> Balance:
        return Balance({bal['tool__name']: bal['amount'] for bal in self.balance_repo.get_balances(user_id)})