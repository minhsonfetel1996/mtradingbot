from django.conf.urls import url

from apis import views

urlpatterns = [ 
    url(r'^api', views.run_bots_action),
    url(r'^api/trading-crypto-currency$', views.handle_trading_crypto_currency_action),
    url(r'^api/trading-crypto-currency/(?P<pk>[0-9]+)$', views.handle_trading_crypto_currency_detail),
]