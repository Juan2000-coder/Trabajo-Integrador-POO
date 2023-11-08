"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * Módulo : CLI
 * 
 * @version  1.0
 * @date     2023.11.07
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""

from cmd import Cmd
import os
import subprocess
import platform


from BrazoRobot import BrazoRobot
from Log import LogServidor
from Job import Job
from Servidor import Servidor
import Excepciones
from Registro import Registrar

class CLI(Cmd):
    """Interprete de comandos para interfaz con el operador."""

    doc_header = "                        Ayuda para comandos documentados                      "
    undoc_header = "Comandos no documentados."
    margen = 5                          # Margen izquierdo para salida por pantalla.
    formatoSalida = ' '*margen + "{}"   # String de formato para margen izquierdo.


    def __init__(self):
        super().__init__()
        self.servidorRpc = None
        self.robot = BrazoRobot()
        self.archivoJob:Job = None
        self.grabando = False

    def estadoServidor(self, msg:str):
        print(msg)

    def precmd(self, linea):
        linea = linea.lower()
        return linea
    
    def onecmd(self, linea):
        try: 
            resultado = super().onecmd(linea)
            if resultado is not None:
                print(resultado)
                if self.grabando:
                    self.archivoJob.actualizar(linea, resultado)
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

    def do_reporte(self, args):

        """
Muestra un reporte general de la actividad del servidor.
reporte
        """
        args = args.split()
        if len(args) == 0:
            archivo = LogServidor('Log')
            try:
                estado = self.robot.estado() 
            except Excepciones.ExcepcionBrazoRobot as e:
                if e.codigoDeExcepcion == 2:
                    estado = "Robot Desconectado."
                else:
                    raise
            return estado + '\n' + archivo.reporteGeneral()
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_log(self, args):

        """
Imprime el detalle del Log del Servidor.
log
        """
        args = args.split()
        if len(args) == 0:
            archivo = LogServidor('Log')
            return archivo.obtenerLog()
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_modo(self, args):
        """
Selecciona el modo de operacion en coordenadas Absolutas(a) o Relativas(r).
modo    a|r
        """
        args = args.split()
        if len(args) == 1:
            resultado = self.robot.seleccionarModo(args[0])
            return Registrar(resultado)
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_robot(self, args):
        """
Conecta o desconecta el robot.
robot   on|off
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == 'on':
                resultado = self.robot.conectarRobot('COM3')
            elif args[0] == 'off':
                resultado = self.robot.desconectarRobot()
            else:
                raise Excepciones.ExcepcionDeComando(2)
            return Registrar(resultado)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_motores(self, args):
        """
Activa o desactiva los motores del robot.
motores on|off
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == 'on':
                resultado = self.robot.activarMotores()
            elif args[0] == 'off':
                resultado = self.robot.desactivarMotores()
            else:
                raise Excepciones.ExcepcionDeComando(2)
            return Registrar(resultado)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_home(self, args):
        """
Realiza el proceso de Homming del robot.
home
        """
        args = args.split()
        if len(args) == 0:
            resultado = self.robot.home()
            return Registrar(resultado)
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_movlineal(self, args):
        """
Realiza el movimiento lineal del efector final.
movLineal <xx.x> <yy.y> <zz.z> [vv.v]
    xx.x    Posicion final en eje x en mm.
    yy.y    Posición final en eje y en mm.
    zz.z    Posición final en eje z en mm.
    vv.v    Velocidad del movimiento en mm/s.
        """
        args = args.split()
        if len(args) == 3:
            resultado = self.robot.movLineal(args[:3])
        elif len(args) == 4:
            resultado = self.robot.movLineal(args[:3], args[3])
        else:
            raise Excepciones.ExcepcionDeComando(1)
        return Registrar(resultado)

    def do_efector(self, args):
        """
Activa o desactiva el efector final del robot.
efector on|off
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == 'on':
                resultado = self.robot.activarEfector()
            elif args[0] == 'off':
                resultado = self.robot.desactivarEfector()
            else:
                raise Excepciones.ExcepcionDeComando(2)
            return Registrar(resultado)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_estado(self, args):
        """
Inidica el estado actual del robot (posicion/modo)
estado
        """
        args = args.split()
        if len(args) == 0:
            resultado = self.robot.estado()
            return Registrar(resultado)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_grabar(self, args):
        """
Inicia/detiene el proceso de grabación de movimientos para construir un archivo de trabajo con la secuencia grabada.
grabar opcion
    opcion    Nombre de un archivo (graba en el archivo) | off (detiene la grabación).
              (El nombre del archivo no puede ser 'off')
    
        """
        args = args.split()
        if len(args) == 1:
            if args[0] != 'off':
                if not self.grabando:
                    self.archivoJob = Job(args[0])
                    resultado = "INFO: Comandos se almacenaran en " + self.archivoJob.nombre
                    self.grabando = True
                else:
                    resultado = "INFO: Grabación en curso."
            else:
                resultado = "INFO: Almacenamiento de comandos detenido."
                self.grabando = False
                self.archivoJob = None
            return Registrar(resultado)
        else:
            raise Excepciones.ExcepcionDeComando(1)
            

    def do_cargar(self, args):
        """
Carga un archivo de trabajo existente en el directorio.
cargar <archivo>
    archivo     El nombre del archivo de trabajo en el directorio.
    """
        args = args.split()
        if len(args) == 1:
            resultado = ''
            for comando in Job(args[0]).obtenerComandos():
                resultado += self.robot.enviarComando(comando.strip('\n')) + '\r\n'
            return Registrar(resultado)
        else:
            raise Excepciones.ExcepcionDeComando(1)

    def do_servidor(self, args):
        """
Inicia/detiene el servidor rpc según el valor dado (on/off).
servidor on|off
        """
        args = args.split()
        if len(args) == 1:
            if args[0] == "on":
                if self.servidorRpc is None:
                    self.servidorRpc = Servidor(self)
            elif args[0] == "off":
                if self.servidorRpc is not None:
                    self.servidorRpc.detener()
                    print("Servidor Apagado")
                    self.servidorRpc = None
            else:
                raise Excepciones.ExcepcionDeComando(2)
        else:
            raise Excepciones.ExcepcionDeComando(1)

            
    def do_listar(self, args):

        """
Muestra los archivos de trabajo en el directorio actual.
listar
        """
        args = args.split()
        if len(args) == 0:
            lista = ""
            for archivo in os.listdir(Job.ruta):
                lista += self.formatoSalida.format(archivo + "\n")
            return lista
        else:
            raise Excepciones.ExcepcionDeComando(1)
        
    def do_ejecutar(self, args):
        """
Ejecuta un comando dado en G-Code.
ejecutar <comando>
    comando     El comando a ejecutar.
        """
        resultado = self.robot.enviarComando(args)
        return Registrar(resultado)
        
    
    def do_salir(self, args):

        """
Termina la ejecucion del programa.
salir
        """
        if self.robot.conexionEstablecida == True:
            print(self.robot.desconectarRobot())
        if self.servidorRpc is not None:
            self.servidorRpc.detener()
        print("Ejecucion CLI SERVIDOR terminada")
        raise SystemExit
    
if __name__ == "__main__":
    try:
        cli = CLI()
        cli.prompt = '->'
        cli.cmdloop('Entrada de comandos')
    except KeyboardInterrupt as e:
        if cli.robot.conexionEstablecida == True:
            print(cli.robot.desconectarRobot())
        if cli.servidorRpc is not None:
            cli.servidorRpc.detener()
        print("Ejecucion CLI SERVIDOR terminada")