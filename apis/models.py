from django.db import models

class TradeCryptoCurrency(models.Model):
    symbol = models.CharField(max_length=150, blank=False)
    title = models.CharField(max_length=255, blank=True)
    closed_price = models.DecimalField(null=False, max_digits=12, decimal_places=2)
    closed_at = models.DateTimeField(null=False)
