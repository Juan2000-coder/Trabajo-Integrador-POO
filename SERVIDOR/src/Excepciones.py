from Registro import Registro

class Excepciones(Exception):
    codigos = {}
    default = "Evento no identificado."

    def __init__(self, codigo):
        self.codigoDeExcepcion = codigo
        self.registro = Registro(self.codigos.get(self.codigoDeExcepcion, (2, Excepciones.default)))
        super().__init__(self.registro.mensaje)

    def __str__(self):
        return  ':'.join([f"({self.codigoDeExcepcion})", str(self.registro)])

class ExcepcionBrazoRobot(Excepciones):
    codigos = {
        1:(4, "No se puede establecer conexión con el brazo."),
        2:(2, "No se puede enviar el comando, robot desconectado."),
        3:(4, "Un evento ocurrió al intentar enviar el comando."),
        4:(2, "El robot ya se encuentra desconectado."),
        5:(4, "Ocurrio un error al desconectar el Robot."),
        6:(2, "Llamada a comando con argumentos no válidos."),
        7:(2, "La conexión ya está establecida.")}
    
    def __init__(self, codigo):
        super().__init__(codigo)

    def __str__(self):
        return "BRAZO ROBOT" + super().__str__()
    
class ExcepcionArchivo(Excepciones):
    codigos = {
        1:(4, "Al devolver el log.")}
    
    def __init__(self, codigo):
        super().__init__(codigo)

    def __str__(self):
        return "LOG" + super().__str__()

class ExcepcionDeComando(Excepciones):
    codigos = {
        1:(2, "Demasiados argumentos/faltan argumentos."),
        2:(2, "Opcion no encontrada.")}
    
    def __init__(self, codigo):
        super().__init__(codigo)

    def __str__(self):
        return "CLI" + super().__str__()
    
class ExcepcionDeServidor(Excepciones):
    codigos = {
        1:(2, "El puerto está en uso.")}
    
    def __init__(self, codigo):
        super().__init__(codigo)

    def __str__(self):
        return "SERVIDOR" + super().__str__()