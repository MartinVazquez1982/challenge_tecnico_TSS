import backtrader as bt

class CrossMethod(bt.Strategy):

    params = (
        ('period', 10),
    )

    def __init__(self):
        self.sma = {assets: bt.indicators.SimpleMovingAverage(self.getdatabyname(assets).close, period=self.params.period) for assets in self.getdatanames() }
        self.positions_strategy = {assets: 0 for assets in self.getdatanames() }
        

    def next(self):
        for assets in self.getdatanames():
            data = self.getdatabyname(assets)
            if self.positions_strategy[assets] == 0 and self.sma[assets][0] < data.close[0]:
                self.buy(data=assets)
            
            elif self.positions_strategy[assets] > 0 and self.sma[assets][0] > data.close[0]:
                self.sell(data=assets)

            
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # La orden ha sido enviada o aceptada - no se necesita acción adicional
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                print(f'COMPRA COMPLETADA, Orden ID: {order.ref}, Asset {order.data._name}')
                self.positions_strategy[order.data._name] += 1
            elif order.issell():
                print(f'VENTA COMPLETADA, Orden ID: {order.ref}, Asset {order.data._name}')
                self.positions_strategy[order.data._name] = 0
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f'ORDEN FALLIDA, Orden ID: {order.ref}')

        # Limpiar la referencia de la orden después de que se ha completado o fallado
        self.order = None
