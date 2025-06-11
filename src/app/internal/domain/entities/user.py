from ninja import Schema


class UserIn(Schema):
    name: str


class UserOut(Schema):
    id: str
    name: str
    role: str
    api_key: str
