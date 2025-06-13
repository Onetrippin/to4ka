import uuid

from app.internal.domain.entities.user import UserIn, UserOut
from app.internal.domain.interfaces.encryption import IEncryptionService
from app.internal.domain.interfaces.user import IUserRepository


class UserService:
    def __init__(self, user_repo: IUserRepository, encryption_service: IEncryptionService) -> None:
        self.user_repo = user_repo
        self.encryption_service = encryption_service

    def create(self, user_data: UserIn) -> UserOut | None:
        token = str(uuid.uuid4())
        token_encrypted = self.encryption_service.encrypt_data(token)
        token_hash = self.encryption_service.get_hash(token)
        user_data = self.user_repo.create(name=user_data.name, token_encrypted=token_encrypted, token_hash=token_hash)
        if not user_data:
            return
        token_decrypted = self.encryption_service.decrypt_data(user_data['api_key_encrypted'])
        return UserOut(id=user_data['id'], name=user_data['name'], role=user_data['role'], api_key=token_decrypted)

    def delete(self, user_id: uuid.UUID, user_role: str) -> UserOut | bool | None:
        if user_role == 'ADMIN':
            user_data = self.user_repo.delete_user_by_id(user_id)
            if not user_data:
                return False
            token_decrypted = self.encryption_service.decrypt_data(user_data['token_encrypted'])
            return UserOut(id=user_data['id'], name=user_data['name'], role=user_data['role'], api_key=token_decrypted)
        return
