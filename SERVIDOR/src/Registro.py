#
# @version 1.0
# @date 2023.10.17
# @author Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco,
# @contact borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com
#/
class Registro():
    niveles = {
            1:"DEBUG",
            2:"INFO",
            3:"WARNING",
            4:"ERROR",
            5:"CRITICAL"}
    
    def __init__(self, args:tuple):
        self.nivelLog = args[0]
        self.mensaje = args[1]

    def __str__(self):
        return ":".join([Registro.niveles[self.nivelLog], self.mensaje])