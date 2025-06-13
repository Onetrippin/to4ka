from abc import ABC, abstractmethod


class IInstrumentRepository(ABC):
    @abstractmethod
    def add(self, name: str, ticker: str) -> bool:
        ...

    @abstractmethod
    def delete(self, ticker: str) -> int:
        ...

    @abstractmethod
    def get_instruments_list(self) -> list:
        ...
