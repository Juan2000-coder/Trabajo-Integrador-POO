from ArchivoLog import ArchivoLog
from Registro import Registro

class ArchivoUsuario(ArchivoLog):
    def __init__(self, id:str):
        self.id = id
        FORMAT = '%(asctime)s [%(levelname)s] %(client_ip)s [%(method_name)s] %(message)s'
        super().__init__(id, FORMAT)

    def extra(self, ipCliente, metodo):
        self.dic = {
            "client_ip": ipCliente,
            "method_name": metodo
        }
    
    def log(self, ipCliente, metodo, registro:Registro):
        self.extra(ipCliente, metodo)
        self.logToFile(registro)