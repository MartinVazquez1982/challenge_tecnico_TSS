import backtrader as bt

class BaseStrategy(bt.Strategy):
    """
    Esta clase representa la base de las estrategias, las que heredan de ella deben
    implementar los metodos "conditions_buy" y "conditions_sell"
 
    Attributes:
        positions_strategy (dict): Almacena los activos en cartera que compro la estrategia.
            Keys: Ticker del activo financiero.
            Values: Cantidad de ese activo.
        
    Class Attributes:
        reserved_money (float): Cantidad de dinero reservado para ordenes que todavia no
        fueron completadas.
        
    Params:
        risk_fraction (float): Fraccion de riesgo, representa cuando porcentaje de la 
        cartera, se usara en cada orden.
            Default: 0.10
    """
    
    params = (
        ('risk_fraction', 0.10),
        ('logger', None),
    )
    
    reserved_money = 0
    
    def __init__(self):
        """
        Inicializa el objeto BaseStrategy con todas las posiciones en 0.
        """
        self.positions_strategy = { assets: 0 for assets in self.getdatanames() }
        
    
    
    def log(self, txt, dt=None):
        """_summary_

        Args:
            txt (_type_): _description_
            dt (_type_, optional): _description_. Defaults to None.
        """
        dt = dt or self.datas[0].datetime.date(0)
        text = '%s, %s' % (dt.isoformat(), txt)
        if self.params.logger is None:
            print(text)
        else:
            self.params.logger.info(text)
        
        
    
    def get_size_buy_order(self, market_data) -> int:
        """
        Realiza el calculo del size de la orden, si no hay liquidez retorna 0.
        En caso que haya, reserva el dinero y retornar el size de la orden

        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            int: Size de la orden a enviar, 0 si no hay liquidez.
        """
        money = self.broker.getvalue() * self.params.risk_fraction
        if money > self.broker.get_cash() - BaseStrategy.reserved_money: return 0
        BaseStrategy.reserved_money += money
        return int ( money / market_data.close[0])
    
    
    
    def conditions_buy(self, market_data) -> bool:
        """
        Metodo que revisa la condicion para comprar un activo.

        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de comprar y False si no.
        """
        pass
    
    
    
    def conditions_sell(self, market_data) -> bool:
        """
        Metodo que revisa la condicion para vender un activo. 

        Args:
            market_data: Market data del activo financiero en cuestion.

        Returns:
            bool: True si se encuentra en condiciones de vender y False si no.
        """
        pass
    
    
    
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
                self.log(f'COMPRA COMPLETADA, Orden ID: {order.ref}, Asset {order.data._name}, Size {order.size}, Strategy {self}')
                
                # Carga la cantidad de activos que compro la estrategia
                self.positions_strategy[order.data._name] += order.size
                
                # El dinero ya no esta reservado, sino que fue utilizado
                BaseStrategy.reserved_money -= order.size * order.data.close[0]
            
            elif order.issell():
                self.log(f'VENTA COMPLETADA, Orden ID: {order.ref}, Asset {order.data._name}, Size {order.size}, Strategy {self}')
                
                # Elimina de la posicion la cantidad del activo que fue vendida, realiza una suma porque backtrader coloca negativos los sizes para las ordenes de venta
                self.positions_strategy[order.data._name] += order.size
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'ORDEN CANCELED/MARGIN/REJECTED, Orden ID: {order.ref}')
            
            # Se habilita el dinero reservado
            BaseStrategy.reserved_money -= order.size * order.data.close[0]

        self.order = None



    def notify_trade(self, trade):
        """_summary_

        Args:
            trade (_type_): _description_
        """
        if trade.isclosed:
            # Información sobre la operación cerrada
            self.log(f'Operacion cerrada: Precio de entrada {trade.price}, '
                     f'Precio de salida {trade.price + trade.pnlcomm}, '
                     f'Beneficio/Pérdida {trade.pnlcomm}')