import backtrader as bt
from pathlib import Path
import yfinance as yf
import datetime
from strategies.GoldenCross import GoldenCross
import pandas as pd
from common.utilities import *
import os

# params = (('tricker', 'SPY'),('start_time','2'))
tricker = 'SPY'
file_name = tricker+'_historical_data.csv'
# check if file exist
if not find_file_in_subdir(Path(), file_name):
    data = yf.download(tricker)
    data.to_csv('database/'+ tricker +'_historical_data.csv')

colnames = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
prices = pd.read_csv('database/'+ tricker+'_historical_data.csv',
                     parse_dates=True, 
                     skiprows = [0, 1, 2],
                     names = colnames,
                     header = None,
                     index_col = 'Date',
                     )
print(prices.dtypes)
print("Stock Data: \n {}".format(prices.head()))
data = bt.feeds.PandasData(dataname=prices)

cerebro = bt.Cerebro()
cerebro.broker.setcash(10000)
cerebro.adddata(data)
cerebro.addstrategy(GoldenCross)
print('Starting Portfolio Value: %.2f' %cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' %cerebro.broker.getvalue())
# cerebro.plot()
# cerebro.plot(start=datetime.date(2023, 7, 1), end=datetime.date(2025, 2, 26))