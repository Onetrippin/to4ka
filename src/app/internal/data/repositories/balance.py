from uuid import UUID

from django.db.models import F

from app.internal.data.models.balance import Balance
from app.internal.domain.interfaces.balance import IBalanceRepository


class BalanceRepository(IBalanceRepository):
    def get_balances(self, user_id: UUID) -> list:
        return list(Balance.objects.filter(user_id=user_id).values('tool__name', 'amount', 'reserved_amount'))

    def make_deposit(self, user_id: UUID, ticker: str, amount: int) -> None:
        Balance.objects.filter(user_id=user_id, tool__ticker=ticker).update(amount=F('amount') + amount)

    def make_withdraw(self, user_id: UUID, ticker: str, amount: int) -> None:
        Balance.objects.filter(user_id=user_id, tool__ticker=ticker).update(amount=F('amount') - amount)

    def get_balance_by_ticker(self, user_id: UUID, ticker: str = 'RUB') -> int:
        return Balance.objects.filter(user_id=user_id, tool__ticker=ticker).values_list('amount', flat=True).first()
