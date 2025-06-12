from django.contrib import admin

from app.internal.data.models.balance import Balance


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'tool', 'amount')
    list_filter = ('user', 'tool', 'amount')
    search_fields = ('user', 'tool', 'amount')
