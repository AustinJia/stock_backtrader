import pandas as pd
from pathlib import Path
from common.utilities import *
import yfinance as yf
import backtrader as bt

if __name__=="__main__":
    tricker = 'SPY'
    file_name = tricker+'_historical_data.csv'
    path = Path()
    if not find_file_in_subdir(path, file_name):
        data = yf.download(tricker)
        data.to_csv('database/'+tricker+'_historical_data.csv')

    colnames = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    prices = pd.read_csv('database/'+ tricker+'_historical_data.csv',
                     parse_dates=True, 
                     skiprows = [0, 1, 2],
                     names = colnames,
                     header = None,
                     )
    print(prices.head())
    data = bt.feeds.PandasData(dataname=prices)