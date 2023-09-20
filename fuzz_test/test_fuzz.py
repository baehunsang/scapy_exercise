#!/usr/bin/env python
import sys
import struct
import os

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr, bind_layers, fuzz, raw
from scapy.all import Packet, IPOption
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import IP, TCP, UDP, Raw, Ether, Padding
from scapy.layers.inet import _IPOption_HDR

class custom_header(Packet):
  """Custom Header"""
  name = "custom header"
  fields_desc = [
    BitField("field1", 0, 16), # BitField("field_name", initial value, byte_length)
    BitField("field2", 0, 8),
    BitField("field3", 0, 8)
  ]

bind_layers(UDP, custom_header)

for _ in range(10):
    p = fuzz(custom_header())
    p.show()
    hexdump(p)
