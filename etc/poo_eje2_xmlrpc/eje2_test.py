#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eje2_rpc_en_cli import XRConsola

if __name__ == '__main__':
    uncli = XRConsola()
    uncli.prompt = ';-) '
    uncli.cmdloop('Iniciando entrada de comandos...')

