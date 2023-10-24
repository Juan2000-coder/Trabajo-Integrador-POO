#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cmd import Cmd 

from eje2_rpc import XRServer

class XRConsola(Cmd):

    elements = ['1', 2, 'TRES', 'Y EL RESTO']
    
    def __init__(self):
        Cmd.__init__(self)
        self.rpc_server = None

    def do_list(self, arg1, arg2=None):
        """Lista elementos."""
        if arg2 is not None:
            return (self.elements)
        else:   
            print(self.elements)
            
    def do_exit(self):
        """"Desconecta de un dispositivo interno y sale del programa."""
        # self.log(_("Chau!"))
        # self.device.disconnect()
        #self.onecmd(rpc(false))
        raise SystemExit    # alternativa sys.exit()

    def do_rpc(self, value):
        """"Inicia/Para el servidor rpc según el valor dado (true/false)."""
        if value:
            if self.rpc_server is None:
                self.rpc_server = XRServer(self)  #este objeto inicia el servidor y se da a conocer
        else:
            if self.rpc_server is not None:
                self.rpc_server.shutdown()
                self.rpc_server = None

    # def do_connect(self):

    # def help_connect(self):

    # def do_disconnect(self):

    # def help_disconnect(self):
