from http import HTTPStatus

from ninja import Body, Path, Router

from app.internal.common.response_entities import ErrorResponse, SuccessResponse, ValidationErrorResponse
from app.internal.domain.entities.instrument import Instrument
from app.internal.presentation.handlers.instrument import InstrumentHandlers


def get_inst_router(inst_handlers: InstrumentHandlers) -> Router:
    router = Router(tags=['instruments'])

    @router.post(
        '/admin/instrument',
        response={
            HTTPStatus.OK: SuccessResponse,
            HTTPStatus.FORBIDDEN: ErrorResponse,
            HTTPStatus.UNPROCESSABLE_ENTITY: ValidationErrorResponse
        },
        summary='Add Instrument',
    )
    def add(request, inst_data: Instrument = Body(...)):
        return inst_handlers.add(request, inst_data)

    @router.delete(
        '/admin/instrument/{ticker}',
        response={
            HTTPStatus.OK: SuccessResponse,
            HTTPStatus.FORBIDDEN: ErrorResponse,
            HTTPStatus.UNPROCESSABLE_ENTITY: ValidationErrorResponse,
        },
        summary='Delete Instrument',
    )
    def delete(request, ticker: str = Path(...)):
        return inst_handlers.delete(request, ticker)

    @router.get(
        '/public/instrument',
        response={HTTPStatus.OK: list[Instrument]},
        summary='List Instruments',
        auth=None,
    )
    def get_instruments_list(request):
        return inst_handlers.get_instruments_list(request)

    return router
