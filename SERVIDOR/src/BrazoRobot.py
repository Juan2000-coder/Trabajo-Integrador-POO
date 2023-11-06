"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * Componente: Brazo Robot.
 * 
 * @version  1.0
 * @date     2023.11.06
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""

import serial
from Excepciones import ExcepcionBrazoRobot     # Clase con excepciones personalizadas.

class BrazoRobot():
    """Clase con implementación de los comandos para la comunicación con
    la placa de control del brazo Robótico."""

    def __init__(self):
        self.posicion = None    # Posición inicial desconocida.
        self.velocidad = None   # Velocidad inicial desconocida.
        self.conexionEstablecida = False
        self.puertoSerie = None

    def conectarRobot(self, puerto:str, baudios = 115200):
        """Establece la comunicación serial con el brazo Robótico.
        
        args:
            puerto(str): Puerto COM donde se conecta la placa del Robot.
            baudios(int): Velocidad normalizada de comuniacion con el Robot.
        returns:
            (str) Un mensaje indicando que la conexion se ha establecido, o 
            una exepción del archivo de Excepciones si se produce un error al 
            intentar establecer la comunicación.
        """
        if not self.conexionEstablecida:
            try:
                self.puertoSerie = serial.Serial(puerto, baudios, timeout = 1)
                self.conexionEstablecida = True
                return "INFO: Conexión exitosa con el robot."
        
            except Exception as e:
                if not self.conexionEstablecida:
                    raise ExcepcionBrazoRobot(1)
        else:
            raise ExcepcionBrazoRobot(7)
        
    def enviarComando(self, comando:str):
        """Envía un comando en G-Code al Robot.
        
        args:
            comando(str): El comando G-Code con los argumentos.
        returns:
            (str) Un mensaje proveniente de la placa del Robot o una excepcion
            del archivo de Excepciones en caso de error.
        """ 
        if self.conexionEstablecida:
            try:
                self.puertoSerie.write((comando + '\r\n').encode())
                
                data = b''
                while True:
                    line = self.puertoSerie.readline()
                    if not line:
                        break
                    data += line

                return data.decode().strip()
            
            except Exception as e:
                raise ExcepcionBrazoRobot(3)

        else:
            raise ExcepcionBrazoRobot(2)


    def desconectarRobot(self):
        """Cierra la conexión serial con el Robot.
        
        returns:
            (str) Un mensaje indicando la desconexión o una excepción
            del archivo de Excepciones en caso de que ocurra un error.
        """ 
        if self.conexionEstablecida:
            try:
                self.puertoSerie.close()
                self.conexionEstablecida = False
                return "INFO: Conexión cerrada."
            except Exception as e:
                raise ExcepcionBrazoRobot(5)
        else:
            raise ExcepcionBrazoRobot(4)
            
    def seleccionarModo(self, modo:str):
        """Selecciona el modo de operación del brazo Robótico
        entre funcionamiento en coordenadas absolutas o relativas.

        args:
            modo(str): El modo 'a' indicando coordenadas Absolutas.
                       El modo 'r' indicando coordenadas Relativas.
        returns:
            (str) Un mensaje desde el robot indicando el modo seleccionado
            o una excepción en caso de error.
        """ 
        if modo.lower() == "a":
            return self.enviarComando("G90")
        elif modo.lower() == "r":
            return self.enviarComando("G91")
        else:
            raise ExcepcionBrazoRobot(6)
    
    def movLineal(self, coor:list, velocidad = 0):
        """Produce el movimento lineal del efector final
        hacia una coordenada indicada.

        args:
            coor(list): Las coordenadas del punto destino.
            velocidad(float): La velocidad del movimiento. Se toma una por
                defecto en caso de no indicarse.
        returns:
            (str) Un mensaje desde el robot indicando el resultado de la operación
            o una excepción en caso de error.
        """
        if velocidad != 0:
            comando = f"G1 X{coor[0]} Y{coor[1]} Z{coor[2]} E{velocidad}"
        else:
            comando = f"G0 X{coor[0]} Y{coor[1]} Z{coor[2]}"
        return self.enviarComando(comando)
        
    def activarEfector(self):
        """Activa el efector final del Robot.
.
        returns:
            (str) Un mensaje desde el robot indicando el resultado de la operación
            o una excepción en caso de error.
        """
        return self.enviarComando("M3")
            
    def desactivarEfector(self):
        """Desactiva el efector final del Robot.
.
        returns:
            (str) Un mensaje desde el robot indicando el resultado de la operación
            o una excepción en caso de error.
        """
        return self.enviarComando("M5") 

    def home(self):
        """Realiza la operación de Homing drl Robot.
.
        returns:
            (str) Un mensaje desde el robot indicando el resultado de la operación
            o una excepción en caso de error.
        """
        return  self.enviarComando("G28")
    
    def estado(self):
        """Obtiene el estado actual del Robot (posicion, modo).
.
        returns:
            (str) Un mensaje desde el robot indicando el resultado de la operación
            o una excepción en caso de error.
        """
        return  self.enviarComando("M114")
    
    def activarMotores(self):
        """Activa los motores del Robot.
.
        returns:
            (str) Un mensaje indicando el exito de la operación o
            una excepción en caso de error.
        """
        self.enviarComando("G17")
        return "INFO: Motor activado."
            
    def desactivarMotores(self):
        """Desactiva el efector final del Robot.
.
        returns:
            (str) Un mensaje indicando el exito de la operación o 
            una excepción en caso de error.
        """
        self.enviarComando("G18")
        return "INFO: Motor desactivado."