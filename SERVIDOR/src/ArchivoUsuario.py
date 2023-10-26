from Registro import Registro
import Excepciones
from ArchivoLog import ArchivoLog

class ArchivoUsuario(ArchivoLog):
    def __init__(self, ipUsuario:str, route:str):
        self.nombreArchivo = route + '\\log_' + ipUsuario + ".csv"
        self.ipUsuario = ipUsuario
        super().__init__(self.nombreArchivo)