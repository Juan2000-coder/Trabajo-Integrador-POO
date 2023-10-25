#
# @version 1.0
# @date 2023.10.17
# @author Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco,
# @contact borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com
#/
class Registro():
        
        def __init__(self, timeStamp, ipCliente:str, comando:str, nivelLog:str, mensaje:str):
            self.comando = comando
            self.nivelLog = nivelLog
            self.timeStamp = timeStamp
            self.ipCliente = ipCliente
            self.mensaje = mensaje
        
        def __str__(self):
            return f"{self.timeStamp};{self.ipCliente};{self.comando};{self.nivelLog};{self.mensaje}\n"