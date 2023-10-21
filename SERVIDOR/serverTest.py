from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Configura el servidor
server = SimpleXMLRPCServer(('localhost', 8000))

# Define una función que corresponde al caso "reporteGeneral"
def generar_reporte_general():
    # Realiza aquí la lógica para generar el reporte general
    reporte = "Este es el reporte general del robot."
    return reporte

# Registra la función en el servidor para que el cliente pueda llamarla
server.register_function(generar_reporte_general, "Generar")

print("Servidor listo para recibir solicitudes.")
server.serve_forever()