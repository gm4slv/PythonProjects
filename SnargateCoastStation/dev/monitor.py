
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
version = "0.1"

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
    filename = r'snargate_status.txt'
    f = open(filename, 'w')  # 
    #timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    f.write(text+"\n")
    #print timenow + "> " +text
    f.close()

        
        
def get_login():
        
    username = "guest"
    password = "guest"
    #login_win.destroy()
    make_con(username,password)
    return

def make_con(username,password):
       
    con = n1.make_con()
    if con:
        #print "asking for random/salt"
        reply = n1.login("login guest")
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
    #print "valid ",valid
    if "Incorrect" in valid:
        showinfo("Validation", valid)
        
    try:
        token = n1.login("alive")
        if token=="pong" or token =="":
            #sock.close()
            sys.exit(0)
        #print "got session token ", token
    except:
        #sock.close()
        sys.exit(0)
    
    if "Try again" not in reply: 
        #token = sock.recv(512)
        motd = n1.connect("ADMIN;MOTD;"+token)
        #print motd
        hello = poll_cmd("hello")
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
        app.cleanup_on_disconnect()
        return "Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected"



            
def status_poll():
    status=poll_cmd("POLLSTATUS")
    
    return status


    
def status_handle(status):
    print status
    status_list = status.split("~")
    
    online = status_list[0]
    tx_state = status_list[1]
    ptt_state = status_list[2]
    last_rx = status_list[3]
    last_tx = status_list[4]
    message_count = status_list[5]
    perband = status_list[6]
    freq_list = status_list[7]
    excluded_rx = status_list[8]
    print "Server status: ",online
    print "Last RX: ",last_rx
    print "Last TX: ",last_tx
    print "TX Stat: ", tx_state
    print "PTT    : ", ptt_state
    print "Messages: ", message_count
    print "Messages per band: ", perband
    text = online+"\n"+tx_state+"\n"+ptt_state+"\n"+last_rx+"\n"+last_tx+"\n"+message_count+"\n"+perband+"\n"+freq_list+"\n"+excluded_rx
    write_file(text)
    
    return
    
if __name__ == '__main__':
    
    
    lock = threading.Lock()
    

    n1 = Network()
    get_login()
    #status_poll()
    while True:
        status = status_poll()
        status_handle(status)
        
        time.sleep(2)
        
