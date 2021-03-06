'''
Wire2waves DSC Coast Station : GMDSS DSC Coast Station server and client

    Copyright (C) 2015  John Pumford-Green

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
'''

##################
#
# 
# Wire2waves Ltd
# 
# Python GMDSS Coast Station Auto-Test Responder
# 
# April/May 2015
# 
# Main server routine
# This provides:
# UDP server to accept UDP datagrams containing DSC messages from 1) individual copies of "YaDD" and 2) a filtered feed
# of messages arriving at http://gm4slv.plus.com:8000 YaDDNet. 
#
# UDP server to accept remote administration commands from a simplified graphical user interface
#
# TCP server to accept administrator connections for remote operation / monitoring.
#
# Received messages from all sources are inspected to ensure all the following are true 
# 1) No "parity failures", 2) No ECC Checksum failures, 3) Addressed "our_mmsi" 4) are TEST REQUESTS.
#
# Messages which match the requirements are logged in an SQLite database and are used to trigger an automatic ACK DSC reply
# Multiple copies of the same message from multiple sources are detected such that only one reply is transmitted regardless of the number of 
# reporting receivers.
# 
# 
import os # used for os._exit(0) - remote closedown and automatic closedown on loss of TX controll
import threading
import SocketServer
import time
import datetime
import re
import json
import random

import hashlib
import pass_verify as pv

# local modules
from dsc_functions import * 

#############################
# TEMPORARY USE IC718
#
from radio_functions_m710 import *
#
############################

from resolve import *
from new_coast_dict import *
import coast_sql as sql


try:
    import readline
except:
    pass

lock = threading.Lock()

#######################################
# SET COAST STATION MMSI HERE
#
our_mmsi = "002320201"
#
#
#######################################

version = "v0.1ham"

debug = 0

#start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
start_time = time.strftime("%H:%M %a, %d %b, %Y", time.gmtime(time.time()))

# Initialize a global queue, a list containing each message (which is itself a list of 
# two items, the frequency and the dsc_symbols(another list)) 
# This is global so that multiple threaded UDP/TCP sessions can all access the same
# queue, to allow duplicate message checking, and to control access to a single transmitter
#

dsc_queue = []



# Some persistent lists of various items, saved to disk as json files
# so the lists are available after software re-starts.
# It is probably worthwhile dropping this in favour of SQLlite database/tables.

try:
    message_per_band = open('message_per_band.json')
    message_per_band_list = json.load(message_per_band)
except:
    # list holds message count for 2,4,6,8,12,16 at each index respectively
    message_per_band_list = [0,0,0,0,0,0]
    
try:
    messages_received = open('messages_received.json')
    messages_received_list = json.load(messages_received)
except:
    # list holds message count All inspected, addressed to us
    messages_received_list = [0,0,""]
    
# a list containing the message sources (receiver IDs) that we don't want to 
# use - perhaps they are in geographically inappropriate locations, or some other
# problem (perhaps messages are delayed and compromise the duplicate checking)
try:
    excluded = open('exclude.json')
    excluded_list = json.load(excluded)
except:
    # if nothing alread stored on disk, we make an empty list. It'll get appended to later
    # as receivers are added on the fly from the administrator utility.
    excluded_list = []

# a list of the frequencies we are prepared to transmit DSC messages on
# a message from a frequency not on this list will be ignored by the message
# processing routines, and we won't transmit on that frequency. All transmissions (including
# locally generated outgoing TEST calls) are affected by this exclusion list.    
try:
    freq_allowed = open('freq_allowed.json')
    freq_allowed_list = json.load(freq_allowed)
except:
    # if the list doesn't already exist we create an "open" list with all the usual 
    # Ham DSC frequencies.
    freq_allowed_list = [ "1996.7", "3619.7", "5373.2", "7103.7",  "10147.2", "14347.0"]
    
    
    
# ensure the Transmitter PTT is OFF at program startup
# a workaround for periods of testing where program restarts may occur during a
# transmission  - we want to ensure the PTT is off when we start. PTT_ON / PTT_OFF is an instruction
# sent over the serial connection, rather than a hardware signal, so we need to explicitly send the
# required instructions.

remote_on()
ptt_off()
#set_dial_lock()
set_mode("USB")

# a global flag to allow global TX enable/disable - for safety/maintenance etc.
tx_ok = 1

# a variable to indicate to connected Clients the current state of the PTT. 
ptt_state = "OFF"

try:
    allowed_users = open('allowed_users.json')
    allowed_users_list = json.load(allowed_users)
except:
    allowed_users_list = ["gm4slv" ]
    

online_users = {}

# a function to cause a hard shutdown, called by the "TX ALIVE" watchdog in the event of 
# a failure to send/receive serial instructions to the transceiver (a separate thread checking the serail connection
# every 2 seconds). If the transceiver is not accessible we shutdown the server and wait for the transciever to be
# restored. This function can also be called in response to a remote client command.
def shutdown():
    ptt_off()
    #time.sleep(1)
    #os.remove('start.txt')
    os._exit(0)

# Restart handled by a script via cron - if "start.txt" is present the server will be re-started
# if "start.txt" is not present it will not be restarted.
def reboot():
    ptt_off()
    #time.sleep(1)
    os._exit(0)

# Log all activity to simple text file.
# 
# Everything
def write_file(text):
    global debug
    filename = r'coast_station_log.txt'
    if debug == 1:
        f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
        timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        log = ";".join((timenow, text))  # make an entry for the log by joining the timestamp with the text passed in
        f.write(log)
        f.close()
    else:
        pass
    
# Administrator commands   
def write_admin(text):
    global debug
    filename = r'coast_station_adminlog.txt'
    if debug == 1:
        f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
        timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        log = ";".join((timenow, text))  # make an entry for the log by joining the timestamp with the text passed in
        f.write(log)
        f.close()
    else:
        pass
    
# Record each transmission made in a separate log
def write_txlog(text):
    global debug
    filename = r'coast_station_txlog.txt'
    if debug == 1:
        f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
        timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        log = ";".join((timenow, text))  # make an entry for the log by joining the timestamp with the text passed in
        f.write(log)
        f.close()
    else:
        pass
    
# Log all RX and TX activity
def write_rxtx(text):
    global debug
    filename = r'coast_station_rxtxlog.txt'
    if debug == 1:
        f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
        timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        log = ";".join((timenow, text))  # make an entry for the log by joining the timestamp with the text passed in
        f.write(log)
        f.close()
    else:
        pass

# A UDP Server, threaded, to handle DSC messages from remote receivers, running YaDD v1.7 or above. 
# A direct feed from http://gm4slv.plus.com:8000 is also carried via this server interface.
#
#
#
class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    
    
                
    def handle(self):
        # that incoming data is a list, element [0] is the user data
        # and element [1] is the details of the socket itself.
        data = self.request[0].strip()
        socket = self.request[1]
        
     
        self.dsc(data)
     
    ##########################################################################
    # This function takes data and parses it. Follow the steps in comments within the function.
    #
    def dsc(self, data):
        # a global "frequency allowed" flag, derived from the "allowed frequency list"
        global freq_flag
        global messages_parsed
        global messages_for_us
        # an empty string for the callsign of a vessel/coast station 
        self.call = ""
        # and empty string for the name of a vessel/coast station
        self.name = ""
        
        print "\nUDP Message %s \n" % data
       
        # a YaDD formatted DSC message is a string delimited by ";"
        # split the string into its elements, using a list.
        self.dsc_list = data.split(";")
        
        # reporting RX, converted to UPPER case
        self.rx_id = self.dsc_list[0].upper()
        
        # YaDD reports RX_FREQ - we use this to select the correct frequency on the 
        # transmitter when sending replies
        self.rx_freq = self.dsc_list[1]
        
        #Standard DSC Message elements.
        self.fmt = self.dsc_list[2]
        self.to_mmsi = self.dsc_list[3]
        self.cat = self.dsc_list[4]
        self.from_mmsi = self.dsc_list[5]
        self.tc1 = self.dsc_list[6]
        self.tc2 = self.dsc_list[7]
        self.freq = self.dsc_list[8]
        self.pos = self.dsc_list[9]
        self.eos = self.dsc_list[10]
        
        # YaDD reports ECC as "ECC xx OK" or "ECC xx ERR"
        # we only need the final word. YaDDNEt splits the ECC string before 
        # sending it to us, but the selection process below can still be used
        # to get the "OK" or "ERR". YaDDNet also filters out the "ERR" before sending them
        # but we still need to inspect directly sent YaDD v1.7+ UDP messages.
        self.ecc = self.dsc_list[11].split()[-1]
        
        # Compare the RX_ID to the excluded_list to decide if the message
        # should be handled or ignored.
        if self.rx_id not in excluded_list:
            self.exclude_flag = 0
            print "Handling this one"
        else:
            self.exclude_flag = 1
            print "Excluded"
        ####
        ## DETECT THE LOCAL Transceiver's RX messages - and replace the RX_FREQ supplied by the local
        # copy of YaDD with the correct frequency.
                        
        self.tx_dial = get_freq()
        if self.rx_id == "[GM4SLV]":
            self.rx_freq = str((float(self.tx_dial) + 1.7))
            print "Local TRX Message on ", self.rx_freq    
            
        # Compare the rx_freq with the freq_allowed list to decide if the message
        # should be handled or ignored.
        if self.rx_freq in freq_allowed_list:
            self.freq_flag = 1
            print "Freq OK"
        else:
            self.freq_flag = 0
            print "Freq disabled"
        
        print "ECC = ", self.ecc
        #print "Exclude flag", self.exclude_flag
        
        # check the flags set in the tests above. Matching an IF / ELIF will jump out of the remaining tests 
        if self.exclude_flag == 1:
            print "Excluded RX, ignoring"
            sql.load_admin("Message from %s ignored (excluded)" % self.rx_id)
        
        elif self.freq_flag == 0:
            print "Excluded freq, ignoring"
            sql.load_admin("Message on %s ignored (channel deselected)" % self.rx_freq)
            
        elif self.ecc != "OK":
            print "Checksum Error"
            #write_file("Checksum Error...\n")
            
        elif len(self.from_mmsi) != 9 :
            print "Incorrectly formatted MMSI"
            sql.load_admin("Incorrectly formatted MMSI ignored" % self.from_mmsi)
            
        else:
            if any("~" in s for s in self.dsc_list):
                print "Parity Error..."
                #write_file("Parity Error...\n")
            else:    
                # the message is to be "handled" - having passed all the 
                # previous tests.
                
                # log it....
                write_file("%s\n" % (data))
                messages_received_list[0] += 1
                # save the list onto disk    
                with open('messages_received.json', 'wb') as outfile:
                    json.dump(messages_received_list, outfile)
                    
                #print "parsed: %d" % messages_parsed
                # we set a our "own address" to determine if messages are addressed to us
                # >>>>>>>>>>>>>>>>>... for a rigourous stress test (into test-load) set
                
                #self.our_mmsi = to_mmsi # which will reply to EVERY TEST REQ message reported.
                
                # otherwise we only respond to the value set at the head of the function
                self.our_mmsi = our_mmsi
                
                ###########################
                ######### Check Log #######
                if self.from_mmsi == self.our_mmsi: # it's our own transmission reported back
                    if self.to_mmsi[0:2] != "00":
                        print "TO:", self.to_mmsi
                        self.result = sql.get_resolve(self.to_mmsi)
                        print "resolver says ", self.result
                        if self.result != None:
                            self.name = self.result[2]
                            self.call = self.result[3]
                        else:
                            self.name = "Unk"
                            self.call = "Unk"
                            
                        print "CHECK LOG!!Name ", self.name
                        print "CHECK LOG!! Call ", self.call
                
                    elif self.to_mmsi[0:2] == "00": # a coast-station
                        # get the name from our own Coast Station lookup table (a dictionary)
                        
                        try:
                            self.name = new_coast_dict[self.to_mmsi]
                            self.call = ""
                        except:
                            self.name = "UNID"
                            self.call = ""
                        #self.name = new_coast_dict[self.from_mmsi]
                        print "CHECK LOG!! coast station: %s  (%s)" % (self.name, self.to_mmsi)
                        # log it
                    self.sql_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                    sql.load_rxtx(self.sql_time, self.rx_freq, "CK", self.to_mmsi, self.name, self.call, self.tc1, self.eos, self.rx_id )
                    sql.load_checklog(self.sql_time, self.rx_freq, "CK", self.to_mmsi, self.name, self.call, self.tc1, self.eos, self.rx_id )
                    sql.load_admin("Checklog on %s (%s / %s) to %s (%s / %s) ; %s" % (self.rx_freq, self.tc1, self.eos, self.to_mmsi, self.name, self.call, self.rx_id))
                    
                # We want to resolve calling SHIP names, via aprs.fi, but only do it if the call is addressed to us...
                if self.to_mmsi == self.our_mmsi:
                    messages_received_list[1] += 1
                    with open('messages_received.json', 'wb') as outfile:
                        json.dump(messages_received_list, outfile)
                        
                    # Logging functions....
                    if self.from_mmsi[0:2] != "00": # not a coast-station 
                        try:
                            # call resolve() with the mmsi of the calling ship
                            self.ship = resolve_aprs(self.from_mmsi)
                            print "Ship = ", self.ship
                            # resolve() returns a list with name/call/position-time/lat/long
                            self.name = self.ship[0]
                            self.call = self.ship[1]
                            self.last = self.ship[2]
                            self.lat = self.ship[3]
                            self.lng = self.ship[4]
                            print "TEST CALL RECEIVED by %s on %s from MMSI: %s" % (self.rx_id, self.rx_freq, self.from_mmsi)
                        
                            print "Name : %s, MMSI : %s, Call : %s , Position Time : %s, Lat : %s, Long : %s" % (self.name, self.from_mmsi, self.call, self.last, self.lat, self.lng)
                            # log the details in the text-file logs....
                            write_file("TEST CALL RECEIVED by %s on %s from MMSI : %s\n\n" % (self.rx_id, self.rx_freq, self.from_mmsi))
                            write_file("MMSI : %s, Name : %s, Call : %s. Postion Time: %s, Lat : %s, Long : %s\n\n" % (self.from_mmsi, self.name, self.call, self.last, self.lat, self.lng))
                            write_rxtx("TEST CALL RECEIVED by %s on %s from MMSI : %s\n\n" % (self.rx_id, self.rx_freq, self.from_mmsi))
                            write_rxtx("MMSI : %s, Name : %s, Call : %s. Postion Time: %s, Lat : %s, Long : %s\n\n" % (self.from_mmsi, self.name, self.call, self.last, self.lat, self.lng))
                        
                            
                        except:  # aprs.fi didn't find anything.....
                            print "Not found at APRS.FI"
                            # log it
                            write_file("Ship data not found at www.aprs.fi\n")
                            write_rxtx("Ship data not found at www.aprs.fi\n")
                            # assign a dummy name/call for later use in the SQLite database
                            self.name = "UNK"
                            self.call = "UNK"
                            
                    elif self.from_mmsi[0:2] == "00": # a coast-station
                        # get the name from our own Coast Station lookup table (a dictionary)
                        
                        try:
                            self.name = new_coast_dict[self.from_mmsi]
                            self.call = ""
                        except:
                            self.name = "UNID"
                            self.call = ""
                        #self.name = new_coast_dict[self.from_mmsi]
                        print "From coast station: %s  (%s)" % (self.name, self.from_mmsi)
                        # log it
                        write_file("From a Coast Station: %s (%s)\n" % (self.name, self.from_mmsi))
                        write_rxtx("From a Coast Station: %s (%s)\n" % (self.name, self.from_mmsi))
                        #####################################################################################
                        # we need to think about "00" mmsis that are not in our list - UNID Coast Stations  #
                        #####################################################################################
                        
                    else:
                        # this is probably redundant - if an MMSI isn't "00" then we've already looked it up
                        print "Not a Coast Station or a Ship : %s " % self.from_mmsi
                        write_file("MMSI of sender is not a recognized type : %s \n\n" % self.from_mmsi)
                        write_rxtx("MMSI of sender is not a recognized type : %s \n\n" % self.from_mmsi)
                    
                    # Add the details to the SQL RX database, using the name/call from the resolve/lookup process
                    self.sql_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                    sql.load_rx(self.sql_time, self.rx_freq, self.rx_id, self.from_mmsi, self.name, self.call, self.tc1, self.eos)
                    sql.load_rxtx(self.sql_time, self.rx_freq, "RX", self.from_mmsi, self.name, self.call, self.tc1, self.eos, self.rx_id )
                    # add the details to the System Log too.
                    sql.load_admin("Received on %s (%s / %s) from %s (%s / %s) ; %s" % (self.rx_freq, self.tc1, self.eos, self.from_mmsi, self.name, self.call, self.rx_id))
                    try: # why in a try/except??
                        sql.load_resolve(self.from_mmsi, self.name, self.call)
                    except:
                        pass
                    
                    ##############################
                    ##############################
                    # The main Auto-responder section.
                    # we need:
                    # to == our_mmsi
                    # format == SEL
                    # TC1 == TEST
                    # EOS == REQ
                    # we should test for CAT == SAF and TC2 == NOINF, but some vessels are known to use CAT = RTN for
                    # TEST calls (wrongly). TC2 : DSCDecoder users don't provide a valid TC2 symbol, so we ignore it in our tests
                    #
                    if self.to_mmsi == self.our_mmsi and self.eos == "REQ":# and self.fmt == "SEL" and self.tc1 == "TEST"
                        print "calling reply()"
                        # Force the outgoing FORMAT to "Selective Call"
                        # self.fmt = "SEL"
                        # Force the outgoing EOS to "BQ" (ack) - the correct response to a RQ (REQ)
                        self.eos = "ACK"
                        # force the pos/freq data to "noinf" (6 x 126 symbols)
                        
                        self.data = "noinf" # this is hard-coded later, in reply()
                            
                        
                    
                        # Log it......
                        write_file("Sending a TEST ACK to MMSI: %s\n" % self.from_mmsi)
                        write_rxtx("Sending a TEST ACK to MMSI: %s\n" % self.from_mmsi) 
                    
                    
                        # convert the reported RX_FREQ in the message to a Float number, for use in tuning the transmitter.
                        
                        
                        
                        self.rx_freq = float(self.rx_freq)
                        # call reply() with the necessary DSC message elements. Some are taken from the incoming message
                        # and others have been explicitly set here, or passed as a string in the function call
                        # swap TO and FROM mmsi for the outgoing message.
                        #
                        self.reply(self.rx_freq, self.fmt, self.from_mmsi, self.cat, self.our_mmsi, self.tc1, "NOINF", self.data, self.eos)
                
                else:
                    # the message wasn't for us, or wasn't a REQ
                    print "No action needed\n\n"
                    write_file("No action needed\n\n")    
            
    
    #####################################
    ############################
    #
    # This function takes the parsed DSC message from the incoming data, with 
    # new EOS, and TO/FROM mmsi swapped. It converts the text into symbols. Resolves the names (via our own database) for logging
    # does duplicate-checking and eventually adds the message to the queue.
    
    def reply(self, rx_freq, fmt, to_mmsi, cat, from_mmsi, tc1, tc2, data, eos):
        # used to decide if we are allowed to transmit.....
        global tx_ok
            
        # use the various dictionaries / functions in "dsc_functions" module to convert between text and symbolic values
        #
        from_symbol = mmsi_symbol(from_mmsi)
        to_symbol = mmsi_symbol(to_mmsi)
        
        if tc1 == "TEST" or tc1 == "J3E TP":
            tc1_symbol = int(tc1_symbol_dict[tc1])
        else:
            tc1_symbol = int(tc1_symbol_dict["unable"])
            
        fmt_symbol = int(fmt_symbol_dict[fmt])
        cat_symbol = int(cat_symbol_dict[cat])
       
        tc2_symbol = int(tc2_symbol_dict[tc2])
        eos_symbol = int(eos_symbol_dict[eos])
        # hard code the data-symbols as 6 NOINF symbols
        if tc1_symbol == 109:
            # top band
            if rx_freq < 3000:
                data_symbol = [ 01, 99, 50, 01, 99, 50 ]
            # 80m
            elif rx_freq > 3000 and rx_freq < 4000:
                data_symbol = [ 03, 61, 80, 03, 61, 80 ]
            # 60m    
            elif rx_freq > 4000 and rx_freq < 7000:
                data_symbol = [ 05, 37, 15, 05, 37, 15 ]
            # 40m
            elif rx_freq > 7000 and rx_freq < 10000:
                data_symbol = [ 07, 10, 20, 07, 10, 20 ]
            # 30m    
            elif rx_freq > 10000 and rx_freq < 14000:
                data_symbol = [ 10, 14, 45, 10, 14, 45 ]
            # 20m
            elif rx_freq > 14000 and rx_freq < 18000:
                data_symbol = [ 14, 34, 60, 14, 34, 60 ]
            else:
                data_symbol = [ 126, 126, 126, 126, 126, 126 ]
            
        else:
            data_symbol = [ 126, 126, 126, 126, 126, 126 ]
        
        # call "dsc_functions.build_call() with the symbols for our outgoing message
        # the returned dsc_call is of the form, includes ECC:
        # 120 120 0 23 20 20 40 108 0 23 20 20 40 118 126 126 126 126 126 126 126 117 105 117 117
        #
        dsc_call = build_call(fmt_symbol, to_symbol, cat_symbol, from_symbol, tc1_symbol, tc2_symbol, data_symbol, eos_symbol)
        
        # make a list containing the frequency and the list of symbols as elements
        new_dsc_call = [rx_freq, dsc_call]
        # delay a random time 0-2 seconds, to attempt to spread out
        # coincident reported messages from being added concurrently - #####  work in progress......#####
        time.sleep(random.random() * 2)
        
        # check to see if a matching message (freq/message symbols) is already in the dsc_queue[]
        # if so, we ignore the new one, as it's a duplicate
        if new_dsc_call in dsc_queue:
            print "Duplicate Message, ignored...%s : %s\n" % (rx_freq, to_mmsi)
            write_file("Duplicate Message, ignored...%s : %s\n" % (rx_freq, to_mmsi))
            write_rxtx("Duplicate Message, ignored...%s : %s\n" % (rx_freq, to_mmsi))
            #sql.load_admin("Duplicate Message, ignored...%s : %s" % (rx_freq, to_mmsi))
        else:
            # otherwise we add this 2-element list to the queue (a list of lists)
            # log it......
            print "adding to the queue"
            write_file("Adding to the queue: Test ACK to %s on %.2f \n" % (to_mmsi, rx_freq))
            write_rxtx("Adding to the queue: Test ACK to %s on %.2f \n" % (to_mmsi, rx_freq))
            ####################
            # first we deal with logging it......
            
            # add the new_dsc call to the SQL TX log.....
            # get the time first
            self.sql_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
            
            # we can check for SHIP names in the resolve SQL table (which was updated during the 
            # initial parse process in dsc() above.) No need to look it up online, we have the latest version
            # in our own database already.
            if to_mmsi[0:2] != "00":
                print "TO:", to_mmsi
                self.result = sql.get_resolve(to_mmsi)
                print "resolver says ", self.result
                self.name = self.result[2]
                self.call = self.result[3]
                print "Name ", self.name
                print "Call ", self.call
                
                
                    
            # it's a coast station, look it up in our local Coast Station table.   
            else:
                try:
                    self.name = new_coast_dict[to_mmsi]
                    self.call = ""
                except:
                    self.name = "UNID"
                    self.call = ""
                #self.name = new_coast_dict[to_mmsi]
                # no callsign for Coast Stations (in our table...)
                #self.call = ""
            
            # test for TX enable/disable - we don't log a call if TX is disabled.....
            if tx_ok == 1: # we can transmit
                # put it in the SQL database
                sql.load_tx(self.sql_time, rx_freq, to_mmsi, self.name, self.call, self.tc1, self.eos)
                sql.load_rxtx(self.sql_time, rx_freq, "TX", to_mmsi, self.name, self.call, self.tc1, self.eos, "TX1")
                # put it in the "System Log"
                sql.load_admin("Transmit on %s (%s / %s) to %s (%s / %s)" % (self.rx_freq, self.tc1, self.eos, to_mmsi, self.name, self.call))
            else: # we can't transmit
                # log it in the System Log
                sql.load_admin("TX Inhibited")
                
            # we can transmit - add the new call to the queue    
            dsc_queue.append(new_dsc_call)
        print dsc_queue

#################################################################################################################################
#################################################################################################################################

# A watchdog that tests for Serial communications with the transceiver, by requesting current frequency at 2-second intervals.
# if the TX is not available (turned off / unplugged / failed) we need to shutdown so that we can re-establish comms
# by re-starting AFTER the TX is back online. The auto-restart is handled on Linux by a cron-job which looks for 
# the server process in the process list, and attempts to start it (in a TMUX session) if it doesn't appear in the proc list.
# it will only start if the TX USB serial port is available. 
# TX_WATCH() runs in its own thread       
def tx_watch():
    global online_users
    count = 0
    while True:
        
        try:
            pass
            #get_freq()
        except:
            print "No TX"
            sql.load_admin("Unable to communicate with Transceiver.... quitting...")
            time.sleep(2)
            os._exit(0)
        count += 1
        if count == 898:     
            sql.load_admin("Server alive : %d users online" % len(online_users))
            count = 0
        time.sleep(2)
        
            
            
# Send a TUNE carrier on the required frequency, to assist AUTO_ATU tuning.
# Test for "TX Enable/Disable" and also toggle PTT On/Off for display on remote GUI.
# THIS FUNCTION IS CURRENTLY NOT USED #
def send_tune(rx_freq):
    global tx_ok
    global ptt_state
    
       
    if tx_ok == 1: # we can transmit
        # ptt_state is sent to connected clients, for display on the status page
        ptt_state = "ON"
        # while transmitting we temporarily inhibit TX - to prevent another transmission
        # this is probably not necessary while the Admin GUI has no "send tune" command
        # - the only transmissions should be via the queue handler.
        tx_ok = 0
        # we need to set the TX at f-1.7kHz
        tx_freq = float(rx_freq) - 1.7
        set_freq(tx_freq)
        # send radio_functions.ptt_on()
        ptt_on()
        # send dsc_functions.tune_carrier() at 30% amplitude / 3 seconds
        tune_carrier(0.3, 3)
        ptt_off()
        tx_ok = 1
        ptt_state = "OFF"
        return
    else: # we can't transmit : no action
        pass

#############################################################################################
#
# This runs in a thread, continuously monitoring the queue for new messages, and then transmits them one at a time, popping the oldest one off
# and sending it, until all calls are sent
       
def check_dsc_queue():
    print "Starting Queue Handler"
    write_file("Queue Handler Thread started.....\n\n") # This runs in a separate thread, 
    while True: # run forever......
        
        # a small delay to stop the WHILE loop from racing and eating CPU
        time.sleep(0.5)
        
        if dsc_queue: # there's something to send....
            # access to the various inhibits and informative variables
            global tx_ok
            global ptt_state
            global send_dsc_call # why is this GLOBAL ????
            
            #print dsc_queue
            time.sleep(5) # this gives a 5-second window for DUPLICATE checking, after this we...
            send_dsc_call = dsc_queue.pop(0) # pop the message off, and send it. 
            
            print "Sending dsc_call", send_dsc_call
            
            # we have a two-element list [freq, message[]]
            rx_freq = send_dsc_call[0]
            # concatenate the elements of the message[] list, into a string
            file_dsc_call = " ".join(str(x) for x in send_dsc_call[1])
            # we are sending the symbols in the message[] list
            tx_dsc_call = send_dsc_call[1]
            # 
            if tx_ok == 1: # we can transmit.....
                print "sending on %.2f : %s \n" % (rx_freq, file_dsc_call)
                # dial frequency f-1.7kHz
                tx_freq = rx_freq - 1.7
                write_txlog("Setting TX dial frequency: %.2f \n" % tx_freq)
                # radio_functions.set_freq()
                set_freq(tx_freq)
                time.sleep(2) # wait.... 
                write_file("PTT ON\n")
                write_txlog("PTT ON\n")
                write_rxtx("PTT ON\n")
                ptt_state = "ON" # set the variable so that GUI users see the state
                
                
                ######################
                #try:
                
                # radio_functions.ptt_on()
                ptt_on()
                # we're sending, possibly on a new frequency. Send a carrier for 3 seconds for the Auto-ATU
                # UPDATE - 25/7/15 - R.Pi produces distorted TUNE carrier - so we'll not
                # send a carrier - let the dotting period suffice for ATU Tune, pending a fix
                # for the Tune function.
                #
                tune_carrier(0.3, 3)
                #
                # log it.......
                write_file("Sending on %.2f : %s \n" % (rx_freq, file_dsc_call))
                write_rxtx("Sending on %.2f : %s \n" % (rx_freq, file_dsc_call))
                write_txlog("Sending : %.2f : %s \n" % (rx_freq, file_dsc_call))
                
                
                # dsc_functions.transmit_dsc() at 70% amplitude
                transmit_dsc(tx_dsc_call, 0.7) 
                # when transmit_dec returns, PTT_OFF...
                ptt_off()
                # log it all....
                ptt_state = "OFF"
                write_file("PTT OFF\n\n")
                write_txlog("PTT OFF\n\n")
                write_rxtx("PTT OFF\n\n")
  
                # add message to each index in message_per_band_list (this list can be re-set to zero via the
                # admin utility, it's for short term monitoring only)
                if rx_freq < 2000:
                    message_per_band_list[0] += 1
                elif rx_freq > 2000 and rx_freq < 5000:
                    message_per_band_list[1] += 1
                elif rx_freq > 5000 and rx_freq < 7000:
                    message_per_band_list[2] += 1
                elif rx_freq > 7000 and rx_freq < 10000:
                    message_per_band_list[3] += 1
                elif rx_freq > 10000 and rx_freq < 14000:
                    message_per_band_list[4] += 1
                elif rx_freq > 14000:
                    message_per_band_list[5] += 1
                # save the list onto disk    
                with open('message_per_band.json', 'wb') as outfile:
                    json.dump(message_per_band_list, outfile)
                    
          
            else: # we cannot transmit
                print "TX Inhibited"
                write_file("TX Inhibited\n\n")
                write_rxtx("TX Inhibited\n\n")
                write_txlog("TX Inhibited\n\n")
                
        
########################################################################
########################################################################
#
# The TCP Server for ADMIN functions
#
#########################################################################   
            
class ThreadedRequestHandler(SocketServer.StreamRequestHandler):
    
    
    timeout = 10
    def handle(self):
        

        # we find the current thread for the client connection just set up, to
        # use in the log file
        cur_thread = threading.currentThread()
        # log the new connection details
        write_file("Connect from %s using %s \n" % ((self.client_address[0]), cur_thread.getName()))
        # print to the server's console the new connection IP address/port
        print self.client_address
        
        write_file("Admin GUI: Login from %s \n\n" % (self.client_address[0]))
        write_admin("Admin GUI: Login from %s \n\n" % (self.client_address[0]))
        #sql.load_admin("Admin; Connect from %s" % (self.client_address[0]))
        
        
        
        #global allowed_users_list
        global online_users
        global motd
        server_id = hashlib.md5("server").hexdigest()  
        self.client_id = ":".join( str(x) for x in self.client_address)    
        #self.client_id = str(self.client_address[0])+":"+str(self.client_address[1])
        
        #self.count_reset_time = ""
        while True:
            # using StreamRequestHandler means our input from the client
            # is  "file-like" and can be read with "file-like" commands
            # we read a line at a time, using readline()
            try:
                cmd = self.rfile.readline().upper()
            except:
                
                self.client_name = online_users[self.client_id].split(":")[0]
                sql.load_admin("Admin; Client %s (%s) gone... read exception" % (self.client_id, self.client_name))
                del online_users[self.client_id]
                #print online_users
                break
            #
            if not cmd:
                print "Client Gone"
                self.client_name = online_users[self.client_id].split(":")[0]
                sql.load_admin("Admin; Client %s (%s) gone...empty read" % (self.client_id, self.client_name))
                del online_users[self.client_id]
                #print online_users
                
                break
            else:
                pass
                
             
            
            ##################################
            #### LOGIN LOGIN LOGIN LOGIN #####
            ##################################
            
            words = cmd.split()
            
            if words[0] == "LOGIN":
                
                print "login"
                # words[1] is the provided username
                print "call login(%s)" % words[1]
         
                self.username = words[1].lower()
                self.salt, self.challenge, self.random = pv.make_challenge(self.username)
                self.wfile.write(self.challenge)
            
            
                
            elif words[0] == "REPLY":
                #user = words[1]
                
                self.client_reply = words[1].lower()
                print "reply ", self.client_reply
                self.valid = pv.compare_challenge(self.username, self.client_reply, self.random)
                self.client_version = words[2].lower()
                if self.valid:
                    print "valid user"
                    self.token = pv.login(server_id, self.client_id, self.username)
                    self.wfile.write("Login success")
                    sql.load_admin("Admin; Client login %s, %s, (%s)" % (self.client_id, self.username, self.client_version))
                    online_users[self.client_id] = self.username+":"+self.client_version+":"+self.token
                    print online_users
                else:
                    self.wfile.write("Incorrect Username or Password")
                    time.sleep(2)
                    break
            
            elif words[0] == "ALIVE":
                if hasattr(self, 'token'):
                    self.wfile.write(self.token)
                else:
                    self.wfile.write("pong")
                    
            elif cmd.split(";")[1] == "IWANTOTQUIT":
                print "Client wants to quit"
                sql.load_admin("Admin; Client %s (%s) wants to quit..." % (self.client_id, self.username))
                self.wfile.write("Goodbye")
                del online_users[self.client_id]
                break
            ###############################
            #### VALIDATE EACH MESSAGE ####
            ###############################
            
            # detect ADMIN messages - at present these are the only type of message
            # sent via TCP, in future there may be other types
            if cmd.split(";")[0] == "ADMIN":
                self.client_token = cmd.split(";")[-1].lower().strip()
                #self.validated_token = online_users[self.client_id].split(":")[-1]
                self.check_token = pv.make_token(server_id, self.client_id)
                
                if self.check_token == self.client_token:
                    self.admin(cmd.strip())
                else:
                    print "invalid user"
                    break
                
                    
                
                
            # a catchall - at present the TCP client does not use this method to disconnect    
            
            
    ############################
    ############################
    #
    # The main function for remote administration
    #
    #
    def admin(self, command):
        #allowed_users_list = ["john", "rich", "dirk", "guest"] # is this still needed here?
        prompt = ""
        
            
        #global allowed_users_list
        global tx_ok
        global ptt_state
        global message_per_band_list
        global messages_received_list
        global start_time
        global online_users
        global motd
        #print "#########ADMIN STARTTIME " , start_time
        # Client commands are a string:
        # ADMIN;COMMAND;ID
        # split this into a list
        
		
        self.command = command.split(";")
        
        # The ID is always sent as the final field in a command 
        #self.id = self.command[-1].lower().strip()
        self.id = online_users[self.client_id].split(":")[0]
        # we use the ID later, for logging commands with IP (ID)
        self.client_v = self.command[-2].lower().strip()
        
        
        # A "ping" request/response
        # The client sends "TESTING" at the start of each 
        # polling cycle. If 'online' is not detected in the response
        # the client will attempt to reconnect until successful
        # 
        

        if self.command[1] == "MOTD":
            with open ("motd.txt", "r") as myfile:
                motd=myfile.read()#.replace('\n', '')
            self.respond = motd
            self.send_response(self.respond)
        
        
        elif self.command[1] == "HELLO":
            #self.login_time = time.strftime("%H:%M:%S", time.gmtime(time.time()))
            self.client_string = self.id +" ("+self.client_v+")"
            self.respond = "Hello %s, welcome to GM4SLV. Server version : %s. Service start : %s" % ( self.client_string, version, start_time)
            self.send_response(self.respond)
        
        elif self.command[1] == "VERIFY":
            print "IN VERIFY"
            self.salt, self.verify_challenge, self.verify_random = pv.make_challenge(self.username)
            print "challenge ", self.challenge
            self.wfile.write(self.verify_challenge)
            
        elif self.command[1] == "CHECK":
            print "IN CHECK"
            self.current_reply = self.command[2].lower()
            print "current reply ",self.current_reply
            self.valid = pv.compare_challenge(self.id, self.current_reply, self.verify_random)
            print "self.valid ", self.valid
            if self.valid:
                print "Verified"
                self.wfile.write("verified")
            else:
                self.wfile.write("fail")
                sql.load_admin("Admin; Password update failure for %s" % self.id)
        
        elif self.command[1] == "UPDATEPW":
            print "new password hash"
            self.new_salt = self.command[2].lower()
            self.new_pass_hash = self.command[3].lower()
            self.update_ok = pv.updatepw(self.id, self.new_salt, self.new_pass_hash)
            if self.update_ok:
                self.wfile.write("Password updated")
                sql.load_admin("Admin; Password update successful for %s" % self.id)
            else:
                self.wfile.write("Update failed")
                sql.load_admin("Admin; Password update failure for %s" % self.id)
            
		######## A Combined STATUS poll 
        elif self.command[1] == "POLLSTATUS":
            self.uptime = self.get_uptime(start_time)
            #print "###### POLLSTATUS UPTIME ", self.uptime
            self.online_reply = "Coast Station online (%s)" % (self.uptime)
            #self.online_reply = "User %s : Coast Station online (Server uptime %s)" % (self.id.title(), self.uptime)
            #self.online_reply = "User %s : Coast Station online" % self.id.title()
            if tx_ok == 1:
                # the response procedure should go in a separate function!!
                self.tx_state_reply = "TX Enabled"                                 
            else:
                # the response procedure should go in a separate function!!
                self.tx_state_reply = "TX Disabled"
                
            self.get_ptt_reply="PTT %s" % ptt_state  
            
 
            last_rx = sql.get_last_rx()
           
            # test that there's something in the list
            if last_rx != "":
                # send back the final element of the list to the client
                try:
                    self.last_rx_reply="%s" % " : ".join([str(x) for x in last_rx[-1]] )
                except:
                    self.last_rx_reply="Nothing Yet"
            # otherwise there has been nothing received
            else:
                # inform the client that there's nothing to show
                self.last_rx_reply="Nothing Received"
                
               
            last_tx = sql.get_last_tx()
            
            # test that there's something in the list
            if last_tx != "":
                # send back the final element of the list to the client
                try:
                    self.last_tx_reply="%s" % " : ".join([str(x) for x in last_tx[-1]] )
                except:
                    self.last_tx_reply="Nothing Yet"
                    
            # otherwise there has been nothing received
            else:
                # inform the client that there's nothing to show
                self.last_tx_reply="Nothing Received"    
            
            
            self.message_count_reply="Message Count : { Sent : %d } { Received : total  %d / for us  %d } {Count reset : %s}" % (sum(message_per_band_list), messages_received_list[0], messages_received_list[1], messages_received_list[2])
            
            
            
            count2 = message_per_band_list[0]
            count4 = message_per_band_list[1]
            count6 = message_per_band_list[2]
            count8 = message_per_band_list[3]
            count12 = message_per_band_list[4]
            count16 = message_per_band_list[5]
            
            # inform the client - make a string with the retrieved data
            self.perband_reply="1.8MHz: %d,  3.5MHz: %d,  5MHz: %d,  7MHz: %d,  10MHz: %d,  14MHz: %d" % (count2,count4,count6,count8,count12,count16)
            
            self.freq_allow = freq_allowed_list
            # join each allowed frequency in a string with ";" delimiters
            self.freq_list_reply="%s" %  ";".join([str(x) for x in self.freq_allow] )
            
            rx = excluded_list 
            
            # send the reply to the client
            self.excluded_rx_reply="Excluded RX: %s " %  ", ".join([str(x) for x in rx] )
            
            
            self.respond=self.online_reply+"~"+self.tx_state_reply+"~"+self.get_ptt_reply+"~"+self.last_rx_reply+"~"+self.last_tx_reply+"~"+self.message_count_reply+"~"+self.perband_reply+"~"+self.freq_list_reply+"~"+self.excluded_rx_reply
            #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXX ", self.respond
            self.send_response(self.respond)
            
		
        elif self.command[1] == "LISTCONNECTED":
            self.connected_clients = ""
            for k,v in online_users.items():
                name = v.split(":")[0]
                client_version = v.split(":")[1]
                self.connected_clients += "\n"+name+" ("+client_version+") "+k+"\n"
            self.respond= self.connected_clients
            self.send_response(self.respond)

        
        # The command to inhibit the TX, to prevent any transmissions
        elif self.command[1] == "TXOFF":
            # set the global variable to "0" to indicate to all
            # functions that attempt to transmit that we are not allowed
            tx_ok = 0
            # Log it....
            write_file("Admin GUI: TX Inhibit applied by %s (%s) \n\n" % (self.client_address[0], self.id))
            write_admin("Admin GUI: TX Inhibit applied by %s (%s) \n\n" % (self.client_address[0], self.id))
            sql.load_admin("Admin; TX Inhibit applied by %s (%s)" % (self.client_id, self.id))
            
            # the response procedure should go in a separate function!!
            self.respond="TX Disabled"
            self.send_response(self.respond)
            
        
        # The command to enable the TX
        elif self.command[1] == "TXON":
            # restore the global flag to "1"         
            tx_ok = 1
            # Log it.....
            write_file("Admin GUI: TX Inhibit removed by %s (%s) \n\n" % (self.client_address[0], self.id))
            write_admin("Admin GUI: TX Inhibit removed by %s (%s) \n\n" % (self.client_address[0], self.id))
            sql.load_admin("Admin; TX Inhibit removed by %s (%s)" % (self.client_id, self.id))
            
            # the response procedure should go in a separate function!!
            self.respond="TX Enabled"
            self.send_response(self.respond)
            
            
        
        # Retreive the status of the TX Inhibit
        elif self.command[1] == "TXSTATE":
            
            if tx_ok == 1:
                # the response procedure should go in a separate function!!
                self.respond="TX Enabled"
                self.send_response(self.respond)
                
                
            else:
                # the response procedure should go in a separate function!!
                self.respond="TX Disabled"
                self.send_response(self.respond)
                
                
        # Send a DSC Test Call with freq/addressee sent in the command:
        # e.g "CALL;002320204;1834.5"
        #
        elif self.command[1] == "CALL":
            # the addressee MMSI
            self.to_mmsi_address = self.command[2]
            self.send_cat = self.command[4]
            print "send cat ", self.send_cat
            self.tc1 = self.command[5]
            print "send tc1 ", self.tc1
            
            # Check if the chosen frequency is currently allowed
            # by being listed in the "freq_allowed_list"
            if self.command[3] in freq_allowed_list:
                self.tx_freq = float(self.command[3])
                
                # Check for malformed MMSI (the client has a manual text
                # entry widget, the user may accidentally type the MMSI wrongly
                # a properly formed MMSI has 9 digits
                if len(self.to_mmsi_address) != 9:
                    # reply to the client
                    self.respond="Incorrectly formed MMSI"
                    self.send_response(self.respond)
                    
                # Check that TX is disabled   
                elif tx_ok == 0:
                    # if disabled inform the client
                    self.respond="TX Inhibit, call rejected"
                    self.send_response(self.respond)
                    
                # Otherwise we're free to send.....    
                else:
                    # Log it.....
                    write_file("Admin GUI: Test Call sent to %s on %.2f by %s (%s) \n\n" % (self.to_mmsi_address, self.tx_freq, self.client_address[0], self.id))
                    write_admin("Admin GUI: Test Call sent to %s on %.2f by %s (%s) \n\n" % (self.to_mmsi_address, self.tx_freq, self.client_address[0], self.id))
                    sql.load_admin("Admin; Test Call sent to %s on %.2f by %s (%s)" % (self.to_mmsi_address, self.tx_freq, self.client_address[0], self.id))
                    # Call reply() with the required parameters, some from the supplied client data, some hard-coded as strings
                    # This will then proceed to add the desired DSC message to the dsc_queue (with duplicate checking etc)
                    # as if it were one triggered by a received TEST REQ. The TCP server class has its own 
                    # copy of reply() - perhaps this can be changed to use a separate reply() module for both the UDP and TCP servers
                    self.reply(self.tx_freq, "SEL", self.to_mmsi_address, self.send_cat, our_mmsi, self.tc1, "NOINF", "noinf", "REQ" )
                    # Inform the client
                    self.respond="Calling %s on %.2f" % (self.to_mmsi_address, self.tx_freq)
                    self.send_response(self.respond)
                    
                    
            # The Frequency wasn't in the allowed_list so we inform the client of failure to send
            else:
                self.respond="Frequency disabled: %s" % self.command[3]
                self.send_response(self.respond)
                
                

        # A command to check the list of "excluded" Receiver IDs        
        elif self.command[1] == "SHOW":
            
            rx = excluded_list 
            
            # send the reply to the client
            self.respond="Excluded: %s " %  ", ".join([str(x) for x in rx] )
            self.send_response(self.respond)
            
            
        # A command to check the currently allowed frequencies
        # The reply is a friendly string for display on the client terminal widget
        #### The client currently does not send this command - it sends POLLFREQ
        #### to configure the state of checkbuttons instead.
        elif self.command[1] == "SHOWFREQ":
        
            freq_allow = freq_allowed_list
            
            # send the reply to the client
            self.respond="Freqs enabled: %s " %  ", ".join([str(x) for x in freq_allow] )
            self.send_response(self.respond)
            
            
        # A command to get the list of allowed frequencies
        # The client sets the status of checkbuttons to display
        # the state of each frequency
        elif self.command[1] == "POLLFREQ":
        
            freq_allow = freq_allowed_list
            # join each allowed frequency in a string with ";" delimiters
            self.respond="%s" %  ";".join([str(x) for x in freq_allow] )
            self.send_response(self.respond)
            
        
            
        # A command to remove a frequency from the allowed_list
        # Sent by the client as e.g. "DEL;1834.5"
        elif self.command[1] == "DELFREQ":
            
            # the frequency to be deleted from the allowed list
            freq_d = self.command[2]
            
            # Test to determine if the frequency is current IN the list
            # otherwise we can't remove it!
            if freq_d in freq_allowed_list:
                # call the list remove() method
                freq_allowed_list.remove(freq_d)
                
                # update the json disk file, for persistence across restarts
                with open('freq_allowed.json', 'wb') as outfile:
                    json.dump(freq_allowed_list, outfile)
                    
                # Inform the client
                self.respond="Removed %s from allowed frequencies" % freq_d
                self.send_response(self.respond)
                
                 
                # Log it...
                write_file("Admin GUI: Removed %s from allowed frequencies by %s (%s) \n\n" % (freq_d, self.client_address[0], self.id) )
                write_admin("Admin GUI: Removed %s from allowed frequencies by %s (%s) \n\n" % (freq_d, self.client_address[0], self.id) )
                sql.load_admin("Admin; Removed %s from allowed frequencies by %s (%s)" % (freq_d, self.client_id, self.id) )
            
            # The requested frequency is not currently allowed anyway, we can't remove it
            else:
                # inform the client
                self.respond="Not found"
                self.send_response(self.respond)
                
                
        # A command to add a frequency to the allowed_list
        elif self.command[1] == "ADDFREQ":
        
            # the frequency to be added/allowed
            freq_a = self.command[2]
            
            # Test to see the client hasn't sent an empty string, and that the frequency 
            # isn't already in the allowed_list. We don't want to add it again!
            if freq_a != "" and freq_a not in freq_allowed_list:
                # call the list append() method to add the new frequency
                freq_allowed_list.append(freq_a)
                
                # update the json disk file, for persistence across restarts
                with open('freq_allowed.json', 'wb') as outfile:
                    json.dump(freq_allowed_list, outfile)
                    
                # inform the client
                self.respond="Added %s to allowed frequencies" % freq_a
                self.send_response(self.respond)
                
                
                # Log it...
                write_file("Admin GUI: Added %s to allowed frequencies by %s (%s) \n\n" % (freq_a, self.client_address[0], self.id))
                write_admin("Admin GUI: Added %s to allowed frequencies by %s (%s) \n\n" % (freq_a, self.client_address[0], self.id))
                sql.load_admin("Admin; Added %s to allowed frequencies by %s (%s)" % (freq_a, self.client_id, self.id))
            
            # either an empty string, or the frequency was already allowed
            # we inform the client that nothing can be done
            else:
                self.respond="Request ignored"
                self.send_response(self.respond)
                
                
        
        # a command to add a receiver to the "EXCLUDED RX" list - i.e. "ADD = EXCLUDE"
        elif self.command[1] == "ADD":
            
            # the receiver name to be excluded
            rx = self.command[2].upper()
            
            # test for an empty string
            if rx != "" and rx not in excluded_list:
                # not empty, so call append() to add the RX to the excluded_list
                excluded_list.append(rx)
                
                # update the json disk file, for persistence across restarts
                with open('exclude.json', 'wb') as outfile:
                    json.dump(excluded_list, outfile)
                    
                # inform the client
                self.respond="Added %s to excluded RX list" % rx
                self.send_response(self.respond)
                
                
                # Log it....    
                write_file("Admin GUI: Added %s to excluded RX list by %s (%s) \n\n" % (rx, self.client_address[0], self.id))
                write_admin("Admin GUI: Added %s to excluded RX list by %s (%s) \n\n" % (rx, self.client_address[0], self.id))
                sql.load_admin("Admin; Added %s to excluded RX list by %s (%s)" % (rx, self.client_id, self.id))
                
            # an empty string was supplied, ignore, and inform the client  
            else:
                self.respond="Empty Request, ignored"
                self.send_response(self.respond)
                
                
        # a command to remove a RX from the "excluded" list - i.e. "DEL = INCLUDE"       
        elif self.command[1] == "DEL":
            
            # the receiver name to be included
            rx = self.command[2].upper()
            
            # test that the RX is actually in the excluded list, we can't remove it if it
            # isn't in the list!
            if rx in excluded_list:
                # call remove() to delete it from the list.
                excluded_list.remove(rx)
                
                # update the json disk file, for persistence across restarts
                with open('exclude.json', 'wb') as outfile:
                    json.dump(excluded_list, outfile)
                    
                # inform the client
                self.respond="Removed %s from excluded RX list" % rx
                self.send_response(self.respond)
                
                
                # Log it....    
                write_file("Admin GUI: Removed %s from excluded RX list by %s (%s) \n\n" % (rx, self.client_address[0], self.id))
                write_admin("Admin GUI: Removed %s from excluded RX list by %s (%s) \n\n" % (rx, self.client_address[0], self.id))
                sql.load_admin("Admin; Removed %s from excluded RX list by %s (%s)" % (rx, self.client_id, self.id))
                
            # The RX wasn't in the excluded list, so we can't remove it.
            # inform the client
            else:
                self.respond="Not found"
                self.send_response(self.respond)
                
                
                
        
        elif self.command[1] == "LAST1":
            
            
            last = sql.get_last_rx()
            # test that there's something in the list
            if last is not None:
                # send back the final element of the list to the client
                self.respond="%s" % " : ".join([str(x) for x in last[-1]] )
                self.send_response(self.respond)
                
            
            # otherwise there has been nothing received
            else:
                # inform the client that there's nothing to show
                self.respond="Nothing Received"
                self.send_response(self.respond)
                
                
        
        elif self.command[1] == "TX1":
            
            
            last_tx = sql.get_last_tx()
            
            # Test that there's something in the list
            if last_tx is not None:
                # send the last element from the list
                self.respond="%s" % " : ".join([str(x) for x in last_tx[-1]] )
                self.send_response(self.respond)
                
            
            # otherwise we've not transmitted anything. Inform the client
            else:
                self.respond="Nothing Sent"
                self.send_response(self.respond)
                
                
        
        # A command to retrieve the current state of the PTT
        # to indicate when a transmission is in progress
        elif self.command[1] == "GETPTT":
            # ptt_state is a global variable
            # inform the client
            self.respond="PTT %s" % ptt_state
            self.send_response(self.respond)
            
        
        
        
        # a command to retrieve a count of the messages sent
        # this is calculated by summing the count for each band in the messages_per_band_list
        # which is a persistent "json" list. The count can be reset to ZERO, and is 
        # only used for short term observation of message numbers.
        elif self.command[1] == "COUNT":
            # calculate the total messages sent
            self.respond="Messages Sent: %d" % sum(message_per_band_list)
            self.send_response(self.respond)
            
        
        # a command to retrieve the message count on a band-by-band basis
        # to display on the client Status page.
        # the message count can be reset to ZERO.
        elif self.command[1] == "PERBAND":
            # the list[] holds the count for
            # each band as a particular list item
            # we can retrieve each band's count from the list
            count2 = message_per_band_list[0]
            count4 = message_per_band_list[1]
            count6 = message_per_band_list[2]
            count8 = message_per_band_list[3]
            count12 = message_per_band_list[4]
            count16 = message_per_band_list[5]
            
            # inform the client - make a string with the retrieved data
            self.respond="2MHz: %d,  4MHz: %d,  6MHz: %d,  8MHz: %d,  12MHz: %d,  16MHz: %d" % (count2,count4,count6,count8,count12,count16)
            self.send_response(self.respond)
            
          
            
        # a command to reset the message counts to ZERO
        elif self.command[1] == "CLEAR":
            # make a new list with six ZEROs - one per band
            self.count_reset_time = time.strftime("%H:%M %d/%m/%y ", time.gmtime(time.time()))
            message_per_band_list = [0] * 6
            
            messages_received_list = [0,0,self.count_reset_time] 
            
            # update the json disk files, for persistence across restarts
            with open('message_per_band.json', 'wb') as outfile:
                    json.dump(message_per_band_list, outfile)
            with open('messages_received.json', 'wb') as outfile:
                    json.dump(messages_received_list, outfile)  
                    
            # Log it.....
            write_file("Admin GUI: Message Count reset by %s (%s) \n\n" % (self.client_address[0], self.id))
            write_admin("Admin GUI: Message Count reset by %s (%s) \n\n" % (self.client_address[0], self.id))
            sql.load_admin("Admin; Message Count reset by %s (%s)" % (self.client_id, self.id))
          
            # Inform the client
            self.respond="Message Count reset to zero"
            self.send_response(self.respond)
            
            
        # a command to retrieve entries from the "ADMIN" system log
        # this is stored in a SQLite database
        # the function sql.get_admin() is set to retrieve a limited list (based on time)
        # from the database.
        elif self.command[1] == "GETADMINSQL":
            # call the sql query function 
            self.sql = sql.get_admin()
            
            # make an empty string to append each retrieved row. The sql query returns a multi row list           
            self.result = ""
            
            # loop through each line in the reply and append the two elements (datetime, message) to the response string
            for row in self.sql:   
                self.result += row[0]+" ; "+ row[1]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)
        
        
            
        elif self.command[1] == "GETALLADMINSQL":
            # call the sql query function 
            self.sql = sql.dump_admin()
            
            # make an empty string to append each retrieved row. The sql query returns a multi row list           
            self.result = ""
            
            # loop through each line in the reply and append the two elements (datetime, message) to the response string
            for row in self.sql:   
                self.result += row[0]+" ; "+ row[1]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)
            
            
        # a command to retrieve entries from the "RX" log
        # this is stored in a SQLite database
        # the function sql.get_rx() is set to retrieve a limited list (based on number)
        # from the database.
        elif self.command[1] == "GETRXSQL":
            self.sql = sql.get_rx()   
            self.result = ""
            for row in self.sql:
                # each record has "datatime, frequency : from_mmsi : name : call : tc1 : eos : rx_id
                # append each line to the response string
                self.result += row[0]+" ; "+row[1]+" ; "+row[3]+" ; "+row[4]+" ; "+ row[5]+" ; "+row[6]+" ; "+row[7]+" ; "+row[2]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)
            
        elif self.command[1] == "GETALLRXSQL":
            self.sql = sql.dump_rx()   
            self.result = ""
            for row in self.sql:
                # each record has "datatime, frequency : from_mmsi : name : call : tc1 : eos : rx_id
                # append each line to the response string
                self.result += row[0]+" ; "+row[1]+" ; "+row[3]+" ; "+row[4]+" ; "+ row[5]+" ; "+row[6]+" ; "+row[7]+" ; "+row[2]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)
            
            
        # a command to retrieve entries from the "TX" log
        # this is stored in a SQLite database
        # the function sql.get_tx() is set to retrieve a limited list (based on number)
        # from the database.   
        elif self.command[1] == "GETTXSQL":
            self.sql = sql.get_tx()   
            self.result = ""
            for row in self.sql:
                # each record has "datatime, frequency : from_mmsi : name : call 
                # append each line to the response string
                self.result += row[0]+" ; "+row[1]+" ; "+row[2]+" ; "+row[3]+" ; "+ row[4]+" ; "+ row[5]+" ; "+row[6]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)
            
        elif self.command[1] == "GETALLTXSQL":
            self.sql = sql.dump_tx()   
            self.result = ""
            for row in self.sql:
                # each record has "datatime, frequency : from_mmsi : name : call 
                # append each line to the response string
                self.result += row[0]+" ; "+row[1]+" ; "+row[2]+" ; "+row[3]+" ; "+ row[4]+" ; "+ row[5]+" ; "+row[6]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)
            
        elif self.command[1] == "GETRXTXSQL":
            self.sql = sql.get_rxtx()   
            self.result = ""
            for row in self.sql:
                # each record has "datatime, frequency : from_mmsi : name : call 
                # append each line to the response string
                self.result += row[0]+" ; "+row[1]+" ; "+row[2]+" ; "+row[3]+" ; "+ row[4]+" ; "+ row[5]+" ; "+row[6]+" ; "+row[7]+" ; "+row[8]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)
            
            
        elif self.command[1] == "GETCHECKSQL":
            self.sql = sql.get_checklog()   
            self.result = ""
            for row in self.sql:
                # each record has "datatime, frequency : from_mmsi : name : call 
                # append each line to the response string
                self.result += row[0]+" ; "+row[1]+" ; "+row[2]+" ; "+row[3]+" ; "+ row[4]+" ; "+ row[5]+" ; "+row[6]+" ; "+row[7]+" ; "+row[8]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)
        
        elif self.command[1] == "GETALLCHECKSQL":
            self.sql = sql.dump_checklog()
            print "Calling dump()"
            self.result = ""
            for row in self.sql:
                # each record has "datatime, frequency : from_mmsi : name : call 
                # append each line to the response string
                self.result += row[0]+" ; "+row[1]+" ; "+row[2]+" ; "+row[3]+" ; "+ row[4]+" ; "+ row[5]+" ; "+row[6]+" ; "+row[7]+" ; "+row[8]+"\n"
            print self.result
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)    
            
        elif self.command[1] == "GETALLRXTXSQL":
            self.sql = sql.dump_rxtx()   
            self.result = ""
            for row in self.sql:
                # each record has "datatime, frequency : from_mmsi : name : call 
                # append each line to the response string
                self.result += row[0]+" ; "+row[1]+" ; "+row[2]+" ; "+row[3]+" ; "+ row[4]+" ; "+ row[5]+" ; "+row[6]+" ; "+row[7]+" ; "+row[8]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)    
            
        # a command to retrieve entries from the "RESOLVE" log
        # this is stored in a SQLite database
        # the function sql.dump_resolve() is set to retrieve all the known recipients (coast and ship)
        # from the database.    
        elif self.command[1] == "GETRESOLVESQL":
            self.sql = sql.dump_resolve()   
            self.result = ""
            for row in self.sql:
                # each record has "mmsi : name : call 
                # append each line to the response string
                self.result += row[1]+" ; "+ row[2]+" ; "+ row[3]+"\n"
            
            # inform the client
            self.respond="%s" % self.result
            self.send_response(self.respond)
            
            
        # a command to remotely shutdown the Server software
        # this is an "emergency stop"
        # the Linux based server will attempt to re-start if it is found to be 
        # not running.
        elif self.command[1] == "SHUTDOWN":
            self.reason = self.command[2]
            # Log it....... we want to know who's been shutting us down.
            write_file("Admin GUI: SHUTDOWN COMMAND FROM  %s (%s) \n\n" % (self.client_address[0], self.id))
            write_admin("Admin GUI: SHUTDOWN COMMAND FROM  %s (%s) \n\n" % (self.client_address[0], self.id))
            sql.load_admin("Admin; SHUTDOWN COMMAND FROM  %s (%s); %s" % (self.client_address[0], self.id, self.reason))
            
            # Inform the client that the command has been received
            self.respond="Shutting Down Coast Station : %s" % self.reason
            self.send_response(self.respond)
            
            
            # call shutdown() function which uses os._exit(0) to force a hard close of the server
            shutdown()
        
        # a command to remotely restart the Server software
        elif self.command[1] == "REBOOT":
            self.reason = self.command[2]
            # Log it....... we want to know who's been shutting us down.
            write_file("Admin GUI: REBOOT COMMAND FROM  %s (%s) \n\n" % (self.client_address[0], self.id))
            write_admin("Admin GUI: REBOOT COMMAND FROM  %s (%s) \n\n" % (self.client_address[0], self.id))
            sql.load_admin("Admin; REBOOT COMMAND FROM  %s (%s); %s" % (self.client_address[0], self.id, self.reason))
            
            # Inform the client that the command has been received
            self.respond="Attempting re-boot of Coast Station : %s" % self.reason
            self.send_response(self.respond)
            
            
            # call reboot() function which uses os._exit(0) to force a hard close of the server
            reboot()
        
        
        elif self.command[1] == "CLEARADMIN7SQL":
            sql.clear_admin_7day_table()
            sql.load_admin("Admin; DATABASE PURGED FROM %s (%s)" % (self.client_id, self.id))
            self.respond="Syslog database purged"
            self.send_response(self.respond)
        
        elif self.command[1] == "CLEARADMINLOGINSQL":
            sql.clear_admin_login_table()
            sql.load_admin("Admin; DATABASE PURGED FROM %s (%s)" % (self.client_id, self.id))
            self.respond="Syslog database purged"
            self.send_response(self.respond)
        
        
        # anything else... we don't recognize   
        else:
            print "NOT UNDERSTOOD"
            
            # inform the client
            self.respond="NOT UNDERSTOOD %s" % self.command
            self.send_response(self.respond)
           
    
    # we need to tell the server how much data we're sending. the simple approach adds a 
    # number (string) to the beginning of each reply representing the number of bytes in the data,
    # separated from the data by a "@" symbol.
    # The server checks the length information and reads as often as necessary to receive ALL the message.
    def send_response(self, respond):
        prompt = str(len(respond))+"@"
        self.wfile.write(prompt+respond)
        return
    
    def get_uptime(self, start_time):
    
        #print start_time
        self.now_time = time.strftime("%H:%M %a, %d %b, %Y", time.gmtime(time.time()))

        self.start = datetime.datetime.strptime(start_time, '%H:%M %a, %d %b, %Y')

        self.now = datetime.datetime.strptime(self.now_time, '%H:%M %a, %d %b, %Y')

        diff = self.now - self.start
        weeks, days  = divmod(diff.days, 7)
        minutes, secs = divmod(diff.seconds, 60)
    
        hours, mins = divmod(minutes, 60)


        uptime = "Service uptime: %d weeks %d days %02d:%02d " % (weeks, days, hours, mins)

        return uptime   
    
    #######################################
    #######################################
    #
    # The TCP server has it's own reply() function used to 
    # create outgoing DSC messages from Client commands
    # and add them to the global DSC_QUEUE[] along with automatic
    # replies created in the UDP server.
    # It may be possible to move this to an external module to be used by both
    # UDP and TCP servers..... 
    #
    # for comments on functionality, see the reply() in the UDP server class
    #
    def reply(self, rx_freq, fmt, to_mmsi, cat, from_mmsi, tc1, tc2, data, eos):
        global tx_ok
        
            
            
        from_symbol = mmsi_symbol(from_mmsi)
        to_symbol = mmsi_symbol(to_mmsi)
        tc1_symbol = int(tc1_symbol_dict[tc1])
        fmt_symbol = int(fmt_symbol_dict[fmt])
        cat_symbol = int(cat_symbol_dict[cat])
       
        tc2_symbol = int(tc2_symbol_dict[tc2])
        eos_symbol = int(eos_symbol_dict[eos])
        
        
         # hard code the data-symbols as 6 NOINF symbols
        if tc1_symbol == 109:
            # top band
            if rx_freq < 3000:
                data_symbol = [ 01, 99, 50, 01, 99, 50 ]
            # 80m
            elif rx_freq > 3000 and rx_freq < 4000:
                data_symbol = [ 03, 61, 80, 03, 61, 80 ]
            # 60m    
            elif rx_freq > 4000 and rx_freq < 7000:
                data_symbol = [ 05, 37, 15, 05, 37, 15 ]
            # 40m
            elif rx_freq > 7000 and rx_freq < 10000:
                data_symbol = [ 07, 10, 20, 07, 10, 20 ]
            # 30m    
            elif rx_freq > 10000 and rx_freq < 14000:
                data_symbol = [ 10, 14, 55, 10, 14, 55 ]
            # 20m
            elif rx_freq > 14000 and rx_freq < 18000:
                data_symbol = [ 14, 34, 60, 14, 34, 60 ]
            else:
                data_symbol = [ 126, 126, 126, 126, 126, 126 ]
            
        else:
            data_symbol = [ 126, 126, 126, 126, 126, 126 ]
            
        
        
        dsc_call = build_call(fmt_symbol, to_symbol, cat_symbol, from_symbol, tc1_symbol, tc2_symbol, data_symbol, eos_symbol)
        
        new_dsc_call = [rx_freq, dsc_call]
        # delay a random time 0-2 seconds, to attempt to spread out
        # coincident reported messages from being added concurrently?
        time.sleep(random.random() * 2)
        if new_dsc_call in dsc_queue:
            print "Duplicate Message, ignored...%s : %s\n" % (rx_freq, to_mmsi)
            write_file("Duplicate Message, ignored...%s : %s\n" % (rx_freq, to_mmsi))
            write_rxtx("Duplicate Message, ignored...%s : %s\n" % (rx_freq, to_mmsi))
        else:
        
            print "adding to the queue"
            write_file("Adding to the queue: Test ACK to %s on %.2f \n" % (to_mmsi, rx_freq))
            write_rxtx("Adding to the queue: Test ACK to %s on %.2f \n" % (to_mmsi, rx_freq))
            
            
            
            self.sql_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
            if to_mmsi[0:2] != "00":
                self.name = ""
                self.call = ""
                print "TO::", to_mmsi
                self.result = sql.get_resolve(to_mmsi)
                print "resolver says ", self.result
                try:
                    self.name = self.result[2]
                    self.call = self.result[3]
                except:
                    pass
                print "Name ", self.name
                print "Call ", self.call
                
                
            else:
                try:
                    self.name = new_coast_dict[to_mmsi]
                    self.call = ""
                except:
                    self.name = "UNID"
                    self.call = ""
                
                
            if tx_ok == 1:
                sql.load_tx(self.sql_time, rx_freq, to_mmsi, self.name, self.call, tc1, eos)
                sql.load_rxtx(self.sql_time, rx_freq, "TX", to_mmsi, self.name, self.call, tc1, eos, "TX1")
                sql.load_admin("Transmit on %s (%s / %s) to %s (%s / %s)" % (rx_freq, tc1, eos, to_mmsi, self.name, self.call))
            else:
                sql.load_admin("TX Inhibited")
            dsc_queue.append(new_dsc_call)
        print dsc_queue
        
    
    
        
# the class for the UDP Server    
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

# the class for the TCP Server
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
    
# the start......   
if __name__ == "__main__":
    
    # The UDP Server host/port assignment
    HOST, PORT = "", 50669
    
    # the TCP Server host/port assignment
    address = ('', 50669)
    
    # both servers use the same port - to allow easy router port-forwarding configuration
    
    # instance of the TCP Server
    tserver = ThreadedTCPServer(address, ThreadedRequestHandler)
    tserver.allow_reuse_address = True
    
    # instance of the UDP Server
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    
    # is this necessary, used elsewhere?????
    ip, port = server.server_address
    
    # thread for the DSC Queue checking function
    tx = threading.Thread(target=check_dsc_queue)
    tx.start()
    
    # Thread for the TX available watchdog 
    watch = threading.Thread(target=tx_watch)
    watch.start()
       
    # thread for the UDP Server
    t = threading.Thread(target=server.serve_forever)
    
    # thread for the TPC Server
    tcp = threading.Thread(target=tserver.serve_forever)
    
    # exit the threads when program closes
    t.daemon = True
    tcp.daemon = True
    
    # Start the UDP Server thread
    t.start()
    
    # Start the TCP Server thread
    tcp.start()
    
    sql.load_admin("Coast Station online......")

    
   
