import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time


def gather_stock_data(tickers, save=True):
    """
    Get stock data from alphavantage. May require time to cool down if we ping too much.

    :param tickers: ticker data to get
    :param save: bool to save data to csv
    :return: df of prices
    """
    prices = pd.DataFrame()
    ts = TimeSeries(key='EY2QBMV6MD9FX9CP', output_format='pandas')

    for ticker in tickers:
        successful_grab = False
        ticker_daily_adj = None

        while successful_grab is not True:
            try:
                ticker_daily_adj = ts.get_daily_adjusted(ticker, outputsize='full')[0]
                successful_grab = True
            except ValueError:
                print('Waiting for API to let me in')
                time.sleep(10)

        ticker_daily_adj.loc[:, '0. ticker'] = ticker
        ticker_daily_adj = ticker_daily_adj[sorted(ticker_daily_adj.columns)]

        prices = pd.concat([prices, ticker_daily_adj])

    prices.sort_index(inplace=True)
    prices.reset_index(inplace=True)
    prices['date'] = pd.to_datetime(prices['date'])
    if save:
        prices.to_csv('stockdata.csv', index=True)

    return prices
