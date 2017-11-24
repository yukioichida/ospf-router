#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.util import ip_checksum

OSPF_HEADER_MASK = '! B B H 4s 4s H H 8s'

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

    def __init__(self, router_id, area_id, auth_type, auth_data):
        self.router_id = router_id
        self.area_id = area_id
        self.auth_type = auth_type
        self.auth_data = auth_data


    def header_pack(self, ospf_type, length):
        checksum = ip_checksum([ord(c) for c in initial_data], 20)
        header_packet = struct.pack(OSPF_HEADER_MASK,
                                    2,
                                    ospf_type,
                                    length,
                                    self.router_id,
                                    self.area_id,
                                    checksum,
                                    self.auth_type,
                                    self.auth_data
                                    )
        return header_packet


    def hello_packet(self, net_mask, hello_interval, options, priority, router_dead_interval,
                     designated_router_ip, bkp_designated_router_ip, neighbor_ip):
        
        hello_data = struct.pack(OSPF_HELLO_MASK, 
                                net_mask, 
                                hello_interval, 
                                options,
                                priority,
                                router_dead_interval,
                                designated_router_ip,
                                bkp_designated_router_ip,
                                neighbor_ip)
        length = len(hello_data)
        header_data = self.header_pack(OSPF_HELLO_TYPE, length)
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
        length = len(hello_data)
        header_data = self.header_pack(OSPF_DBDESC_TYPE, length)
        return header_data + db_desc_packet



    def lsa_request_packet(self, 
                            ls_type, 
                            link_state_id, 
                            adv_router_ip):
        
        lsa_request_packet = struct.pack(OSPF_LSA_REQUEST_MASK, 
                                ls_type, 
                                link_state_id, 
                                adv_router_ip)
        length = len(hello_data)
        header_data = self.header_pack(OSPF_LSA_REQ_TYPE, length)
        return header_data + lsa_request_packet




