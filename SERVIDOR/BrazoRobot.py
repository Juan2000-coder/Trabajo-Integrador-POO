import serial
import time

from Punto import Punto
class BrazoRobot():
    def __init__(self):
        self.posicion = Punto(-1, -1, -1)
        # Cuando se crea el objeto, a priori no se conoce la posición
        # del efector final dado que no se inició la conexión con el robot.
        # Entonces se deja en parámetros inválidos
        self.velocidad = -10 # Lo mismo para la velocidad
        #gregado de Fran -M-
        self.conexion_establecida = False
        self.puerto_serie = None

    def conectarRobot(self, puerto, baud_rate):
        # Me imagino que esta debe recibir los parámetros para la conexión
        # Aunque no se si se utiliza una velocidad por defecto o se puede indicar.
        # Revise el proyecto de Arduino y la velocidad de comunicación sí está dada por
        # defecto a 115200 baudios. Se indica en el archivo config.h como BAUD
        # Entonces solamente habría que habilitar la comunicación serial desde la computadora
        # hacia el arduino.
        
        try:
            self.puerto_serie = serial.Serial(puerto, baud_rate)
            self.conexion_establecida = True
            print("Conexión exitosa con el puerto", puerto)

        except serial.SerialException:
            print("Error al intentar establecer la conexión.")
            self.conexion_establecida = False
            
    def enviarComando(self, comando):
        if self.conexion_establecida:
            self.puerto_serie.write((comando + '\r'+'\n').encode('utf-8'))
            # Ajusta un tiempo de espera (timeout) en segundos
            self.puerto_serie.timeout = 1  # Puedes ajustar este valor según tus necesidades
            data = b""
            while True:
                line = self.puerto_serie.readline()
                if not line:
                    break
                data += line
            return data.decode('utf-8').strip()
        else:
            return "No se pudo enviar el comando. La conexión no está establecida."


    def desconectarRobot(self):
        if self.conexion_establecida:
            self.puerto_serie.close()
            self.conexion_establecida = False
            print("Conexión cerrada.")
        else:
            print("No hay una conexión activa que cerrar.")

