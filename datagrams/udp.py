#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct

#Dados que representam cabeçalho UDP
class UDP:

	def __init__(self, src_port, dest_port, length):
		self.src_port = src_port
		self.dest_port = dest_port
		self.length = length + 8 # Incrementa o cabeçalho udp
		self.checksum = 0x0000
		self.mask = "! H H H H "


	def raw_format(self):
		return struct.pack(self.mask, self.src_port, self.dest_port, 
			self.length, self.checksum)


