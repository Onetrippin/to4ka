import uuid

from django.db import models

from app.internal.data.models.tool import Tool
from app.internal.data.models.user import User


class Order(models.Model):
    ORDER_DIR_CHOICES = [('BUY', 'Покупка'), ('SELL', 'Продажа')]

    ORDER_TYPE_CHOICES = [('market', 'Рыночная'), ('limit', 'Лимитная')]

    ORDER_STATUS_CHOICES = [
        ('NEW', 'Новая'),
        ('EXECUTED', 'Выполнена'),
        ('PARTIALLY_EXECUTED', 'Частично исполнена'),
        ('CANCELLED', 'Отменена'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    direction = models.CharField(max_length=5, choices=ORDER_DIR_CHOICES)
    type = models.CharField(max_length=32, choices=ORDER_TYPE_CHOICES)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField()
    status = models.CharField(max_length=32, choices=ORDER_STATUS_CHOICES)
    filled = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.user}: {self.direction} {self.tool} ({self.type}) - {self.status}'
