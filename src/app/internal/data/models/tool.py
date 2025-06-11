from django.db import models


class Tool(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'

    def __str__(self):
        return f'{self.name}({self.ticker})'
