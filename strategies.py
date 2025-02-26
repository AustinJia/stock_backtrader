import backtrader as bt

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        print("executed bar_executed time !!!!!!!!!!!")
        # self.bar_executed = 0
        self.order = None

    def notify_order(self, order):
        # order doesn't executed
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2F' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2F' % order.executed.price)

            self.bar_executed = len(self)
            print('*********BUY/SELLL: bar_executed: ', self.bar_executed)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def next(self):
        print(len(self))
        if len(self) < 10:
            print(self.position)
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            print('in self.order function !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return 
        
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close
                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close
                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    print('[-2]:', self.dataclose[-2], '[-1]:', self.dataclose[-1], '[0]:', self.dataclose[0])
                    self.order = self.buy()
        else:
        # Already in the market ... we might sell
            if len(self) >= (self.bar_executed +5):
                print('bar_executed: ', self.bar_executed)
                # SELL, SELL, SELL!!! (with all possible default paremeters)
                self.log('SELL CREATED {}'.format(self.dataclose[0]))
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()