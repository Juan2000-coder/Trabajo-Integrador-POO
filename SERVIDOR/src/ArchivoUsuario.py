from ArchivoLog import ArchivoLog

class ArchivoUsuario(ArchivoLog):
    def __init__(self, id:str):
        self.id = id
        super().__init__(id)