from Excepciones import ExcepcionArchivo
import logging
import os
from Registro import Registro

class ArchivoLog(logging.Logger):
    route = os.path.dirname(os.path.abspath(__file__))
    route = os.path.join(route, "..", "archivos")
    FORMAT = '%(asctime)s [%(levelname)s] - %(id)s - %(client_ip)s - %(method_name)s - %(message)s'
    DATEFMT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, nombre: str):
        super().__init__(nombre)
        self.archivo = os.path.join(self.route, nombre)
        self.fileHandler = logging.FileHandler(f'{self.archivo}.log')
        self.formatter = logging.Formatter(fmt = self.FORMAT, datefmt=self.DATEFMT)
        self.fileHandler.setFormatter(self.formatter)
        self.addHandler(self.fileHandler)
        #logging.basicConfig(filename=self.nombreArchivo, level=logging.INFO, format=self.FORMAT, )

    def obtenerLog(self):
        try:
            with open(self.fileHandler.baseFilename, "r") as archivo:
                return archivo.readlines()
        except Exception as e:
            raise ExcepcionArchivo(1)
        
    def log(self, ipCliente, metodo, registro:Registro):
        self.dic = {
            "client_ip": ipCliente,
            "method_name": metodo
            }
        if registro.nivelLog == "DEBUG":
            self.debug(registro.mensaje, extra=self.dic)
        elif registro.nivelLog == "INFO":
            self.info(registro.mensaje, extra=self.dic)
        elif registro.nivelLog == "WARNING":
            self.warning(registro.mensaje, extra=self.dic)
        elif registro.nivelLog == "ERROR":
            self.error(registro.mensaje, extra=self.dic)
        elif registro.nivelLog == "CRITICAL":
            self.critical(registro.mensaje, extra=self.dic)