from ninja import Schema
from pydantic import RootModel


class Balance(RootModel):
    root: dict[str, int]


class Deposit(Schema):
    user_id: str
    ticker: str
    amount: int


class Withdraw(Schema):
    user_id: str
    ticker: str
    amount: int
