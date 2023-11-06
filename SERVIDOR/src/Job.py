"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * Módulo: Job
 * 
 * @version  1.0
 * @date     2023.11.06
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""
import os
from Excepciones import ExcepcionArchivo
from Comandos import ComandosGcode

class Job():
    """Clase para el tratamiento de archivos de Trabajo."""
    ruta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(ruta, "..", "job")

    def __init__(self, archivo):
        self.archivo = os.path.join(self.ruta, archivo)

    def agregarComando(self, comando):
        """Agrega un comando al archivo.
        args:
            comando: Un comando Gcode con parámetros.
        """
        with open(self.archivo, "a") as archivo:
            if comando != "":
                archivo.write(comando + "\n")

    def obtenerComandos(self):
        """Obtiene un comando de un archivo de Trabajo.
        returns:
            (str): Un Comando G-Code con parámetros.
        """
        try:
            with open(self.archivo, 'r') as archivo:
                return archivo.readlines()
        except Exception:
            raise ExcepcionArchivo(2)
        
    def actualizar(self, linea:str):
        """Actualiza un archivo de trabajo partir de una línea del CLI.
        args:
            linea(str): una línea la entrada de prompt del CLI con un comando del Robot.
        """
        lineaSeparada = linea.split()
        comando = lineaSeparada[0]
        params = lineaSeparada[1:]

        if comando != "grabar":
            comandoTransformado = ComandosGcode.comandoAGcode(comando, *params)
            self.agregarComando(comandoTransformado)