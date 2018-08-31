import datacollection as dc
import stockportfolio as sp
import datetime
import strategies as strats

t = ['TSLA', 'AAPL', 'GOOG']

print('Gathering Stock Data')
prices = dc.gather_stock_data(t)

portfolio = sp.StockPortfolio()
start = datetime.datetime(2014, 3, 27)
end = datetime.datetime(2018, 8, 30)

strat = strats.PraiseMusk(portfolio, prices)

strat.initialize(start, 200000)
strat.set_end_date(end)

print('Running Strat')
strat.run_strategy()

performance = strat.get_performance()
