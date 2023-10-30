#
# @version 1.0
# @date 2023.10.17
# @author Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco,
# @contact borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com
#/
from typing import List
import Excepciones
class Registro():
    niveles = {
            "DEBUG":1,
            "INFO":2,
            "WARNING":3,
            "ERROR":4,
            "CRITICAL":5}
    
    def __init__(self, args:tuple):
        if args[0] in self.niveles:
            self.nivelLog = args[0]
            if len(args) > 1:
                self.mensaje = args[1]
            else:
                self.mensaje =''
        else:
            raise Excepciones.ExcepcionDeRegistro(1)
    def __str__(self):
        return ":".join([self.nivelLog, self.mensaje])
    
class Registrar():
    def __init__(self, result:str):
        self.registros:List[Registro] = []
        for elem in result.split('\r\n'):
            entrada = elem.split(':')
            if len(entrada) > 1:
                entrada = (entrada[0], ''.join(entrada[1:]))
                self.registros.append(Registro(entrada))
    def __str__(self):
        ret = ""
        for elem in self.registros:
            ret += (' '*5 +'{}').format(str(elem) + '\n')
        return ret