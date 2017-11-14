#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, sys, struct, binascii

# Classe que representa os dados do cabeçalho ETHERNET
class Ethernet:

	def __init__(self,mac_dest, mac_src, protocol = 0x0800):
		self.mac_src = mac_src
		self.mac_dest = mac_dest
		self.protocol = protocol

	def raw_format(self):
		raw_mac_src = binascii.unhexlify(self.mac_src.replace(":",""))
		raw_mac_dest = binascii.unhexlify(self.mac_dest.replace(":",""))
		return struct.pack("! 6s 6s H", raw_mac_dest, raw_mac_src, self.protocol)