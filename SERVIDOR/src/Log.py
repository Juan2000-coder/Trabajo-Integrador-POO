"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * 
 * 
 * @version  1.0
 * @date     2023.11.06
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""

from Excepciones import ExcepcionArchivo
import logging
import os
from Registro import Registro
import re
from prettytable import PrettyTable


class Log(logging.Logger):
    ruta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(ruta, "..", "archivos")
    DATEFMT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, nombre: str, FORMAT = '[%(asctime)s] [%(levelname)s] %(client_id)s %(client_ip)s [%(method_name)s] %(message)s'):
        super().__init__(nombre)
        self.archivo = os.path.join(self.ruta, nombre)
        self.fileHandler = logging.FileHandler(f'{self.archivo}.log')
        self.FORMAT = FORMAT
        self.formatter = logging.Formatter(fmt = self.FORMAT, datefmt=self.DATEFMT)
        self.fileHandler.setFormatter(self.formatter)
        self.addHandler(self.fileHandler)

    def obtenerLog(self):
        """Obtiene el log como un str.
        returns:
            (str): El archivo como un str.
            O una excepción en caso de error.
        """
        try:
            with open(self.fileHandler.baseFilename, 'r') as log:
                return ''.join(log.readlines())
        except Exception as e:
            raise ExcepcionArchivo(1)
        
    def extra(self, idCliente, ipCliente, metodo):
        """Define un diccionario con valores para la entrada en el Log.
        args:
            idCliente: El id de un Cliente.
            ipCliente: La dirección ip del Cliente.
            metodo: El nombre del método RPC.
        """
        self.dic = {
            "client_id": idCliente,
            "client_ip": ipCliente,
            "method_name": metodo
        }
        return self.dic
        
    def log(self, idCliente, ipCliente, metodo, registro:Registro):
        """Crea la entrada de log y llama a la función de escritura.
        args:
            idCliente: El id de un Cliente.
            ipCliente: La dirección ip del Cliente.
            metodo: El nombre del método RPC.
            registro: Un registro con el nivel del Log y un mensaje.
        """
        extra = self.extra(idCliente, ipCliente, metodo)
        self.logToFile(registro, extra)

    def logToFile(self, registro:Registro, dic):
        """Escribe el log en el archivo.
        
        args:
            registro: un registro con el nivel de Log y un mensaje.
            dic: un diccionario con el resto de los campos de la entrada de log.
        """
        if registro.nivelLog == "DEBUG":
            self.debug(registro.mensaje, extra=dic)
        elif registro.nivelLog == "INFO":
            self.info(registro.mensaje, extra=dic)
        elif registro.nivelLog == "WARNING":
            self.warning(registro.mensaje, extra=dic)
        elif registro.nivelLog == "ERROR":
            self.error(registro.mensaje, extra=dic)
        elif registro.nivelLog == "CRITICAL":
            self.critical(registro.mensaje, extra=dic)

    def reporteGeneral(self):
        """Obtiene el reporte general a partir del log en formato de tabla.
        returns:
            (str): El Reporte conteniendo el estado del robot y una tabla
                   a 3 columnas con los campos (metodo|ocurrencias|errores).
        """
        patron = r'\[([^\]]*)\]'    # El patrón de búsqueda.
        metodos = {}                # Un diccionario cuyas claves son los métodos.
        with open(self.fileHandler.baseFilename, 'r') as archivo:

            # Se recorre el archivo registrando para cada método
            # el número de ocurrencias y la cantidad de veces que dió error.
            for i, registro in enumerate(archivo):
                secuencias = re.findall(patron, registro)
                if i == 0:
                    inicio = secuencias[0]  # Indica la estampa de tiempo de la primer entrada.
                nivel = secuencias[1]       # El nivel de log de la entrada.
                metodo = secuencias[2]      # El nombre del método de la entrada.

                if metodo in metodos:
                    metodos[metodo]["ocurrencias"] += 1
                    if nivel == "ERROR":
                        metodos[metodo]["errores"] += 1
                else:
                    reporteMetodo = {"ocurrencias": 1,
                                     "errores": 0}
                    metodos[metodo] = reporteMetodo
                    if nivel == "ERROR":
                        metodos[metodo]["errores"] = 1
                    else:
                        metodos[metodo]["errores"] = 0

        table = PrettyTable()
        table.field_names = ["metodo", "ocurrencias", "errores"]
        for metodo, valores in metodos.items():
            entrada = [metodo]
            entrada = entrada + list(valores.values())
            table.add_row(entrada, divider = True)
        return "INICIO ACTIVIDAD: " + inicio + '\n' + str(table)
    
class LogServidor(Log):
    """La clase para el Log del Servidor."""
    pass
    
class LogUsuario(Log):
    """La clase para el log del usuario"""
    def __init__(self, id:str):
        self.id = id
        # Cambia el formato de las entradas en el archivo.
        FORMAT = '[%(asctime)s] [%(levelname)s] %(client_ip)s [%(method_name)s] %(message)s'
        super().__init__(id, FORMAT)

    def extra(self, ipCliente, metodo):
        self.dic = {
            "client_ip": ipCliente,
            "method_name": metodo
        }
        return self.dic
    
    def log(self, ipCliente, metodo, registro:Registro):
        extra = self.extra(ipCliente, metodo)
        self.logToFile(registro, extra)

    def _log(func):
        def metodoRPC(self, *args, **kwargs):
            try:
                if len(args) > 0:
                    id = str(args[0])
                    if UsuariosValidos.validarUsuario(id):
                        if self.idActual != id:
                            self.idActual = id
                            self.logUsuario = LogUsuario(id)
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