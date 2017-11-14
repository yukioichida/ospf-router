#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json,util

from util import *


#Classe que recupera as configurações do arquivo dhcp_config.json contido no diretório raiz do projeto
class DHCPConfigLoader:

	def __init__(self):
		try:
			with open('dhcp_config.json') as data_file:    
				self.configuration = json.load(data_file)
		except:
			self.configuration = dict()

	def interface(self):
		iface = self.configuration.get('interface')
		if iface == None:
			raise Exception('[ERROR] Network Interface must be defined.')
		return str(iface) 

	def ip_lease_time(self):
		return int(self.configuration.get('ip_lease_time',3600))

	def dns_servers(self):
		dns_servers = self.configuration.get('dns_servers',['8.8.8.8'])
		return [str(dns) for dns in dns_servers]

	def router_ip(self):
		iface = self.interface()
		#Caso não esteja configurado, assume que o próprio host ira rotear pacotes
		return str(self.configuration.get('router_ip', get_ip_lan_address(iface)))

	def dhcp_server(self):
		iface = self.interface()
		#Caso não esteja configurado, assume que o próprio host será o dhcp server
		return str(self.configuration.get('dhcp_server', get_ip_lan_address(iface)))

	def subnet_mask(self):
		return str(self.configuration.get('subnet_mask','255.255.255.0'))