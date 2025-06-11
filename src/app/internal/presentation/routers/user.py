from http import HTTPStatus

from ninja import Body, Router

from app.internal.domain.entities.user import UserIn, UserOut
from app.internal.presentation.handlers.user import UserHandlers


def get_users_router(user_handlers: UserHandlers) -> Router:
    router = Router(tags=['users'])

    @router.post(
        '/public/register',
        response={HTTPStatus.OK: UserOut},
        summary='Register'
    )
    def create(request, user_data: UserIn = Body(...)):
        return user_handlers.create(request, user_data)

    return router
