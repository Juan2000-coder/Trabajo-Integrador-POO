from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
import socket
import logging

hostname = socket.getfqdn()
RPC_PORT = 8000

class Servidor():
    server = None

    def __init__(self, consola, port = RPC_PORT):
        self.consola = consola
        used_port = port
        while True:
            try:
                self.server = SimpleXMLRPCServer((socket.gethostbyname_ex(hostname)[2][1], port),
                                                 allow_none = True,
                                                 logRequests = None)
                if used_port != port:
                    logging.warning(_("RPC server bound on non-default port %d") % used_port)
                break
            except socket.error as e:
                if e.errno == 98:
                    used_port += 1
                    continue
                else:
                    raise

        self.server.register_function(self.conectarRobot, 'conectarRobot')   
        self.server.register_function(self.activarMotores, 'activarMotores') 
        self.server.register_function(self.desactivarMotores, 'desactivarMotores') 
        self.server.register_function(self.reporteGeneral, 'reporteGeneral') 
        self.server.register_function(self.home, 'home') 
        self.server.register_function(self.obtenerLogServidor, 'obtenerLogServidor') 
        self.server.register_function(self.movLineal, 'movLineal') 
        self.server.register_function(self.activarPinza, 'activarPinza') 
        self.server.register_function(self.desactivarPinza, 'desactivarPinza') 
        self.server.register_function(self.grabar, 'grabar') 
        self.server.register_function(self.cargar, 'cargar')        
        self.server.register_function(self.listarArchivosDeTrabajo, 'listarArchivosDeTrabajo') 

        self.thread = Thread(target = self.run_server)
        self.thread.start()
        print("Servidor RPC iniciado en el puerto [%s]" % str(self.server.server_address))

    def run_server(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.thread.join()
    
    def conectarRobot(self):
        return self.consola.onecmd("conectarRobot")
    
    def activarMotores(self):
        return self.consola.onecmd("activarMotores")
    
    def desactivarMotores(self):
        return self.consola.onecmd("desactivarMotores")
    
    def reporteGeneral(self):
        return self.consola.onecmd("reporteGeneral")
    
    def obtenerLogServidor(self):
        return self.consola.onecmd("obtenerLogServidor")
    
    def seleccionarModo(self, args):
        return self.consola.onecmd("seleccionarModo" + args)
    
    def home(self):
        return self.consola.onecmd("home")
    
    def movLineal(self,args):
        return self.consola.onecmd("movLineal" + args)
    
    def activarPinza(self):
        return self.consola.onecmd("activarPinza")
    
    def desactivarPinza(self):
        return self.consola.onecmd("desactivarPinza")
    
    def grabar(self):
        return self.consola.onecmd("grabar")
    
    def cargar(self):
        return self.consola.onecmd("cargar")
    
    def listarArchivosDeTrabajo(self):
        return self.consola.onecmd("listarArchivosDeTrabajo")