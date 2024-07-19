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
        """
        Metodo que revisa la condicion para compra un activo. Realiza la compra si la 
        SMA de periodo corto supero a la SMA de periodo largo.
        
        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de comprar y False si no.
        """
        return self.sma[market_data._name][0] > self.long_sma[market_data._name][0]
    
    def conditions_sell(self, market_data) -> bool:
        """
        Metodo que revisa la condicion para vender un activo. Realiza la compra si la 
        SMA de periodo largo supero a la SMA de periodo corto.
        
        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de vender y False si no.
        """
        return self.sma[market_data._name][0] < self.long_sma[market_data._name][0]
    
    def __str__(self) -> str:
        """
        Retonda una representación en cadena del objeto.

        Returns:
            str: Representación en cadena del objeto.
        """
        return f"Golden Death Cross - Short Period {self.params.period}|Long Period {self.params.long_period}"
