#
# @version 1.0
# @date 2023.10.17
# @author Borquez Juan Manuel, D'Alessandro Francisco, Miranda Francisco,
# @contact francisconehuenmiranda@gmail.com
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
