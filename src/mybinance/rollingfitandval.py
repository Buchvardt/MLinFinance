from numpy import short
import mybinance.config as config
import datetime
import doctest
from binance.client import Client
from mybinance.get_data import get_candlesticks_df
from mybinance.papertrade import PaperClient, paper_order
from binance.enums import *
import pandas as pd

def get_n_windows(df_size, window_size, jump_size):
    """Return the number of windows in a df with the given parameters.

    Parameters:
        df_size (int): The total size of the data frame, also known as number of bars.
        window_size (int): The desired size of the sliding window.
        jump_size (int): The number of bars to shift the window for each slide.

    Returns:
        Int representing the number of windows.  

    >>> get_n_windows(10, 4, 2)
    4
    >>> get_n_windows(10, 5, 5)
    2
    >>> get_n_windows(16, 7, 2)
    5
    """

    overlap = window_size - jump_size

    n_windows = 1 + (df_size - window_size) // (window_size - overlap)

    return n_windows


def get_roling_fit_and_val(candlesticks_df, fit_size, val_size, jump_size):

    fit = []

    val = []

    total_len = len(candlesticks_df)

    window_size = fit_size + val_size

    n_windows = get_n_windows(total_len, window_size, jump_size)

    fit_start_idx = 0

    val_start_idx = fit_start_idx + fit_size

    for i in range(0, n_windows):

        fit_end_idx = fit_start_idx + fit_size

        val_end_idx = val_start_idx + val_size

        fit.append(candlesticks_df.iloc[fit_start_idx:fit_end_idx])
        
        val.append(candlesticks_df.iloc[val_start_idx:val_end_idx])

        fit_start_idx = fit_start_idx + jump_size

        val_start_idx = fit_start_idx + fit_size

    return fit, val


def calc_moving_avg(df, n):

    return df.Close.rolling(n).mean()


def calc_moving_avg_combinations(df):

    short_mas = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    long_mas = [20, 30, 40, 50, 60, 70]

    for n in short_mas:

        df.loc[:,f"Short_{n}_ma"] = calc_moving_avg(df, n)

    for n in long_mas:

        df.loc[:,f"Long_{n}_ma"] = calc_moving_avg(df, n)

    return df

def trade_MACO(paper_client, df_bar, sma, lma, in_position, quant, trade_symbol):

    if df_bar[f"Short_{sma}_ma"] > df_bar[f"Long_{lma}_ma"]: # small moving avg over long

        if not in_position:
            
            #print("Small moving avg over long! Buy!")
            
            order_succeeded = paper_order(paper_client, SIDE_BUY, quant, trade_symbol, df=df_bar)
            
            if order_succeeded:
                
                in_position = True
                
                #print(paper_client.trade_history)
                
        else:
                
            #print("Small moving avg over long, but we are in position Nothing to do.")
            pass
            
    if df_bar[f"Short_{sma}_ma"] < df_bar[f"Long_{lma}_ma"]: # small moving avg under long

        if not in_position:

            #print("Small moving avg under long, but not in position, nothing to do.")
            pass
                
        else:
            
            #print("Small moving avg under long, Sell")

            actual_quant = paper_client.asset_balance
             
            order_succeeded = paper_order(paper_client, SIDE_SELL, actual_quant, trade_symbol, df=df_bar)

            if order_succeeded:
            
                in_position = False
            
                #print(paper_client.trade_history)

    return in_position


if __name__ == "__main__":
    doctest.testmod()

    INTERVAL = "1h"
    TIMEDELTA = 90
    SYMBOL = "ETHUSDT"

    fit_size = 200
    val_size = 100
    jump_size = 50

    from_date = datetime.datetime.today() - datetime.timedelta(days=TIMEDELTA)
    from_date = from_date.strftime("%d %b, %Y")

    client = Client(config.API_KEY, config.API_SECRET)

    candlesticks_df = get_candlesticks_df(client,
                                            symbol=SYMBOL,
                                            from_date=from_date,
                                            to_date=None, 
                                            interval=INTERVAL)

    calc_moving_avg_combinations(candlesticks_df)

    fit, val = get_roling_fit_and_val(candlesticks_df, fit_size, val_size, jump_size)

    # simulate "new" fit every time to include nas for non possible MA
    #fit = [calc_moving_avg_combinations(df) for df in fit]
    #val = [calc_moving_avg_combinations(df) for df in val]

    QUANTITY = 2

    USD_BALANCE = 10000

    ASSET_BALANCE = 0

    in_position = False

    combination_dict = dict()

    short_mas = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    long_mas = [20, 30, 40, 50, 60, 70]

    window_n = 0

    for window in fit:

        window_n += 1

        for sma in short_mas:

            for lma in long_mas:

                paper_client = PaperClient(None, USD_BALANCE, ASSET_BALANCE)

                print(f"Windowd Number: {window_n}, SMA: {sma}, LMA: {lma}")

                for index, df_bar in window.iterrows():

                    #print(f"Bar {index}:\n")

                    in_position = trade_MACO(paper_client, df_bar, sma, lma, in_position, QUANTITY, SYMBOL)

                if in_position: # Delete last entry so all is in $
                    
                    paper_client.trade_history = paper_client.trade_history[:-1]

                if f"{sma}_{lma}" not in combination_dict:

                    combination_dict[f"{sma}_{lma}"] = [paper_client.trade_history.usd_balance[-1:][0]]

                    # TODO

                    # Implement Buy&Hold usd_balance
                else:

                    combination_dict[f"{sma}_{lma}"].append(paper_client.trade_history.usd_balance[-1:][0])   

    print(combination_dict)