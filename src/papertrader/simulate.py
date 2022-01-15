import random
import pandas as pd
import matplotlib.pyplot as plt

from pandas.core.indexes.datetimes import date_range

def simulate_prices(start_date="1/1/2020", n_days=50):

    prices = []

    for i in range(n_days):

        prices.append(round(random.uniform(258.50, 392.55), 2))

    timeseries = pd.Series(prices, index=date_range(start_date, periods=n_days))

    timeseries = timeseries.rolling(3).mean()  # reduce fluctuations

    return timeseries
    
