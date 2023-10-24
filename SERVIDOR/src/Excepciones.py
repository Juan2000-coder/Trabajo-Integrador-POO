class ExcepcionBrazoRobot(Exception):
    def __init__(self, codigoDeExcepcion: int):
        self.codigoDeExcepcion = codigoDeExcepcion

        if codigoDeExcepcion == 1: 
            super().__init__("Error al intentar establecer la conexión con el Robot.")

        elif codigoDeExcepcion == 2:
            super().__init__("No se pudo enviar el comando. La conexión con el Robot no está establecida.")
        
        elif codigoDeExcepcion == 3: 
            super().__init__("Error no identificado en el envio de comando.")
        
        elif codigoDeExcepcion == 4: 
            super().__init__("No hay una conexión activa con el Robot que cerrar.")
        
        elif codigoDeExcepcion == 5:
            super().__init__("Error al intentar cerrar la conexión con el Robot.")

        elif codigoDeExcepcion == 6:
            super().__init__("El argumento debe ser un objeto de la clase Punto.")

        elif codigoDeExcepcion == 7:
            super().__init__("Modo de coordenadas no válido. Use 'a' o 'r'")
        
        elif codigoDeExcepcion == 8:
            super().__init__("Conexión a establecida.")

    def __str__(self):
        return f"Excepcion de Brazo Robot con mensaje: {self.args[0]} - Codigo: {self.codigoDeExcepcion}"
    
class ExcepcionArchivo(Exception):
    def __init__(self, codigoDeExcepcion:int):
        self.codigoDeExcepcion = codigoDeExcepcion

        if codigoDeExcepcion == 1:
            super().__init__("Error al agregar el registro al archivo.")
        if codigoDeExcepcion == 2:
            super().__init__("Error al devolver un registro.")

    def __str__(self):
        return f"Excepcion de Archivo con mensaje: {self.args[0]} - Codigo: {self.codigoDeExcepcion}"

class ExcepcionDeComando(Exception):
    """A class for specific C4 class exceptions."""

    def __init__(self, codigoDeExcepcion):
        self.codigoDeExcepcion = codigoDeExcepcion

        if codigoDeExcepcion == 1:
            super().__init__("Sintaxis de comando incorrecta.")

        if codigoDeExcepcion == 2:
            super().__init__("Opcion de comando no encontrada.")

    def __str__(self):
        return f"Excepcion de comando con mensaje: {self.args[0]} - Codigo: {self.codigoDeExcepcion}"