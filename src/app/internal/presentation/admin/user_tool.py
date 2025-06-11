from django.contrib import admin

from app.internal.data.models.user_tool import UserTool


@admin.register(UserTool)
class UserToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tool', 'quantity', 'created_at')
    list_filter = ('user', 'tool', 'quantity')
    search_fields = ('user', 'tool', 'quantity')
