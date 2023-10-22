#
# @version 1.0
# @date 2023.10.17
# @author Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco,
# @contact borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com
#/

class Punto():
    def __init__(self, X: float, Y: float, Z: float):
        self.x = X
        self.y = Y
        self.z = Z
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getZ(self):
        return self.z
