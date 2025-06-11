from http import HTTPStatus

from app.internal.presentation.handlers.admin import AdminHandlers
from ninja import Router
from ninja.security import HttpBearer

from app.internal.domain.entities.admin import User, Instrument, Ok
from app.internal.domain.entities.error_response import HTTPValidationError

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

def get_admin_routers(admin_handlers: AdminHandlers) -> Router:
    router = Router(tags=['admin'], auth=AuthBearer())

    @router.delete(
        '/v1/admin/user/{user_id}',
        response={
            HTTPStatus.OK: User,
            HTTPStatus.UNPROCESSABLE_ENTITY: HTTPValidationError
        },
        summary='Delete User',
        openapi_extra={
            "responses": {
                200: {"description": "Successful Response"},
                422: {"description": "Validation Error"}
            }
        }
    )

    def delete_user(request, user_id: str):
        return admin_handlers.delete_user(request, user_id)

    @router.post(
        '/v1/admin/instrument',
        response={
            HTTPStatus.OK: Ok,
            HTTPStatus.UNPROCESSABLE_ENTITY: HTTPValidationError
        },
        summary='Add Instrument',
        openapi_extra={
            "responses": {
                200: {"description": "Successful Response"},
                422: {"description": "Validation Error"}
            }
        }
    )

    def add_instrument(request, data: Instrument):
        return admin_handlers.add_instrument(request, data)

    @router.delete(
        '/v1/admin/instrument/{ticker}',
        response={
            HTTPStatus.OK: Ok,
            HTTPStatus.UNPROCESSABLE_ENTITY: HTTPValidationError
        },
        summary='Delete Instrument',
        description='Удаление инструмента',
        openapi_extra={
            "responses": {
                200: {"description": "Successful Response"},
                422: {"description": "Validation Error"}
            }
        }
    )

    def delete_instrument(request, ticker: str):
        return admin_handlers.delete_instrument(request, ticker)

    return router