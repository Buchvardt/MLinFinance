#%%
import pandas
from simulate import simulate_prices

start_date = "1/1/2020"

n_days = 1000

ts = simulate_prices(start_date=start_date, n_days=n_days)

ts.plot()
# %%
# Simple Moving Average

sma_10 = ts.rolling(10).mean()

sma_10.plot()
# %%
# Generate more SMAs

def generate_smas(timeseries, window_sizes = [3, 5, 10, 15]):

    d = dict((f"sma_{s}", timeseries.rolling(s).mean()) for s in window_sizes)

    d['timeseries'] = timeseries

    return pandas.DataFrame(d)


df = generate_smas(ts)

df.plot()


#%%
# Generate more exponentially moving averages

def generate_emas(timeseries, alphas = [0.1, 0.2, 0.3, 0.4, 0.5]):

    d = dict((f"ewm_{a}", timeseries.ewm(alpha=a, adjust=False).mean()) for a in alphas)

    d['timeseries'] = timeseries

    return pandas.DataFrame(d)

df = generate_emas(ts)

df.plot()


# %%
import itertools
import numpy as np


def generate_smas_pos(timeseries, window_sizes = [3, 5, 10, 15]):

    # Inner function
    def _cross_overs(df, low, high):

        s = f'signal_{low}_{high}'
        
        result_df = pandas.DataFrame({s: np.where(df[f'sma_{low}'] > df[f'sma_{high}'], 1.0, 0.0)},
                                    index = df.index)

        result_df[f'position_{low}_{high}'] = result_df[s].diff()

        result_df.drop([s], inplace=True, axis=1)

        return result_df


    d = dict((f"sma_{s}", timeseries.rolling(s).mean()) for s in window_sizes)

    d['timeseries'] = timeseries

    df = pandas.DataFrame(d)

    df_list = [df]

    tuples = list(itertools.combinations(window_sizes, 2))

    df_list.extend([_cross_overs(df, t[0], t[1]) for t in tuples])

    return pandas.concat(df_list, axis=1)


df = generate_smas_pos(ts)

df.plot()








# %%
