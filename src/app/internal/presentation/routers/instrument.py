from http import HTTPStatus

from ninja import Body, Path, Router

from app.internal.common.response_entities import ErrorResponse, SuccessResponse
from app.internal.domain.entities.instrument import InstrumentIn
from app.internal.presentation.handlers.instrument import InstrumentHandlers


def get_inst_router(inst_handlers: InstrumentHandlers) -> Router:
    router = Router(tags=['instruments'])

    @router.post(
        '/admin/instrument',
        response={HTTPStatus.OK: SuccessResponse, HTTPStatus.FORBIDDEN: ErrorResponse},
        summary='Add Instrument',
    )
    def add(request, inst_data: InstrumentIn = Body(...)):
        return inst_handlers.add(request, inst_data)

    @router.delete(
        '/admin/instrument/{ticker}',
        response={HTTPStatus.OK: SuccessResponse, HTTPStatus.FORBIDDEN: ErrorResponse},
        summary='Delete Instrument',
    )
    def delete(request, ticker: str = Path(...)):
        return inst_handlers.delete(request, ticker)

    return router
