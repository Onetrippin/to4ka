from app.internal.data.models.tool import Tool
from app.internal.domain.interfaces.instrument import IInstrumentRepository


class InstrumentRepository(IInstrumentRepository):
    def add(self, name: str, ticker: str) -> None:
        Tool.objects.get_or_create(name=name, defaults={'ticker': ticker})

    def delete(self, ticker: str) -> None:
        Tool.objects.filter(ticker=ticker).delete()
