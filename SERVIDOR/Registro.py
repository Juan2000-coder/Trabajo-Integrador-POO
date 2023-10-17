#
# @version 1.0
# @date 2023.10.17
# @author Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco,
# @contact borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com
#/
class Registro():
        
        def __init__(self, comando,nivelLog,timeStamp,ipCliente):
            self.comando = comando
            self.nivelLog = nivelLog
            self.timeStamp = timeStamp
            self.ipCliente = ipCliente
        
        def getComando(self):
            return self.comando

        def getNivelLog(self):
             return self.nivelLog
        
        def getTimeStamp(self):
            return self.timeStamp
        
        def getIpCliente(self):
            return self.ipCliente
        