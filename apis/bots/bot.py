from apis.shared.trading_template import TradingThread
from apis.shared.config.slack_config import ALICE_USDT_CHANNEL, AXS_USDT_CHANNEL

# START TRADING ALICE_USDT
def run_bots():
    ALICE_USDT_KLINE_1m_THREAD_NAME = 'alice_usdt_kLine_1m_thread'
    ALICE_USDT_TRADE_SYMBOL = 'ALICE_USDT'
    SOCKET_ALICE_USDT_1m = "wss://stream.binance.com:9443/ws/aliceusdt@kline_1m"

    alice_usdt_kLine_1m_thread = TradingThread(
        ALICE_USDT_KLINE_1m_THREAD_NAME, ALICE_USDT_TRADE_SYMBOL, SOCKET_ALICE_USDT_1m, ALICE_USDT_CHANNEL,
        'https://s2.coinmarketcap.com/static/img/coins/64x64/8766.png')

    print('#### START TRADING ALICE_USDT with thread name: {} ####'.format(
        ALICE_USDT_KLINE_1m_THREAD_NAME))
    alice_usdt_kLine_1m_thread.start()

# END TRADING ALICE_USDT

# START TRADING AXS_USDT
# AXS_USDT_KLINE_1m_THREAD_NAME = 'axs_usdt_kLine_1m_thread'
# AXS_USDT_TRADE_SYMBOL = 'AXS_USDT'
# SOCKET_AXS_USDT_1m = "wss://stream.binance.com:9443/ws/axsusdt@kline_1m"

# axs_usdt_kLine_1m_thread = TradingThread(
#     AXS_USDT_KLINE_1m_THREAD_NAME, AXS_USDT_TRADE_SYMBOL, SOCKET_AXS_USDT_1m, AXS_USDT_CHANNEL)

# print('#### START TRADING AXS_USDT with thread name: {} ####'.format(AXS_USDT_KLINE_1m_THREAD_NAME))
# axs_usdt_kLine_1m_thread.start()
