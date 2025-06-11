from ninja import Schema


class SuccessResponse(Schema):
    success: bool = True


class ErrorResponse(Schema):
    error: bool = True
    detail: str
