import backtrader as bt
import yfinance as yf
import pandas as pd
from pathlib import Path
from strategies.GoldenCross import GoldenCross
from strategies.buyAndHold import buyAndHold
from common.utilities import *
import os, argparse, datetime, sys

strategies = {
    "golden_cross":GoldenCross,
    "buy_hold":buyAndHold
}
parser = argparse.ArgumentParser()
parser.add_argument("strategy", help="which strategy to run", type=str)
args = parser.parse_args()
if not args.strategy in strategies:
    print("please choose one strategy in following: {}".format(strategies.keys()))
    sys.exit()

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
data = bt.feeds.PandasData(dataname=prices)

cerebro = bt.Cerebro()
cerebro.broker.setcash(10000)
cerebro.adddata(data)
cerebro.addstrategy(strategies[args.strategy])
print('Starting Portfolio Value: %.2f' %cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' %cerebro.broker.getvalue())
cerebro.plot()
# cerebro.plot(start=datetime.date(2023, 7, 1), end=datetime.date(2025, 2, 26))