from uuid import UUID

from ninja import Schema
from pydantic import RootModel, Field


class Balance(RootModel):
    root: dict[str, int]


class Deposit(Schema):
    user_id: UUID
    ticker: str
    amount: int = Field(..., gt=0)


class Withdraw(Schema):
    user_id: UUID
    ticker: str
    amount: int = Field(..., gt=0)
