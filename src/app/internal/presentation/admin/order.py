from django.contrib import admin

from app.internal.data.models.order import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tool',
        'user',
        'direction',
        'type',
        'price',
        'quantity',
        'status',
        'filled',
        'created_at',
        'closed_at'
    )
    list_filter = ('tool', 'user', 'direction', 'type', 'status')
    search_fields = ('tool', 'user', 'direction', 'type', 'status')
