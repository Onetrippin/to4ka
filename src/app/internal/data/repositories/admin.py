from typing import Optional

from app.internal.data.models.user import User as UserModel
from app.internal.data.models.tool import Tool

from app.internal.domain.interfaces.admin import IAdminRepository
from app.internal.domain.entities.admin import User, UserRole


class AdminRepository(IAdminRepository):
    def delete_user(self, user_id: str) -> Optional[User]:
        try:
            user = UserModel.objects.get(id=user_id)

            response = User(
                id=str(user.id),
                name=user.username,
                role=UserRole.USER,
                api_key="",
            )

            user.delete()

            return response
        except UserModel.DoesNotExist:
            return None

    def add_instrument(self, name: str, ticker: str) -> bool:
        try:
            Tool.objects.create(
                name=name,
                ticker=ticker,
                type='stock'
            )
            return True
        except Exception:
            return False

    def delete_instrument(self, ticker: str) -> bool:
        try:
            Tool.objects.filter(ticker=ticker).delete()
            return True
        except Exception:
            return False