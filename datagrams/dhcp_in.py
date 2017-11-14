#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, struct, binascii

from datagrams.dhcp import *
from util import *

# Mascara para desserialização dos dados do pacote
dhcp_base_mask = '! b b b b 4s H H 4s 4s 4s 4s 6s 202x 4s'

# Classe que representa pacotes DHCP recebidos (DISCOVER/REQUEST)
class DHCPIn(DHCP):

	def __init__(self, raw_data):
		struct_data = struct.unpack(dhcp_base_mask, raw_data)
		self.type = struct_data[0]
		self.transaction = struct_data[4]
		self.ip_client = struct_data[7]
		self.ip_offer = struct_data[8]
		self.client_mac = struct_data[11]	
		self.op_dhcp_server = None


	def get_options(self, raw_data):
		offset = 0

		while offset <= len(raw_data):

			op_code = raw_data[offset]			
			if op_code == OP_END: # Opção 255, final
				break
			# Todas as options são seguidas de código+tamanho
			length = struct.unpack('! b',raw_data[offset+1])[0] 
			init_offset = offset + 2 # Inicia depois do op_code e byte de tamanho
			end_offset = init_offset + length #offset do final da msg de opção
			option_msg = raw_data[init_offset:end_offset]

			# Verifica a opção DHCP
			if op_code == OP_MESSAGE_TYPE:
				self.op_dhcp_type = option_msg
			elif op_code == OP_REQUESTED_IP:
				self.op_requested_ip = socket.inet_ntoa(option_msg)
			elif op_code == OP_HOST_NAME:
				#UTF-8 por rodar em linux
				self.op_host_name = option_msg.decode('utf-8')
			elif op_code == OP_DHCP_SERVER:
				self.op_dhcp_server = socket.inet_ntoa(option_msg)
			
			offset = end_offset


	def __str__(self):
		mac = binascii.hexlify(self.client_mac)
		params = (self.type, binascii.hexlify(self.transaction), self.ip_client, self.ip_offer, mac)
		return "Type: %s - Transaction %s - Ip Client: %s - Ip Offer: %s - Client MAC: %s" % params
