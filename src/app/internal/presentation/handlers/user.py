from http import HTTPStatus
from uuid import UUID

from ninja import Body, Path

from app.internal.common.response_entities import ErrorResponse
from app.internal.domain.entities.user import UserIn
from app.internal.domain.services.user import UserService


class UserHandlers:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def create(self, request, user_data: UserIn = Body(...)):
        user_out = self.user_service.create(user_data)
        if user_out:
            return HTTPStatus.OK, user_out
        return HTTPStatus.BAD_REQUEST, ErrorResponse(detail='User already exists')

    def delete(self, request, user_id: UUID = Path(...)):
        user_out = self.user_service.delete(user_id, request.user_role)
        if user_out is None:
            return HTTPStatus.FORBIDDEN, ErrorResponse(detail='You are not admin user')
        if not user_out:
            return HTTPStatus.BAD_REQUEST, ErrorResponse(detail='User doesn\'t exist')
        return HTTPStatus.OK, user_out
