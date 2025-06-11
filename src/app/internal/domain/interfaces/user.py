from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    def create(self, name: str, token_encrypted: str, token_hash: str) -> dict:
        ...

    @abstractmethod
    def get_user_by_token_hash(self, token_hash: str) -> dict | None:
        ...
