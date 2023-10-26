from Registro import Registro
import Excepciones
import csv

class ArchivoLog():

    def __init__(self, nombreArchivo: str):
        self.nombreArchivo = nombreArchivo
        self.lineFormat = "{:^20}" + " "*2 + "{:^20}" + " "*2 + "{:^20}" + " "*2 + "{:^20}" + " "*2 + "{:^20}"
        self.header = "timestamp;ipCliente;comando;nivelLog;mensaje\n"

        try:
            with open(self.nombreArchivo, 'a') as archivo:
                if archivo.tell() == 0:
                    archivo.write(self.header)
        except Exception as e:
            raise Excepciones.ExcepcionArchivo()

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
            with open(self.nombreArchivo, 'a') as archivo:
                for registro in self.obtenerRegistro(comando, ipCliente, timeStamp, mensaje):
                    archivo.write(str(registro)) # Me parece que el write pone automaticamente el fin de linea.

        except Exception as e:
            raise Excepciones.ExcepcionArchivo(1)
    
    # Este devolver registro como que no hace mucho sentido. Capaz que conviene
    # cambiarle el nombre a leer registro y que se encargue de hacer la lectyra del siguiente
    # registro en el archivo.

    def obtenerRegistro(self, comando:str, ipCliente:str, timeStamp, mensaje:str):
        registros = []
        for linea in mensaje.split('\n'):
            segmentos = linea.split(':')
            registros.append(Registro(timeStamp, ipCliente, comando, segmentos[0], ":".join(segmentos[1:])))
        return registros
    
    def obtenerLog(self):
        try:
            log:str = ''
            with open(self.nombreArchivo, "r") as archivo:
                reader = csv.reader(archivo, delimiter = ';')
                for i, linea in enumerate(reader):
                    if i > 0:
                        #aca esta largando error por alguna razon
                        log += self.lineFormat.format(*linea) + "\n"
            return log
        except Exception as e:
            print(e)
            raise Excepciones.ExcepcionArchivo(2)