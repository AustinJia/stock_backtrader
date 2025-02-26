from strategies import TestStrategy
import backtrader as bt
import datetime
# from strategies import TestStrategy

cerebro = bt.Cerebro()
cerebro.broker.set_cash(1000000)

# path_data = 'orcl-1995-2014.csv'

# Create a Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname='orcl-1995-2014.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2000, 3, 31),
    reverse=False)
cerebro.adddata(data)

cerebro.addstrategy(TestStrategy)
print('Starting Portfolio Value: %.2f' %cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' %cerebro.broker.getvalue())