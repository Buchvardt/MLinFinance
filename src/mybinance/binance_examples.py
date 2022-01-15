import mybinance.config as config
from mybinance.get_data import get_candlesticks
from binance.client import Client

# API DOCS:
# https://readthedocs.org/projects/python-binance/downloads/pdf/latest/

##### Set Constants
ASSET = "ETH"
SYMBOL = "ETHUSDT"
N = 10
FROM_DATE = "1 Jan, 2020"
INTERVAL = "1h"

##### Create Binance Client
client = Client(config.API_KEY, config.API_SECRET)

##### Get Balance
balance = client.get_asset_balance(asset=ASSET)

print(f"\nBalance of asset: {ASSET}\n")

print(balance)

##### Get first bid and ask entry in the order book for all markets.
tickers = client.get_orderbook_tickers()

print(f"\nBid and ask entries:\n")

for ticker in tickers:

    if ticker["symbol"] == SYMBOL:

        print(ticker)

##### Get market depth
depth = client.get_order_book(symbol=SYMBOL)

# Get the total quntity
# sum([float(x[1]) for x in depth["asks"]])
# 524.3528700000003
# sum([float(x[1]) for x in depth["bids"]])
# 226.26691999999994

##### Get Brokerage fee
fee = client.get_trade_fee()

print(f"\nBroker Fees:\n")

for tradefee in fee['tradeFee']:

    if tradefee["symbol"] == SYMBOL:

        print(tradefee)

##### Get bid/ask spread
# TODO 
# Research what this spread means and correlate to the term "slippage"
bid_ask = None

for ticker in tickers:

    if ticker["symbol"] == SYMBOL:

        bid_ask = ticker

bid_ask_spread = float(bid_ask["askPrice"]) - float(bid_ask["bidPrice"])

print(f"\nThe Bid Ask Spread for {SYMBOL} is: {bid_ask_spread}\n")

##### Get Markets
cnt = 1

print(f"{N} Markets with ETH:")

for ticker in tickers:

    symbol = ticker["symbol"]

    if "ETH" in symbol:

        print(f"\nMarket SYMBOL #{cnt}: {symbol}")

        #cnt = cnt + 1

    if cnt > N:

        break

##### Submit sell order
# TODO
# Resarch spot vs specific price

##### Submit buy order 
# TODO
# Resarch spot vs specific price

# Buy test order
quantity = 0.01
price = bid_ask["askPrice"]

order = client.create_test_order(symbol=SYMBOL,
                                 side=client.SIDE_BUY,
                                 type=client.ORDER_TYPE_LIMIT,
                                 timeInForce=client.TIME_IN_FORCE_GTC,
                                 quantity=quantity,
                                 price=price)

orders = client.get_all_orders(symbol=SYMBOL)

print(f"\nAll Orders for {SYMBOL}")

for order in orders:

    print(order)

##### Get dividend history
history = client.get_asset_dividend_history()

##### Get Candlestick historic data
candlesticks = get_candlesticks(client,
                                symbol=SYMBOL,
                                from_date=FROM_DATE,
                                to_date=None, 
                                interval=INTERVAL)

print(f"\nFirst {N} candlesticks:\n")
print(candlesticks[0:N])

##### Connect to websocket