from ninja import Schema


class Instrument(Schema):
    name: str
    ticker: str
