from abc import ABC, abstractmethod
from uuid import UUID


class IBalanceRepository(ABC):
    @abstractmethod
    def get_balances(self, user_id: UUID) -> list:
        ...

    @abstractmethod
    def make_deposit(self, user_id: str, ticker: str, amount: int) -> None:
        ...
