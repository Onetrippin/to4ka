from django.db import models

from app.internal.data.models.order import Order
from app.internal.data.models.tool import Tool
from app.internal.data.models.user import User


class Trade(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='bids')
    ask = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='asks')
    tool = models.ForeignKey(Tool, models.CASCADE)
    buyer = models.ForeignKey(User, models.CASCADE, related_name='buy_trades')
    seller = models.ForeignKey(User, models.CASCADE, related_name='sell_trades')
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    quantity = models.IntegerField()

    objects = models.Manager()

    class Meta:
        verbose_name = 'Trade'
        verbose_name_plural = 'Trades'

    def __str__(self):
        return f'{self.id}'
