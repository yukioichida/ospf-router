#!/usr/bin/env python
# -*- coding: utf-8 -*-


OSPF_HEADER_MASK = '! B B H I I B B I I'

OSPF_HELLO_MASK = '! I H B B I I I I'


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

    def header_raw_data(self, packet_length):
        return struct.pack("! 6s 6s H", raw_mac_dest, raw_mac_src, self.protocol)

    def hello_packet(self, net_mask, hello_interval, options, priority, router_dead_interval,
                     designated_router, bkp_designated_router, neighbor_id):
        hello_data = struct.pack(OSPF, raw_mac_dest, raw_mac_src, self.protocol)
