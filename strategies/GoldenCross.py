import backtrader as bt
import math

class GoldenCross(bt.Strategy):
    params = (
        ('fast', 50),
        ('slow', 200),
        ('order_percentage', 0.95),
        ('ticker', 'SPY'),
    )
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # keeps a reference to the open line. Only one level of indirection is later needed to access the close values
        self.dataopen = self.datas[0].open 
        self.dataclose = self.datas[0].close 
        self.fast_move_avg = bt.indicators.SMA(self.data.close, period=self.params.fast, plotname = '50 day moving average')
        self.slow_move_avg = bt.indicators.SMA(self.data.close, period=self.params.slow, plotname = '200 day moving average')
        self.crossover = bt.indicators.CrossOver(self.fast_move_avg, self.slow_move_avg)
        
    
    def next(self):
        # print("data0000_open {}".format(self.open))
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = self.params.order_percentage * self.broker.cash
                self.size = math.floor(amount_to_invest/ self.data.close)
                self.order = self.buy(size = self.size)
                self.log("BUY {} shares, ${:.2f}".format(self.size, self.data.close[0]))

        if self.position.size > 0:
            if self.crossover < 0:
                # self.order = self.sell(size.self.)
                self.log("SELL {} shares, ${:.2f}".format(self.size, self.data.close[0]))
                self.close()
