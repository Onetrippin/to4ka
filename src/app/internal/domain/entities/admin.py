from typing import Literal
from ninja import Schema, Field
from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Schema):
    id: str = Field(format='uuid4')
    name: str
    role: UserRole
    api_key: str

class Instrument(Schema):
    name: str
    ticker: str = Field(pattern=r'^[A-Z]{2,10}$')

class Ok(Schema):
    success: Literal[True] = Field(default=True)