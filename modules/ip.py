#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import ip_checksum
import socket
import struct

DEFAULT_OPCODE = 0x45  # IPV4 com 20 bytes de cabeçalho
DEFAULT_SERVICE = 0x00
ipv4_mask = "! b b H H H b b H 4s 4s"
OSPF_PROTOCOL = 0x59


# Datagrama IP
class IP:
    def __init__(self, sender, receiver, data_size):
        self.sender = socket.inet_aton(sender)
        self.receiver = socket.inet_aton(receiver)
        self.size = data_size + 20  # acrescenta o tamanho do cabeçalho IP
        self.identification = 0x0000
        self.fragment = 0x0000  # dont fragment 40 + fragment offset 00
        self.ttl = 0x40  # 64 - 0x40
        self.protocol = OSPF_PROTOCOL
        self.padding = 0x0000

    @classmethod
    def load_from_raw(cls, raw_data):
        """
        Inicializa o objeto via conteúdo binário
        :param raw_data: bytes do pacote capturado
        """
        struct_data = struct.unpack(ipv4_mask, raw_data)
        sender = socket.inet_ntoa(struct_data[8])
        receiver = socket.inet_ntoa(struct_data[9])
        size = struct_data[2]
        protocol = struct_data[6]
        return cls(sender, receiver, size, protocol)

    def __str__(self):
        return "Sender: %s, Receiver: %s, Size: %d, Protocol: %d" % (
            self.sender, self.receiver, self.size, self.protocol)

    # Formato binário que deve ser enviado via socket raw
    def raw_format(self):
        initial_data = struct.pack(ipv4_mask,
                                   DEFAULT_OPCODE, DEFAULT_SERVICE, self.size, self.identification,
                                   self.fragment, self.ttl, self.protocol, self.padding,
                                   self.sender, self.receiver)

        checksum = ip_checksum([ord(c) for c in initial_data], 20)
        print checksum

        return struct.pack(ipv4_mask,
                           DEFAULT_OPCODE, DEFAULT_SERVICE, self.size, self.identification,
                           self.fragment, self.ttl, self.protocol, checksum,
                           self.sender, self.receiver)
