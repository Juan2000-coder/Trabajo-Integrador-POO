
from Registro import Registro


class ArchivoLog():

    def __init__(self):
        self.nombreArchivo = 'log.csv'
    
    def agregarRegistro(self, registro: Registro):
        # Acá lo que decía era que capaz que estaría bueno que solamente se lancen excepciones
        # Ponele, en caso de que ocurra una excepción al leer el archivo, que se lance pero que
        # se captura en una clase de la capa de control o de la capa de visualización.        
        try:
            with open(self.nombreArchivo, 'a') as archivo:
                # Pordríamos acordar como ordenar los campos y entonces ponemos
                # En el archivo los datos en crudo separados por punto y coma.
                # También podríamos definir un método __str__  en la clase registro
                # Qué le de el formato .csv al registro
                # Para poner directamente aca en el write write ("registro")

                archivo.write(f"Hora: {registro.getTimeStamp()} - {registro.getNivelLog()}: Comando: {self.getComando()} (IP: {self.getIpCliente()})" + "\n")

                # Definí el método __str__ en la clase Registro de modo que se podría hacer lo siguiente:
                #archivo.write(registro) # Me parece que el write pone automaticamente el fin de linea.
        except Exception as e:
            print("Error al agregar el registro al archivo:", str(e))

    def obtenerRegistro(self, comando:str, nivelLog:str, timeStamp, ipCliente:str):
        registro = Registro(comando, nivelLog, timeStamp, ipCliente)
        return registro
    
    # Este devolver registro como que no hace mucho sentido. Capaz que conviene
    # cambiarle el nombre a leer registro y que se encargue de hacer la lectyra del siguiente
    # registro en el archivo.

    def devolverRegistro():
        pass
    