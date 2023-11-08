"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * Componente: UsuariosValidos.
 * 
 * @version  1.0
 * @date     2023.11.07
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""
import os
from Excepciones import ExcepcionArchivo

class UsuariosValidos:
    """Clase definida por el método para validar un Usuario."""
    route = os.path.dirname(os.path.abspath(__file__))
    usuariosRegistrados = os.path.join(route, "..","archivos","usuariosRegistrados.txt")
    
    @staticmethod
    def validarUsuario(id):
        """Busca el id en el archivo usuariosRegistrados.txt.
        returns: true (el id esta en el archivo) false (el id no está en el archivo).
                 Produce una excepción de Archivo en caso de que se produzca un error.
        """
        try:
            with open(UsuariosValidos.usuariosRegistrados) as archivo:
                usuarios = archivo.readlines()
                return id in [usuario.strip('\n') for usuario in usuarios]
        except:
            raise ExcepcionArchivo(2)