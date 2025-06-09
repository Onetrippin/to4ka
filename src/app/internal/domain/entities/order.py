from datetime import datetime
from typing import Optional, Union

from ninja import Schema


class LimitOrderListBody(Schema):
    direction: str
    ticker: str
    qty: int
    price: float


class MarketOrderListBody(Schema):
    direction: str
    ticker: str
    qty: int


class OrderListOut(Schema):
    id: str
    status: str
    user_id: str
    timestamp: datetime
    body: Union[LimitOrderListBody, MarketOrderListBody]
    filled: Optional[int] = None
