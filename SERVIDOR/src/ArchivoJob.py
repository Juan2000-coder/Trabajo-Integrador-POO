import os
from Excepciones import ExcepcionArchivo
from Comando import ComandosGcode

class ArchivoJob:
    route = os.path.dirname(os.path.abspath(__file__))
    jobroute = os.path.join(route, "..", "job")

    def __init__(self, nombreArchivo):
        self.nombreArchivo = os.path.join(self.jobroute, nombreArchivo)

    def agregarComando(self, comando):
        with open(self.nombreArchivo, "a") as archivo_job:
            if comando != "":
                archivo_job.write(comando + "\n")

    def obtenerComandos(self):
        try:
            with open(self.nombreArchivo, 'r') as archivo:
                return archivo.readlines()
        except Exception:
            raise ExcepcionArchivo(2)
        
    def actualizar(self, linea:str):
        lineaSeparada = linea.split()
        comando = lineaSeparada[0]
        params = lineaSeparada[1:]

        if comando != "grabar":
            comandoTransformado = ComandosGcode.comandoAGcode(comando, *params)
            self.agregarComando(comandoTransformado)