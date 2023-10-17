
from Registro import Registro


class ArchivoLog():

    def __init__(self):
        self.archivo = None
        self.nombreArchivo = None
    
    def agregarRegistro():
        pass
    
    def obtenerRegistro(comando, nivelLog, timeStamp, ipCliente):
        registro = Registro(comando,nivelLog,timeStamp,ipCliente)
        return registro
    
    