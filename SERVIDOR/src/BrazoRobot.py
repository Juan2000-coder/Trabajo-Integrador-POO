import serial
import time

from Punto import Punto
from Excepciones import ExcepcionBrazoRobot

class BrazoRobot():
    def __init__(self):
        self.posicion = None    # Posición inicial desconocida.
        self.velocidad = None   # Lo mismo para la velocidad.
        self.conexion_establecida = False
        self.puerto_serie = None

    def conectarRobot(self, puerto:str, baud_rate):
        # La velocidad de comunicación que acepta al momento es de 115200 baudios.   
        if not self.conexion_establecida:
            try:
                self.puerto_serie = serial.Serial(puerto, baud_rate)
                self.conexion_establecida = True
                time.sleep(2)   #Tiempo para que realice bien la conexion, si no envia los comandos muy rapido.
                return "INFO:Conexión exitosa con el robot."
        
            except Exception as e:
                if not self.conexion_establecida:
                    raise ExcepcionBrazoRobot(1)
        else:
            raise ExcepcionBrazoRobot(7)
        
    def enviarComando(self, comando:str):
        #USO: respuesta = robot.enviarComando("G28")
        #     print("Arduino dice:", respuesta)
        #Primero almacenar la respuesta del comando, luego printear. 
        if self.conexion_establecida:
            try:
                self.puerto_serie.write((comando + '\r'+'\n').encode('utf-8'))

                # Ajusta un tiempo de espera (timeout) en segundos
                self.puerto_serie.timeout = 1
                data = b""

                while True:
                    line = self.puerto_serie.readline()
                    if not line:
                        break
                    data += line

                return data.decode('utf-8').strip()
            
            except Exception as e:
                raise ExcepcionBrazoRobot(3)

        else:
            raise ExcepcionBrazoRobot(2)


    def desconectarRobot(self):
        if self.conexion_establecida:
            try:
                self.puerto_serie.close()
                self.conexion_establecida = False
                return "INFO:Conexión cerrada."
            except Exception as e:
                raise ExcepcionBrazoRobot(5)
        else:
            raise ExcepcionBrazoRobot(4)
            
    def seleccionarModo(self, modo:str):
        if modo.lower() == "a":
            return self.enviarComando("G90")
        elif modo.lower() == "r":
            return self.enviarComando("G91")
        else:
            raise ExcepcionBrazoRobot(6)
    
    def movLineal(self, punto:Punto, velocidad=None):
        if isinstance(punto, Punto):
            if velocidad is not None:
                comando = f"G1 X{punto.x:.2f} Y{punto.y:.2f} Z{punto.z:.2f} E{velocidad:.2f}"
            else:
                comando = f"G1 X{punto.x:.2f} Y{punto.y:.2f} Z{punto.z:.2f}"
            return self.enviarComando(comando)
        else:
            raise ExcepcionBrazoRobot(6)
        
    def activarPinza(self):
        return self.enviarComando("M3")
            
    def desactivarPinza(self):
        return self.enviarComando("M5") 

    def home(self):
        return  self.enviarComando("G28")
    
    def posicionActual(self):
        return  self.enviarComando("M114")
    
    def activarMotor(self):
        self.enviarComando("G17")
        return "INFO:Motor activado."
            
    def desactivarMotor(self):
        self.enviarComando("G18")
        return "INFO:Motor desactivado."

'''
Ejemplo test
if __name__ == "__main__":
robot = BrazoRobot()
puerto = 'COM5'
velocidad = 115200
robot.conectarRobot(puerto, velocidad)

#   while robot.conexion_establecida:
#      comando = input("Ingresa un comando (o 'q' para salir): ")
#     if comando.lower() == 'q':
#        break
    #   respuesta = robot.enviarComando(comando)
    #  print("Arduino dice:", respuesta)
respuesta = robot.enviarComando("G28")
print("Arduino dice:", respuesta)


robot.seleccionarModo("absolutas")


# Opción 1: Modo coordenadas absolutas
# Esto enviará "G90" a Arduino

#robot.seleccionarModo("relativas")
# Opción 2: Modo coordenadas relativas
# Esto enviará "G91" a Arduino

# Crear un objeto Punto con las coordenadas deseadas
objetivo = Punto(10.0, 180.0, 130.0)
robot.movLineal(objetivo)

respuesta = robot.enviarComando("G28")
print("Arduino dice:", respuesta)

objetivo = Punto(10.0, 180.0, 130.0)
robot.movLineal(objetivo, 5)

robot.seleccionarModo("relativas")
respuesta = robot.enviarComando("G0")
print("Arduino dice:", respuesta)

respuesta = robot.enviarComando("M5")
print("Arduino dice:", respuesta)

respuesta = robot.enviarComando("M3")
print("Arduino dice:", respuesta)



robot.desconectarRobot()
'''