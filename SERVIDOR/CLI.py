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
from BrazoRobot import BrazoRobot
from ArchivoLog import ArchivoLog
from ArchivoUsuario import ArchivoUsuario

class commandException(Exception):
    """A class for specific C4 class exceptions."""

    def __init__(self, message):
        super().__init__(message)

class C4(Cmd):
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
        self.requerimientos = {}
        # Será un diccionario donde las claves son los ids o ips de usuario
        # Y las claves serán los archivos de usuario.

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

                print(self.requerimientos[arguments[0]].reporte())
                """
                requerimientos seria un diccionario en el que las claves
                son los id de los usuarios y los valores asociados son objetos
                del tipo Archivo usuario.
                Los objetos del tipo ArchivoUsuario tendrían un método reporte()
                que devuelve el reporte en forma de str o bien como pretty table.
                """
        except commandException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        except archivoLogExepiton as e:
            peint(self.outFormat.format(e))
        finally:
            print()
    
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
                print(logServidor)

                """
                logServidor seria un objeto del tipo ArchivoLog.
                Definiendo el método __str__ en esa clase podemos hacer print(objeto)
                y de esa manera imprimimos el contenido por pantalla.
                """
            else:
                raise commandException("Sintaxis de comando incorrecta.")
        except commandException as e:
            print(self.outFormat.format(e))
        except FileNotFoundError as e:
            print(self.outFormat.format(f"El archivo {e.filename} no se encontró."))
        except Exception as e:
            print(self.outFormat.format(e))
        except archivoLogException as e:
            print(self.outFormat.format(e))
        finally:
            print()

    def do_seleccionarModo(self, args):

        """
Selecciona el modo de operacion Manual(m) o Automático(a).
seleccionarModo <modo>
    modo        modo = a || modo = m.
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 1:
                # Debería llamar al método correspondiente en la clase Robot.
                brazoRobot.seleccionarModo(arguments[0])

                """
                El brazo tiene un método que le permite seleccionar el modo.
                """
            else:
                raise commandException("Sintaxis de comando incorrecta.")
        except commandException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

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
                brazoRobot.conectar()
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

    def do_desconectarRobot(self, args):
        """
Desconecta el robot.
desconectarRobot
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería llamar al método correspondiente en la clase Robot.
                brazoRobot.desconectar()
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

    def do_activarMotores(self, args):
        """
Activa los motores del brazo.
activarMotores
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 1:
                # Debería llamar al método correspondiente en la clase Robot.
                brazoRobot.activarMotores()
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

    def do_desactivarMotores(self, args):
        """
Desactiva los motores del brazo.
desactivarMotores
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería llamar al método correspondiente en la clase Robot.
                brazoRobot.desactivarMotores()
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

    def do_home(self, args):
        """
Activa el proceso de Homming del brazo.
home
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Debería llamar al método correspondiente en la clase Robot.
                brazoRobot.home()
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

    def do_movLineal(self, args):
        """
Realiza el movimiento lineal del efector final.
movLineal <xx.x> <yy.y> <zz.z> [vv.v]
    xx.x    Posicion final en eje x en cm.
    yy.y    Posición final en eje y en cm.
    zz.z    Posición final en eje z en cm.
    vv.v    Velocidad del movimiento.
        """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 3:
                # Debería llamar al metodo correspondiente en el brazo
                # En la forma solo con 3 argumentos.
                brazoRobot.movlineal(arguments[0], arguments[1], arguments[2])
            elif len(arguments) == 4:
                # Debería llamar al método correspondiente en la clase Robot.
                # En la forma con 4 argumentos.
                brazoRobot.movlineal(arguments[0], arguments[1], arguments[2], arguments[3])
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

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
                brazoRobot.activarPinza()
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

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
                brazoRobot.desactivarPinza()
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

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

                self.enGrabación = True
                self.jobs.append(ArchivoJob("Grabacion1" + str(id) + ".txt"))
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except archivoJobException as e:
            print(self.outFormat.format(e))
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
                self.jobs.append(ArchivoJob(arguments[0]))
                brazoRobot.ejecutar(self.jobs[-1])
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except archivoJobException as e:
            print(self.outFormat.format(e))
        except brazoRobotException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()
    
    def do_levantarServidor(self, args):
        """
Levanta el Servidor en el puerto indicado.
levantarServiror <port>
    port     El puerto del servidor.
    """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 1:
                # Supongo que crea el objeto servidor o bien
                # llama al método para activar el mismo.
                pass
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except servidorException as e:
            print(self.outFormat.format(e))
        except Exception as e:
            print(self.outFormat.format(e))
        finally:
            print()

    def do_desconectarServidor(self, args):
        """
Desconecta el Servidor.
desconectarServidor
    """
        print()
        try:
            arguments = args.split()
            if len(arguments) == 0:
                # Supongo que destruye el objeto servidor o bien
                # llama al método para desactivar el mismo.
                pass
            else:
                raise commandException("Sintaxis de comando incorrecta.")
            
        except commandException as e:
            print(self.outFormat.format(e))
        except servidorException as e:
            print(self.outFormat.format(e))
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
                        raise commandException("Opcion de comando no encontrada.")
                print(self.outFormat.format(fileName))
        except commandException as e:
            print(self.outFormat.format(e))
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