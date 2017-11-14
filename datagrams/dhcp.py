#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, struct, binascii

#Classe base DHCP
class DHCP:

	def __init__(self):
		print("Construct DHCP packet")
		self.op_router_ip = None
		self.op_dhcp_type = None
		self.op_requested_ip = None
		self.op_host_name = None
		self.op_dhcp_server = None
		self.op_subnet_mask = None
		self.op_dns_list = []
		self.op_router_ip = None





