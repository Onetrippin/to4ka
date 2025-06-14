from uuid import UUID

from app.internal.data.models.balance import Balance
from app.internal.data.models.tool import Tool
from app.internal.data.models.user import User
from app.internal.domain.interfaces.user import IUserRepository


class UserRepository(IUserRepository):
    def create(self, name: str, token_encrypted: str, token_hash: str) -> dict | None:
        user, created = User.objects.get_or_create(
            name=name,
            defaults={
                'token_encrypted': token_encrypted,
                'token_hash': token_hash,
            },
        )
        if created:
            Balance.objects.bulk_create(
                [Balance(user=user, tool_id=tool_id, amount=0) for tool_id in Tool.objects.values_list('id', flat=True)]
            )
            return {'id': user.id, 'name': user.name, 'role': user.role, 'api_key_encrypted': user.token_encrypted}
        return

    def get_user_by_token_hash(self, token_hash: str) -> dict | None:
        return User.objects.filter(token_hash=token_hash).values_list('id', 'role').first()

    def delete_user_by_id(self, user_id: UUID) -> dict | None:
        user_data = User.objects.filter(id=user_id).values('id', 'name', 'role', 'token_encrypted').first()
        if user_data:
            User.objects.filter(id=user_id).delete()
            return user_data
        return
