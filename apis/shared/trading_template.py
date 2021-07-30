
# START IMPORTS
import threading
import websocket
import json
import talib
import numpy
import requests
import threading
import datetime

from apis.shared.config.slack_config import SLACK_BOT_TOKEN
# END IMPORTS


class TradingThread(threading.Thread):

    def __init__(self, threadName, symbol, socket_url, channelSlack, image_url, order_book=False):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.symbol = symbol
        self.socket_url = socket_url
        self.order_book = order_book
        self.channelSlack = channelSlack
        self.closed_prices = []
        self.in_position = False
        self.image_url = image_url
        # START TRADING CONSTANTS
        self.RSI_PERIOD = 14
        self.RSI_OVERBOUGHT = 70
        self.RSI_OVERSOLD = 30
        # END TRADING CONSTANTS

    def log(self, message):
        print('{} || {} || {}'.format(
            datetime.datetime.now(), self.threadName, message))

    def prepareAliceUsdtTemplate(self, header, label, value):
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": header
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{}: {}".format(label, value)
                },
                "accessory": {
                    "type": "image",
                    "image_url": self.image_url,
                    "alt_text": self.symbol
                }
            }
        ]

    def post_message_to_slack(self, blocks, text=None):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(SLACK_BOT_TOKEN),
        }
        return requests.post('https://slack.com/api/chat.postMessage', json.dumps({
            'token': SLACK_BOT_TOKEN,
            'channel': self.channelSlack,
            'text': text if text else None,
            'blocks': json.dumps(blocks) if blocks else None
        }), headers=headers).json()

    def calculate_rsi(self):
        np_closed_prices = numpy.array(self.closed_prices)
        rsi = talib.RSI(np_closed_prices, self.RSI_PERIOD)
        last_rsi = rsi[-1]

        if last_rsi > self.RSI_OVERBOUGHT:
            if self.in_position:
                self.log('It is overbought, we do not own any. Nothing to do')
            else:
                self.post_message_to_slack(self.prepareAliceUsdtTemplate(
                    '*OVERBOUGHT: SELL! SELL! SELL!*', 'The last RSI', last_rsi))
        elif last_rsi < self.RSI_OVERSOLD:
            if self.in_position:
                self.log('It is oversold, but you already own it, nothing to do')
            else:
                self.post_message_to_slack(self.prepareAliceUsdtTemplate(
                    '*OVERSOLD: BUY! BUY! BUY!*', 'The last RSI', last_rsi))
        else:
            self.post_message_to_slack(
            self.prepareAliceUsdtTemplate('LAST RSI', 'The last RSI', last_rsi))

    def on_open(self, ws):
        self.log('Open connection')

    def on_close(self, ws):
        self.log('Closed connection')

    def on_message(self, ws, message):
        self.log('Recieved message')
        json_message = json.loads(message)

        candle_data = json_message['k']
        is_candle_closed = candle_data['x']

        if is_candle_closed:
            self.closed_prices.append(float(candle_data['c']))
            self.post_message_to_slack(
                None, 'Closed_prices: {}'.format(self.closed_prices))
            if len(self.closed_prices) > self.RSI_PERIOD:
                self.calculate_rsi()
                self.closed_prices.clear()

    def run(self):
        ws = websocket.WebSocketApp(
            self.socket_url, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)
        ws.run_forever()
