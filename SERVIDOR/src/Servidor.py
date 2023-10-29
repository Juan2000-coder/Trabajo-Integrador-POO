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
                argsstr = ''
                for arg in args:
                    argsstr += str(arg) + ' '
                    
                resultado = func(self, argsstr, **kwargs)
                logging.info(resultado, extra=self.dic)
                return resultado
            except Excepciones.Excepciones as e:
                return "error"
        return metodoRPC
    
    @_log
    def conectarRobot(self, args):
        return self.consola.do_conectarRobot(args)

    @_log
    def desconectarRobot(self, args):
        return self.consola.do_desconectarRobot(args)
    
    @_log
    def activarMotores(self, args):
        return self.consola.do_activarMotores(args)
    
    @_log
    def desactivarMotores(self, args):
        return self.consola.do_desactivarMotores(args)
    
    @_log
    def reporteGeneral(self, args):
        return self.consola.do_reporteGeneral(args)
    
    @_log
    def obtenerLogServidor(self, args):
        return self.logServidor.obtenerLog(args)
    
    @_log
    def seleccionarModo(self, args): 
        return self.consola.do_seleccionarModo(args)
    
    @_log
    def home(self, args):
        return self.consola.do_home(args)
    
    @_log
    def movLineal(self, args):
        return self.consola.do_movLineal(args)
    
    @_log
    def activarPinza(self, args):
        return self.consola.do_activarPinza(args)
    
    @_log
    def desactivarPinza(self, args):
        return self.consola.do_desactivarPinza(args)
    
    @_log
    def grabar(self, args):
        return self.consola.do_grabar(args)
    
    @_log
    def cargar(self, args):
        return self.consola.do_cargar(args)
    
    @_log
    def listarArchivosDeTrabajo(self, args):
        return self.consola.do_listarArchivosDeTrabajo(args)
    
    @_log
    def posicionActual(self, args):
        return self.consola.do_posicionActual(args)