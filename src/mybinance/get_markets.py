import mybinance.config as config
import numpy as np
import pandas as pd
import datetime
from binance.client import Client
from mybinance.get_data import get_candlesticks_df

def get_volatility(candlesticks_df, period=365):

    # calculate daily logarithmic return
    returns = (np.log(candlesticks_df.Close / candlesticks_df.Close.shift(-1)))
        
    # calculate daily standard deviation of returns
    daily_std = np.std(returns)
    
    # annualized daily standard deviation 365 days for crypto / 252 days for stocks
    std = daily_std * period ** 0.5

    return std

def get_liquid_markets(client, max_bid_ask_spread_perc):

    tickers = client.get_orderbook_tickers()

    symbols = dict()

    for ticker in tickers:

        bidPrice = float(ticker["bidPrice"]) 
        
        askPrice = float(ticker["askPrice"])

        if bidPrice > 0.0 and askPrice > 0.0:

            bid_ask_spread_perc = (askPrice - bidPrice) / askPrice

            if bid_ask_spread_perc < max_bid_ask_spread_perc:

                symbols[ticker["symbol"]] = bid_ask_spread_perc

    return symbols  

def get_volatile_markets(client, symbols, from_date, interval):
    
    df_symbols = []
    df_spreads = []
    df_volatilities = []

    for symbol, spread in symbols.items():

        candlesticks_df = get_candlesticks_df(client,
                                            symbol=symbol,
                                            from_date=from_date,
                                            to_date=None, 
                                            interval=interval)

        volatility = get_volatility(candlesticks_df, 365)

        df_symbols.append(symbol)
        df_spreads.append(spread)
        df_volatilities.append(volatility)

    df_targets = pd.DataFrame({"symbol": df_symbols, "spread": df_spreads, "volatility": df_volatilities })

    df_targets.sort_values(by=['volatility'], inplace=True)

    return df_targets 


if __name__ == "__main__":

    # Find top n markets with high liquitity and high volatility

    # TODO use depth to ensure enough quantity i.e 100 * planned trading quantity

    INTERVAL = "1d"
    TIMEDELTA = 370
    MAX_BID_ASK_SPREAD_PERC = 0.0005

    from_date = datetime.datetime.today() - datetime.timedelta(days=1)
    from_date = from_date.strftime("%m %b, %Y"  )

    client = Client(config.API_KEY, config.API_SECRET)

    symbols = get_liquid_markets(client, MAX_BID_ASK_SPREAD_PERC)

    df_targets = get_volatile_markets(client, symbols, from_date, INTERVAL)

    # Look at markets with i.e ETH
    print(df_targets[df_targets["symbol"].str.contains("ETH")])