import backtrader as bt

from strategies.base_strategy import BaseStrategy

class GoldenDeathCross (BaseStrategy):
    """
    Esta clase representa la estrategia Golden Cross y Death Cross que se basa en comprar un activo
    cuando la Media Movil Simple (SMA) de corto plazo supera a la de largo plazo y vender cuando la
    SMA de largo plazo supere a la de corto plazo.
 
    Attributes:
        long_sma (dict): Media Movil Simple de largo plazo de cada activo financiero
            keys: Ticker del activo financiero
            values: SMA correspondiente a ese activo
        short_sma (dict): Media Movil Simple de corto plazo de cada activo financiero
            keys: Ticker del activo financiero
            values: SMA correspondiente a ese activo
        
    Params:
        long_period (int): Periodo de la SMA de largo plazo
            Default: 10
        short_period (int): Periodo de la SMA de corto plazo
            Default: 10
    """
    
    params = (
        ('long_period', 30),
        ('short_period', 10),
    )
    
    def __init__(self):
        """
        Inicializa el objeto GoldenDeathCross y las media moviles de corto plazo y largo plazo correspondiente a cada activo.
        """
        super().__init__()
        self.long_sma = { assets: bt.indicators.SimpleMovingAverage(self.getdatabyname(assets).close, period=self.params.long_period) for assets in self.getdatanames() }
        self.short_sma = { assets: bt.indicators.SimpleMovingAverage(self.getdatabyname(assets).close, period=self.params.short_period) for assets in self.getdatanames() }




    def conditions_buy(self, market_data) -> bool:
        """
        Realiza la compra si la SMA de periodo corto supero a la SMA de periodo largo.
        
        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de comprar y False si no.
        """
        return self.short_sma[market_data._name][0] > self.long_sma[market_data._name][0]



    def conditions_sell(self, market_data) -> bool:
        """
        Realiza la compra si la SMA de periodo largo supero a la SMA de periodo corto.
        
        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de vender y False si no.
        """
        return self.short_sma[market_data._name][0] < self.long_sma[market_data._name][0]



    def __str__(self) -> str:
        """
        Retorna una representación en cadena del objeto.

        Returns:
            str: Representación en cadena del objeto.
        """
        return f"Golden Death Cross - Short Period {self.params.short_period}|Long Period {self.params.long_period}"
