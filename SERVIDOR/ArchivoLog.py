
from Registro import Registro


class ArchivoLog():

    def __init__(self):
        self.nombreArchivo = 'log.csv'
    
    def agregarRegistro(self, registro):

        try:
            with open(self.nombreArchivo, 'a') as archivo:
                archivo.write(f"Hora: {registro.getTimeStamp()} - {registro.getnNivelLog}: Comando: {self.getComando} (IP: {self.getIpCliente})" + "\n")
        except Exception as e:
            print("Error al agregar el registro al archivo:", str(e))

    def obtenerRegistro(self, comando, nivelLog, timeStamp, ipCliente):
        registro = Registro(comando,nivelLog,timeStamp,ipCliente)
        return registro
    
    def devolverRegistro():
        pass
    