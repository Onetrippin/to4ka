from app.internal.data.models.balance import Balance
from app.internal.data.models.tool import Tool
from app.internal.data.models.user import User
from app.internal.domain.interfaces.instrument import IInstrumentRepository


class InstrumentRepository(IInstrumentRepository):
    def add(self, name: str, ticker: str) -> None:
        tool, created = Tool.objects.get_or_create(name=name, defaults={'ticker': ticker})
        if created:
            Balance.objects.bulk_create([
                Balance(user_id=user, tool_id=tool.id, amount=0)
                for user in User.objects.values_list('id', flat=True)
            ])

    def delete(self, ticker: str) -> None:
        Tool.objects.filter(ticker=ticker).delete()

    def get_instruments_list(self) -> list:
        return list(Tool.objects.values('name', 'ticker'))
