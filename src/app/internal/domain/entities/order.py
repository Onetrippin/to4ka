from datetime import datetime
from uuid import UUID

from ninja import Schema


class BaseOrderListBody(Schema):
    direction: str
    ticker: str
    qty: int


class MarketOrderListBody(BaseOrderListBody):
    ...


class LimitOrderListBody(BaseOrderListBody):
    price: int


class BaseOrderListOut(Schema):
    id: UUID
    status: str
    user_id: UUID
    timestamp: datetime


class MarketOrderListOut(BaseOrderListOut):
    body: MarketOrderListBody


class LimitOrderListOut(BaseOrderListOut):
    body: LimitOrderListBody
    filled: int


class Level(Schema):
    price: int
    qty: int


class OrderBook(Schema):
    bid_levels: list[Level]
    ask_levels: list[Level]


class Transaction(Schema):
    ticker: str
    amount: int
    price: int
    timestamp: datetime
