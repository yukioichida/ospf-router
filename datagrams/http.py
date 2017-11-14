#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class HTTP:

	def __init__(self, raw_data):
		self.context = ""
		self.fields = dict()
		try:
			self.data = raw_data.decode('utf-8')
			self.error = False
			self.parse_data()
		except:
			self.data = raw_data
			self.error = True

	def http_host(self):
		if self.fields.get("Host") != None:
			host = self.fields.get("Host")
			return "http://" + host.strip() + self.context
		return None


	def parse_data(self):
		http_props = self.data.split("\r\n")

		#Regex para extração do restante da url
		search = re.search('GET (.+) HTTP.*', http_props[0])
		if search != None:
			self.context = search.group(1)
		else:
			self.error = True

		regex = re.compile("(.+):(.+)")
		for prop in http_props[1:]:
			if regex.match(prop):
				http_field = regex.findall(prop)[0]
				key, value = str(http_field[0]), str(http_field[1])
				self.fields[key] = value

	def valid_http_package(self):
		if self.error:
			return False
		# Valida recurso contido no contexto http
		invalid_formats = ['jpg','png','css','js','swg']
		for fmt in invalid_formats:
			if fmt in self.context:
				return False;

		# Pega requisições http com accept text/html
		accept = self.fields.get("Accept")
		if accept == None:
			return False
		elif "text/html" not in accept:
			return False
		elif "text/javascript" in accept:
			return False

		return True;






