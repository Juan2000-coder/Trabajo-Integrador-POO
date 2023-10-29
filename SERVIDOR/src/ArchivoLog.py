import Excepciones
import os

class ArchivoLog():
    def __init__(self, nombreArchivo: str):
        self.route = os.path.dirname(os.path.abspath(__file__))
        self.nombreArchivo = os.path.join(self.route, "..", "archivos", nombreArchivo)

    def obtenerLog(self):
        try:
            log:str = ''
            with open(self.nombreArchivo, "r") as archivo:
                for linea in archivo:
                    log += linea
            return log
        except Exception as e:
            raise Excepciones.ExcepcionArchivo(2)