from abc import ABC, abstractmethod
from typing import Optional

from app.internal.domain.entities.admin import User


class IAdminRepository(ABC):
    @abstractmethod
    def delete_user(self, user_id: str) -> Optional[User]:
        ...

    @abstractmethod
    def add_instrument(self, name: str, ticker: str) -> bool:
        ...

    @abstractmethod
    def delete_instrument(self, ticker: str) -> bool:
        ...