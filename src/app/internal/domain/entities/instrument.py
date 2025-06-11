from ninja import Schema


class InstrumentIn(Schema):
    name: str
    ticker: str
