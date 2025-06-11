from uuid import UUID

from ninja import Schema


class UserIn(Schema):
    name: str


class UserOut(Schema):
    id: UUID
    name: str
    role: str
    api_key: str
