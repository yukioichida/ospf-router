#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii

class DNS:

	def __init__(self, raw_value):
		size = len(raw_value)
		raw_data = []
		print raw_value
		#Remoção de bytes sem representação
		for i in range(1,size-5):
			if raw_value[i] < b'\x31':
				raw_data.append(b'\x2e')
			else:
				raw_data.append(raw_value[i])

		self.data = ''.join(raw_data)