#!/usr/bin/env python
# -*- coding: Latin-1 -*-
# test UDP Client for YaDD UDP
import socket
#import sys

import time


HOST, PORT = "192.168.21.4", 50669

data1 = "[TEST];18123;SEL;002320201;RTN;002320201;J3E TP;NOINF;--;--;REQ;OK"
#data2 = "[W2WTEST2];8414.5;SEL;002320204;SAF;002320010;TEST;NOINF;--;--;REQ;OK"
#data3 = "[W2WTEST3];8414.5;SEL;002320204;SAF;002320009;TEST;NOINF;--;--;REQ;OK"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



sock.sendto(data1, (HOST, PORT))

#