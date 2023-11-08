"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * Componente: Registro.
 * 
 * @version  1.0
 * @date     2023.11.07
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""
from typing import List
import Excepciones

class Registro():
    """Una clase para obtener registros faciles de convertir en 
    entradas de un archivo de log del servidor.
        niveles: Los niveles de log existentes."""
    
    niveles = {
            "DEBUG":1,
            "INFO":2,
            "WARNING":3,
            "ERROR":4,
            "CRITICAL":5}
    
    def __init__(self, args:tuple):
        """Se inicia con una tupla cuyo primer elemento es el nivel de Log
        y cuyo segundo elemento es el mensaje del registro."""
        if args[0] in self.niveles:
            self.nivelLog = args[0]
            if len(args) > 1:
                self.mensaje = args[1]
            else:
                self.mensaje =''
        else:
            raise Excepciones.ExcepcionDeRegistro(1)
    def esDebug(self):
        return self.nivelLog == "DEBUG"
    def esInfo(self):
        return self.nivelLog == "INFO"
    def esWarning(self):
        return self.nivelLog == "WARNING"
    def esError(self):
        return self.nivelLog == "ERROR"
    def esCritical(self):
        return self.nivelLog == "CRITICAL"
    def __str__(self):
        """Devuelve el registro en un formato como el propio el robot."""
        return ":".join([self.nivelLog, self.mensaje])
    
class Registrar():
    """Es un contenedor de Registros."""
    
    def __init__(self, result:str):
        """A partir de una respuesta del robot (result) se obtiene
        una respuesta como una serie de registros de log.
        args:
            result(str): Una cadena con el resultado de un comando en el formato
            en que es devuelta por el robot.
        """
        self.registros:List[Registro] = []
        for elem in result.split('\r\n'):
            entrada = elem.split(':')
            if len(entrada) > 1:
                entrada = (entrada[0], ':'.join(entrada[1:]))
                self.registros.append(Registro(entrada))

    def __str__(self):
        ret = ""
        for elem in self.registros:
            ret += (' '*5 +'{}').format(str(elem) + '\n')
        return ret