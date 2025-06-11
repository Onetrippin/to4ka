from django.contrib import admin

from app.internal.data.models.trade import Trade


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'bid', 'ask', 'tool', 'buyer', 'seller', 'date', 'price', 'quantity')
    list_filter = ('bid', 'ask', 'tool', 'buyer', 'seller')
    search_fields = ('bid', 'ask', 'tool', 'buyer', 'seller')
