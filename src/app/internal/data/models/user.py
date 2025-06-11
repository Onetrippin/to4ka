import uuid

from django.db import models

from app.internal.data.models.tool import Tool


class User(models.Model):
    USER_ROLES = [('USER', 'Пользователь'), ('ADMIN', 'Админ')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    role = models.CharField(max_length=32, choices=USER_ROLES, default='USER')
    token_encrypted = models.TextField(unique=True)
    token_hash = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tools = models.ManyToManyField(Tool, through='UserTool', related_name='users')

    objects = models.Manager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.name}'
