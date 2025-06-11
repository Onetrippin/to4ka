from django.contrib import admin

from app.internal.data.models.tool import Tool


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'ticker')
    list_filter = ('name', 'type', 'ticker')
    search_fields = ('name', 'type', 'ticker')
