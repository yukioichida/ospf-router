#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.util import ip_checksum
import socket
import struct

OSPF_VERSION = 2
OSPF_HEADER_MASK = '! B B H 4s 4s H H xxxxxxxx'
# ultimo 4s se refere ao ip do roteador adjascente
OSPF_HELLO_MASK = '! 4s H B B I 4s 4s 4s'
# request
OSPF_LSA_REQUEST_MASK = '! 4s 4s 4s'


# intervalo de 20 segundos
HELLO_INTERVAL = 10
# Prioridade alta para eleição do master
ROUTER_PRIORITY = 0xff
ROUTER_DEAD_INTERVAL = 40
OSPF_HELLO_OPTION = 0x02

# db description constants
MTU_INTERFACE = 1500
DB_DESC_OPTION = 2

#OSPF Types
OSPF_HELLO_TYPE = 0x01
OSPF_DBDESC_TYPE = 0x02
OSPF_LSA_REQ_TYPE = 0x03


class OSPF:
    """
    Pacote OSPF Básico
    """

    def __init__(self, router_id, area_id):
        self.router_id = socket.inet_aton(router_id)
        self.area_id = socket.inet_aton(area_id)


    def header_pack(self, ospf_type, payload_data):

        length = len(payload_data) + 24
        
        # Header apenas para calcular o checksum, sem o auth_data vide RFC
        header_packet = struct.pack('! B B H 4s 4s H H',
                                    OSPF_VERSION,
                                    ospf_type,
                                    length,
                                    self.router_id,
                                    self.area_id,
                                    0x0000,
                                    0)
        # Calculo do checksum
        entire_packet = header_packet + payload_data
        checksum = ip_checksum([ord(c) for c in entire_packet], len(entire_packet))

        # Informações finais do cabeçalho
        header_packet = struct.pack(OSPF_HEADER_MASK,
                                    OSPF_VERSION,
                                    ospf_type,
                                    length,
                                    self.router_id,
                                    self.area_id,
                                    checksum,
                                    0)
        return header_packet


    def hello_packet(self, net_mask, designated_router_ip, bkp_designated_router_ip, neighbor_ip):

        net_mask_data = socket.inet_aton(net_mask)
        neighbor_ip = socket.inet_aton(neighbor_ip)
        bkp_designated_router_ip = socket.inet_aton(bkp_designated_router_ip)
        designated_router_ip = socket.inet_aton(designated_router_ip)


        hello_data = struct.pack('! 4s H B B I 4s 4s 4s',
                                 net_mask_data,
                                 HELLO_INTERVAL,
                                 OSPF_HELLO_OPTION,
                                 ROUTER_PRIORITY,
                                 ROUTER_DEAD_INTERVAL,
                                 designated_router_ip,
                                 bkp_designated_router_ip,
                                 neighbor_ip)
        header_data = self.header_pack(OSPF_HELLO_TYPE, hello_data)
        return header_data + hello_data

    def db_desc_packet(self,
                        control_bits,
                        dd_seq_number):


        db_desc_packet = struct.pack('! H B B I',
                                    MTU_INTERFACE,
                                    DB_DESC_OPTION,
                                    control_bits,
                                    dd_seq_number)
        header_data = self.header_pack(OSPF_DBDESC_TYPE, db_desc_packet)
        return header_data + db_desc_packet
