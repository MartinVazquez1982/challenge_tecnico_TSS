import backtrader as bt

from strategies.base_strategy import BaseStrategy

class CrossMethod(BaseStrategy):
    """
    Esta clase representa la estrategia CrossMethod que se basa en comprar un activo
    cuando su precio supera a la Media Movil Simple (SMA) y vender cuando su precio caiga
    por debajo de la SMA.
 
    Attributes:
        sma (dict): Media Movil Simple de cada activo financiero
            keys: Ticker del activo financiero
            values: SMA correspondiente a ese activo
        
    Params:
        period (int): Periodo de la SMA
            Default: 10
    """

    params = (
        ('period', 10),
    )
    
    def __init__(self):
        """
        Inicializa el objeto CrossMethod y la media movil correspondiente a cada activo.
        """
        super().__init__()
        self.sma = { assets: bt.indicators.SimpleMovingAverage(self.getdatabyname(assets).close, period=self.params.period) for assets in self.getdatanames() }    
    
    
    def conditions_buy(self, market_data) -> bool:
        """
        Realiza la compra si el precio supero a la SMA. 

        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de comprar y False si no.
        """
        return self.sma[market_data._name][0] < market_data.close[0]



    def conditions_sell(self, market_data) -> bool:
        """
        Realiza la compra si la SMA supero al precio del activo. 

        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de vender y False si no.
        """
        return self.sma[market_data._name][0] > market_data.close[0]



    def __str__(self) -> str:
        """
        Retorna una representación en cadena del objeto.

        Returns:
            str: Representación en cadena del objeto.
        """
        return f"Cross Method - Period {self.params.period}"
