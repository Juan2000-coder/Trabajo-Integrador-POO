from Registro import Registro

class Excepciones(Exception):
    codigos = {}
    default = "Evento no identificado."

    def __init__(self, codigo):
        self.codigoDeExcepcion = codigo
        self.registro = Registro(self.codigos.get(self.codigoDeExcepcion, ("INFO", Excepciones.default)))
        super().__init__(self.registro.mensaje)

    def __str__(self):
        return  ':'.join([f"({self.codigoDeExcepcion})", str(self.registro)])

class ExcepcionBrazoRobot(Excepciones):
    codigos = {
        1:("ERROR", "No se puede establecer conexión con el brazo."),
        2:("INFO", "No se puede enviar el comando, robot desconectado."),
        3:("ERROR", "Un evento ocurrió al intentar enviar el comando."),
        4:("INFO", "El robot ya se encuentra desconectado."),
        5:("ERROR", "Ocurrio un error al desconectar el Robot."),
        6:("INFO", "Llamada a comando con argumentos no válidos."),
        7:("ERROR", "La conexión ya está establecida.")}
    
    def __init__(self, codigo):
        super().__init__(codigo)

    def __str__(self):
        return "BRAZO ROBOT" + super().__str__()
    
class ExcepcionArchivo(Excepciones):
    codigos = {
        1:("ERROR", "Al devolver el log.")}
    
    def __init__(self, codigo):
        super().__init__(codigo)

    def __str__(self):
        return "LOG" + super().__str__()

class ExcepcionDeComando(Excepciones):
    codigos = {
        1:("INFO", "Demasiados argumentos/faltan argumentos."),
        2:("INFO", "Opcion no encontrada.")}
    
    def __init__(self, codigo):
        super().__init__(codigo)

    def __str__(self):
        return "CLI" + super().__str__()
    
class ExcepcionDeServidor(Excepciones):
    codigos = {
        1:("INFO", "El puerto está en uso.")}
    
    def __init__(self, codigo):
        super().__init__(codigo)

    def __str__(self):
        return "SERVIDOR" + super().__str__()
    
class ExcepcionDeRegistro(Excepciones):
    codigos = {
        1:("DEBUG", "Nivel log no registrado.")}
    
    def __init__(self, codigo):
        super().__init__(codigo)

    def __str__(self):
        return "REGISTRO" + super().__str__()