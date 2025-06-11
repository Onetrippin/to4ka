from ninja.errors import HttpError
from ninja.security import HttpBearer

from app.internal.data.repositories.user import UserRepository
from app.internal.domain.services.encryption import EncryptionService

encryption_service = EncryptionService()
user_repo = UserRepository()


class ApiKeyAuth(HttpBearer):
    def __call__(self, request):
        auth = request.headers.get('Authorization')
        if not auth:
            raise HttpError(401, 'Missing Authorization header')

        try:
            token_type, token = auth.split(' ', 1)
        except ValueError:
            raise HttpError(401, 'Malformed Authorization header')

        if token_type.upper() != 'TOKEN':
            raise HttpError(401, 'Unsupported token type')

        return self.authenticate(request, token)

    def authenticate(self, request, token: str):
        token_hash = encryption_service.get_hash(token)
        user_data = user_repo.get_user_by_token_hash(token_hash)
        if not user_data:
            raise HttpError(401, 'Invalid API key')
        request.user_id, request.user_role = user_data
        return token
