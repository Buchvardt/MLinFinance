import websocket, json, pprint, talib, numpy
import mybinance.config as config

from mybinance.papertrade import PaperClient, paper_order
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 5
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 40

TRADE_SYMBOL = 'ETHUSDT'
TRADE_QUANTITY = 3
USD_BALANCE = 3500
ASSET_BALANCE = 3

real_client = Client(config.API_KEY, config.API_SECRET)

paper_client = PaperClient(real_client, USD_BALANCE, ASSET_BALANCE)

closes = []

in_position = True

client = Client(config.API_KEY, config.API_SECRET)

    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position
    
    #print('received message')
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("\ncandle closed at {}".format(close))
        closes.append(float(close))
        print("Number of closes")
        print(len(closes))

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)

            cleanedList = [x for x in rsi if not numpy.isnan(x)]
            print(f"Highest rsis calculated so far {max(cleanedList)}")
            print(f"Lowest rsis calculated so far {min(cleanedList)}")
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    # put binance sell logic here
                    actual_quant = paper_client.asset_balance
                    order_succeeded = paper_order(paper_client, SIDE_SELL, actual_quant, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                    print(paper_client.trade_history)
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    # put binance buy order logic here
                    order_succeeded = paper_order(paper_client, SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True
                    print(paper_client.trade_history)

                
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()