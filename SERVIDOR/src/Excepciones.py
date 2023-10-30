from Registro import Registro

class Excepciones(Exception):
    codigos = {}
    default = " Evento no identificado."
    modulo = "NO IDENTIFICADO"
    def __init__(self, codigo):
        self.codigoDeExcepcion = codigo
        self.registro = Registro(self.codigos.get(self.codigoDeExcepcion, ("INFO", Excepciones.default)))
        super().__init__(self.registro.mensaje)

    def __str__(self):
        return (' '*5 + "{}").format(self.modulo + f"({self.codigoDeExcepcion})" + ' ' + str(self.registro) + '\n')

class ExcepcionBrazoRobot(Excepciones):
    codigos = {
        1:("ERROR", " No se puede establecer conexión con el brazo."),
        2:("INFO", " No se puede enviar el comando, robot desconectado."),
        3:("ERROR", " Un evento ocurrió al intentar enviar el comando."),
        4:("INFO", " El robot ya se encuentra desconectado."),
        5:("ERROR", " Ocurrio un error al desconectar el Robot."),
        6:("INFO", " Llamada a comando con argumentos no válidos."),
        7:("ERROR", " La conexión ya está establecida.")}
    
    modulo = "BRAZO ROBOT"
    def __init__(self, codigo):
        super().__init__(codigo)
    
class ExcepcionArchivo(Excepciones):
    codigos = {
        1:("ERROR", " Al devolver el log.")}
    modulo = "ARCHIVO"

    def __init__(self, codigo):
        super().__init__(codigo)

class ExcepcionDeComando(Excepciones):
    codigos = {
        1:("INFO", " Demasiados argumentos/faltan argumentos."),
        2:("INFO", " Opcion no encontrada.")}
    modulo = "CLI"

    def __init__(self, codigo):
        super().__init__(codigo)
    
class ExcepcionDeServidor(Excepciones):
    codigos = {
        1:("INFO", " El puerto está en uso."),
        2:("CRITICAL", "El servidor termino inesperadamente.")}
    modulo = "SERVIDOR"

    def __init__(self, codigo):
        super().__init__(codigo)
    
class ExcepcionDeRegistro(Excepciones):
    codigos = {
        1:("DEBUG", " Nivel log no registrado.")}
    modulo = "REGISTRO"

    def __init__(self, codigo):
        super().__init__(codigo)