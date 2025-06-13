from django.db import IntegrityError

from app.internal.data.models.balance import Balance
from app.internal.data.models.tool import Tool
from app.internal.data.models.user import User
from app.internal.domain.interfaces.instrument import IInstrumentRepository


class InstrumentRepository(IInstrumentRepository):
    def add(self, name: str, ticker: str) -> bool:
        try:
            tool, created = Tool.objects.get_or_create(ticker=ticker, name=name)
            if created:
                Balance.objects.bulk_create(
                    [Balance(user_id=user, tool_id=tool.id, amount=0) for user in User.objects.values_list('id', flat=True)]
                )
                return True
        except IntegrityError:
            return False
        else:
            return False

    def delete(self, ticker: str) -> int:
        number, _ = Tool.objects.filter(ticker=ticker).delete()
        return number

    def get_instruments_list(self) -> list:
        return list(Tool.objects.values('name', 'ticker'))
