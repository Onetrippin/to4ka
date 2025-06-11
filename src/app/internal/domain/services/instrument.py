from app.internal.data.repositories.instrument import InstrumentRepository
from app.internal.domain.entities.instrument import InstrumentIn


class InstrumentService:
    def __init__(self, inst_repo: InstrumentRepository) -> None:
        self.inst_repo = inst_repo

    def add(self, inst_data: InstrumentIn, user_role: str):
        if user_role == 'ADMIN':
            self.inst_repo.add(name=inst_data.name, ticker=inst_data.ticker)
            return True
        return False
