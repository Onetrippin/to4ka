from django.contrib import admin

from app.internal.data.models.tool import Tool


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ticker')
    list_filter = ('name', 'ticker')
    search_fields = ('name', 'ticker')
