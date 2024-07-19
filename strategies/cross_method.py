import backtrader as bt

class CrossMethod(bt.Strategy):

    params = (
        ('period', 10),
        ('risk_fraction', 0.10),
    )



    def __init__(self):
        self.sma = { assets: bt.indicators.SimpleMovingAverage(self.getdatabyname(assets).close, period=self.params.period) for assets in self.getdatanames() }
        self.positions_strategy = { assets: 0 for assets in self.getdatanames() }

    
    
    def get_size_buy_order(self, market_data) -> int:
        """
        Realiza el calculo del size de la orden, si no hay liquidez retorna 0.

        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            int: Size de la orden a enviar, 0 si no hay liquidez.
        """
        money = self.broker.getvalue() * self.params.risk_fraction
        if money > self.broker.get_cash(): return 0
        return int ( money / market_data.close[0])

    
    
    def conditions_buy(self, market_data) -> bool:
        """
        Metodo que revisa la condicion para comprar un activo. Realiza la compra si el 
        precio supero a la SMA. 

        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de comprar y False si no.
        """
        return self.sma[market_data._name][0] < market_data.close[0]



    def conditions_sell(self, market_data) -> bool:
        """
        Metodo que revisa la condicion para vender un activo. Realiza la compra si la 
        SMA supero al precio del activo. 

        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de vender y False si no.
        """
        return self.sma[market_data._name][0] > market_data.close[0]



    def next(self):
        """
        Este metodo se ejecuta en cada cambio en la market data, para cada activo
        en cuestion revisa si se encuentra en condiciones de vender o de comprar.
        """
        for assets in self.datas:
            
            # Condicion para realizar la compra
            if self.positions_strategy[assets._name] == 0 and self.conditions_buy(assets):
                size_order = self.get_size_buy_order(assets)
                if size_order > 0:
                    self.buy(data=assets._name, size=size_order)
            
            # Condicion para realizar la venta
            elif self.positions_strategy[assets._name] > 0 and self.conditions_sell(assets):
                self.sell(data=assets, size=self.positions_strategy[assets._name])


  
    def notify_order(self, order):
        """
        metodo se ejecuta cuando hay cambios en el estado de la orden, para cuando 
        fue enviada o aceptada, no se realiza ninguna acción. Para el resto de
        las situaciones se realiza un log.

        Args:
            order: Orden en cuestion.
        """
        if order.status in [order.Submitted, order.Accepted]:
            # La orden ha sido enviada o aceptada - no se necesita ninguna acción adicional
            return

        if order.status == order.Completed:
            if order.isbuy():
                print(f'COMPRA COMPLETADA, Orden ID: {order.ref}, Asset {order.data._name}, Size {order.size}, Strategy {self}')
                
                # Carga la cantidad de activos que compro la estrategia
                self.positions_strategy[order.data._name] += order.size
            elif order.issell():
                print(f'VENTA COMPLETADA, Orden ID: {order.ref}, Asset {order.data._name}, Size {order.size}, Strategy {self}')
                
                # Elimina de la posicion la cantidad del activo que fue vendida, realiza una suma porque backtrader coloca negativos los sizes para las ordenes de venta
                self.positions_strategy[order.data._name] += order.size
        
        elif order.status == order.Canceled:
            print(f'ORDEN CANCELED, Orden ID: {order.ref}, Status: {order.status}')
        
        elif order.status == order.Margin:
            print(f'ORDEN MARGIN, Orden ID: {order.ref}, Size: {order.size}, Asset {order.data.close[0]}')
        
        elif order.status == order.Rejected:
            print(f'ORDEN REJECTED, Orden ID: {order.ref}, Status: {order.status}')

        self.order = None



    def __str__(self) -> str:
        """
        Retonda una representación en cadena del objeto.

        Returns:
            str: Representación en cadena del objeto.
        """
        return f"Cross Method - Period {self.params.period}"
