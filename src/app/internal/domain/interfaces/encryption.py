from abc import ABC, abstractmethod


class IEncryptionService(ABC):
    @abstractmethod
    def get_hash(self, data: str) -> str:
        ...

    @abstractmethod
    def encrypt_data(self, data: str) -> str:
        ...

    @abstractmethod
    def decrypt_data(self, data: str) -> str:
        ...
