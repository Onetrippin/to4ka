from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.internal.data.models.user import User


@admin.register(User)
class UserAdmin(UserAdmin):
    pass
