from typing import List, Union
from ninja import Schema

class ValidationError(Schema):
    loc: List[Union[str, int]]
    msg: str
    type: str

class HTTPValidationError(Schema):
    detail: List[ValidationError]