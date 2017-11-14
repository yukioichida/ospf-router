#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shelve, re

from dhcp_config_loader import *


# Classe que gerencia a política de geração de IPs(VERSÃO 4) para os HOSTS atacados
# OBSERVAÇÃO: IMPLEMENTAÇÃO NÃO É THREAD-SAFE
class IPV4Generator:

	def __init__(self):
		config = DHCPConfigLoader()
		
		self.subnet_mask = config.subnet_mask()
		 # Gera IPS com mesmo prefixo, 
		self.dhcp_server = config.dhcp_server()
		self.hosts = dict()
		self.suffix = 10 # começa a atribuir IPs a partir do sufixo 10. Ex: 10.0.0.10
		#Regex para formato String do IPV4
		self.ip_regex = re.compile("^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")


	# Not thread-safe!
	def generate_ip(self):		
		self.suffix +=1		
		return self.extract_prefix() + str(self.suffix)


	# Not thread-safe!
	def confirm_ip(self, ip, mac, hostname):
		s = self.extract_suffix(ip)
		self.hosts[s] = (ip, mac, hostname)


	# Extrai o prefixo do IP usando o ip do servidor DHCP, pois os hosts atacados estao na mesma rede, observando a máscara de sub-rede
	def extract_prefix(self):
		regex = self.ip_regex
		if regex.match(self.dhcp_server) == None:
			raise Exception('[ERROR] Invalid DHCP Server IP')
		else:
			octets = regex.findall(self.dhcp_server)[0]
			if self.subnet_mask == '255.0.0.0': #Classe A
				return "%s.0.0." % (octets[0])
			elif self.subnet_mask == '255.255.0.0':# Classe B
				return "%s.%s.0." % (octets[0], octets[1])
			elif self.subnet_mask == '255.255.255.0':#Classe C
				return "%s.%s.%s." % (octets[0],octets[1],octets[2])
			else:
				raise Exception("[ERROR] Unsupported Subnet Mask "+self.subnet_mask)


	# Retorna o SUFIXO do ip gerado
	def extract_suffix(self, ip):
		regex = self.ip_regex
		if regex.match(ip) == None:
			raise Exception('Invalid IP generated - '+ip)
		else:
			octets = regex.findall(self.dhcp_server)[0]
			return octets[3]