import uuid

from app.internal.data.repositories.user import UserRepository
from app.internal.domain.entities.user import UserIn, UserOut
from app.internal.domain.interfaces.encryption import IEncryptionService


class UserService:
    def __init__(self, user_repo: UserRepository, encryption_service: IEncryptionService) -> None:
        self.user_repo = user_repo
        self.encryption_service = encryption_service

    def create(self, user_data: UserIn) -> UserOut:
        token = str(uuid.uuid4())
        token_encrypted = self.encryption_service.encrypt_data(token)
        token_hash = self.encryption_service.get_hash(token)
        user_data = self.user_repo.create(name=user_data.name, token_encrypted=token_encrypted, token_hash=token_hash)
        token_decrypted = self.encryption_service.decrypt_data(user_data['api_key_encrypted'])
        return UserOut(id=user_data['id'], name=user_data['name'], role=user_data['role'], api_key=token_decrypted)
