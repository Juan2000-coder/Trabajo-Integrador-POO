"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * Componente: Comando.
 * 
 * @version  1.0
 * @date     2023.11.06
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""
class ComandosGcode:
    """Clase que ofrece un método para convertir comandos del cli
    en los equivalentes comandos de Gcode.
        ComandosDeelRobot: Un diccionario con los nombres de comando como claves
                            y los códigos G equivalentes como valores."""

    comandosDelRobot = {
        "modo": {"a": "G90", "r": "G91"},
        "motores": {"on":"G17", "off": "G18"},
        "home": "G28",
        "estado": "G0",
        "efector": {"on":"M3", "off":"M5"},
    }

    @staticmethod
    def comandoAGcode(comando, *args):
        """Convierte una línea de comando de CLI (comando y argumentos)
        en un comando G-Code."""

        if comando == "movLineal":
            if len(args) == 3:
                x, y, z = args
                e = 0
            elif len(args) == 4:
                x, y, z, e = args
            return f"G1 X{x} Y{y} Z{z} E{e}"
        
        elif comando == "modo":
            if args[0] == "a":
                return ComandosGcode.comandosDelRobot["modo"]["a"]
            elif args[0] == "r":
                return ComandosGcode.comandosDelRobot["modo"]["r"]
            
        elif comando == "motores":
            if args[0] == "on":
                return ComandosGcode.comandosDelRobot["motores"]["on"]
            elif args[0] == "off":
                return ComandosGcode.comandosDelRobot["motores"]["off"]
        
        elif comando == "efector":
            if args[0] == "on":
                return ComandosGcode.comandosDelRobot["efector"]["on"]
            elif args[0] == "off":
                return ComandosGcode.comandosDelRobot["efector"]["off"]
            
        elif comando in ComandosGcode.comandosDelRobot:
            return ComandosGcode.comandosDelRobot[comando]
        return ''