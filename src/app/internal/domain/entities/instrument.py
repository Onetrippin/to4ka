from ninja import Schema
from pydantic import Field


class Instrument(Schema):
    name: str
    ticker: str = Field(..., min_length=2, max_length=10, pattern=r'^[A-Z]+$')
