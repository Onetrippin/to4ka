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
        return {'id': user.id, 'name': user.name, 'role': user.role, 'api_key_encrypted': user.token_encrypted}

    def get_user_by_token_hash(self, token_hash: str) -> dict | None:
        return User.objects.filter(token_hash=token_hash).values_list('id', 'role').first()
