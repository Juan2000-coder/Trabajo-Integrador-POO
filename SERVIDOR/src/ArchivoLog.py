from Registro import Registro
import Excepciones
import csv

class ArchivoLog():

    def __init__(self, nombreArchivo: str):
        self.nombreArchivo = nombreArchivo

    def __enter__(self):
        self.archivo = open(self.nombreArchivo, "a+", newline = '')
        self.reader = csv.reader(self.archivo, delimiter = ';')
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.archivo.close()
        self.reader = None

    def agregarRegistro(self, comando: str, ipCliente:str, timeStamp, mensaje:str):
        # Acá lo que decía era que capaz que estaría bueno que solamente se lancen excepciones
        # Ponele, en caso de que ocurra una excepción al leer el archivo, que se lance pero que
        # se captura en una clase de la capa de control o de la capa de visualización.        
        try:
            #with open(self.nombreArchivo, 'a') as archivo:
                # Pordríamos acordar como ordenar los campos y entonces ponemos
                # En el archivo los datos en crudo separados por punto y coma.
                # También podríamos definir un método __str__  en la clase registro
                # Qué le de el formato .csv al registro
                # Para poner directamente aca en el write write ("registro")

                #archivo.write(f"Hora: {registro.getTimeStamp()} - {registro.getNivelLog()}: Comando: {self.getComando()} (IP: {self.getIpCliente()})" + "\n")

                # Definí el método __str__ en la clase Registro de modo que se podría hacer lo siguiente:
            for registro in self.obtenerRegistro(comando, ipCliente, timeStamp, mensaje):
                self.archivo.write(str(registro)) # Me parece que el write pone automaticamente el fin de linea.

        except Exception as e:
            raise Excepciones.ExcepcionArchivo(1)
    
    # Este devolver registro como que no hace mucho sentido. Capaz que conviene
    # cambiarle el nombre a leer registro y que se encargue de hacer la lectyra del siguiente
    # registro en el archivo.

    def obtenerRegistro(self, comando:str, ipCliente:str, timeStamp, mensaje:str):
        registros = []
        for linea in mensaje.split('\n'):
            segmentos = linea.split(':')
            registros.append(Registro(comando, segmentos[0], timeStamp, ipCliente, ":".join(segmentos[1:])))
        return registros

    def devolverRegistro(self):
        try:
            linea = next(self.reader)
            return Registro(linea[0], linea[1], linea[2], linea[3], linea[4])
        except StopIteration:
            return None
        except Exception as e:
            raise Excepciones.ExcepcionArchivo(2)