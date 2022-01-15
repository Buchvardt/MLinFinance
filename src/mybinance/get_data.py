import mybinance.config as config, csv, datetime
from binance.client import Client
from io import StringIO, BytesIO
import datetime
import pandas as pd

def get_candlesticks(client, symbol="BTCUSDT", from_date="1 Jan, 2020", to_date=None, interval=None):
    '''
    Get list of candlestick lists.

    Parameters:
        client (binance.client.Client): The client object from binance.
        symbol (str):A string which is the symbol.
        from_date (str): A string in the format "d M, Y" : "1 Jan, 2020".
        from_date (str): A string in the format "d M, Y" : "12 Jul, 2020".
                         If no value is provided, today will be used.
        interval (str): Inveral of the candlestick ["1m", "15m", "30m", "1h", "6h", "12h", "1d"].
                        If no value is provided default will be 1d.

    Returns:
        list of candlestick lists.   
    '''

    if interval == None:

        interval = "1d"

    if to_date == None:

        to_date = datetime.datetime.today().strftime("%d %b, %Y")

    interval_dict = {
                     "1m": Client.KLINE_INTERVAL_1MINUTE,
                     "15m": Client.KLINE_INTERVAL_15MINUTE, 
                     "30m": Client.KLINE_INTERVAL_30MINUTE, 
                     "1h": Client.KLINE_INTERVAL_1HOUR,
                     "6h": Client.KLINE_INTERVAL_6HOUR,
                     "12h": Client.KLINE_INTERVAL_12HOUR,
                     "1d": Client.KLINE_INTERVAL_1DAY
                     }

    candlesticks = client.get_historical_klines(symbol, 
                                                interval_dict[interval],
                                                from_date,
                                                to_date)

    return candlesticks

def get_candlesticks_df(client, symbol="BTCUSDT", from_date="1 Jan, 2020", to_date=None, interval=None):

    candlesticks = get_candlesticks(client, symbol, from_date, to_date, interval)

    write = StringIO()

    wr = csv.writer(write)

    [wr.writerow(candle) for candle in candlesticks]

    bytes_object = BytesIO(write.getvalue().encode())

    df = pd.read_csv(bytes_object, header=0)

    colnames = ["OpenTime",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "CloseTime",
                "QuoteAssetVolume",
                "NumberOfTrades",
                "TakerBuyBaseAssetVolume",
                "TakerBuyQuoteAssetVolume",
                "Ignore"]

    df.columns = colnames

    format_OpenTime = [datetime.datetime.fromtimestamp(timestamp / 1000) for timestamp in df["OpenTime"]]

    format_CloseTime = [datetime.datetime.fromtimestamp(timestamp / 1000) for timestamp in df["OpenTime"]]

    df["OpenTime"] = format_OpenTime

    df["CloseTime"] = format_CloseTime

    df.set_index("OpenTime", inplace=True)

    return df


def write_candlesticks_to_csv(candlesticks, csv_full_path):
    '''
    Write candlesticks lists to .csv.

    Parameters:
        candlesticks (list): List of candlestick lists
        csv_full_path (str): Path of csv to write

    Returns:
          None
    '''

    csvfile = open(csv_full_path, 'w', newline='') 
    
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    for candlestick in  candlesticks:

        candlestick[0] = candlestick[0] / 1000   # Change to miliseconds

        candlestick_writer.writerow(candlestick)

    csvfile.close()

    # Main Function Call

if __name__ == "__main__":

    client = Client(config.API_KEY, config.API_SECRET)

    candlesticks = get_candlesticks(client,
                                    symbol="BTCUSDT",
                                    from_date="1 Jan, 2020",
                                    to_date=None, 
                                    interval="1h")

    print(candlesticks)
