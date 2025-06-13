from django.db import models

from app.internal.data.models.tool import Tool
from app.internal.data.models.user import User


class Balance(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='balances')
    tool = models.ForeignKey(Tool, models.CASCADE, related_name='balances')
    amount = models.IntegerField(default=0)
    reserved_amount = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        unique_together = ('user', 'tool')
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'

    def __str__(self):
        return f'{self.user}-{self.tool}: {self.amount}'
