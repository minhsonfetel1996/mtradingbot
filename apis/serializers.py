from django.db.models import fields
from rest_framework import serializers
from apis.models import TradeCryptoCurrency


class TradeCryptoCurrencySerializers(serializers.ModelSerializer):
    class Meta:
        model = TradeCryptoCurrency
        fields = ('id', 'symbol', 'title', 'closed_price', 'closed_at')
