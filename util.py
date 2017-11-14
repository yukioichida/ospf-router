#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, fcntl, struct


from uuid import getnode as get_mac

#DHCP OPERACTION CODES
DHCP_DISCOVERY_CODE = b'\x01'
DHCP_OFFER_CODE = 0x02
DHCP_REQUEST_CODE= b'\x03'
DHCP_ACK_CODE = 0x05
# DHCP OPTION CODES
OP_MESSAGE_TYPE = b'\x35'
OP_CLIENT_MAC = b'\x3d'
OP_REQUESTED_IP = b'\x32'
OP_CLIENT_FQDN = b'\x51'
OP_HOST_NAME = b'\x0c'
OP_DHCP_SERVER = b'\x36'
OP_ROUTER_ID = b'\x03'
OP_SUBNET_MASK = b'\x01'
OP_LEASE_TIME = b'\x33'
OP_DNS = b'\x06'
OP_END = b'\xff'


"""
    Pega o MAC da máquina local
"""
def get_local_mac():
	mac = get_mac()
	mac = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
	return mac


"""
Pega o IP da rede local
"""
def get_ip_lan_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


"""
Cálculo do checksum
"""
def ip_checksum(ip_header, size):    
    cksum = 0
    pointer = 0    
    #The main loop adds up each set of 2 bytes. They are first converted to strings and then concatenated
    #together, converted to integers, and then added to the sum.
    while size > 1:
        cksum += int((str("%02x" % (ip_header[pointer],)) + 
                      str("%02x" % (ip_header[pointer+1],))), 16)
        size -= 2
        pointer += 2
    if size: #This accounts for a situation where the header is odd
        cksum += ip_header[pointer]        
    cksum = (cksum >> 16) + (cksum & 0xffff)
    cksum += (cksum >>16)    
    return (~cksum) & 0xFFFF


