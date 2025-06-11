from http import HTTPStatus
from uuid import UUID

from ninja import Body, Path, Router

from app.internal.common.response_entities import ErrorResponse
from app.internal.domain.entities.user import UserIn, UserOut
from app.internal.presentation.handlers.user import UserHandlers


def get_users_router(user_handlers: UserHandlers) -> Router:
    router = Router(tags=['users'])

    @router.post(
        '/public/register',
        response={HTTPStatus.OK: UserOut},
        summary='Register',
        auth=None,
    )
    def create(request, user_data: UserIn = Body(...)):
        return user_handlers.create(request, user_data)

    @router.delete(
        '/admin/user/{user_id}',
        response={HTTPStatus.OK: UserOut, HTTPStatus.FORBIDDEN: ErrorResponse},
        summary='Delete User',
    )
    def delete(request, user_id: UUID = Path(...)):
        return user_handlers.delete(request, user_id)

    return router
