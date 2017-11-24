#!/usr/bin/env python
# -*- coding: utf-8 -*-


OSPF_HEADER_MASK = '! B B H 4s 4s H H 8s'

# ultimo 4s se refere ao ip do roteador adjascente
OSPF_HELLO_MASK = '! 4s H B B I 4s 4s 4s'

# lsa_header vazio
OSPF_DB_DESC_MASK = '! H B B 4s 20s'

# request
OSPF_LSA_REQUEST_MASK = '! 4s 4s 4s'



class OSPF:
    """
    Pacote OSPF Básico
    """

    def __init__(self, ospf_type, router_id, area_id, auth_type, auth_data, version=2):
        self.version = version
        self.ospf_type = ospf_type
        self.router_id = router_id
        self.area_id = area_id
        self.auth_type = auth_type
        self.auth_data = auth_data

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
        header_data = self.header_pack(length)
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
        header_data = self.header_pack(length)
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
        header_data = self.header_pack(length)
        return header_data + lsa_request_packet




