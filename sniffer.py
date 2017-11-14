#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, sys, struct, binascii

from dhcp_config_loader import *
from datagrams.http import *
from datagrams.ip import *
from datagrams.dns import *
from data_access import *

class Sniffer:

	def __init__(self):
		configs = DHCPConfigLoader()
		self.interface = configs.interface()
		self.data_access = DataAccess()


	def run(self):
		print "--------------------------------"
		print "------Running SNIFFER-----------"
		print "--------------------------------"
		try:
		    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
		    s.bind((self.interface, 0))
		except socket.error , msg:
		    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		    sys.exit()

		ipv4_mask = "! 8x B B 2x 4s 4s"
		tcp_mask = "! H H 16x"		
		udp_mask = "! H H 2x H"
		
		while 1==1:
			packet = s.recvfrom(65576)
			headers = packet[0]
			ipv4_header = IP.load_from_raw(headers[14:34])
			if ipv4_header.protocol == 0x06:# Verifica se é TCP
				tcp_header = struct.unpack(tcp_mask, headers[34:54]) #32 bytes
				#Capturando respostas HTTP
				if tcp_header[1] == 80: #or tcp_header[0]== 80:
					http_packet = HTTP(headers[66:])
					if http_packet.valid_http_package():
						print http_packet.data
						url, ip =  http_packet.http_host(), socket.inet_ntoa(ipv4_header.sender)
						self.data_access.save_request(ip, url)

			elif ipv4_header.protocol == 0x11: #Verifica se é UDP
				udp_header = struct.unpack(udp_mask, headers[34:42])
				if udp_header[1] == 53: # Verifica se o serviço a ser chamada é para um DNS
					dns_packet = DNS(headers[54:])
					url, ip =  dns_packet.data, socket.inet_ntoa(ipv4_header.sender)
					self.data_access.save_dns(ip, url)

						

							



sniffer = Sniffer()
sniffer.run()