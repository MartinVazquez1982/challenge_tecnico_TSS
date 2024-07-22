import logging

class LogStrategy:
    """
    Esta clase realiza la logica para el manejo del log, 
    donde se mostraran los mensajes de la estrategia
    
    Attributes:
        logger (Logger): Objeto encargado de realizar los logs en el archivo de salida.
    """
    
    def __init__(self, output_file,log_level=logging.INFO) -> None:
        """
        Inicializa un objeto LogStrategy y crea el log para registrar las salidas

        Args:
            log_level: Nivel del log. Defaults to logging.INFO.
        """
        logging.basicConfig(
            filename=output_file,
            filemode='w',
            level=log_level,
            format='%(levelname)s - %(message)s',
        )
        
        self.logger = logging.getLogger()



    def write_log(self, text: str) -> None:
        """
        Realiza la escritura en el archivo log. En caso que ocurra una exception, 
        realiza un print del texto

        Args:
            text (str): Texto a almacenar en el log
        """
        try:
            self.logger.info(text)
        except:
            print(text)