#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys

IF_NAME = 'wlp3s0'


def main():
    """
    Main Method
    """
    try:
        s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        s.bind((IF_NAME, 0))
    except socket.error, msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()


if __name__ == '__main__':
    main()
