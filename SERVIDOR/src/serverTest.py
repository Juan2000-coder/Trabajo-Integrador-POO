# -*- coding: utf-8 -*-
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import subprocess
import re

def get_wifi_ipv4():
    try:
        # Ejecuta el comando 'ipconfig' y captura su salida
        result = subprocess.run(["ipconfig"], stdout=subprocess.PIPE, text=True)
        ipconfig_output = result.stdout

        # Utiliza una expresión regular para buscar la dirección IPv4 de la interfaz de Wi-Fi
        pattern = r"Adaptador de LAN inalámbrica Wi-Fi:\s+Dirección IPv4\..+?(\d+\.\d+\.\d+\.\d+)"
        match = re.search(pattern, ipconfig_output)

        if match:
            return match.group(1)  # Devuelve la dirección IPv4 encontrada
        else:
            return "No se encontró la dirección IPv4 de Wi-Fi"
    except Exception as e:
        return str(e)

# Llama a la función para obtener la dirección IPv4 de Wi-Fi
wifi_ipv4 = get_wifi_ipv4()
print(f"Dirección IPv4 de Wi-Fi: {wifi_ipv4}")

# Configura el servidor
server = SimpleXMLRPCServer((wifi_ipv4, 8000))

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