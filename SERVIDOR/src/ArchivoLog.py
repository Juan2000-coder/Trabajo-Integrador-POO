from Excepciones import ExcepcionArchivo
import logging
import os
from Registro import Registro
import re
from prettytable import PrettyTable


class ArchivoLog(logging.Logger):
    route = os.path.dirname(os.path.abspath(__file__))
    route = os.path.join(route, "..", "archivos")
    #FORMAT = '%(asctime)s - [%(levelname)s] - %(client_ip)s - %(method_name)s - %(message)s'
    DATEFMT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, nombre: str, FORMAT = '[%(asctime)s] [%(levelname)s] %(client_id)s %(client_ip)s [%(method_name)s] %(message)s'):
        super().__init__(nombre)
        self.archivo = os.path.join(self.route, nombre)
        self.fileHandler = logging.FileHandler(f'{self.archivo}.log')
        self.FORMAT = FORMAT
        self.formatter = logging.Formatter(fmt = self.FORMAT, datefmt=self.DATEFMT)
        self.fileHandler.setFormatter(self.formatter)
        self.addHandler(self.fileHandler)

    def obtenerLog(self):
        try:
            with open(self.fileHandler.baseFilename, 'r') as log:
                return ''.join(log.readlines())
        except Exception as e:
            raise ExcepcionArchivo(1)
        
    def extra(self, idCliente, ipCliente, metodo):
        self.dic = {
            "client_id": idCliente,
            "client_ip": ipCliente,
            "method_name": metodo
        }
        
    def log(self, idCliente, ipCliente, metodo, registro:Registro):
        self.extra(idCliente, ipCliente, metodo)
        self.logToFile(registro)

    def logToFile(self, registro:Registro):
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

    def reporteGeneral(self):
        patron = r'\[([^\]]*)\]'
        metodos = {}
        with open(self.fileHandler.baseFilename, 'r') as archivo:
            for i, registro in enumerate(archivo):
                secuencias = re.findall(patron, registro)
                if i == 0:
                    inicio = secuencias[0]
                nivel = secuencias[1]
                metodo = secuencias[2]
                if metodo in metodos:
                    metodos[metodo]["ocurrencias"] += 1
                    if nivel == "ERROR":
                        metodos[metodo]["errores"] += 1
                else:
                    reporteMetodo = {"ocurrencias": 1,
                                     "errores": 0}
                    metodos[metodo] = reporteMetodo
                    if nivel == "ERROR":
                        metodos[metodo]["errores"] = 1
                    else:
                        metodos[metodo]["errores"] = 0

        table = PrettyTable()
        table.field_names = ["metodo", "ocurrencias", "errores"]
        for metodo, valores in metodos.items():
            entrada = [metodo]
            entrada = entrada + list(valores.values())
            table.add_row(entrada, divider = True)
        return "INICIO ACTIVIDAD: "+inicio + '\n' + str(table)