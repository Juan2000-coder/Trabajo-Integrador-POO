# -*- coding: utf-8 -*-
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Configura el servidor
server = SimpleXMLRPCServer(('localhost', 8000))
#server = SimpleXMLRPCServer(('IP', 8000))

# Definimos una función para manejar el comando "Generar" con argumento "reporteGeneral"
def generar_reporte():
    
        # Realiza aquí la lógica para generar el reporte general
        reporte = "Este es el reporte general del robot."
        return reporte

def seleccionar_modo(modo):
    
        # Realiza aquí la lógica para generar el reporte general
        if modo == 'auto':
                return "Modo automatico activado"
        
        elif modo == 'man':

                return "Modo manual activado"
        
        else:
                return "Modo no valido"



# Registramos la función en el servidor
server.register_function(generar_reporte, "reporteGeneral")
server.register_function(seleccionar_modo, "seleccionarModo")



print("Servidor listo para recibir solicitudes.")
server.serve_forever()