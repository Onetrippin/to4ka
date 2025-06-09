from django.db import models

from app.internal.data.models.tool import Tool
from app.internal.data.models.user import User


class Order(models.Model):
    ORDER_SIDE_CHOICES = [('buy', 'Покупка'), ('sell', 'Продажа')]

    ORDER_TYPE_CHOICES = [('market', 'Рыночная'), ('limit', 'Лимитная')]

    ORDER_STATUS_CHOICES = [
        ('open', 'Открыта'),
        ('partially_filled', 'Частично исполнена'),
        ('filled', 'Исполнена'),
        ('cancelled', 'Отменена'),
        ('rejected', 'Отклонена'),
    ]

    id = models.AutoField(primary_key=True)
    tool_id = models.ForeignKey(Tool, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    side = models.CharField(max_length=5, choices=ORDER_SIDE_CHOICES)
    type = models.CharField(max_length=32, choices=ORDER_TYPE_CHOICES)
    price = models.FloatField(null=True, blank=True)
    tool_quantity = models.IntegerField()
    status = models.CharField(max_length=32, choices=ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    filled = models.IntegerField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.user_id}: {self.side} {self.tool_id} ({self.type}) - {self.status}'
