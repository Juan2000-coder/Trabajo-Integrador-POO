# Clase para manejar la creación de archivos job
import os
import os.path


class ArchivoJob:
    def __init__(self, nombre_archivo,directorio):
        self.nombre_archivo = nombre_archivo
        self.directorio = directorio

    def agregarComando(self, comando):
        ruta_completa = os.path.join(self.directorio, self.nombre_archivo)
        with open(ruta_completa, "a") as archivo_job:
            if comando != "":
                archivo_job.write(comando + "\n")