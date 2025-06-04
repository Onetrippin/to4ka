from django.db import models

from app.internal.data.models.trade import Tool
from app.internal.data.models.user import User


class UserTool(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'tool'], name='unique_user_tool')]
        verbose_name = 'UserTool'
        verbose_name_plural = 'UserTools'

    def __str__(self):
        return f'{self.user}:{self.tool} - {self.quantity}'
