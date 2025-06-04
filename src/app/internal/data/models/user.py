from django.contrib.auth.models import AbstractUser
from django.db import models

from app.internal.data.models.tool import Tool


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    tools = models.ManyToManyField(Tool, through='UserTools', related_name='users')

    objects = models.Manager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.email}'
