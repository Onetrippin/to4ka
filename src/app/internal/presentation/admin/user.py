from django.contrib import admin

from app.internal.data.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('name', 'role')
