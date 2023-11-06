from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import socket
import Registro
from ArchivoLog import ArchivoLog
from ArchivoUsuario import ArchivoUsuario
import Excepciones
from UsuariosValidos import UsuariosValidos
from Streaming import VideoStreaming
from CLI import CLI

class Handler(SimpleXMLRPCRequestHandler):
    """Un Handler proprio definido sobre todo para obtener la ip
    de un cliente remoto que hace una solicitud."""

    def __init__(self, peticion, direccionCliente, servidor):
        # Esto actualiza la ip de cliente que conoce el Servidor.
        servidor.ipCliente = direccionCliente[0]
        super().__init__(peticion, direccionCliente, servidor)

class Servidor(SimpleXMLRPCServer):
    def __init__(self, consola:CLI, puertoRPC = 8000, addr = None, requestHandler= Handler,
                     logRequests=False, allow_none=False, encoding=None,
                     bind_and_activate=True, use_builtin_types=False):
        self.hostname = socket.getfqdn()
        self.consola = consola      # Corresponde al CLI que construye al Servidor.
        self.puerto = puertoRPC
        self.logServidor = ArchivoLog('Log')
        self.streamer = VideoStreaming()
        self.logUsuario:ArchivoUsuario = None      # El archivo de log para un usuario.
        self.idActual = ''     # El id del usuario de la solicitud actual.
        self.ipCliente = None

        addr = (socket.gethostbyname_ex(self.hostname)[2][0], self.puerto)
        #addr = (socket.gethostbyname_ex(self.hostname)[2][1], self.puerto)

        try:
            super().__init__(addr, requestHandler, logRequests, allow_none, encoding, bind_and_activate,
                             use_builtin_types)
            
        except socket.error as e:
            if e.errno == 98:
                raise Excepciones.ExcepcionDeServidor(1)
            else:
                raise

        self.register_function(self.robot, 'robot')
        self.register_function(self.motores, 'motores') 
        self.register_function(self.modo, 'modo')
        self.register_function(self.reporte, 'reporte') 
        self.register_function(self.home, 'home') 
        self.register_function(self.log, 'log') 
        self.register_function(self.movLineal, 'movLineal') 
        self.register_function(self.efector, 'efector')  
        self.register_function(self.grabar, 'grabar') 
        self.register_function(self.cargar, 'cargar')        
        self.register_function(self.listar, 'listar') 
        self.register_function(self.estado, 'estado')
        self.register_function(self.ejecutar, 'ejecutar')
        self.register_introspection_functions()

        self.hiloRPC = Thread(target = self.correrServidor, daemon = True)
        self.hiloRPC.start()
        self.streamer.start()
        
        print("Servidor RPC iniciado en el puerto [%s]" % str(self.server_address))

    def correrServidor(self):
        self.serve_forever()

    def detener(self):
        super().shutdown()
        super().server_close()
        self.streamer.detenerStreaming()
        self.hiloRPC.join()
        self.streamer.join()

    def _log(func):
        def metodoRPC(self, *args, **kwargs):
            try:
                if len(args) > 0:
                    id = str(args[0])
                    if UsuariosValidos.validarUsuario(id):
                        if self.idActual != id:
                            self.idActual = id
                            self.logUsuario = ArchivoUsuario(id)
                        argsstr = ''
                        for arg in args[1:]:
                            argsstr += str(arg) + ' '
                        resultado = func(self, argsstr, **kwargs)
                        if type(resultado) is Registro.Registrar:
                            respuesta = ""
                            for registro in resultado.registros:
                                self.logServidor.log(id, self.ipCliente, func.__name__, registro)
                                self.logUsuario.log(self.ipCliente, func.__name__, registro)
                                respuesta += registro.mensaje + '\n'
                            resultado = respuesta
                            if self.consola.grabando:
                                self.archivoJob.actualizar(func.__name__ + argsstr)
                        else:
                            self.logServidor.log(id, self.ipCliente, func.__name__, Registro.Registro(("INFO", "Solicitud Exitosa")))
                            self.logUsuario.log(self.ipCliente, func.__name__, Registro.Registro(("INFO", "Solicitud Exitosa")))
                        return resultado
                    else:
                        return "Usuario no registrado."
                else:
                    return "Usuario no registrado."
            except Excepciones.Excepciones as e:
                self.logServidor.log(id, self.ipCliente, func.__name__, e.registro)
                self.logUsuario.log(self.ipCliente, func.__name__, e.registro)
                return e.registro.mensaje
            except Exception as e:
                self.logServidor.log(id, self.ipCliente, func.__name__, Registro.Registro(("CRITICAL",str(e))))
                self.logUsuario.log(self.ipCliente, func.__name__, Registro.Registro(("CRITICAL", str(e))))
                self.consola.estadoServidor(str(e))
                return "El servidor no pudo ejecutar una peticion. Excepcion no identificada."
        return metodoRPC
    @_log
    def robot(self, args):
        return self.consola.do_robot(args)
    
    @_log
    def motores(self, args):
        return self.consola.do_motores(args)

    @_log
    def reporte(self, args):
        respuesta = ""
        try:
            estado = self.consola.do_estado('')
            for registro in estado.registros:
                respuesta += registro.mensaje + '\n'

        except Excepciones.ExcepcionBrazoRobot as e:
            if e.codigoDeExcepcion == 2:
                respuesta += "Robot Desconectado.\n"
            else:
                raise

        respuesta += self.logUsuario.reporteGeneral()
        return respuesta
    
    @_log
    def log(self, args):
        return self.logUsuario.obtenerLog()
    
    @_log
    def modo(self, args): 
        return self.consola.do_modo(args)
    
    @_log
    def home(self, args):
        return self.consola.do_home(args)
    
    @_log
    def movLineal(self, args):
        return self.consola.do_movLineal(args)
    
    @_log
    def efector(self, args):
        return self.consola.do_efector(args)

    @_log
    def grabar(self, args):
        return self.consola.do_grabar(args)
    
    @_log
    def cargar(self, args):
        return self.consola.do_cargar(args)
    
    @_log
    def listar(self, args):
        return self.consola.do_listar(args)
    
    @_log
    def estado(self, args):
        return self.consola.do_estado(args)
    
    @_log
    def ejecutar(self, args):
        return self.consola.do_ejecutar(args)