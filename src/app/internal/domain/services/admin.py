from typing import Optional

from app.internal.domain.interfaces.admin import IAdminRepository
from app.internal.domain.entities.admin import User


class AdminService:
    def __init__(self, admin_repo: IAdminRepository) -> None:
        self.admin_repo = admin_repo

    def delete_user(self, user_id: str) -> Optional[User]:
        return self.admin_repo.delete_user(user_id)

    def add_instrument(self, name: str, ticker: str) -> bool:
        return self.admin_repo.add_instrument(name, ticker)

    def delete_instrument(self, ticker: str) -> bool:
        return self.admin_repo.delete_instrument(ticker)