#!/usr/bin/env python

import SocketServer
import socket
#from coast_dict import *
import threading
import re

############## change to PyYadd when in service and change call to PyYadd() in make_dsc()
# update PyYadd with "GROUP" detect code
#import PyYadd2
##############
import PyYadd
import pysql
import time

# define a list of RX_IDs to be ignored in the automatic feed to Snargate Coast Station 
# UDP server
rx_not_for_snargate = []


def write_file(text):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    filename = '/var/www/html/pages/php/test/yudp.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    f.write(datetime+"; "+text+'\r\n')
    f.close()

  
    
class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
   

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        #write_file("%s:%s => %s" % (self.client_address[0], self.client_address[1], data))
        
        
        #PyYadd.send_to_mirror(data, 50666) 
        pysql.load_logger("UDP", "%s : %s" % (data.split(";")[0][1:-1], self.client_address[0]))
        
        self.dsc_list = self.make_dsc(data)
    
    # A UDP Client to send all incoming packets to the Coast Station Software - ensure correct IP address
    # is set, and consider a "lock file" test so that it can be disabled?
    
    def send_to_coast(self, data):
        
        HOST, PORT = "192.168.21.105", 50669
        
        # SOCK_DGRAM is the socket type to use for UDP sockets
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.bind(('',50661))
        # As you can see, there is no connect() call; UDP has no connections.
        # Instead, data is directly sent to the recipient via sendto().
        sock.sendto(data, (HOST, PORT))
        
    def make_dsc(self,dsc_message):
        print "\r\nUDP Message %s \r\n" % dsc_message
        if "~" in dsc_message:
            print "\r\n\nParity Error. Message Discarded\r\n\n"
            #write_file("Parity Error. Message discarded : "+dsc_message)
            pysql.load_logger("yUDPSERV", "Parity error, discarded : %s" % ( dsc_message))

            return

        dsc_list = dsc_message.split(";")
        
        
        
        
            
        #print dsc_list
        
        # rx_id comes from YaDD as "[john_fcdpp]"
        # we need to discard the 1st and last char. "[" and "]"
        # slicing with [1:-1] does this
        
        # Also...consider curtailing to 18 chars? YaDD tells user to use up to 18 chars
        # some users make long RX_IDs. SQL table allows 30 for the RX_ID field
        # but curtailing might discourage them from using > 18 ?
        rx_id = dsc_list[0][1:-1]

	rx_id = rx_id[0:18]
        
        rx_id = "".join(x for x in rx_id if ord(x) != 35 and ord(x) != 43)

        # add a bridge to Coast Station - Snargate
        # RX_ID Filtering to restrict this to European Receivers
        #if rx_id not in rx_not_for_snargate:
        #    self.send_to_coast(dsc_message)
        
        
        rx_freq = dsc_list[1]
        #print rx_id
        
        
        #print "rx_freq raw ", rx_freq
        
        rx_freq = rx_freq[-7:]
        
        rx_freq = "".join(x for x in rx_freq if ord(x) < 58 and ord(x) > 45)
        
        # trap events where the rx_freq word has a ";" character in its leading bytes
        # which causes the split() to choose the wrong fields
        
       
        fmt = dsc_list[2]
        
        to_mmsi = dsc_list[3]
        
       
            
        if fmt == "DIS" or fmt == "ALL":
            print "\r\nALL ALL ALL.......\r\n"
            to_mmsi = "ALL SHIPS"
            
        elif fmt == "AREA":
            print "\r\nAREA CALL\r\n"
            #to_mmsi = to_mmsi  
        
        elif to_mmsi[0:2] == "00":
        #elif (fmt != "DIS" or fmt != "ALL") and to_mmsi[0:2] == "00": # coast station
            print "to coast station ", to_mmsi
            #try:
            #    from_mmsi = coast_dict[from_mmsi]
            #except:
            #   from_mmsi = "COAST,%s, UNID" % from_mmsi
            to_mmsi = "COAST,%s" % to_mmsi
        
        elif to_mmsi[0] == "0" and to_mmsi[1] != "0":
        #elif (fmt != "DIS" or fmt != "ALL") and to_mmsi[0] == "0" and to_mmsi[1] != "0": # group callsign
            print "to a group", to_mmsi
            to_mmsi = "GROUP,"+to_mmsi
        
        else:# to_mmsi[0] != "0":
        #elif (fmt != "DIS" or fmt != "ALL") and to_mmsi[0] != "0": # not a group or a coast, not DIS or an ALL, 
            print "to Ship ", to_mmsi
            to_mmsi = "SHIP,"+to_mmsi
           
            
        cat = dsc_list[4]
      
        from_mmsi = dsc_list[5]
        
        if from_mmsi[0:2] == "00": # coast station
            print "from coast station ", from_mmsi
            #try:
            #    from_mmsi = coast_dict[from_mmsi]
            #except:
            #   from_mmsi = "COAST,%s, UNID" % from_mmsi
            from_mmsi = "COAST,%s" % from_mmsi
            
        elif from_mmsi[0] == "0" and from_mmsi[1] != "0": # group callsign
            print "from a group", from_mmsi
            from_mmsi = "GROUP,"+from_mmsi
        else:
            print "from Ship ", from_mmsi
            from_mmsi = "SHIP,"+from_mmsi
        
        tc1 = dsc_list[6]
        tc2 = dsc_list[7]
        freq = dsc_list[8]
        pos = dsc_list[9]
        eos = dsc_list[10]
        
        ecc = dsc_list[11]
        
        ecc_ok = ecc.split()[-1]
        
        if ecc_ok == "ERR":
            print "\r\n\nECC Error\nMessage discarded\n\n"
        #    #write_file("ECC Error, Message discarded : "+dsc_message)
            pysql.load_logger("yUDPSERV", "ECC error, discarded : %s" % ( dsc_message))
            return

        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        
        yadd_message = datetime+";"+rx_id+";"+rx_freq+";"+fmt+";"+to_mmsi+";"+cat+";"+from_mmsi+";"+tc1+";"+tc2+";"+freq+";"+pos+";"+eos+";"+ecc
        print yadd_message
        pysql.load_logger("yUDPSERV", "YaDD message added :  %s" % (yadd_message))
        PyYadd.make_dsc_call(dsc_message,yadd_message)
        return
 
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

if __name__ == "__main__":
    pysql.load_logger("yUDPSERV", "Starting YaDD UDP interface....")
    HOST, PORT = "", 50666

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    ip, port = server.server_address
    server.serve_forever()
    # Start a thread with the server -- 
	# that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    server.shutdown()
