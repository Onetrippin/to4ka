from uuid import UUID

from app.internal.data.models.balance import Balance
from app.internal.domain.interfaces.balance import IBalanceRepository


class BalanceRepository(IBalanceRepository):
    def get_balances(self, user_id: UUID) -> list:
        return list(Balance.objects.filter(user_id=user_id).values('tool__name', 'amount'))
