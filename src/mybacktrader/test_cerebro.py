# Set up env
import backtrader as bt
import pandas as pd
import ccxt
import datetime
import csv
from io import StringIO, BytesIO

# Load util Functions
from myccxt.utils import generate_ohlc_df, generate_ohlc

# Load strategy
from mybacktrader.smacross import SmaCross


def generate_dataframes(symbols, timeframes):

    dfs_dict = dict()

    for symbol in symbols:

        timeframes_dict = dict()

        for timeframe in timeframes:

            ohlc = generate_ohlc(from_datetime_str=from_datetime_str,
                                timeframe=timeframe,
                                symbol=symbol)

            timeframes_dict[timeframe] = generate_ohlc_df(ohlc)

        dfs_dict[symbol] = timeframes_dict

    return dfs_dict

def run_cerebro(cash, commission, percents, df, symbol, timeframe, strategy=SmaCross):
    
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(cash)

    cerebro.broker.setcommission(commission=commission)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=percents)

    data = bt.feeds.PandasData(dataname=df)

    cerebro.adddata(data)

    cerebro.addstrategy(strategy)

    print("\nMarket: {}, Timeframe: {}".format(symbol, timeframe))

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


if __name__ == "__main__":

    cash = 5000.0  # Set initial cash for backtesting 

    commission = 0.001  # Set the commission - 0.1% ... divide by 100 to remove the %

    percents = 95  # Perc of cash investet in trade

    from_datetime_str = '2020-10-01 02:00:00'  # Set the start date for backtrading

    symbols=['ETH/EUR', 'BTC/EUR']  # Define markets to analyse

    timeframes = ['1d', '1h']  # Define candlestick timeframes

    dfs_dict = generate_dataframes(symbols, timeframes)

    results_dict = dict()

    for symbol, timeframe_dict in dfs_dict.items():

        for timeframe, df in timeframe_dict.items():
                
            run_cerebro(cash, commission, percents, df, symbol, timeframe, SmaCross)


                



# cerebro.plot()



