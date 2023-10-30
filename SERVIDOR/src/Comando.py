class ComandosGcode:
    comandosDelRobot = {
        "seleccionarModo": {"a": "G90", "r": "G91"},
        "activarMotores": "G17",
        "desactivarMotores": "G18",
        "home": "G28",
        "posicionActual": "G0",
        "activarPinza": "M3",
        "desactivarPinza": "M5",
    }

    @staticmethod
    def comandoAGcode(comando, args):
        if comando == "movLineal":

            if len(args) == 3:
                x, y, z = args
                e = 0  # Velocidad por defecto
            elif len(args) == 4:
                x, y, z, e = args
            else:
                return ""#raise Excepciones.ExcepcionDeComando(3)
            return f"G1 X{x} Y{y} Z{z} E{e}"
        elif comando == "seleccionarModo":
            if args[0] == "a":
                return ComandosGcode.comandosDelRobot["seleccionarModo"]["a"]
            elif args[0] == "r":
                return ComandosGcode.comandosDelRobot["seleccionarModo"]["r"]
            else:
                return ""
        elif comando in ComandosGcode.comandosDelRobot:
            return ComandosGcode.comandosDelRobot[comando]
        else:
            return ""

    @staticmethod
    def gcodeAComando(gcode):
        for comando, valor in ComandosGcode.comandosDelRobot.items():
            if gcode == valor:
                return comando

        if gcode.startswith("G1 "):
            gcode = gcode[3:]  # Eliminar el prefijo "G1 "
            partes = gcode.split()
            if len(partes) == 4 and all(part.startswith(axis) for part, axis in zip(partes, "XYZE")):
                x, y, z, e = [float(part[1:]) for part in partes]
                if e == 0:
                    return f"movLineal {x} {y} {z}"
                else:
                    return f"movLineal {x} {y} {z} {e}"
        elif gcode.startswith("G90"):
            return f"seleccionarModo a"
        elif gcode.startswith("G91"):
            return f"seleccionarModo r"
        #raise Excepciones.ExcepcionDeComando(2)