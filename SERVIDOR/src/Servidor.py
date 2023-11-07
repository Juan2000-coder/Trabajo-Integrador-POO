"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * Modulo: Servidor
 * 
 * @version  1.0
 * @date     2023.11.06
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import socket
import Registro
from Log import LogServidor, LogUsuario
import Excepciones
from UsuariosValidos import UsuariosValidos
from Streaming import VideoStreaming

class Handler(SimpleXMLRPCRequestHandler):
    """Un Handler proprio definido sobre todo para obtener la ip
    de un cliente remoto que hace una solicitud."""

    def __init__(self, peticion, direccionCliente, servidor):
        # Esto actualiza la ip de cliente que conoce el Servidor.
        servidor.ipCliente = direccionCliente[0]
        super().__init__(peticion, direccionCliente, servidor)

class Servidor(SimpleXMLRPCServer):
    def __init__(self, consola, puertoRPC = 8000, addr = None, requestHandler= Handler,
                     logRequests=False, allow_none=False, encoding=None,
                     bind_and_activate=True, use_builtin_types=False):
        self.hostname = socket.getfqdn()
        self.consola = consola      # Corresponde al CLI que construye al Servidor.
        self.puerto = puertoRPC
        self.logServidor = LogServidor('Log')
        self.streamer = VideoStreaming()
        self.logUsuario:LogUsuario = None   # El archivo de log para un usuario.
        self.idActual = ''                  # El id del usuario de la solicitud actual.
        self.ipCliente = None               # La ip del cliente actual.

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

        self.register_function(self.robot, 'robot')
        self.register_function(self.motores, 'motores') 
        self.register_function(self.modo, 'modo')
        self.register_function(self.reporte, 'reporte') 
        self.register_function(self.home, 'home') 
        self.register_function(self.log, 'log') 
        self.register_function(self.movlineal, 'movlineal') 
        self.register_function(self.efector, 'efector')  
        self.register_function(self.grabar, 'grabar') 
        self.register_function(self.cargar, 'cargar')        
        self.register_function(self.listar, 'listar') 
        self.register_function(self.estado, 'estado')
        self.register_function(self.ejecutar, 'ejecutar')
        self.register_introspection_functions()

        self.hiloRPC = Thread(target = self.correrServidor, daemon = True)
        self.hiloRPC.start()    # Inicia el servidor RPC.
        self.streamer.start()   # Inicia el Straming.
        
        print("Servidor RPC iniciado en el puerto [%s]" % str(self.server_address))

    def correrServidor(self):
        """Inicia el Servidor RPC."""
        self.serve_forever()

    def detener(self):
        """Detiene el Servidor y el Straming"""
        super().shutdown()
        super().server_close()
        self.streamer.detenerStreaming()
        self.hiloRPC.join()
        self.streamer.join()

    def _log(func):
        """Un decorador que decora todos los métodos accesibles de forma
        remota para registrar en el log del usuario actual y del servidor.
        Además llama al método de validación de usuarios.
        """
        def metodoRPC(self, *args, **kwargs):
            try:
                if len(args) > 0:   # Al menos hay que indicar el id.

                    id = str(args[0])       # Id cliente actual.
                    if UsuariosValidos.validarUsuario(id):
                        if self.idActual != id:
                            self.idActual = id
                            self.logUsuario = LogUsuario(id)

                        # Se transforman los argumentos en str.
                        argsstr = ''        
                        for arg in args[1:]:
                            argsstr += str(arg) + ' '

                        # Llama al método del servidor.
                        resultado = func(self, argsstr, **kwargs)

                        if type(resultado) is Registro.Registrar:
                            # Se convierte el resultado del método en un str.
                            respuesta = ""
                            for registro in resultado.registros:
                                # Se actualiza el log.
                                self.logServidor.log(id, self.ipCliente, func.__name__, registro)
                                self.logUsuario.log(self.ipCliente, func.__name__, registro)
                                respuesta += registro.mensaje + '\n'
                                
                            if self.consola.grabando:   # Si se encuentra en grabación.
                                self.consola.archivoJob.actualizar(func.__name__+ ' ' + argsstr, resultado)
                            resultado = respuesta       # La respuesta en str.
                        else:
                            # El flujo viene aquí cuando se llaman a los método de reporte
                            # o de log, los que no devuelven un objeto de tipo Registro.Registrar.
                            self.logServidor.log(id, self.ipCliente, func.__name__, Registro.Registro(("INFO", "Solicitud Exitosa")))
                            self.logUsuario.log(self.ipCliente, func.__name__, Registro.Registro(("INFO", "Solicitud Exitosa")))

                        return resultado
                    else:
                        return "Usuario no registrado."
                else:
                    return "No se ha indicado id."
                
            except Excepciones.Excepciones as e:
                #  Se registran las excepciones.
                self.logServidor.log(id, self.ipCliente, func.__name__, e.registro)
                self.logUsuario.log(self.ipCliente, func.__name__, e.registro)
                return e.registro.mensaje # Se devuelve el mensaje de la excepcion.
            
            except Exception as e:
                #  Excepciones no identificadas.
                self.logServidor.log(id, self.ipCliente, func.__name__, Registro.Registro(("CRITICAL",str(e))))
                self.logUsuario.log(self.ipCliente, func.__name__, Registro.Registro(("CRITICAL", str(e))))
                self.consola.estadoServidor(str(e))     # En estos casos se reporta el error al CLI.
                return "El servidor no pudo ejecutar una peticion. Excepcion no identificada."
        return metodoRPC
    @_log
    def robot(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato."""
        return self.consola.do_robot(args)
    
    @_log
    def motores(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato."""
        return self.consola.do_motores(args)

    @_log
    def reporte(self, args):
        """Obtiene el reporte de actividad del cliente que hace el llamado.
        args:
            args(str): Los parámetros del comando.
        returns:
            (str): El reporte de actividad en formato de tabla."""
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
        """Obtiene el log del usuario que hace el llamado.
        args:
            args(str): Los parámetros del comando.
        returns:
            (str): El contenido del log en formato str."""
        return self.logUsuario.obtenerLog()
    
    @_log
    def modo(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato.""" 
        return self.consola.do_modo(args)
    
    @_log
    def home(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato."""
        return self.consola.do_home(args)
    
    @_log
    def movlineal(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato."""
        return self.consola.do_movlineal(args)
    
    @_log
    def efector(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato."""
        return self.consola.do_efector(args)

    @_log
    def grabar(self, args):
        return self.consola.do_grabar(args)
    
    @_log
    def cargar(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato."""
        return self.consola.do_cargar(args)
    
    @_log
    def listar(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato."""
        return self.consola.do_listar(args)
    
    @_log
    def estado(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato."""
        return self.consola.do_estado(args)
    
    @_log
    def ejecutar(self, args):
        """Llama al metodo en la consola.
        args:
            args(str): Los parámetros del comando.
        returns:
            (Registro.Registrar): El resultado dado por el Robot en este formato."""
        return self.consola.do_ejecutar(args)