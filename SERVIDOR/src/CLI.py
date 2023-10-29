"""
 * Application for general processing of ASCCI art files.
 * Solution for assignment 4 of Part C of TP1
 * Course: Oriented Object programming
 * 
 * @version 1.0
 * @date 	2023.09.23
 * @author 	Juan Manuel BORQUEZ PEREZ
 * @contact borquez.juan00@gmail.com
 * 
"""

"""Carguemos la responsabilidad de la RAISE de excepciones sobre cada una de las clases
ya sean de entidad(modelo) principalmente o de control. En cambio el manejo de las excepciones
lo hacemos en la capa de visualización o en la capa de control. Es decir, las verificaciones 
propias de los métodos de las clases se hacen dentro de esas clases y no en la llamada a las funciones.

Observar que se indican los los bloques de capturas de excepciones varios tipos de excepciones asociadas
a las distintas clases. Cada una de estas clases habría que definirlas en los archivos correspondientes.

Podríamos tener un archivo entero para definición de clases de excepciones de todas las clases o bien definir
cada una de las clases de excepciones en cada uno de los archivos de las clases del proyecto.
"""

from cmd import Cmd
import os
import os.path
from pathlib import Path
import subprocess
import platform
import datetime

from BrazoRobot import BrazoRobot
from ArchivoLog import ArchivoLog
from ArchivoUsuario import ArchivoUsuario
from ArchivoJob import ArchivoJob
from Punto import Punto
from Servidor import Servidor
import Excepciones
from Comandos import ComandosGcode

class CLI(Cmd):
    """Command Interpreter. Interface with user."""
    
    doc_header = "Ayuda para comandos documentados."
    undoc_header = "Comandos no documentados."
    marginLevel = 5                      # Left Margin for output
    outFormat = ' '*marginLevel + "{}"   # Left Margin string for use with format()

    def __init__(self):
        """"""
        super().__init__()
        self.rpc_server = None
        self.nombreArchivoJob = None
        self.route = os.path.dirname(os.path.abspath(__file__))
        self.jobRoute = os.path.join(self.route, "..", "Job")    # The path of the solution.
        
        self.brazoRobot = BrazoRobot()

        # Será un diccionario donde las claves son los ids o ips de usuario
        # Y las claves serán los archivos de usuario (objetos).
        self.jobFlag = False

    """def postcmd(self, stop, line):    
        if type(stop) == str:
            return False
        else:
            return stop"""
    
    def onecmd(self, comando):


        # Acciones a realizar antes de ejecutar un comando
        # Podriamos hacer la validación de usuario

        timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Habria que ver porque el servidor obtiene el timstamp de las peticiones de usuario de una
       
   
        ipCliente = "127.0.0.1"
        # Hay que ver como recuperarlo del servidor que lo conoce
        
        # Ejecutar el comando
        result = super().onecmd(comando)

        # Acciones a realizar después de ejecutar un comando
        # result debería contener tanto el nievl log y un mensaje que es el resultado
        # del comando.
        # Podemos hacer que siempre se devuelva un valor
        # Sobre todo para aquellos que tienen sentido que den un valor

        
        if result is not None:
            if comando == "obtenerLogServidor":
                mensaje = "INFO:Muestra del Log del Servidor."
            elif comando == "reporteGeneral":
                mensaje = "INFO:Muestra de reporte de usuario."
            else:
                mensaje = result

            if self.jobFlag == True:
                
                job = ArchivoJob(self.nombreArchivoJob, self.jobRoute)

                try:
                    lineLista = comando.split()
                    comandoo = lineLista[0]
                    params = tuple(lineLista[1:])
                    if comandoo != "grabar":
                        comandoTransformado = ComandosGcode.comandoAGcode(comandoo,params)
                        job.agregarComando(comandoTransformado)

                except Exception as e:

                    print(self.outFormat.str(e))
                    self.archivoLog.agregarRegistro(':'.join(["ERROR", str(e)]))

            try:
                self.archivoLog.agregarRegistro(comando, ipCliente, timeStamp, mensaje)
                if not (ipCliente in self.requerimientos):
                    self.requerimientos[ipCliente] = ArchivoUsuario(ipCliente, self.logRoute)
                self.requerimientos[ipCliente].agregarRegistro(comando, ipCliente, timeStamp, mensaje)

            except Exception as e:
  
                print(self.outFormat.str(e))
                self.archivoLog.agregarRegistro(':'.join(["ERROR", str(e)]))
        return result

    def do_cls(self, args):

        """
Limpia la pantalla.
cls
        """

        if platform.system() == 'Windows':
            subprocess.call('cls', shell = True)
        else:
            subprocess.call('clear', shell = True)

    def do_reporteGeneral(self, args):

        """
Muestra un reporte general de la actividad del usuario.
reporteGeneral <id>
    id      El id del usuario.
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería buscar en la lista de requerimientos aquella que corresponda
                # Con el ID indicado para luego llamar a un método del archivo de usuario
                # asociado con el requerimiento, que arme el reporte y que lo devuelva
                # como un str o algún objeto imprimible.

                """
                requerimientos seria un diccionario en el que las claves
                son los id de los usuarios y los valores asociados son objetos
                del tipo Archivo usuario.
                Los objetos del tipo ArchivoUsuario tendrían un método reporte()
                que devuelve el reporte en forma de str o bien como pretty table.
                """

                return "INFO: Reporte del Usuario."
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result
        
    def do_obtenerLogServidor(self, args):

        """
Imprime el detalle del Log del Servidor.
obtenerLogServidor
        """
        if len(args) == 0:
            archivo = ArchivoLog('Log.log')
            print(archivo.obtenerLog())
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_seleccionarModo(self, *args):
        """
Selecciona el modo de operacion en coordenadas Absolutas(a) o Relativas(r).
seleccionarModo <modo>
    modo        modo = a || modo = r.
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 1:
                # Debería llamar al método correspondiente en la clase Robot.
                result = self.brazoRobot.seleccionarModo(arguments[0])
                for elem in result.split('\n'):
                    print(self.outFormat.format(elem))
                return result
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result
        
    def do_conectarRobot(self, *args):
        """
Conecta el robot.
conectarRobot
        """
        if args == ('',) * len(args):
            result = self.brazoRobot.conectarRobot('COM3', 115200)
            print(self.outFormat.format(result))
            return result
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_desconectarRobot(self, *args):
        """
Desconecta el robot.
desconectarRobot
        """
        if args == ('',) * len(args):
            result = self.brazoRobot.desconectarRobot()
            print(self.outFormat.format(result))
            return result
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_activarMotores(self, *args):
        """
Activa los motores del brazo.
activarMotores
        """
        if args == ('',) * len(args):
            result = self.brazoRobot.activarMotor()
            print(self.outFormat.format(result))
            return result
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_desactivarMotores(self, *args):
        """
Desactiva los motores del brazo.
desactivarMotores
        """
        if args == ('',) * len(args):
            result = self.brazoRobot.desactivarMotor()
            print(self.outFormat.format(result))
            return result
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_home(self, *args):
        """
Activa el proceso de Homming del brazo.
home
        """
        if args == ('',) * len(args):
            result = self.brazoRobot.home()
            for elem in result.split('\n'):
                print(self.outFormat.format(elem))
            return result
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_movLineal(self, *args):
        """
Realiza el movimiento lineal del efector final.
movLineal <xx.x> <yy.y> <zz.z> [vv.v]
    xx.x    Posicion final en eje x en mm.
    yy.y    Posición final en eje y en mm.
    zz.z    Posición final en eje z en mm.
    vv.v    Velocidad del movimiento en mm/s.
        """
        result = None
        if len(args) == 3:
            result = self.brazoRobot.movLineal(Punto(float(args[0]), float(args[1]), float(args[2])))
           
        elif len(args) == 4:
            result = self.brazoRobot.movLineal(Punto(float(args[0]), float(args[1]), float(args[2])), float(args[3]))
            
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
        for elem in result.split('\n'):
            print(self.outFormat.format(elem))
        return result

    def do_activarPinza(self, *args):
        """
Activa el efector final.
activarPinza
        """
        if args == ('',) * len(args):
            # Debería llamar al metodo correspondiente en el brazo
            result = self.brazoRobot.activarPinza()
            for elem in result.split('\n'):
                print(self.outFormat.format(elem))
            return result
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_desactivarPinza(self, args):
        """
Desactiva el efector final.
desactivarPinza
        """
        if args == ('',) * len(args):
            # Debería llamar al metodo correspondiente en el brazo
            result = self.brazoRobot.desactivarPinza()
            for elem in result.split('\n'):
                print(self.outFormat.format(elem))
            return result
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_posicionActual(self, *args):
        """
Indica la posicion actual
        """
        if args == ('',) * len(args):
            # Debería llamar al metodo correspondiente en el brazo
            result = self.brazoRobot.posicionActual()
            for elem in result.split('\n'):
                print(self.outFormat.format(elem))
            return result
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_grabar(self, *args):
        """
Inicia el proceso de grabación de movimientos para construir un archivo de trabajo con la secuencia grabada.
grabar <Archivo>
    Archivo     El archivo donde se guardará la secuencia.
        """
        if self.jobFlag == False:
            if len(args) == 1 and args[0] != '':
                self.nombreArchivoJob= args[0]
                result = "INFO:Comandos se almacenaran en " + self.nombreArchivoJob
                print(result)
                self.jobFlag = True
                return result
            else:
                raise Excepciones.ExcepcionDeComando(1)
        else:
            result = "INFO:Almacenamiento de comandos parado"
            print(result)
            self.jobFlag = False
            return result

    def do_cargar(self, *args):
        """
Carga un archivo de trabajo existente en el directorio.
cargar <JobFile>
    JobFile     El nombre del archivo de Trabajo en el directorio.
    """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 1:

                direccion = self.jobRoute + "\\"+ arguments[0]
                with open(direccion, 'r') as archivo:
                    lineas = archivo.readlines()

                for linea in lineas:
                    result = self.brazoRobot.enviarComando(linea)
                    return result

            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result

    def do_levantarServidor(self, args):
        """
Inicia/Para el servidor rpc según el valor dado (true/false).
levantarServidor true|false
        """
        arguments = args.split()
        if len(arguments) == 1:
            if arguments[0].lower() =="true":
                if self.rpc_server is None:
                    self.rpc_server = Servidor(self)  #este objeto inicia el servidor y se da a conocer
            elif arguments[0].lower() =="false":
                if self.rpc_server is not None:
                    self.rpc_server.shutdown()
                    print("Servidor Apagado")
                    self.rpc_server = None
            else:
                raise Excepciones.ExcepcionDeComando(2)
        else:
            raise Excepciones.ExcepcionDeComando(1)

            
    def do_listarArchivosDeTrabajo(self, *args):

        """
Muestra los archivos de trabajo en el directorio actual.
listarArchivosDeTrabajo
        """
        
        if args == ('',) * len(args):
            lista = ""
            for fileName in os.listdir(self.jobRoute):
                lista += fileName + "\n"
                print(self.outFormat.format(fileName))
            return lista
        else:
            raise Excepciones.ExcepcionDeComando(1)
    
    def do_exit(self, args):

        """
Termina la ejecucion del programa.
exit
        """
        try:
            self.brazoRobot.desconectarRobot()
        except Excepciones.ExcepcionBrazoRobot:
            print("Robot desconectado.")
            print("Ejecucion CLI SERVIDOR terminada")
            raise SystemExit
    
if __name__ == "__main__":
    try:
        commandLine = CLI()
        commandLine.prompt = '->'
        commandLine.cmdloop('Entrada de comandos')
    except KeyboardInterrupt:
        # Cuando se presiona Ctrl+C, el flujo llega aquí.
        try:
            CLI.BrazoRobot.desconectarRobot()
        except Excepciones.ExcepcionBrazoRobot:
            print("Robot desconectado.")
            print("Ejecucion CLI SERVIDOR terminada")