from app.internal.data.models.user import User
from app.internal.domain.interfaces.user import IUserRepository


class UserRepository(IUserRepository):
    def create(self, name: str, token_encrypted: str, token_hash: str) -> dict:
        user, _ = User.objects.get_or_create(
            name=name,
            defaults={
                'token_encrypted': token_encrypted,
                'token_hash': token_hash,
            }
        )
        return {'id': str(user.id), 'name': user.name, 'role': user.role, 'api_key_encrypted': user.token_encrypted}
