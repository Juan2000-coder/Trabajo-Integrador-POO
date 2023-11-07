"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * Componente: Excepciones.
 * 
 * @version  1.0
 * @date     2023.11.06
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""
from Registro import Registro

class Excepciones(Exception):
    """Clase para excepciones personalizadas del aplicativo.
        codigos: Un diccionario con los códigos de excepcion.
                 Los valores son los una tupla dada por el nivel de log y un mensaje.
        modulo: Identifica el módulo en el que se lanza la excepción."""
    codigos = {}
    default = " Evento no identificado."
    modulo = "NO IDENTIFICADO"
    
    def __init__(self, codigo):
        """Inicia un objeto de excepción con el código indicado asociado a un registro de Log
        con nivel de Log y un mensaje especifico de la excepción en caso de que sea identificada o
        un mensaje por defecto en caso de que no sea identificada."""

        self.codigoDeExcepcion = codigo
        self.registro = Registro(self.codigos.get(self.codigoDeExcepcion, ("INFO", Excepciones.default)))
        super().__init__(self.registro.mensaje)

    def __str__(self):
        """Para la impresión por pantalla de la excepción con formato personalizado."""
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
        1:("ERROR", " Al devolver el log."),
        2:("ERROR", " Al leer un archivo de trabajo."),
        3:("ERROR", " Al validar un usuario.")}
    modulo = "ARCHIVO"

    def __init__(self, codigo):
        super().__init__(codigo)

class ExcepcionDeComando(Excepciones):
    codigos = {
        1:("INFO", " Una cantidad incorrecta de argumentos fueron dados."),
        2:("INFO", " Opcion no encontrada.")}
    modulo = "CLI"

    def __init__(self, codigo):
        super().__init__(codigo)
    
class ExcepcionDeServidor(Excepciones):
    codigos = {
        1:("INFO", " El puerto está en uso.")}
    modulo = "SERVIDOR"

    def __init__(self, codigo):
        super().__init__(codigo)
    
class ExcepcionDeRegistro(Excepciones):
    codigos = {
        1:("DEBUG", " Nivel log no registrado.")}
    modulo = "REGISTRO"

    def __init__(self, codigo):
        super().__init__(codigo)