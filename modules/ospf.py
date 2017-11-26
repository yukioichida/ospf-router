#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.util import ip_checksum
import socket
import struct

OSPF_VERSION = 2

OSPF_HEADER_MASK = '! B B H 4s 4s H H xxxxxxxx'

# ultimo 4s se refere ao ip do roteador adjascente
OSPF_HELLO_MASK = '! 4s H B B I 4s 4s 4s'

# lsa_header vazio
OSPF_DB_DESC_MASK = '! H B B 4s 20s'

# request
OSPF_LSA_REQUEST_MASK = '! 4s 4s 4s'

OSPF_HELLO_TYPE = 0x01
OSPF_DBDESC_TYPE = 0x02
OSPF_LSA_REQ_TYPE = 0x03


class OSPF:
    """
    Pacote OSPF Básico
    """

    def __init__(self, router_id, area_id):
        self.router_id = router_id
        self.area_id = area_id


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


    def hello_packet(self, net_mask, hello_interval, options, priority, router_dead_interval,
                     designated_router_ip, bkp_designated_router_ip, neighbor_ip):

        net_mask_data = socket.inet_aton(net_mask)
        neighbor_ip = socket.inet_aton(neighbor_ip)
        bkp_designated_router_ip = socket.inet_aton(bkp_designated_router_ip)
        designated_router_ip = socket.inet_aton(designated_router_ip)


        hello_data = struct.pack(OSPF_HELLO_MASK,
                                 net_mask_data,
                                 hello_interval,
                                 options,
                                 priority,
                                 router_dead_interval,
                                 designated_router_ip,
                                 bkp_designated_router_ip,
                                 neighbor_ip)
        header_data = self.header_pack(OSPF_HELLO_TYPE, hello_data)
        return header_data + hello_data

    def db_desc_packet(self,
                       mtu_interface,
                       hello_interval,
                       options,
                       control_bits,
                       dd_seq_number,
                       lsa_header):
        db_desc_packet = struct.pack(OSPF_DB_DESC_MASK,
                                     mtu_interface,
                                     hello_interval,
                                     control_bits,
                                     dd_seq_number,
                                     lsa_header)
        header_data = self.header_pack(OSPF_DBDESC_TYPE, db_desc_packet)
        return header_data + db_desc_packet
