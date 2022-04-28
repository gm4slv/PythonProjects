#!/usr/bin/python

'''
Python Console Client for remote control of Icom IC-M710 Marine HF SSB Transceiver

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
'''

import socket
version = "v1.0"

try:
    import readline
except ImportError:
    pass

import threading
import time

HOST, PORT = "192.168.21.7", 9710

radio_num = "r1" 
rname = "IC-M710"

def make_con():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

def prompt():
    print ""
    print "************ Command List *************"
    print "=" * 39
    
    print " gm  :  Get Mode       sm  :  Set Mode"
    print " gf  :  Get Freq       sf  :  Set Freq"
    print " ga  :  Get Freq/Mode   t  :  ATU Tune"
    #print " gs  :  Get S-meter    ga  :  Get All"
    #print " t   :  ATU Tune"
    print "=" * 39
    print " don : Disp On       doff  : Disp Off"
    print " son : Spkr On       soff  : Spkr Off"
    print " ron : Remote On     roff  : Remote Off"
    print "=" * 39
    print " h   : Help            lm  : List Modes"          
    print " q   : Quit"
    print "=" * 39
    print ""


def start():
    global radio_num
    global rname
    global sock

    data = raw_input(rname + " > ").lower().strip()
    if len(data.split()) > 1:
        prompt()
        print "only one command at a time please"
        start()
    
    elif data == "gm":
        mode = connect("getmode" + " " + radio_num)
        print "%s replied: %s" % (rname, mode)
        start()

    elif data == "sm":
        smode = raw_input("Enter mode: ")
        if smode == "u":
            smode = "usb"
        elif smode == "l":
            smode = "lsb"
        elif smode == "a":
            smode = "am"
        elif smode == "c":
            smode = "cw"
        elif smode == "f":
            smode = "fsk"
        elif smode == "j":
            smode = "j2b"
        elif smode == "r":
            smode = "r3e"
        mode = connect("setmode" + " " + smode + " " + radio_num)
        print "%s replied: %s" % (rname, mode)
        start()

    elif data == "gf":
        freq = connect("getfreq" + " " + radio_num)
        print "%s replied: %s kHz" % (rname, freq)
        start()

    elif data == "sf":
        sfreq = raw_input("Enter freq (kHz): ")
        #while len(sfreq) < 3:
        #    print "try again..."
        #    sfreq = raw_input("Enter freq (kHz): ")
        try:
            f = float(sfreq)
        except:
            print "Freq. not recognized"
            #prompt()
            start()
        freq = connect("setfreq" + " " + sfreq + " " + radio_num)
        print "%s replied: %s" % (rname, freq)
        start()

    elif data == "gs":
        smeter = connect("getsmeter" + " " + radio_num)
        print "%s replied: %s" % (rname, smeter)
        start()
        
    elif data == "ron":
        remote = connect("remoteon" + " " + radio_num)
        print "%s replied: %s" % (rname, remote)
        start()
        
    elif data == "roff":
        remote = connect("remoteoff" + " " + radio_num)
        print "%s replied: %s" % (rname, remote)
        start()
        
    elif data == "t":
        tune = connect("tune" + " " + radio_num)
        print "%s replied: %s" % (rname, tune)
        start()
        
    # Doff = Display Off = DIM ON for the radio    
    elif data == "doff":
        remote = connect("dimon" + " " + radio_num)
        print "%s replied: %s" % (rname, remote)
        start()   
    # DON = Display On = DIM OFF for the radio    
    elif data == "don":
        remote = connect("dimoff" + " " + radio_num)
        print "%s replied: %s" % (rname, remote)
        start()
        
    elif data == "son":
        remote = connect("spon" + " " + radio_num)
        print "%s replied: %s" % (rname, remote)
        start()
    elif data == "soff":
        remote = connect("spoff" + " " + radio_num)
        print "%s replied: %s" % (rname, remote)
        start()
        
    elif data == "ga":
        get_all()
        start()

    elif data == "lm":
        print "Available Modes : u|usb, l|lsb, a|am, c|cw, j|j2b, f|fsk, r|r3e"
        start()
        
    elif data == "h" or data == "help":
        prompt()
        start()

    elif data == "q" or data == "quit":
        rx = connect("quit")
        print "%s replied: %s " % (rname, rx)

    else:
        prompt()
        start()

def get_all():
    n = "r1"
    freq = connect("getfreq" + " " + n)
    mode = connect("getmode" + " " + str(n))
    #smeter = connect("getsmeter" + " " + str(n))
    
    print "********** Current settings **********"
    print "=" * 38
    print " Frequency : %s kHz  Mode : %s" % (freq, mode)
    #print " S-Meter   : %s" % smeter
    print "=" * 38

# Try to send and receive in one-go, to prevent the logging thread and the main prog
# getting the wrong receive data

def connect(data):
    try:
        lock.acquire()
        global sock
        sock.sendall(data + "\n")
        received = sock.recv(2048)
    finally:
        lock.release()

    return received

make_con()

lock = threading.Lock()


print "Welcome to the IC-M710 Network Client"
print ""
get_all()
prompt()
start()
