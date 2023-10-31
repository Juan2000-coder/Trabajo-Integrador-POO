import os
from Excepciones import ExcepcionArchivo

class UsuariosValidos:
    route = os.path.dirname(os.path.abspath(__file__))
    usuariosRegistrados = os.path.join(route, "..","archivos","usuariosRegistrados.txt")
    
    @staticmethod
    def validarUsuario(id):
        try:
            with open(UsuariosValidos.usuariosRegistrados) as archivo:
                usuarios = archivo.readlines()
                return id in [usuario.strip('\n') for usuario in usuarios]
        except:
            raise ExcepcionArchivo(2)