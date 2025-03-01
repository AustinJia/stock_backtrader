from strategies.TestStrategy import TestStrategy, MovingAvgStrategy
import backtrader as bt
from datetime import datetime
import yfinance as yf
from pathlib import Path

# from strategies import TestStrategy

cerebro = bt.Cerebro()
cerebro.broker.set_cash(10000)

# path_data = 'orcl-1995-2014.csv'

# Create a Data Feed

# data = bt.feeds.PandasData(dataname=yf.download("ONEQ", start="2018-01-01", end="2018-12-31"))
interested_stock = 'AAPL'
file_path = Path(interested_stock+'.csv')
if not file_path.exists():
    data = yf.download(interested_stock)
    data.to_csv(interested_stock+'_historical_data.csv')

data = bt.feeds.YahooFinanceCSVData(
    dataname=interested_stock+'_historical_data.csv',
    # Do not pass values before this date
    fromdate=datetime(2004, 1, 1),
    # Do not pass values after this date
    todate=datetime.now(),
    reverse=False)

cerebro.adddata(data)

cerebro.addstrategy(MovingAvgStrategy)
print('Starting Portfolio Value: %.2f' %cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' %cerebro.broker.getvalue())