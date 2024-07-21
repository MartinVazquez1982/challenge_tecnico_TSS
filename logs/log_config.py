import os
import logging

class LogConfig:
    """
    Esta clase realiza la creacion de un logger para que se coloquen las salidas de las estrategias
    """
    
    @staticmethod
    def getLogger(log_level=logging.INFO):
        """
        Crea un logger y lo retorna

        Args:
            log_level (optional): Nivel del log. Defaults to logging.INFO.

        Returns:
            Logger: Logger creado
        """
        
        # Configurar el logger principal
        logging.basicConfig(
            filename=os.path.join('logs', 'app.log'),
            filemode='w',
            level=log_level,
            format='%(levelname)s - %(message)s',
        )
        
        return logging.getLogger()