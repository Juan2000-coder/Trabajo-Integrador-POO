import os
from Excepciones import ExcepcionArchivo

class UsuariosValidos:
    route = os.path.dirname(os.path.abspath(__file__))
    usuariosRegistrados = os.path.join(route, "..", "archivos","usuariosRegistrados.txt")
    
    @staticmethod
    def validarUsuario(id):
        try:
            with open(UsuariosValidos.usuariosRegistrados, 'r') as usuarios:
                if id in usuarios.readlines():
                    return True
                else:
                    return False
        except:
            raise ExcepcionArchivo(2)