#!/usr/bin/env python
import argparse
import sys
import socket
import struct

from scapy.all import sendp, send, get_if_list, get_if_hwaddr, hexdump
from scapy.all import Packet
from scapy.all import Ether, IP, UDP
from scapy.all import hexdump, BitField, BitFieldLenField, ShortEnumField, X3BytesField, ByteField, XByteField

class custom_header(Packet):
    """Custom Header"""
    name = "custom header"
    fields_desc = [
        BitField("field1", 0, 16), # BitField("field_name", 0, byte_length)
        BitField("field2", 0, 8),
        BitField("field3", 0, 8)
    ]

def main():
    iface = "" # need to change
    print('\n---------- Send pakcet ----------')
    pkt = Ether(src='00:00:00:00:00:01', dst='00:00:00:00:00:02') / IP(src='10.0.0.1', dst='10.0.0.2', proto=17) / UDP(sport=1234, dport=5678) / custom_header(field1=10, field2=20, field3=30)

    
    sendp(pkt, iface=iface, verbose=False)

if __name__ == '__main__':
    main()