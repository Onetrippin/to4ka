from http import HTTPStatus

from ninja import Body, Path
from ninja.errors import HttpError
from pydantic import ValidationError
from pydantic.v1.error_wrappers import ErrorWrapper

from app.internal.common.response_entities import ErrorDetail, ErrorResponse, SuccessResponse, ValidationErrorResponse
from app.internal.domain.entities.instrument import Instrument
from app.internal.domain.services.instrument import InstrumentService


class InstrumentHandlers:
    def __init__(self, inst_service: InstrumentService) -> None:
        self.inst_service = inst_service

    def add(self, request, inst_data: Instrument = Body(...)):
        is_success = self.inst_service.add(inst_data, request.user_role)
        if not is_success:
            return HTTPStatus.FORBIDDEN, ErrorResponse(detail='You are not admin user')
        return HTTPStatus.OK, SuccessResponse

    def delete(self, request, ticker: str = Path(...)):
        is_success = self.inst_service.delete(ticker, request.user_role)
        if is_success is None:
            return HTTPStatus.FORBIDDEN, ErrorResponse(detail='You are not admin user')
        if not is_success:
            return HTTPStatus.UNPROCESSABLE_ENTITY, ValidationErrorResponse(
                detail=[ErrorDetail(loc=['body', 0], msg='Invalid value', type='value_error')]
            )
        return HTTPStatus.OK, SuccessResponse

    def get_instruments_list(self, request):
        return self.inst_service.get_instruments_list()
