from app.internal.domain.entities.instrument import Instrument
from app.internal.domain.interfaces.instrument import IInstrumentRepository


class InstrumentService:
    def __init__(self, inst_repo: IInstrumentRepository) -> None:
        self.inst_repo = inst_repo

    def add(self, inst_data: Instrument, user_role: str) -> bool:
        if user_role == 'ADMIN':
            self.inst_repo.add(name=inst_data.name, ticker=inst_data.ticker)
            return True
        return False

    def delete(self, ticker: str, user_role: str) -> bool:
        if user_role == 'ADMIN':
            self.inst_repo.delete(ticker=ticker)
            return True
        return False

    def get_instruments_list(self) -> list[Instrument]:
        inst_list = self.inst_repo.get_instruments_list()
        return [Instrument(name=inst['name'], ticker=inst['ticker']) for inst in inst_list]
