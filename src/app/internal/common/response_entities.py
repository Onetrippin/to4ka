from ninja import Schema
from pydantic import Field


class SuccessResponse(Schema):
    success: bool = True


class ErrorResponse(Schema):
    error: bool = True
    detail: str


class ErrorDetail(Schema):
    loc: list[str | int] = Field(..., examples=['body', 'field_name'])
    msg: str = Field(..., examples=['Some error message'])
    type: str = Field(..., examples=['value_error'])


class ValidationErrorResponse(Schema):
    detail: list[ErrorDetail]
