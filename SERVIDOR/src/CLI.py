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
import subprocess
import platform
import datetime
##Para levantar el SV
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from BrazoRobot import BrazoRobot
from ArchivoLog import ArchivoLog
from ArchivoUsuario import ArchivoUsuario
from Punto import Punto
from Registro import Registro
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
        self.route = os.getcwd()    # The path of the solution.
        self.brazoRobot = BrazoRobot()
        self.archivoLog = ArchivoLog('Log.csv')
        self.requerimientos = {}
        # Será un diccionario donde las claves son los ids o ips de usuario
        # Y las claves serán los archivos de usuario (objetos).
    
    def onecmd(self, line):
        # Acciones a realizar antes de ejecutar un comando
        # Podriamos hacer la validación de usuario
        timeStamp = datetime.datetime.now()
        comando = line
        ipCliente = "127.0.0.1" #Buscar alguna forma de obtenerlo
        
        # Ejecutar el comando
        result = super().onecmd(line)

        # Acciones a realizar después de ejecutar un comando
        # result debería contener tanto el nievl log y un mensaje que es el resultado
        # del comando.
        # Podemos hacer que siempre se devuelva un valor
        # Sobre todo para aquellos que tienen sentido que den un valor

        print("chota")
        if result is not None:
            with self.archivoLog as Log:
                Log.agregarRegistro(comando, ipCliente, timeStamp, result)

            if not (ipCliente in self.requerimientos):
                self.requerimientos[ipCliente] = ArchivoUsuario(ipCliente)

            with self.requerimientos[ipCliente] as LogUsuario:
                LogUsuario.agregarRegistro(comando, ipCliente, timeStamp, result)
    
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
            if len(arguments) == 1:
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
                result = self.brazoRobot.enviarComando('M114').split(':')
                for i, elem in enumerate(result):
                    if i > 0:
                        print(elem, end='')
                with self.requerimientos[arguments[0]] as archivo:
                    contador = 0
                    while True:
                        contador += 1
                        registro = archivo.obe
                        if registro is not None:
                            print(self.outFormat.format(registro))
                        else:
                            break

                return ":".join("INFO""Reporte del Usuario.")
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]
        
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
                y de esa manera imprimimos el contenido por pantalla.
                """
                with self.archivoLog:
                    while True:
                        registro = self.archivoLog.devolverRegistro()
                        if registro is not None:
                            print(self.outFormat.format(registro))
                        else:
                            break

                return ["INFO", "Muestra del Log del Servidor."]

            else:
                raise Excepciones.ExcepcionDeComando(1)
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]

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
                return result.split(':')
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]
        
    def do_conectarRobot(self, args):
        """
Conecta el robot.
conectarRobot
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería llamar al método correspondiente en la clase Robot.
                result = self.brazoRobot.conectarRobot('COM3', 115200)
                print(self.outFormat.format(result))
                return ["INFO", result]
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]
        
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
                return ["INFO", result]
            
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]

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
                return ["INFO", result]
            
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]

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
                return ["INFO", result]
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]

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
                print(self.outFormat.format(result))
                return result.split(':')
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]
        
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
            arguments = args.split()
            if len(arguments) == 3:
                result = self.brazoRobot.movLineal(Punto(arguments[0], arguments[1], arguments[2]))
                print(self.outFormat.format(result))
                return result.split(':')
            
            elif len(arguments) == 4:
                result = self.brazoRobot.movLineal(Punto(arguments[0], arguments[1], arguments[2]), arguments[3])
                print(self.outFormat.format(result))
                return result.split(':')
            
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]

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
                print(self.outFormat.format(result))
                return result.split(':')
            else:
                raise Excepciones.ExcepcionDeComando(1)

        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]

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
                print(self.outFormat.format(result))
                return result.split(':')
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            print(self.outFormat.format(e))
            return ["ERROR", str(e)]

    def do_grabar(self, args):
        """
Inicia el proceso de grabación de movimientos para construir un archivo de trabajo con la secuencia grabada.
grabar
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería llamar al metodo correspondiente en el brazo
                # En realidad podemos activar un flag en esta misma clase o en el brazo Robot
                # Crear un nuevo archivo de Job y entonces en cada llamada a un comando 
                # Este se coloca en el archivo. Algo como lo siguiente
                pass
                #self.enGrabación = True
                #self.jobs.append(ArchivoJob("Grabacion1" + str(id) + ".txt"))
            else:
                raise Excepciones.ExcepcionDeComando(1)
            
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

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
            print(self.outFormat.format(e))
        finally:
            print()
    
    def do_levantarServidor(self, args):
        """
        Levanta el servidor XML-RPC en el puerto indicado.
        levantarServidor <port>
        port: El puerto del servidor.
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 1:
                port = int(arguments[0])  # Obtiene el puerto desde el argumento
                server = SimpleXMLRPCServer(('192.168.131.188', int(port)))  # Crea una instancia del servidor
                #Definimos funciones
                  
                #Registramos funciones
                server.register_function(conectarRobot, "conectarRobot")
            
                #self.registrar_funciones(server)  # Registra tus funciones en el servidor
                print("Servidor listo para recibir solicitudes en el puerto", int(port))
                server.serve_forever()  # Inicia el servidor
            else:
                raise Excepciones.ExcepcionDeComando(1)
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

    def do_desconectarServidor(self, args):
        """
        Detiene y desconecta el servidor.
        desconectarServidor
        """
        print()
        try:
            if self.server is not None:
                self.server.shutdown()  # Detiene el servidor
                self.server.server_close()  # Cierra la conexión del servidor
                self.server = None  # Restablece la variable del servidor a nula
                print("Servidor desconectado.")
            else:
                print("No se encontró un servidor para desconectar.")
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

    def do_listarArchivosDeTrabajo(self, args):

        """
Muestra los archivos de trabajo en el directorio actual.
listarArchivosDeTrabajo [-e EXTENSION]
    -e      Muestra los archivos con la extension indicada por EXTENSION (.txt ie)
        """
        
        arguments = args.split()
        print()
        try:
            for fileName in os.listdir(self.route):
                if len(arguments) > 0:
                    if arguments[0] == '-e':
                        if not (fileName[-len(arguments[1]):] == arguments[1]):
                            continue
                    else:
                        raise Excepciones.ExcepcionDeComando(2)
                print(self.outFormat.format(fileName))

        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()
    
    def do_exit(self, args):

        """
Termina la ejecucion del programa.
exit
        """

        raise SystemExit
    
if __name__ == "__main__":
    commandLine = CLI()
    commandLine.prompt = '->'
    commandLine.cmdloop('Entrada de comandos')