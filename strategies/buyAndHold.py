
import backtrader as bt
import math
class buyAndHold(bt.Strategy):
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
        self.dataclose = self.datas[0].close
    
    def next(self):
        if self.position.size == 0:
            amount = math.floor(self.broker.cash * self.p.order_percentage / self.dataclose[0])
            self.order = self.buy(size = amount)