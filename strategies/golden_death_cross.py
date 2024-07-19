import backtrader as bt

from strategies.cross_method import CrossMethod

class GoldenDeathCross (CrossMethod):
    
    params = (
        ('long_period', 30),
    )
    
    def __init__(self):
        super().__init__()
        self.long_sma = { assets: bt.indicators.SimpleMovingAverage(self.getdatabyname(assets).close, period=self.params.long_period) for assets in self.getdatanames() }

    def conditions_buy(self, market_data) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self.sma[market_data._name][0] > self.long_sma[market_data._name][0]
    
    def conditions_sell(self, market_data) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self.sma[market_data._name][0] < self.long_sma[market_data._name][0]
    
    def __str__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return f"Golden Death Cross - Short Period {self.params.period}|Long Period {self.params.long_period}"
