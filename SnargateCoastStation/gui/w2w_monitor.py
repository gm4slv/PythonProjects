
"""
Wire2waves DSC Coast Station : GMDSS DSC Coast Station server and client

    Copyright (C) 2016  John Pumford-Green

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
##################
#
# 
# Wire2waves Ltd
# 
# Python GMDSS Coast Station Auto-Test Responder
# 
# May 2016
# 
# Data retrieval client
#
import time
import re
import socket
import json
import hashlib
import os

import threading
import Queue

HOST, PORT = "snargate", 50669
version = "mon/0.1"

class Network(object):
    def __init__(self):
        # when the n1 instance is created, do nothing - we'll connect later.
        
        pass
    
    # connect to the Coast Station server at the HOST, PORT
    # make_con() is called 
    # 1) in the GUI's __INIT__
    # 2) by an auto-reconnect mechanism driven by the regular polling of server information
    def make_con(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
        
            return self.sock
        except:
            return
    
    # the send/receive function to send a command to the server and read the reply.
    # To allow the server to send a unspecified amount of data, which may exceed the recv() buffer
    # size we prepend the data from the server by a number, delimited by a "@" character, which is 
    # the number of bytes in the full message. The initial recv() buffer is 8k, but will be increased 
    # in response to the reported message length, and receive is called until all the data is
    # transferred.
    # The recipe came from a combination of sources:
    # http://stackoverflow.com/questions/1708835/receiving-socket-python
    # for the general idea to prepend the data with a length and a delimiting character. I chose the 
    # "@" character because it is not sent by any server replies.
    # http://code.activestate.com/recipes/408859/
    # for the buffer handling in the "recv_size" method described, but substituting the simpler
    # len(message) from the first reference for the packed 4-byte method of the second.
    
    def login(self, data):
        
        lock.acquire()
        #print "sending ", data
        self.sock.sendall(data + "\n")
        
        received = self.sock.recv(2048)
        lock.release()
        return received
        
    def connect(self, data):
        try:
        
            lock.acquire()
            #print lock
            # sendall our data to the server in a single line
            #print "sending ", data
            self.sock.sendall(data + "\n")
        
            # the buffer management
            # initialize a measure of total length received and a list "total_data" to hold
            # the incoming message in chunks as it's read into "buffer"
            total_len = 0
            total_data = []
            # initially we set the maximum expected message size to 64k - although this could be increased
            # when we begin taking in the data
            size = 65532
            size_data = sock_data = ''
            # buffer to append each incoming string to
            buffer = ""
            recv_size = 8192
        
            # total_len is zero at the start... it will grow as the message is read, until it is equal to 
            # the reported message size. Initially "size" = "a big number", but after the first loop we know the 
            # true payload size and "size" is reassigned this value. We keep looping until total_len (all the data
            # received so far) = the expected data payload size.
            while total_len < size:
            
                sock_data = self.sock.recv(recv_size)
                if not sock_data:
                    break
                
                # total_data is empty at the start so we do the first "find the length" and the first 
                # section of payload process... setting the recv() buffer size to match 
                # the expected length of data so that the second recv() will get all the remaining data as the 
                # TCP buffer will now be large enough.
                if not total_data:
 
                    # append the read data to the buffer
                    buffer += sock_data
                    # determine the length_str, ignore the "@" delimiter, buffer is now the remaining 
                    # data in this block
                    length_str, ignored, buffer = buffer.partition('@')
                    # the size string is converted to an integer
                    size = int(length_str)
                    # set the recv() to buffer "size" number of bytes - the expected size of the message
                    recv_size=size
                    # set a maximum limit to the size of the TCP recv() buffer.
                    if recv_size>524288:
                        recv_size = 5224288
                        
                    # add the first block ("buffer") to the list total_data[] - this is the data minus the size header
                    # from the first "8k" of data from the first recv()
                    total_data.append(buffer)
                
                   
                    # total_data already has the first buffer-full, so we do the else: clause the second time round, ignoring 
                    # the size determining process
                    # This should give us a list with all the data in two elements
                else:
                    total_data.append(sock_data)
            
                    # total_len is the length of the data received.
                    # we test it in the While statement to see if it is < the expected size. 
                    # when total_len >= size we can stop the While loop.
                total_len=sum([len(i) for i in total_data])
                #print total_len
        finally:
            lock.release()
            # our result is a join of the two elements of the total_data list
            return ''.join(total_data)
              
              
              
def start_polls():
    pass

def write_file(text):
    filename = r'/var/www/html/pages/php/test/snargate_status.html'
    f = open(filename, 'w')  #
    header = "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\"><html><head><title>Snargate Status</title>\
	<meta http-equiv=\"refresh\" content=\"60\"><meta http-equiv=\"Content-Type\" content=\"text/html;charset=ISO-8859-1\">\
	</head><body bgcolor=\"b0c4de\"><basefont face=\"Arial\">"

    timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    f.write(header+"\n")
    f.write(text+"<center><br>Last Update : "+timenow+" UTC<br>")
    f.write("<table cellpadding=5 rules=all><tr><td><a href=\"./snargate_syslog.txt\">Syslog</a></td>")
    f.write("<td><a href=\"./snargate_motd.txt\">MOTD</a></td>")
    f.write("<td><a href=\"./snargate_rxtx.txt\">RX/TX Log</a></td>")
    f.write("<td><a href=\"./snargate_txpwr.txt\">TX Power/SWR log</a></td>")
    #f.write("<td><a href=\"./snargate_changes.txt\">Version Control Changelog</a></td>")
    f.write("<td><a href=\"../../../index.php\">YaDDNet</a></td></tr>")
    f.write("</table></center>")
    f.write("Snargate Radio, callsign MNC, MMSI 002320204<br>is licensed by OFCOM to provide MF/HF DSC Test facilites.<br>The station is operated by <a target=\"_blank\" href=\"http://www.gmdsstraining.co.uk/\">GMDSS Training</a><br>125 Snargate Street, Dover")
    f.write("</body></html>")
    #print timenow + "> " +text
    f.close()

def write_syslog(text):
    filename = r'/var/www/html/pages/php/test/snargate_syslog.txt'
    f = open(filename, 'w')
    f.write(text)
    f.close()         
        
def write_rxtx(text):
    filename = r'/var/www/html/pages/php/test/snargate_rxtx.txt'
    f = open(filename, 'w')
    f.write(text)
    f.close()  

def write_motd(text):
    filename = r'/var/www/html/pages/php/test/snargate_motd.txt'
    f = open(filename, 'w')
    f.write(text)
    f.close()  
       
def write_txpwr(text):
    filename = r'/var/www/html/pages/php/test/snargate_txpwr.txt'
    f = open(filename, 'w')
    f.write("Forward power 0-255 and Reflected power 0-255\n\n")
    f.write("yyyy-mm-dd hh:mm:ss ;  kHz   ; F/255 ; R/255\n====================================================\n")
    f.write(text)
    f.close()         
        
        
def get_login():
        
    username = "monitor"
    password = "monitorpasswd"
    #login_win.destroy()
    make_con(username,password)
    return

def make_con(username,password):
       
    con = n1.make_con()
    if con:
        #print "asking for random/salt"
        reply = n1.login("login %s" % username)
        #print "reply",reply
        random, salt = reply.split(":")
        #print "random ", random
        #print "salt ", salt
        challenge_client(username, random, salt, password, reply)
    
def challenge_client(user, random, salt, client_password, reply):
    global token
    #print "in challenge_client"
    client_hash = hashlib.sha256(salt + client_password).hexdigest()
    #print "client hash ", client_hash

    client_value = hashlib.sha256(random + client_hash).hexdigest()
    #print "client value ", client_value
        
    valid = n1.login("reply %s %s" % (client_value, version))
    print "valid ",valid
    if "Incorrect" in valid:
        showinfo("Validation", valid)
        
    try:
        token = n1.login("alive")
        if token=="pong" or token =="":
            #sock.close()
            sys.exit(0)
        print "got session token ", token
    except:
        #sock.close()
        sys.exit(0)
    
    if "Try again" not in reply: 
        #token = sock.recv(512)
        motd = n1.connect("ADMIN;MOTD;"+token)
        print motd
        hello = poll_cmd("hello")
        print hello
        #snargate_reply8.set(hello)
        #show_motd_win()
        start_polls()

def close():
    goodbye = poll_cmd("iwantotquit")
        
def poll_cmd(cmd):
    global token
    if cmd.split(";")[0] == "ADD":
        app.exclude_e.delete(0, 'end')
        
    if cmd.split(";")[0] == "DEL": 
        app.include_e.delete(0, 'end')

    header = "ADMIN"            # All commands are prefixed with "ADMIN"
    sendcommand = header+";"+cmd+";"+version+";"+token     # build the command string - a ";" delimited string with ID as the last element

    try:
        received = n1.connect(sendcommand)      # send the command and read the returned data
        return received
    except:
        print "no reply \r\n"
        quit()

def get_last_rx(rxlist):
        #print "in get_last_rx with ", rxlist
        last_list = rxlist.split(";")
        last_datetime = last_list[0]
        last_freq = last_list[1]
        last_mmsi = last_list[2]
        last_from_name = last_list[3]
        last_from_call = last_list[4]
        if len(last_from_call) < 3:
            last_from_call = "unk"
        last_tc1 = last_list[5]
        last_eos = last_list[6]
        last_stn = "DSC"+last_tc1+" "+last_eos+" received from  <a target=\"_blank\" href=\"http://www.marinetraffic.com/en/ais/details/ships/mmsi:"+last_mmsi+"\">"+last_mmsi+", "+last_from_name+" ("+last_from_call+")</a>"
        last = last_datetime+"   "+last_freq+"   "+last_stn
        #print "in get_last_rx returning ", last
        return last

def get_last_tx(txlist):
        #print "in get_last_tx with ", txlist

        last_list = txlist.split(";")
        last_datetime = last_list[0]
        last_freq = last_list[1]
        last_mmsi = last_list[2]
        last_from_name = last_list[3]
        last_from_call = last_list[4]
        if len(last_from_call) < 3:
            last_from_call = "unk"
        last_tc1 = last_list[5]
        last_eos = last_list[6]
        last_stn = "DSC"+last_tc1+" "+last_eos+" sent to  <a target=\"_blank\" href=\"http://www.marinetraffic.com/en/ais/details/ships/mmsi:"+last_mmsi+"\">"+last_mmsi+", "+last_from_name+" ("+last_from_call+")</a>"
        #last_stn = "DSC"+last_tc1+" "+last_eos+" sent to "+last_mmsi+", "+last_from_name+" ("+last_from_call+")"
        last = last_datetime+"   "+last_freq+"   "+last_stn
        return last

def get_last_ck(cklist):
        #print "in get_last_ck with ", cklist

        last_list = cklist.split(";")
        last_datetime = last_list[0]
        last_freq = last_list[1]
        last_mmsi = last_list[2]
        last_from_name = last_list[3]
        last_from_call = last_list[4]
        if len(last_from_call) < 3:
            last_from_call = "unk"
        last_tc1 = last_list[5]
        last_eos = last_list[6]
        last_stn = "DSC"+last_tc1+" "+last_eos+" addressed to  <a target=\"_blank\" href=\"http://www.marinetraffic.com/en/ais/details/ships/mmsi:"+last_mmsi+"\">"+last_mmsi+", "+last_from_name+" ("+last_from_call+")</a>"
        #last_stn = "DSC"+last_tc1+" "+last_eos+" addressed to  "+last_mmsi+", "+last_from_name+" ("+last_from_call+")"
        last = last_datetime+"   "+last_freq+"   "+last_stn
        return last
            
def status_poll():
    status=poll_cmd("POLLSTATUS")
    return status

def syslog_poll():
    syslog = poll_cmd("GETADMINSQL")
    return syslog

def rxtx_poll():
    rxtx = poll_cmd("GETRXTXSQL")
    return rxtx

def txpwr_poll():
    txpwr = poll_cmd("GETALLTXPWRSQL")
    return txpwr

def motd_poll():
    motd = poll_cmd("MOTD")
    return motd
    
def status_handle(status):
    #print status
    try:
        status_list = status.split("~")
    
        
    	online = status_list[0]
    	tx_state = status_list[1]
    	ptt_state = status_list[2]
    	last_rx_raw = status_list[3]
    	last_tx_raw = status_list[4]
    	message_count = status_list[5]
    	perband = status_list[6]
    	freq_list = status_list[7].split(";")
        last_ck_raw = status_list[8]
        last_rx = get_last_rx(last_rx_raw)
        last_tx = get_last_tx(last_tx_raw)
        last_ck = get_last_ck(last_ck_raw)
    	
        
        f_list  = [float(i) for i in freq_list]
    	freq_allowed = sorted(f_list)
    	freqs = " ".join(map(str, freq_allowed))
    	#print freqs	
    	excluded_rx = status_list[8]
    	heading = "<center><h2><font color=white>Snargate 002320204 DSC Server Status Monitor</font></h2></center>"
        if tx_state == "TX Enabled":
	    tx_enable = "<tr><td><font color=green>TX Inhibit Status</td><td><font color=green><b>"+tx_state+"</font></b></td></tr>"
        else:
	    tx_enable = "<tr><td><font color=red>TX Inibit Status</td><td><font color=red> "+tx_state+"</font></td></tr>"
        #if ptt_state == "PTT ON":
        #   ptt_on = "<tr><td><font color=red>PTT State</td><td><b><font color=red>"+ptt_state+"</font></b></td></tr>"
        #else:
            #ptt_on = "<tr><td><font color=green>PTT State</td><td><font color=green> "+ptt_state+"</font><br></td></tr>"
        online = "<tr><td><font color=green>Server Status</td><td><font color=green> <b>"+online+"</font></b></td></tr>"
        last_rx = "<tr><td><font color=blue>Last Received Call</td><td><font color=blue> <b>"+last_rx+"</font></b></tr></td>"
        last_tx = "<tr><td><font color=#b50414>Last Transmitted Call</td><td><font color=#b50414> <b>"+last_tx+"</font></b></td></tr>"
        last_ck = "<tr><td><font color=#4d4d4d>Last Own TX heard</td><td><font color=#4d4d4d> <b>"+last_ck+"</font></b></td></tr>"
        message_count = "<tr><td><font color=black>Message Count</td><td><font color=black> <b>"+message_count+"</font></b></tr></td>"
        perband = "<tr><td><font color=black>Messages Per Band</td><td> <font color=black>"+perband+"</font></td></tr>"
        freqs_allowed = "<tr><td><font color=green>Allowed Transmit Frequencies</td><td><font color=green> "+freqs+"</font></td></tr>"
        text = heading+"<center><table cellpadding=5 rules=all>"+online+tx_enable+freqs_allowed+last_rx+last_tx+last_ck+message_count+perband+"</table></center>"
        text = text + "<center><br><br><iframe width=800 height=250 style=\"border:none\" src=\"./snargate_motd.txt\"></iframe></center>"
	write_file(text)
    except:
    	pass
    return

def syslog_handle(syslog):
    write_syslog(syslog)
    return

def rxtx_handle(rxtx):
    write_rxtx(rxtx)
    return

def txpwr_handle(txpwr):
    write_txpwr(txpwr)
    return

def motd_handle(motd):
    write_motd(motd)
    return


if __name__ == '__main__':
    
    
    lock = threading.Lock()
    

    n1 = Network()
    get_login()
    #status_poll()
    print "Logging begin..."
    while True:
        status = status_poll()
        status_handle(status)
        time.sleep(2)
        syslog = syslog_poll()
        syslog_handle(syslog)
        time.sleep(2)
        rxtx = rxtx_poll()
        rxtx_handle(rxtx)
        time.sleep(2)
        txpwr = txpwr_poll()
        txpwr_handle(txpwr)
        time.sleep(2)
        motd = motd_poll()
        motd_handle(motd)
        time.sleep(2)
