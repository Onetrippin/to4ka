from http import HTTPStatus

from ninja import Body

from app.internal.common.response_entities import SuccessResponse, ErrorResponse
from app.internal.domain.entities.instrument import InstrumentIn
from app.internal.domain.services.instrument import InstrumentService


class InstrumentHandlers:
    def __init__(self, inst_service: InstrumentService) -> None:
        self.inst_service = inst_service

    def add(self, request, inst_data: InstrumentIn = Body(...)):
        is_success = self.inst_service.add(inst_data, request.user_role)
        if not is_success:
            return HTTPStatus.FORBIDDEN, ErrorResponse(detail='You are not admin user')
        return HTTPStatus.OK, SuccessResponse
