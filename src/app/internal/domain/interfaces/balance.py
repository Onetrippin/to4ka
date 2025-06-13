from abc import ABC, abstractmethod
from uuid import UUID


class IBalanceRepository(ABC):
    @abstractmethod
    def get_balances(self, user_id: UUID) -> list:
        ...

    @abstractmethod
    def make_deposit(self, user_id: UUID, ticker: str, amount: int) -> None:
        ...

    @abstractmethod
    def make_withdraw(self, user_id: UUID, ticker: str, amount: int) -> None:
        ...

    @abstractmethod
    def get_balance_by_ticker(self, user_id: UUID, ticker: str = 'RUB') -> int:
        ...
