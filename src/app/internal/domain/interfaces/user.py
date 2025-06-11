from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    def create(self, name: str, token_encrypted: str, token_hash: str) -> dict:
        ...
