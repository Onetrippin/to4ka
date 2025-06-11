from http import HTTPStatus

from ninja import Body

from app.internal.domain.entities.user import UserIn
from app.internal.domain.services.user import UserService


class UserHandlers:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def create(self, request, user_data: UserIn = Body(...)):
        return HTTPStatus.OK, self.user_service.create(user_data)
