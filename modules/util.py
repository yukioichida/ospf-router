#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fcntl
import socket
import struct
from uuid import getnode as get_mac


def get_local_mac():
    """
        Pega o MAC da máquina local
    """
    mac = get_mac()
    mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
    return mac


def get_ip_lan_address(ifname):
    """
    Pega o IP da rede local.
    :parameter ifname - Nome da interface de rede
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def ip_checksum(ip_header, size):
    """
    Cálculo do checksum
    """
    cksum = 0
    pointer = 0
    # The main loop adds up each set of 2 bytes. They are first converted to strings and then concatenated
    # together, converted to integers, and then added to the sum.
    while size > 1:
        cksum += int((str("%02x" % (ip_header[pointer],)) +
                      str("%02x" % (ip_header[pointer + 1],))), 16)
        size -= 2
        pointer += 2
    if size:  # This accounts for a situation where the header is odd
        cksum += ip_header[pointer]
    cksum = (cksum >> 16) + (cksum & 0xffff)
    cksum += (cksum >> 16)
    return (~cksum) & 0xFFFF
