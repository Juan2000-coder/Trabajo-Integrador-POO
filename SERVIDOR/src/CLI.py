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
import logging

from BrazoRobot import BrazoRobot
from ArchivoLog import ArchivoLog
from ArchivoJob import ArchivoJob
from Servidor import Servidor
import Excepciones
from Registro import Registrar
from Comando import ComandosGcode

class CLI(Cmd):
    """Command Interpreter. Interface with user."""

    doc_header = "                        Ayuda para comandos documentados                      "
    undoc_header = "Comandos no documentados."
    marginLevel = 5                      # Left Margin for output
    outFormat = ' '*marginLevel + "{}"   # Left Margin string for use with format()


    def __init__(self):
        """"""
        super().__init__()
        self.rpcServer = None
        self.brazoRobot = BrazoRobot()
        self.nombreArchivoJob = None
        self.jobFlag = False

    #ESTO POR AHÍ NO ESTAN CORRECTO PARA EL SAKE DE LA POO
    def estadoServidor(self, msg:str):
        print(msg)
    
    #ESTO HABRÍA QUE VERLO POR EL MISMO SAKE
    def actualizarJob(self, line:str):
        if self.jobFlag == True:
            job = ArchivoJob(self.nombreArchivoJob)
            lineSplit = line.split()
            comando = lineSplit[0]
            params = lineSplit[1:]

            if comando != "grabar":
                comandoTransformado = ComandosGcode.comandoAGcode(comando, *params)
                job.agregarComando(comandoTransformado)

    def onecmd(self, line):
        try: 
            result = super().onecmd(line)
            if result is not None:
                print(result)
                self.actualizarJob(line)
        except Excepciones.Excepciones as e:
            print(e)

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
        args = args.split()
        if len(args) == 0:
            archivo = ArchivoLog('Log')
            for entrada in archivo.obtenerLog():
                print(entrada)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_seleccionarModo(self, args):
        """
Selecciona el modo de operacion en coordenadas Absolutas(a) o Relativas(r).
seleccionarModo <modo>
    modo        modo = a || modo = r.
        """
        args = args.split()
        if len(args) == 1:
            # Debería llamar al método correspondiente en la clase Robot.
            result = self.brazoRobot.seleccionarModo(args[0])
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_conectarRobot(self, args):
        """
Conecta el robot.
conectarRobot
        """
        args = args.split()
        if len(args) == 0:
            result = self.brazoRobot.conectarRobot('COM3', 9600)
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_desconectarRobot(self, args):
        """
Desconecta el robot.
desconectarRobot
        """
        args = args.split()
        if len(args) == 0:
            result = self.brazoRobot.desconectarRobot()
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_activarMotores(self, args):
        """
Activa los motores del brazo.
activarMotores
        """
        args = args.split()
        if len(args) == 0:
            result = self.brazoRobot.activarMotor()
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_desactivarMotores(self, args):
        """
Desactiva los motores del brazo.
desactivarMotores
        """
        args = args.split()
        if len(args) == 0:
            result = self.brazoRobot.desactivarMotor()
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_home(self, args):
        """
Activa el proceso de Homming del brazo.
home
        """
        args = args.split()
        if len(args) == 0:
            result = self.brazoRobot.home()
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_movLineal(self, args):
        """
Realiza el movimiento lineal del efector final.
movLineal <xx.x> <yy.y> <zz.z> [vv.v]
    xx.x    Posicion final en eje x en mm.
    yy.y    Posición final en eje y en mm.
    zz.z    Posición final en eje z en mm.
    vv.v    Velocidad del movimiento en mm/s.
        """
        args = args.split()
        result = None
        if len(args) == 3:
            result = self.brazoRobot.movLineal(args[:3])
        elif len(args) == 4:
            result = self.brazoRobot.movLineal(args[:3], args[3])
        else:
            raise Excepciones.ExcepcionDeComando(1)
        return Registrar(result)

    def do_activarPinza(self, args):
        """
Activa el efector final.
activarPinza
        """
        args = args.split()
        if len(args) == 0:
            # Debería llamar al metodo correspondiente en el brazo
            result = self.brazoRobot.activarPinza()
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_desactivarPinza(self, args):
        """
Desactiva el efector final.
desactivarPinza
        """
        args = args.split()
        if len(args) == 0:
            # Debería llamar al metodo correspondiente en el brazo
            result = self.brazoRobot.desactivarPinza()
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_posicionActual(self, args):
        """
Inidica la posicion actual
        """
        args = args.split()
        if len(args) == 0:
            # Debería llamar al metodo correspondiente en el brazo
            result = self.brazoRobot.posicionActual()
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_grabar(self, args):
        """
Inicia el proceso de grabación de movimientos para construir un archivo de trabajo con la secuencia grabada.
grabar <Archivo>
    Archivo     El archivo donde se guardará la secuencia.
        """
        args = args.split()
        if self.jobFlag == False:
            if len(args) == 1:
                self.nombreArchivoJob = args[0]
                result = "INFO: Comandos se almacenaran en " + self.nombreArchivoJob
                self.jobFlag = True
                return Registrar(result)
            else:
                raise Excepciones.ExcepcionDeComando(1)
        else:
            result = "INFO: Almacenamiento de comandos parado."
            self.jobFlag = False
            return Registrar(result)

    def do_cargar(self, args):
        """
Carga un archivo de trabajo existente en el directorio.
cargar <JobFile>
    JobFile     El nombre del archivo de Trabajo en el directorio.
    """

        arguments = args.split()
        if len(arguments) == 1:
            result = ''
            for comando in ArchivoJob(arguments[0]).obtenerComandos():
                result += self.brazoRobot.enviarComando(comando) + '\r\n'
            return Registrar(result)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_levantarServidor(self, args):
        """
Inicia/Para el servidor rpc según el valor dado (true/false).
levantarServidor true|false
        """
        args = args.split()
        if len(args) == 1:
            if args[0].lower() =="true":
                if self.rpcServer is None:
                    self.rpcServer = Servidor(self)  #este objeto inicia el servidor y se da a conocer
            elif args[0].lower() =="false":
                if self.rpcServer is not None:
                    self.rpcServer.shutdown()
                    print("Servidor Apagado")
                    self.rpcServer = None
            else:
                raise Excepciones.ExcepcionDeComando(2)
        else:
            raise Excepciones.ExcepcionDeComando(1)

            
    def do_listarArchivosDeTrabajo(self, args):

        """
Muestra los archivos de trabajo en el directorio actual.
listarArchivosDeTrabajo
        """
        args = args.split()
        if len(args) == 0:
            lista = ""
            for fileName in os.listdir(ArchivoJob.jobroute):
                lista += self.outFormat.format(fileName + "\n")
            return lista
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_enviarComando(self, args):
        """
Envia un comando al brazo robot.
enviarComando <comando>
    comando     El comando a enviar al brazo robot.
        """
        result = self.brazoRobot.enviarComando(args)
        return Registrar(result)
        
    
    def do_exit(self, args):

        """
Termina la ejecucion del programa.
exit
        """
        if self.brazoRobot.conexion_establecida == True:
            print(self.brazoRobot.desconectarRobot())
        if self.rpcServer is not None:
            commandLine.rpcServer.shutdownStream()
            self.rpcServer.shutdown()
        print("Ejecucion CLI SERVIDOR terminada")
        raise SystemExit
    
if __name__ == "__main__":
    try:
        commandLine = CLI()
        commandLine.prompt = '->'
        commandLine.cmdloop('Entrada de comandos')
    except KeyboardInterrupt as e:
        if commandLine.brazoRobot.conexion_establecida == True:
            print(commandLine.brazoRobot.desconectarRobot())
        if commandLine.rpcServer is not None:
            commandLine.rpcServer.shutdownStream()
            commandLine.rpcServer.shutdown()
        print("Ejecucion CLI SERVIDOR terminada")