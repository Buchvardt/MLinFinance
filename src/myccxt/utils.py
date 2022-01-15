import pandas as pd
import ccxt
import datetime
import csv
from io import StringIO, BytesIO

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def generate_ohlc(from_datetime_str=None, timeframe=None, symbol='ETH/EUR'):

    if from_datetime_str == None:

        from_datetime_str = '2019-10-01 02:00:00'

    if timeframe == None:

        timeframe = '1d'

    from_datetime = datetime.datetime.strptime(from_datetime_str, DATE_TIME_FORMAT)

    from_utc_milliseconds = int(from_datetime.timestamp() * 1000)

    exchange = ccxt.bitpanda()

    ohlc = exchange.fetch_ohlcv(symbol=symbol, 
                                timeframe=timeframe,
                                since=from_utc_milliseconds)

    return ohlc

def generate_ohlc_df(ohlc):

    write = StringIO()

    wr = csv.writer(write)

    [wr.writerow(candle) for candle in ohlc]

    bytes_object = BytesIO(write.getvalue().encode())

    df = pd.read_csv(bytes_object, header=0)

    colnames = ["datetime", "open", "high", "low", "close", "volume"]

    df.columns = colnames

    format_datetime = [datetime.datetime.fromtimestamp(timestamp / 1000) for timestamp in df["datetime"]]

    df["datetime"] = format_datetime

    df.set_index("datetime", inplace=True)

    return df