import backtrader as bt
from datetime import datetime

if __name__ == '__main__':
    
    msft = bt.feeds.YahooFinance(
        dataname='AAPL',
        fromdate=datetime(2021, 1, 1),
        todate=datetime(2022, 1, 1)
    )
    
    
    
    cerebro = bt.Cerebro()

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())