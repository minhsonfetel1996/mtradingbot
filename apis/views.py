from apis.bots.bot import run_bots

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from apis.models import TradeCryptoCurrency
from apis.serializers import TradeCryptoCurrencySerializers
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def handle_trading_crypto_currency_action(request):
    if request.method == 'GET':
        # TODO To get list trading crypto currency
        trading_crypto_currencies = TradeCryptoCurrency.objects.all()

        trading_crypto_currencies_serializer = TradeCryptoCurrencySerializers(
            trading_crypto_currencies, many=True)
        # for objects serialization
        return JsonResponse(trading_crypto_currencies_serializer.data, safe=False)
    elif request.method == 'POST':
        dto = JSONParser().parse(request)
        dto_serializer = TradeCryptoCurrencySerializers(data=dto)
        if dto_serializer.is_valid():
            dto_serializer.save()
            return JsonResponse(dto_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(dto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def handle_trading_crypto_currency_detail(request, pk):
    trading_crypto_currencies = TradeCryptoCurrency.objects.get(pk=pk)
    if request.method == 'GET':
        trading_crypto_currencies_serializer = TradeCryptoCurrencySerializers(
            trading_crypto_currencies)
        return JsonResponse(trading_crypto_currencies_serializer.data)
    elif request.method == 'PUT':
        dto = JSONParser().parse(request)
        trading_crypto_currencies_serializer = TradeCryptoCurrencySerializers(
            trading_crypto_currencies, data=dto)
        if trading_crypto_currencies_serializer.is_valid():
            trading_crypto_currencies_serializer.save()
            return JsonResponse(trading_crypto_currencies_serializer.data)
        return JsonResponse(trading_crypto_currencies_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        trading_crypto_currencies.delete()
        return JsonResponse({'message': 'Trading crypto currency was deleted!'})


@api_view(['GET'])
def run_bots_action(request):
    run_bots()
    return JsonResponse({'message': 'The bots are running...'})
