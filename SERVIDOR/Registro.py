
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