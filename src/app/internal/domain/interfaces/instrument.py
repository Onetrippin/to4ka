from abc import ABC, abstractmethod


class IInstrumentRepository(ABC):
    @abstractmethod
    def add(self, name: str, ticker: str) -> None:
        ...
