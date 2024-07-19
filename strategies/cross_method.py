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
        """_summary_

        Args:
            market_data (_type_): _description_

        Returns:
            int: _description_
        """
        money = self.broker.getvalue() * self.params.risk_fraction
        if money > self.broker.get_cash(): return 0
        return int ( money / market_data.close[0])

    def next(self):
        """_summary_
        """
        for assets in self.datas:
            if self.positions_strategy[assets._name] == 0 and self.sma[assets._name][0] < assets.close[0]:
                size_order = self.get_size_buy_order(assets)
                if size_order > 0:
                    order = self.buy(data=assets._name, size=size_order)
                    order.addinfo(strategy=self)
            
            elif self.positions_strategy[assets._name] > 0 and self.sma[assets._name][0] > assets.close[0]:
                order = self.sell(data=assets, size=self.positions_strategy[assets._name])
                order.addinfo(strategy=self)

            
    def notify_order(self, order):
        """_summary_

        Args:
            order (_type_): _description_
        """
        if order.status in [order.Submitted, order.Accepted]:
            # La orden ha sido enviada o aceptada - no se necesita acción adicional
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                print(f'COMPRA COMPLETADA, Orden ID: {order.ref}, Asset {order.data._name}, Size {order.size}, Strategy {order.info.strategy}')
                self.positions_strategy[order.data._name] += order.size
            elif order.issell():
                print(f'VENTA COMPLETADA, Orden ID: {order.ref}, Asset {order.data._name}, Size {order.size}, Strategy {order.info.strategy}')
                self.positions_strategy[order.data._name] = 0
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f'ORDEN FALLIDA, Orden ID: {order.ref}')

        # Limpiar la referencia de la orden después de que se ha completado o fallado
        self.order = None
    
    def __str__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return f"Cross Method - Period {self.params.period}"
