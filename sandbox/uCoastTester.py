#!/usr/bin/env python
# -*- coding: Latin-1 -*-
# test UDP Client for YaDD UDP
import socket
#import sys

import time


HOST, PORT = "shack", 50666
data4 = "W2WTEST1 156525;235901425;(routine);from;235025416;Position N50 40.2350' W001 03.3670' ACK;18-08-17 13:37:19;"
data1 = "[W2WTEST1];8414.5;ALL;;SAF;123456789;TEST;NOINF;--;--;EOS;OK"
data2 = "[W2WTEST1];8414.5;AREA;AREA 20°S =>06° 147°E=>06°;RTN;005030001;J3E TP;NOINF;08291.0/08291.0KHz; -- ;EOS;ECC 122 OK"
data3 = "[W2WTEST];8414.5;SEL;111111111;SAF;222222222;TEST;NOINF;--;--;REQ;OK"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



#sock.sendto(data1, (HOST, PORT))

#time.sleep(1)

#sock.sendto(data2, (HOST, PORT))

#time.sleep(1)

sock.sendto(data3, (HOST, PORT))

#sock.sendto(data1, (HOST, PORT))

#time.sleep(1)

#sock.sendto(data2, (HOST, PORT))

#time.sleep(1)

#sock.sendto(data4, (HOST, PORT))
