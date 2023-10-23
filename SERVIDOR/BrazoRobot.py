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
            time.sleep(2) #Tiempo para que realice bien la conexion, si no envia los comandos muy rapido.

        except serial.SerialException:
            print("Error al intentar establecer la conexión.")
            self.conexion_establecida = False
            
    def enviarComando(self, comando):
        #USO: respuesta = robot.enviarComando("G28")
        #     print("Arduino dice:", respuesta)
        #Primero almacenar la respuesta del comando, luego printear. 
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
            
    def seleccionarModo(self, modo):
        if modo.lower() == "absolutas":
            respuesta = self.enviarComando("G90")
            print("Arduino dice:", respuesta)
        elif modo.lower() == "relativas":
            respuesta = self.enviarComando("G91")
            print("Arduino dice:", respuesta)
        else:
            print("Modo de coordenadas no válido. Use 'absolutas' o 'relativas'.")
            return  # No se envía un comando si el modo no es válido
    
    def movLineal(self, punto, velocidad=None):
        if isinstance(punto, Punto):
            if velocidad is not None:
                comando = f"G1 X{punto.x:.2f} Y{punto.y:.2f} Z{punto.z:.2f} E{velocidad}"
            else:
                comando = f"G1 X{punto.x:.2f} Y{punto.y:.2f} Z{punto.z:.2f}"
            
            respuesta = self.enviarComando(comando)
            print("Arduino dice:", respuesta)
        else:
            print("El argumento debe ser un objeto de la clase Punto.")

    def activarPinza(self):
            respuesta = self.enviarComando("M3")
            print("Arduino dice:", respuesta)
            
    def desactivarPinza(self):
            respuesta = self.enviarComando("M5")
            print("Arduino dice:", respuesta)  

    def home(self):
            respuesta = self.enviarComando("G28")
            print("Arduino dice:", respuesta)  
    
    def activarMotor(self):
        print("Arduino dice: Motor activado")  
            
    def desactivarMotor(self):
        print("Arduino dice: Motor desactivado")  

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