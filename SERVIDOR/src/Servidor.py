from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import socket
import Registro
from ArchivoLog import ArchivoLog
import Excepciones
import UsuariosValidos
from Streaming import VideoStreamer

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
        self.streamer = VideoStreamer()
        # self.logUsuarios = {} #Este seria un diccionario para los logs de los usuarios
        self.ipCliente = None

        #addr = (socket.gethostbyname_ex("Juan_Portátil")[2][0], self.puerto)
        addr = (socket.gethostbyname_ex(self.hostname)[2][1], self.puerto)

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

        self.threadRPC = Thread(target = self.run_server, daemon = True)
        self.threadStream = Thread(target = self.streamer.run, daemon = True)
        self.threadRPC.start()
        self.threadStream.start()

        print("Servidor RPC iniciado en el puerto [%s]" % str(self.server_address))

    def run_server(self):
        self.serve_forever()

    def shutdown(self):
        super().shutdown()
        super().server_close()
        self.threadRPC.join()
    
    def shutdownStream(self):
        self.streamer.stop_streaming()

    def _log(func):
        def metodoRPC(self, *args, **kwargs):
            try:
                # Ponemos lo del id de la siguiente manera
                # id = args[0] #El primer argumento que se envia es el id
                #if len(args) > 0:
                    #id = str(args[0])
                    #if UsuariosValidos.validarUsuario(id):
                        argsstr = ''
                        for arg in args:
                            argsstr += str(arg) + ' '
                        resultado = func(self, argsstr, **kwargs)
                        if type(resultado) is Registro.Registrar:
                            respuesta = ""
                            for registro in resultado.registros:
                                self.logServidor.log(self.ipCliente, func.__name__, registro)
                                respuesta += registro.mensaje + '\n'
                            resultado = respuesta
                            self.consola.actualizarJob(func.__name__)#medio tranfuga
                        else:
                            self.logServidor.log(self.ipCliente, func.__name__, Registro.Registro(("INFO", "Solicitud Exitosa")))
                        return resultado
                    #else:
                    #    return "Usuario no registrado." #habría que poner en el log
                #else:
                    #return "Usuario no registrado."#habría que poner en el log
            except Excepciones.Excepciones as e:
                self.logServidor.log(self.ipCliente, func.__name__, e.registro)
                #if id in self.logUsuaros:
                    #self.logUsuarios[id].log(self.ipCliente, func.__name__, e.registro)
                #else:
                    #self.logUsuarios[id] = ArchivoUsuario('Log'+'id.log')
                return e.registro.mensaje
            except Exception as e:
                self.logServidor.log(self.ipCliente, func.__name__, Registro.Registro(("CRITICAL",str(e))))
                #self.logUsuarios[id].log(self.ipCliente, func.__name__, Registro.Regstro(("CRITCAL", str(e))))
                self.consola.estadoServidor(str(e))
                return "El servidor no pudo ejecutar una peticion. Excepcion no identificada."
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
    
    @_log
    def enviarComando(self, args):
        return self.consola.do_enviarComando(args)