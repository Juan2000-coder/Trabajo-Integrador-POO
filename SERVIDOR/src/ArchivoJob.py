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
            if comando[0] == "movLineal":
                if len(comando) == 4:
                    velocidad = 0
                else:
                    velocidad = comando[4]
                archivo_job.write(f"G1 X{comando[1]} Y{comando[2]} Z{comando[3]} E{velocidad} \n")
            else:
                archivo_job.write(comando + "\n")