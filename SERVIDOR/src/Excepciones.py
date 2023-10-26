class ExcepcionBrazoRobot(Exception):
    def __init__(self, codigoDeExcepcion: int):
        self.codigoDeExcepcion = codigoDeExcepcion

        if codigoDeExcepcion == 1: 
            super().__init__("Al intentar conectar con el brazo.")

        elif codigoDeExcepcion == 2:
            super().__init__("No se pudo enviar el comando, robot desconectado.")
        
        elif codigoDeExcepcion == 3: 
            super().__init__("Al enviar comando.")
        
        elif codigoDeExcepcion == 4: 
            super().__init__("Robot ya desconectado.")
        
        elif codigoDeExcepcion == 5:
            super().__init__("Al intentar desconectar Robot.")

        elif codigoDeExcepcion == 6:
            super().__init__("Argumento invalido.")

        elif codigoDeExcepcion == 7:
            super().__init__("Modo incorrecto, use 'a' o 'r'.")
        
        elif codigoDeExcepcion == 8:
            super().__init__("Conexión ya establecida.")

    def __str__(self):
        return f"De Brazo Robot - {self.args[0]} Codigo({self.codigoDeExcepcion})"
    
class ExcepcionArchivo(Exception):
    def __init__(self, codigoDeExcepcion:int):
        self.codigoDeExcepcion = codigoDeExcepcion

        if codigoDeExcepcion == 1:
            super().__init__("Al agregar registro al archivo.")
        if codigoDeExcepcion == 2:
            super().__init__("Al devolver el log.")
        if codigoDeExcepcion == 3:
            super().__init__("Al crear el archivo.")

    def __str__(self):
        return f"De Archivo - {self.args[0]} Codigo({self.codigoDeExcepcion})"

class ExcepcionDeComando(Exception):
    """A class for specific C4 class exceptions."""

    def __init__(self, codigoDeExcepcion):
        self.codigoDeExcepcion = codigoDeExcepcion

        if codigoDeExcepcion == 1:
            super().__init__("Sintaxis incorrecta.")

        if codigoDeExcepcion == 2:
            super().__init__("Opcion no encontrada.")
        
        if codigoDeExcepcion == 3:
            super().__init__("Faltan argumentos.")

    def __str__(self):
        return f"De Comando - {self.args[0]} Codigo({self.codigoDeExcepcion})"