import mybinance.config as config
import datetime
from mybinance.get_markets import get_liquid_markets, get_volatile_markets
from binance.client import Client
from binance.enums import *

# MACO - Mooving average crossover

# Variables

# 1. Choose asset
#   Liquidity
#   Volatility

# 2. Choose Bar type
#   Time ticker
#       minute, hour, day, ...
#   Volumne Bar
#   Dollar Bar
#   ...

# 3. Choose 


##### 1. Find top n markets with high liquitity and high volatility

INTERVAL = "1d"
TIMEDELTA = 370
MAX_BID_ASK_SPREAD_PERC = 0.0005

from_date = datetime.datetime.today() - datetime.timedelta(days=1)
from_date = from_date.strftime("%m %b, %Y"  )

client = Client(config.API_KEY, config.API_SECRET)

symbols = get_liquid_markets(client, MAX_BID_ASK_SPREAD_PERC)

df_targets = get_volatile_markets(client, symbols, from_date, INTERVAL)

# TODO use depth to ensure enough quantity i.e 100 * planned trading quantity

##### 2. Find the best value for small, medium and large moving average - optimize risk/reward

### 2.1 For 1m, 15m, 30m and 1h candlesticks

### 2.2 For long only

### 2.3 (for long and short)

### 2.4 Research BNB for trading fees discount

##### 3. pick the best market symbol

##### 4. papertrade for 24 h with Binance Futures

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

SYMBOL = "ETHUSDT"

BALANCE = 10000

QUANTITY = 0.01

real_client = Client(config.API_KEY, config.API_SECRET)

paper_client = PaperClient(real_client, BALANCE)


