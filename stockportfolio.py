class Position:
    """
    Class to pull together data of a position held on a certain stock
    """
    def __init__(self, ticker, shares, enter_price):
        """
        We can store the price at which we entered a position.
        If we keep entering a position, do we want to store every enter price? Maybe delete the position
            if we go to zero stocks longed / shorted

        :param ticker: String ticker
        :param shares: Number of shares of position. negative means shorts
        :param enter_price: Price at which we entered
        """
        self.ticker = ticker
        self.entered = enter_price
        self.current_price = enter_price
        self.shares = shares

    def __str__(self):
        return self.ticker + \
               ' -- Shares: ' + str(self.shares) + \
               ' -- Enter Price: ' + str(self.entered) + \
               ' -- Quote: ' + str(self.current_price)

    def update_current_price(self, current):
        self.current_price = current
        return

    def update_shares(self, ds):
        self.shares += ds
        return

    def get_total_value(self):
        return self.shares * self.current_price

    def get_num_shares(self):
        return self.shares


class StockPortfolio:
    def __init__(self):
        self.cash = 0
        self.stocks = {}  # Represent longs or shorts
        self.value = None  # Total value
        self.profit = 0  # Profit
        self.initial_value = None
        self.initialization_date = None
        self.current_date = None

        return

    def add_cash(self, inject):
        self.cash += inject
        return

    def initialize(self, date, cash):
        self.add_cash(cash)
        self.value = self.initial_value = self.cash
        self.initialization_date = self.current_date = date

    def trade_stock(self, trade):
        ticker = trade.ticker
        shares = trade.shares
        price = trade.price

        self.cash -= shares * price

        if ticker in self.stocks:
            self.stocks[ticker].update_shares(shares)
            self.stocks[ticker].update_current_price(price)

        else:
            self.stocks[ticker] = Position(ticker, shares, price)

    def set_current_date(self, date):
        self.current_date = date
        return

    def get_value(self):
        c = self.cash

        for v in self.stocks.values():
            c += v.get_total_value()

        return c

    def __str__(self):
        s = 'Cash: ' + str(self.cash) + '\n'
        s += 'Value: ' + str(self.value) + '\n'
        for v in self.stocks.values():
            s += str(v)
            s += '\n'

        return s
