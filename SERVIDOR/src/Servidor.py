from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import socket
import logging

from ArchivoLog import ArchivoLog
import Excepciones

class Handler(SimpleXMLRPCRequestHandler):
    def __init__(self, request, client_address, server):
        server.ipCliente = client_address[0]
        super().__init__(request, client_address, server)

class Servidor(SimpleXMLRPCServer):
    def __init__(self, consola, puertoRPC = 8000, addr = None, requestHandler= Handler,
                     logRequests=False, allow_none=False, encoding=None,
                     bind_and_activate=True, use_builtin_types=False):
        
        self.hostname = socket.getfqdn()
        self.consola = consola
        self.puerto = puertoRPC
        self.logServidor = ArchivoLog('Log.log')
        self.ipCliente = None

        addr = (socket.gethostbyname_ex(self.hostname)[2][0], self.puerto)

        FORMAT = '%(asctime)s [%(levelname)s] - %(client_ip)s - %(method_name)s - %(message)s'
        logging.basicConfig(filename=self.logServidor.nombreArchivo, level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

        try:
            super().__init__(addr, requestHandler, logRequests, allow_none, encoding, bind_and_activate,
                             use_builtin_types)
            
        except socket.error as e:
            if e.errno == 98:
                raise Excepciones.ExcepcionDeServidor(1)
            else:
                raise

        self.register_function(self.conectarRobot, 'conectarRobot')
        self.register_function(self.desconectarRobot, 'desconectarRobot')
        self.register_function(self.activarMotores, 'activarMotores') 
        self.register_function(self.seleccionarModo, 'seleccionarModo')
        self.register_function(self.desactivarMotores, 'desactivarMotores') 
        self.register_function(self.reporteGeneral, 'reporteGeneral') 
        self.register_function(self.home, 'home') 
        self.register_function(self.obtenerLogServidor, 'obtenerLogServidor') 
        self.register_function(self.movLineal, 'movLineal') 
        self.register_function(self.activarPinza, 'activarPinza') 
        self.register_function(self.desactivarPinza, 'desactivarPinza') 
        self.register_function(self.grabar, 'grabar') 
        self.register_function(self.cargar, 'cargar')        
        self.register_function(self.listarArchivosDeTrabajo, 'listarArchivosDeTrabajo') 
        self.register_function(self.posicionActual, 'posicionActual')
        self.register_function(self.enviarComando, 'enviarComando')
        #self.register_function(self.video_server.get_video_frame, 'get_video_frame')
    
        self.thread = Thread(target = self.run_server)
        self.thread.start()
        print("Servidor RPC iniciado en el puerto [%s]" % str(self.server_address))

    def run_server(self):
        self.serve_forever()

    def shutdown(self):
        self.shutdown()
        self.thread.join()
    
    def _log(func):
        def metodoRPC(self, *args, **kwargs):
            print(func.__name__)
            self.dic = {
                "client_ip": self.ipCliente,
                "method_name": func.__name__
            }
            try:
                resultado = func(self, *args, **kwargs)
                logging.info(resultado, extra=self.dic)
                return resultado
            except Excepciones as e:
                return "error"
        return metodoRPC
    
    @_log
    def conectarRobot(self):
        return self.consola.do_conectarRobot()

    @_log
    def desconectarRobot(self):
        return self.consola.onecmd("desconectarRobot")
    
    @_log
    def activarMotores(self):
        return self.consola.onecmd("activarMotores")
    
    @_log
    def desactivarMotores(self):
        return self.consola.onecmd("desactivarMotores")
    
    @_log
    def reporteGeneral(self):
        return self.consola.onecmd("reporteGeneral")
    
    @_log
    def obtenerLogServidor(self):
        return self.logServidor.obtenerLog()
    
    @_log
    def seleccionarModo(self, args):
        return self.consola.onecmd("seleccionarModo " + args)
    
    @_log
    def home(self):
        return self.consola.onecmd("home")
    
    @_log
    def movLineal(self,arg1, arg2, arg3, arg4=""):
        return self.consola.onecmd("movLineal " + arg1 +" "+ arg2+" "+arg3+" "+arg4)
    
    @_log
    def activarPinza(self):
        return self.consola.onecmd("activarPinza")
    
    @_log
    def desactivarPinza(self):
        return self.consola.onecmd("desactivarPinza")
    
    @_log
    def grabar(self, args):
        return self.consola.onecmd("grabar "+ args)
    
    @_log
    def cargar(self):
        return self.consola.onecmd("cargar")
    
    @_log
    def listarArchivosDeTrabajo(self):
        return self.consola.onecmd("listarArchivosDeTrabajo")
    
    @_log
    def posicionActual(self):
        return self.consola.onecmd("posicionActual")
    
    @_log
    def enviarComando(self, args):
        return self.consola.onecmd("enviarComando " + args)