from Punto import Punto
class BrazoRobot():
    def __init__(self):
        self.posicion = Punto(-1, -1, -1)
        # Cuando se crea el objeto, a priori no se conoce la posición
        # del efector final dado que no se inició la conexión con el robot.
        # Entonces se deja en parámetros inválidos
        self.velocidad = -10 # Lo mismo para la velocidad

    def conectarRobot(self):
        # Me imagino que esta debe recibir los parámetros para la conexión
        # Aunque no se si se utiliza una velocidad por defecto o se puede indicar.
        # Revise el proyecto de Arduino y la velocidad de comunicación sí está dada por
        # defecto a 115200 baudios. Se indica en el archivo config.h como BAUD
        # Entonces solamente habría que habilitar la comunicación serial desde la computadora
        # hacia el arduino.
        
        pass