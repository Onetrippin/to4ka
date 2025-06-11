import hashlib

from cryptography.fernet import Fernet
from django.conf import settings

from app.internal.domain.interfaces.encryption import IEncryptionService


class EncryptionService(IEncryptionService):
    def __init__(self) -> None:
        self.cipher = Fernet(settings.FERNET_KEY)

    def get_hash(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def encrypt_data(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, data: str) -> str:
        return self.cipher.decrypt(data.encode()).decode()
