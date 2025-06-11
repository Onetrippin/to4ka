from http import HTTPStatus
from typing import Tuple, Union

from app.internal.domain.services.admin import AdminService
from app.internal.domain.entities.admin import User, Ok
from app.internal.domain.entities.error_response import HTTPValidationError, ValidationError


class AdminHandlers:
    def __init__(self, admin_service: AdminService):
        self.admin_service = admin_service

    def delete_user(self, request, user_id: str) -> Tuple[HTTPStatus, Union[User, HTTPValidationError]]:
        try:
            result = self.admin_service.delete_user(user_id)
            if result:
                return HTTPStatus.OK, result
            return HTTPStatus.UNPROCESSABLE_ENTITY, HTTPValidationError(
                detail=[ValidationError(loc=["path", "user_id"], msg="User not found", type="not_found")]
            )
        except Exception as e:
            return HTTPStatus.UNPROCESSABLE_ENTITY, HTTPValidationError(
                detail=[ValidationError(loc=["path", "user_id"], msg=str(e), type="error")]
            )

    def add_instrument(self, request, data) -> Tuple[HTTPStatus, Union[Ok, HTTPValidationError]]:
        try:
            success = self.admin_service.add_instrument(data.name, data.ticker)
            if success:
                return HTTPStatus.OK, Ok(success=True)
            return HTTPStatus.UNPROCESSABLE_ENTITY, HTTPValidationError(
                detail=[ValidationError(loc=["body"], msg="Failed to add instrument", type="error")]
            )
        except Exception as e:
            return HTTPStatus.UNPROCESSABLE_ENTITY, HTTPValidationError(
                detail=[ValidationError(loc=["body"], msg=str(e), type="error")]
            )

    def delete_instrument(self, request, ticker: str) -> Tuple[HTTPStatus, Union[Ok, HTTPValidationError]]:
        try:
            success = self.admin_service.delete_instrument(ticker)
            if success:
                return HTTPStatus.OK, Ok(success=True)
            return HTTPStatus.UNPROCESSABLE_ENTITY, HTTPValidationError(
                detail=[ValidationError(loc=["path", "ticker"], msg="Instrument not found", type="not_found")]
            )
        except Exception as e:
            return HTTPStatus.UNPROCESSABLE_ENTITY, HTTPValidationError(
                detail=[ValidationError(loc=["path", "ticker"], msg=str(e), type="error")]
            ) 