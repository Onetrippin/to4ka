from datetime import datetime
from typing import Literal
from uuid import UUID

from ninja import Schema
from pydantic import Field


class BaseOrderListBody(Schema):
    direction: Literal['BUY', 'SELL']
    ticker: str
    qty: int = Field(..., ge=1)


class MarketOrderListBody(BaseOrderListBody):
    ...


class LimitOrderListBody(BaseOrderListBody):
    price: int = Field(..., gt=0)


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


class CreateOrderOut(Schema):
    success: bool = True
    order_id: UUID
