import os
from datetime import datetime

import backtrader as bt

from strategies.cross_method import CrossMethod
from strategies.golden_death_cross import GoldenDeathCross
from logs.log_strategy import LogStrategy

if __name__ == '__main__':
    
    # Trae todos los archivos del directorio datafeeds
    path_files = os.listdir(os.path.join('datafeeds'))
    
    # Crear un array con los path de cada datafeed
    path_datafeeds = [ os.path.join('datafeeds', f) for f in path_files if f.endswith('.csv') ]
        
    # Instanciacion del cerebro
    cerebro = bt.Cerebro()

    # Carga de los datafeeds al cerebro
    for path_df in path_datafeeds:
        df = bt.feeds.YahooFinanceCSVData(
            dataname=path_df,
            fromdate=datetime(2021, 1, 1),
            todate=datetime(2022, 1, 1),
        )
        
        cerebro.adddata(df, os.path.basename(path_df).split('.')[0])
    
    # Instanciacion del log
    logger = LogStrategy(output_file=os.path.join('logs', 'app.log'))

    # Carga de las estrategias
    cerebro.addstrategy(CrossMethod, logger=logger)
    cerebro.addstrategy(CrossMethod, period=30, logger=logger)
    cerebro.addstrategy(GoldenDeathCross, logger=logger)
    
    # Setteo de cash
    cerebro.broker.setcash(100000.0)

    
    # Inicio de ejecucion de la estrategia general
    logger.write_log('VALOR INICIAL DEL PORTFOLIO: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    logger.write_log('VALOR FINAL DEL PORTFOLIO: %.2f' % cerebro.broker.getvalue())