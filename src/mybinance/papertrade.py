import mybinance.config as config
import pandas as pd
import datetime

from binance.client import Client
from binance.enums import *

class PaperClient():

    trade_features = ["datetime", "symbol", "side", "type", "quantity", "bid", "ask", "fee", "usd_balance", "asset_balance"]

    trade_history = pd.DataFrame(index=None, columns=trade_features)

    def __init__(self, real_client, usd_balance, asset_balance):

        self.real_client = real_client

        self.usd_balance = usd_balance

        self.asset_balance = asset_balance

        return None

    def create_order(self, symbol, side, type, quantity, df=None):

        if self.real_client != None:

            bid, ask = self._get_bid_ask(symbol)

            fee = self._get_fee(symbol, side)

        elif len(df) > 0:

            bid = df.Close * .9995  # Simulate 1% lower bid price

            ask = df.Close * 1.0005  # Simulate 1% higher ask price

            fee = 0.001  # Simulate 1% fee 

        dt = datetime.datetime.today().strftime("%Y %b %d, %H:%M:%S")

        if side == SIDE_BUY:

            if (quantity * ask) <= self.usd_balance:

                self.usd_balance = self.usd_balance - (quantity * ask)

                self.asset_balance = self.asset_balance + (1 - fee) * quantity
            
            else:

                #print("NO BUY ORDER")

                #print(f"Quantity {quantity} * ask {ask}: {(quantity * ask)} > usd_balance {self.usd_balance}")

                return None

        else:

            if quantity <= self.asset_balance:

                self.usd_balance = self.usd_balance + ((1 - fee) * quantity * bid)

                self.asset_balance = self.asset_balance - quantity

            else:

                #print("NO SELL ORDER")

                #print(f"Quantity {quantity}  > usd_balance {self.asset_balance}")

                return None
        
        
        
        order = {"datetime": [dt],
                 "symbol": [symbol],
                 "side": [side],
                 "type": [type],
                 "quantity": [quantity],
                 "bid": [bid],
                 "ask": [ask],
                 "fee": [fee],
                 "usd_balance": [self.usd_balance],
                 "asset_balance": [self.asset_balance]}

        self.trade_history = pd.concat([self.trade_history, pd.DataFrame(order)])

        return order

    def _get_bid_ask(self, symbol):

        tickers = self.real_client.get_orderbook_tickers()
        
        for ticker in tickers:

            if ticker["symbol"] == symbol:

                bid_ask = ticker

        ask = float(bid_ask["askPrice"])
        
        bid = float(bid_ask["bidPrice"])

        return bid, ask

    def _get_fee(self, symbol, side):
        
        fees = self.real_client.get_trade_fee()

        fee = None

        for tradefee in fees['tradeFee']:

            if tradefee["symbol"] == symbol:

                if side == SIDE_BUY:

                    fee = tradefee["taker"]

                else:

                    fee = tradefee["maker"]

        return fee
                


def paper_order(paper_client, side, quantity, symbol, order_type=ORDER_TYPE_MARKET, df=None):

    try:

        #print("sending order")
        
        order = paper_client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity, df=df)
        
        #print(order)
    
    except Exception as e:
    
        print("an exception occured - {}".format(e))
    
        return False

    return True


if __name__ == "__main__":

    SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

    SYMBOL = "ETHUSDT"

    QUANTITY = 0.01

    USD_BALANCE = 10000

    ASSET_BALANCE = 0

    real_client = Client(config.API_KEY, config.API_SECRET)

    paper_client = PaperClient(real_client, USD_BALANCE, ASSET_BALANCE)

    sides = [SIDE_BUY, SIDE_SELL, SIDE_BUY, SIDE_SELL]

    for side in sides:

        quant = paper_client.asset_balance

        if side == SIDE_SELL and quant < QUANTITY:

            paper_order(paper_client, side, quant, SYMBOL)

        else:

            paper_order(paper_client, side, QUANTITY, SYMBOL)

    print(paper_client.trade_history)




