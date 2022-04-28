#!/usr/bin/env python
# -*- coding: Latin-1 -*-
# test UDP Client for YaDD UDP
import socket
#import sys

import time


HOST, PORT = "gm4slv.plus.com", 50666

data1 = "[W2WTEST1];8414.5;SEL;002320204;SAF;123456789;TEST;NOINF;--;--;REQ;OK"
data2 = "[W2WTEST2];12577.0;SEL;002320204;SAF;002320010;TEST;NOINF;--;--;REQ;OK"
data3 = "[W2WTEST3];2187.5;SEL;002320204;SAF;002320009;TEST;NOINF;--;--;REQ;OK"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



sock.sendto(data1, (HOST, PORT))

#time.sleep(1)

#sock.sendto(data2, (HOST, PORT))

#time.sleep(1)

#sock.sendto(data3, (HOST, PORT))

#sock.sendto(data1, (HOST, PORT))

#time.sleep(1)

#sock.sendto(data2, (HOST, PORT))

#time.sleep(1)

#sock.sendto(data3, (HOST, PORT))
