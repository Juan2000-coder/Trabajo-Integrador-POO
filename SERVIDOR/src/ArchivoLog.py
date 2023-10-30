import Excepciones
import logging
import os
from Registro import Registro

class ArchivoLog():
    def __init__(self, nombreArchivo: str, FORMAT = '%(asctime)s [%(levelname)s] - %(client_ip)s - %(method_name)s - %(message)s'):
        self.route = os.path.dirname(os.path.abspath(__file__))
        self.nombreArchivo = os.path.join(self.route, "..", "archivos", nombreArchivo)
        self.FORMAT = FORMAT
        logging.basicConfig(filename=self.nombreArchivo, level=logging.INFO, format=self.FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        
    def obtenerLog(self):
        try:
            log:str = ''
            with open(self.nombreArchivo, "r") as archivo:
                for linea in archivo:
                    log += linea
            return log
        except Exception as e:
            raise Excepciones.ExcepcionArchivo(2)
        
    def log(self, ipCliente, metodo, registro:Registro):
        self.dic = {
            "client_ip": ipCliente,
            "method_name": metodo
            }
        if registro.nivelLog == "DEBUG":
            logging.debug(registro.mensaje, extra=self.dic)
        elif registro.nivelLog == "INFO":
            logging.info(registro.mensaje, extra=self.dic)
        elif registro.nivelLog == "WARNING":
            logging.warning(registro.mensaje, extra=self.dic)
        elif registro.nivelLog == "ERROR":
            logging.error(registro.mensaje, extra=self.dic)
        elif registro.nivelLog == "CRITICAL":
            logging.critical(registro.mensaje, extra=self.dic)