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
##Para levantar el SV
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from BrazoRobot import BrazoRobot
from ArchivoLog import ArchivoLog
from ArchivoUsuario import ArchivoUsuario
from ArchivoJob import ArchivoJob
from Punto import Punto
from Servidor import Servidor
import Excepciones

class CLI(Cmd):
    """Command Interpreter. Interface with user."""

    doc_header = "Ayuda para comandos documentados."
    undoc_header = "Comandos no documentados."
    marginLevel = 5                      # Left Margin for output
    outFormat = ' '*marginLevel + "{}"   # Left Margin string for use with format()


    def __init__(self):
        """"""
        super().__init__()        
        subdirectorio_bytes = "\\job"   
        directorio_primario = os.path.dirname(str(Path(__file__).resolve()))
        
        self.rpc_server = None
        self.jobRoute = directorio_primario + subdirectorio_bytes
        self.nombreArchivoJob = None
        self.route = os.path.dirname(os.path.abspath(__file__))
        self.fileroute = os.path.join(self.route, "..", "archivos")    # The path of the solution.
        self.brazoRobot = BrazoRobot()
        self.archivoLog = ArchivoLog(os.path.join(self.fileroute, "Log.csv")) #.csv o .log?
        self.requerimientos = {}
        # Será un diccionario donde las claves son los ids o ips de usuario
        # Y las claves serán los archivos de usuario (objetos).
        self.jobFlag = False

    def postcmd(self, stop, line):
        
        if type(stop) == str:
            return False
        else:
            return stop
    
    def onecmd(self, line):

        comandosDelRobot = {"seleccionarModo": {"a" : "G90",
                                                "r" : "G91"},
                        "activarMotores" : "G17",
                        "desactivarMotores" : "G18",
                        "home" : "G28",
                        "posicionActual" : "G0",
                        "movLineal" : "G1", 
                        "activarPinza" : "M3",
                        "desactivarPinza" : "M5"}
        # Acciones a realizar antes de ejecutar un comando
        # Podriamos hacer la validación de usuario

        timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Habria que ver porque el servidor obtiene el timstamp de las peticiones de usuario de una
       
        comando = line 
        ipCliente = "127.0.0.1"
        # Hay que ver como recuperarlo del servidor que lo conoce
        
        # Ejecutar el comando
        result = super().onecmd(line)

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
                try:
                    lineLista = line.split()
                    job = ArchivoJob(self.nombreArchivoJob, self.jobRoute)
                    if lineLista[0] in comandosDelRobot:
                        # Verifica si se proporcionan parámetros adicionales
                        if len(lineLista) == 4 or len(lineLista) == 5:
                            job.agregarComando(lineLista) ## Resolver que pasa si pongo movLineal con menos argumentos de los necesarios. Resolver tambien si se ponen comandos que no llevan argumentos, con argumentos
                        elif len(lineLista) == 1:
                            job.agregarComando(comandosDelRobot.get(lineLista[0], ""))
                        elif lineLista[0] == "seleccionarModo":
                            if lineLista[1] == "a":
                                job.agregarComando(comandosDelRobot["seleccionarModo"]["a"])
                            elif lineLista[1] == "r":
                                job.agregarComando(comandosDelRobot["seleccionarModo"]["r"])
                            else:
                                raise Excepciones.ExcepcionDeComando(2)
                        else:
                            raise Excepciones.ExcepcionDeComando(1)
                        
                except Exception as e:
                    return ':'.join(["ERROR", str(e)])

                
            with self.archivoLog as Log:
                Log.agregarRegistro(comando, ipCliente, timeStamp, mensaje)

            try:
                self.archivoLog.agregarRegistro(comando, ipCliente, timeStamp, mensaje)
                if not (ipCliente in self.requerimientos):
                    self.requerimientos[ipCliente] = ArchivoUsuario(ipCliente, self.fileroute)
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
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería llamar a un método del archivoLog que devuelve el contenido
                # del archivo como un str para imprimirlo por pantalla o un objeto imprimible
                # por pantalla.

                """
                logServidor seria un objeto del tipo ArchivoLog.
                Definiendo el método __str__ en esa clase podemos hacer print(objeto)
                y de esa manera imprimimos el contenido por pantalla."""
                result = self.archivoLog.obtenerLog()
                print(result)
                return result
            else:
                raise Excepciones.ExcepcionDeComando(1)
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result

    def do_seleccionarModo(self, args):

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
        
    def do_conectarRobot(self, args):
        """
Conecta el robot.
conectarRobot
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                result = self.brazoRobot.conectarRobot('COM4', 115200)
                print(self.outFormat.format(result))
                return ':'.join(["INFO", result])
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result
        
    def do_desconectarRobot(self, args):
        """
Desconecta el robot.
desconectarRobot
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                result = self.brazoRobot.desconectarRobot()
                print(self.outFormat.format(result))
                return ':'.join(["INFO", result])
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result

    def do_activarMotores(self, args):
        """
Activa los motores del brazo.
activarMotores
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                result = self.brazoRobot.activarMotor()
                print(self.outFormat.format(result))
                return ':'.join(["INFO", result])
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result

    def do_desactivarMotores(self, args):
        """
Desactiva los motores del brazo.
desactivarMotores
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                result = self.brazoRobot.desactivarMotor()
                print(self.outFormat.format(result))
                return ':'.join(["INFO", result])
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result

    def do_home(self, args):
        """
Activa el proceso de Homming del brazo.
home
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                result = self.brazoRobot.home()
                for elem in result.split('\n'):
                    print(self.outFormat.format(elem))
                return result
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result
        
    def do_movLineal(self, args):
        """
Realiza el movimiento lineal del efector final.
movLineal <xx.x> <yy.y> <zz.z> [vv.v]
    xx.x    Posicion final en eje x en mm.
    yy.y    Posición final en eje y en mm.
    zz.z    Posición final en eje z en mm.
    vv.v    Velocidad del movimiento en mm/s.
        """
        print()
        try:
            margs = args.split()
            if len(margs) == 3:
                result = self.brazoRobot.movLineal(Punto(float(margs[0]), float(margs[1]), float(margs[2])))
                for elem in result.split('\n'):
                    print(self.outFormat.format(elem))
                return result
            
            elif len(margs) == 4:
                result = self.brazoRobot.movLineal(Punto(float(margs[0]), float(margs[1]), float(margs[2])), float(margs[3]))
                for elem in result.split('\n'):
                    print(self.outFormat.format(elem))
                return result
            
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result

    def do_activarPinza(self, args):
        """
Activa el efector final.
activarPinza
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería llamar al metodo correspondiente en el brazo
                result = self.brazoRobot.activarPinza()
                for elem in result.split('\n'):
                    print(self.outFormat.format(elem))
                return result
            else:
                raise Excepciones.ExcepcionDeComando(1)

        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result

    def do_desactivarPinza(self, args):
        """
Desactiva el efector final.
desactivarPinza
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería llamar al metodo correspondiente en el brazo
                result = self.brazoRobot.desactivarPinza()
                for elem in result.split('\n'):
                    print(self.outFormat.format(elem))
                return result
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result
        
    def do_posicionActual(self, args):
        """
Inidica la posicion actual
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería llamar al metodo correspondiente en el brazo
                result = self.brazoRobot.posicionActual()
                for elem in result.split('\n'):
                    print(self.outFormat.format(elem))
                return result
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result

    def do_grabar(self, args):
        """
Inicia el proceso de grabación de movimientos para construir un archivo de trabajo con la secuencia grabada.
grabar
        """
        print()
        try:
            arguments = args.split()
            if self.jobFlag == False:
                if len(arguments) == 1:
                    
                    self.nombreArchivoJob= arguments[0]
                    result = "Comandos se almacenaran en " + self.nombreArchivoJob
                    print(result)
                    self.jobFlag = True
                    return result
                    # Debería llamar al metodo correspondiente en el brazo
                    # En realidad podemos activar un flag en esta misma clase o en el brazo Robot
                    # Crear un nuevo archivo de Job y entonces en cada llamada a un comando 
                    # Este se coloca en el archivo. Algo como lo siguiente
                    #self.enGrabación = True
                    #self.jobs.append(ArchivoJob("Grabacion1" + str(id) + ".txt"))
                else:
                    raise Excepciones.ExcepcionDeComando(1)
            else:
                result = "Almacenamiento de comandos parado"
                print(result)
                self.jobFlag = False
                return result

        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result
        
    def do_cargar(self, args):
        """
Carga un archivo de trabajo existente en el directorio.
cargar <JobFile>
    JobFile     El nombre del archivo de Trabajo en el directorio.
    """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 1:
                # Debería llamar al metodo correspondiente en el brazo
                # Podríamos pasar directamente el objeto de archivoJob
                # como parámetro a una función en el brazo (por lo tanto es dependencia)
                # que use los métodos de este objeto archivo para decodificar los comandos
                # y de esa manera irlos ejecutando.

                #   Algo así
                pass
                #self.jobs.append(ArchivoJob(arguments[0]))
                #self.brazoRobot.ejecutar(self.jobs[-1])
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
        print()
        try:
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
                raise Excepciones.ExcepcionDeComando(3)
        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result
            
    def do_listarArchivosDeTrabajo(self, args):

        """
Muestra los archivos de trabajo en el directorio actual.
listarArchivosDeTrabajo [-e EXTENSION]
    -e      Muestra los archivos con la extension indicada por EXTENSION (.txt ie)
        """
        
        print()
        try:
            arguments = args.split()

            for fileName in os.listdir(self.route):
                if len(arguments) > 0:
                    if arguments[0] == '-e':
                        if not (fileName[-len(arguments[1]):] == arguments[1]):
                            continue
                    else:
                        raise Excepciones.ExcepcionDeComando(2)
                print(self.outFormat.format(fileName))

        except Exception as e:
            result = ':'.join(["ERROR", str(e)])
            print(self.outFormat.format(result))
            return result
    
    def do_exit(self, args):

        """
Termina la ejecucion del programa.
exit
        """
        print("Ejecucion CLI SERVIDOR terminada")
        raise SystemExit
    
if __name__ == "__main__":
    commandLine = CLI()
    commandLine.prompt = '->'
    commandLine.cmdloop('Entrada de comandos')