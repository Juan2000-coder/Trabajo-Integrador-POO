# -*- coding: utf-8 -*-
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import socket
import os
import logging

#hostname = socket.getfqdn()
hostname = "Juan_Portátil"
print("IP Address:",socket.gethostbyname_ex(hostname)[2][0])

# Configura el nivel de registro (puedes ajustarlo según tus necesidades)

class myhandler(SimpleXMLRPCRequestHandler):
        def __init__(self, request, client_address, server):
                server.clientAddress = client_address[0]
                super().__init__(request, client_address, server)

class myserver(SimpleXMLRPCServer):
        def __init__(self, addr, requestHandler=SimpleXMLRPCRequestHandler,
                     logRequests=True, allow_none=False, encoding=None,
                     bind_and_activate=True, use_builtin_types=False):
                
                self.route = os.path.dirname(os.path.abspath(__file__))
                self.log = os.path.join(self.route, "..", "archivos", "Log.log")
                FORMAT = '%(asctime)s [%(levelname)s] %(method_name)s - %(message)s - %(client_ip)s'
                logging.basicConfig(filename=self.log, level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

                self.clientAddress = None

                super().__init__(addr, requestHandler,
                     logRequests, allow_none, encoding,
                     bind_and_activate, use_builtin_types)
        # Configura el servidor
        # Definimos una función para manejar el comando "Generar" con argumento "reporteGeneral"

        def generar_reporte(self):
                # Realiza aquí la lógica para generar el reporte general
                ip = self.clientAddress
                reporte = "Este es el reporte general del robot."

                dic = {
                        "method_name": "reporteGeneral",
                        "client_ip": ip
                        }
                
                logging.info("Solicitud RPC recibida", extra=dic)
                return reporte

        def seleccionar_modo(self, modo):
                # Realiza aquí la lógica para generar el reporte general
                ip = self.clientAddress

                result = ""
                if modo == 'auto':
                        result =  "Modo automatico activado"
                elif modo == 'man':
                        result = "Modo manual activado"
                else:
                        
                        result = "Modo no valido"

                dic = {
                        "method_name": "seleccionarModo",
                        "client_ip": ip
                        }
                
                logging.info("Solicitud RPC recibida", extra=dic)
                return result


servidor = myserver((socket.gethostbyname_ex(hostname)[2][0], 8000), myhandler, False)

# Registramos la función en el servidor
servidor.register_function(servidor.generar_reporte, "reporteGeneral")
servidor.register_function(servidor.seleccionar_modo, "seleccionarModo")



print("Servidor listo para recibir solicitudes.")
servidor.serve_forever()