from abc import ABC, abstractmethod
from uuid import UUID


class IUserRepository(ABC):
    @abstractmethod
    def create(self, name: str, token_encrypted: str, token_hash: str) -> dict | None:
        ...

    @abstractmethod
    def get_user_by_token_hash(self, token_hash: str) -> dict | None:
        ...

    @abstractmethod
    def delete_user_by_id(self, user_id: UUID) -> dict | None:
        ...
