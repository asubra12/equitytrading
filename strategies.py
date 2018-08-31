import pandas as pd
import datetime
from abc import ABC, abstractmethod


class Trade:
    """
    Structure-like class to hold trade data together
    """
    def __init__(self, ticker, shares, price):
        self.ticker = ticker
        self.shares = shares
        self.price = price

        return

    def __str__(self):
        return self.ticker + \
               ' -- Shares: ' + str(self.shares) + \
               ' -- Price: ' + str(self.price)


class TradingStrategy(ABC):
    """
    Abstract class for a trading strategy
    """
    def __init__(self, stock_portfolio, stock_data):
        self.sp = stock_portfolio
        self.start_date = None
        self.end_date = None
        self.current_date = None
        self.stock_data = stock_data
        self.performance = []
        self.trades = []

        return

    def initialize(self, date, cash):
        """
        Initialize with a start date for strategy and capital

        :param date: start date
        :param cash: Initial capital
        :return:
        """
        self.start_date = date
        self.current_date = date
        self.sp.initialize(date, cash)
        self.performance.append([date, cash])
        self.stock_data = self.stock_data[self.stock_data.date >= self.start_date]
        return

    def set_end_date(self, date):
        self.end_date = date
        self.stock_data = self.stock_data[self.stock_data.date <= self.end_date]
        return

    def update_performance(self, date):
        """
        Need to include dividends
        Can definitely be optimized

        :param date: Date through which to update performance of portfolio
        :return: Nothing
        """
        self.sp.set_current_date(date)
        update_chunk = self.stock_data.loc[((self.stock_data.date > self.current_date) &
                                            (self.stock_data.date <= date)), :]

        dates = update_chunk.date.unique()
        positions = self.sp.stocks

        for d in dates:
            keys = positions.keys()
            closes = update_chunk.loc[update_chunk.date == d, ['0. ticker',
                                                               '4. close',
                                                               '8. split coefficient']]
            for k in keys:
                positions[k].update_current_price(float(closes.loc[closes['0. ticker'] == k, '4. close']))
                positions[k].shares *= float(closes.loc[closes['0. ticker'] == k, '8. split coefficient'])

            self.performance.append([d, self.sp.get_value()])

        return

    def move_to_date(self, date):
        """
        This needs to be a date in the data set.
        - Actually, not really right? we pass in a date but our update chunk uses comparisons <= and > to
          isolate the relevant data. self.current_date might be a weekend day, but the next time we
          update it still shouldn't mater

        :param date: Date to move to before the next trade
        :return: Nothing
        """
        if date < self.current_date:
            print('Cannot move backwards in time with move_to_date')
            exit()

        self.update_performance(date)
        self.current_date = date
        self.sp.set_current_date(date)
        return

    def perform_to_end(self):
        """
        Continue performance with current portfolio through end of time specified
        :return: Nothing
        """
        self.update_performance(self.end_date)
        self.current_date = self.end_date
        return

    def trade(self, date, trade):
        self.trades.append((date, trade))
        self.sp.trade_stock(trade)
        return

    @abstractmethod
    def run_strategy(self, **kwargs):
        """
        Trade securities using self.trade(date, tradeobject)
        only use move_to_date to move forward, and any time we want to increase the information we have
        :param kwargs: keyword list of arguments to be used. Anything can be used tbh
        :return:
        """
        pass

    def get_performance(self):
        df = pd.DataFrame(self.performance, columns=['Date', 'Value'])
        return df


class PraiseMusk(TradingStrategy):

    def run_strategy(self, **kwargs):
        """
        The only Tesla shorts I wanna get into are Elon Musk's

        :param kwargs: who needs data when you have memes
        :return:
        """
        d1 = self.start_date  # datetime.datetime objects
        t1 = Trade('TSLA', 100, 212)
        self.trade(d1, t1)

        dt = datetime.timedelta(weeks=12)
        new_date = self.start_date + dt
        self.move_to_date(new_date)

        d2 = new_date
        t2 = Trade('TSLA', 200, 227)
        self.trade(d2, t2)

        self.perform_to_end()
        return
