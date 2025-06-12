from abc import ABC, abstractmethod
from uuid import UUID


class IBalanceRepository(ABC):
    @abstractmethod
    def get_balances(self, user_id: UUID) -> list:
        ...