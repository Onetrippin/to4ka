from django.db import models


class Tool(models.Model):
    TOOL_TYPE_CHOICES = [('crypto', 'Криптовалюта'), ('stock', 'Акции'), ('bond', 'Облигации'), ('currency', 'Валюта')]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=32, choices=TOOL_TYPE_CHOICES)
    ticker = models.CharField(max_length=10)
    isin = models.CharField(max_length=12, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'

    def __str__(self):
        return f'{self.name}({self.ticker})'
