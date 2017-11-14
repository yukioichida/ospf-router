	#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, struct, binascii

from datagrams.dhcp import *
from dhcp_config_loader import *


#Atributos fixos
htype = 0x01
hlen = 0x06
hops = 0x00
sec_elapsed = 0x0000
bootp_flag = 0x8000	
magic_cookie = 0x63825363
next_server = socket.inet_aton('0.0.0.0')
relay_agent = socket.inet_aton('0.0.0.0')


# Mascara para desserialização dos dados do pacote
dhcp_base_mask = '! b b b b 4s H H 4s 4s 4s 4s 6s 202x 4s'


# Classe para representar o datagrama de DHCP para envio(OFFER/ACK)
class DHCPOut(DHCP):

	def __init__(self, msg_type, transaction, ip_offer, client_mac):
		self.type = msg_type
		self.transaction = transaction
		self.ip_offer = socket.inet_aton(ip_offer)
		self.ip_client = socket.inet_aton('0.0.0.0')
		self.client_mac = client_mac
		self.load_configurations()
		
	# Carrega as configurações do servidor.
	def load_configurations(self):
		configurations = DHCPConfigLoader()
		self.op_dns_list = configurations.dns_servers()
		self.op_subnet_mask = configurations.subnet_mask()
		self.op_router_ip = configurations.router_ip()
		self.op_lease_time = configurations.ip_lease_time()
		self.op_dhcp_server = configurations.dhcp_server()

	# Monta a parte de DHCP OPTIONS
	def raw_option_format(self):
		raw_option = self.raw_message_type()

		if self.op_dhcp_server:
			raw_option += self.raw_dhcp_server()

		if self.op_lease_time:
			raw_option += self.raw_lease_time()
		
		if self.op_router_ip:
			raw_option += self.raw_router_ip()

		if self.op_subnet_mask:
			raw_option += self.raw_subnet_mask()

		if self.op_dns_list:
			raw_option += self.raw_dns_list()

		raw_option += self.raw_end_option()
		return raw_option


	def raw_end_option(self):
		return struct.pack('! B', 255)


	def raw_message_type(self):
		return struct.pack('! b b b', 0x35, 0x01, self.type)


	def raw_dns_list(self):
		dns_qtd = len(self.op_dns_list)		
		length = dns_qtd*4
		mask = "! b b "+str(length)+"s"
		print mask
		op_code = 0x06
		raw_dns = socket.inet_aton(self.op_dns_list[0])
		for dns in self.op_dns_list[1:]:
			raw_dns += socket.inet_aton(dns)
		return struct.pack(mask, op_code, length, raw_dns)


	def raw_subnet_mask(self):
		op_code, length = 0x01, 0x04 # opcode 1 - tamanho 4
		mask_pack = socket.inet_aton(self.op_subnet_mask)
		return struct.pack('! b b 4s', op_code, length, mask_pack)


	def raw_dhcp_server(self):
		op_code = 0x36 # 54
		length = 0x04
		ip_pack = socket.inet_aton(self.op_dhcp_server)
		return struct.pack('! b b 4s', op_code, length, ip_pack)


	def raw_router_ip(self):
		op_code = 0x03 # 3
		length = 0x04
		ip_pack = socket.inet_aton(self.op_router_ip)
		return struct.pack('! b b 4s', op_code, length, ip_pack)


	def raw_lease_time(self):
		op_code = 0x33
		length = 0x04
		return struct.pack('! b b i', op_code, length, self.op_lease_time)


	def raw_format(self):
		raw_pt1 = struct.pack('! b b b b', 0x02, htype, hlen, hops)
		raw_pt2 = struct.pack('! 4s H H', self.transaction, sec_elapsed, bootp_flag)
		raw_pt3 = struct.pack('! 4s 4s 4s 4s', self.ip_client, self.ip_offer, socket.inet_aton(self.op_dhcp_server), relay_agent)
		raw_pt4 = struct.pack('! 6s 202x i', self.client_mac, magic_cookie)
		
		raw_options = self.raw_option_format()
		print(binascii.hexlify(raw_options))
		return raw_pt1 + raw_pt2 + raw_pt3 + raw_pt4 + raw_options