#!/usr/bin/env python
# -*- coding: Latin-1 -*-
# test UDP Client for YaDD UDP
import socket
#import sys

import time


HOST, PORT = "192.168.21.251", 50669
#data = "[UDPTEST];"+freq+";"+fmt+";"+to_mmsi+";SAF;"+from_mmsi+";"+tc1+";NOINF;--;--;"+eos+";ECC 28 OK"
#data1 = "[W2WTEST];8414.5;AREA;AREA 12345;SAF;002320204;TEST;NOINF;--;--;REQ;ECC 0 OK"
#data1 = "ADMIN;TXOFF"
data2 = "[W2WTEST];8414.5;SEL;002320204;SAF;002320204;TEST;NOINF;--;--;REQ;OK"

#data3 = "[TEST];12577.0;SEL;002320204;SAF;"+from_mmsi+";TEST;NOINF;--;--;REQ;ECC 0 OK"

#data4 = "[W2WTEST];12577.0;SEL;002320204;SAF;002320204;TEST;NOINF;--;--;REQ;ECC 0 OK"
#data2 = "ADMIN;UPDATE"
#data3 = "ADMIN;HELP"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#sock.sendto(data1, (HOST, PORT))
#time.sleep(2)
sock.sendto(data2, (HOST, PORT))
#sock.sendto(data2, (HOST, PORT))
#time.sleep(1)
#sock.sendto(data3, (HOST, PORT))
