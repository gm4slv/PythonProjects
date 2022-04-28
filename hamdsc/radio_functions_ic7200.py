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
# Serial Port control for the Icom IC-7200
# 
#

import threading
import serial

# used to control access to the serial port in case of multiple attempts to read/write data
# to the radio
lock = threading.Lock()

version = "v1.0"

# The serial port  - linux /dev/ttyUSB0 - windows "COMx"
sport = '/dev/ttyUSB0'

###### LINUX UDEV RULE TO SYMLINK the IC-7200 to "/dev/IC7200" 

#sport = '/dev/IC7200'
#sport = "COM1"
# instance of Serial, with required baud rate.
ser = serial.Serial(sport, 9600, timeout=1)

#
# Icom CiV hex-codes
# requests are built as strings concatenating these codes as required
preamble = "\xfe"
controller = "\xe0"
eom = "\xfd"
ack = "\xfb"
nak = "\xfa"
radio_address = "\x76" # IC-7200
tx_on = "\x1c" + "\x00" + "\x01"
tx_off = "\x1c" + "\x00" + "\x00"
set_freq_cmd = "\x05"
get_freq_cmd = "\x03"
set_mode_cmd = "\x06"
set_dig_cmd = "\x1a" + "\x04" + "\x01" + "\x03"
set_lock_cmd = "\x16" + "\x50" + "\x01"
ack = "\xfb"
nak = "\xfa"

# we only use a subset of available CiV commands for Coast Station use
# we don't need "get_mode(), attenuator, pre_amp, etc. etc...


# For Coast Station we only request USB mode from the Server, so there's no conversion of other 
# modes to CiV Hex codes.
def set_mode(mode):
    
    # It should only ever be "usb"
    if mode == "usb":
        set_mode_val = "\x01"
        
    else: # the server has requested something else??
        return "Mode not recognized"
        
    # concatenate the required hex codes into a string according to the CiV protocol
    sendStr = preamble + preamble + radio_address + controller + set_mode_cmd + set_mode_val + eom
    
    # call tx_rx() with the string
    result = tx_rx(sendStr)
    
    # the result is a (list or string?) of bytes. 
    # We look for an ACK byte at position [4]
    if result[4] == ack:
        return "Set Mode Success"
    elif result[4] == nak:
        return "NAK received / Mode not supported"

def set_dial_lock():
    sendStr = preamble + preamble + radio_address + controller + set_lock_cmd + eom
    result = tx_rx(sendStr)
    return 

# we always need to set "DIGI" mode on the IC-7200 to ensure the internal USB soundcard is used as the
# modulation source.
def set_digi():
    
    sendStr = preamble + preamble + radio_address + controller + set_dig_cmd + eom
        
    result = tx_rx(sendStr)
    return 
            
# get current dial frequency - only used in the Server "Watchdog" function to detect
# a radio failure - if we can't get the frequency then the radio is not available.
def get_freq():
    # the string is simple enough....
    sendStr = preamble + preamble + radio_address + controller + get_freq_cmd + eom
    # call tx_rx() and get the reply
    result = tx_rx(sendStr)
    
    if not result:
        return "0"
    # we have an answer containing the frequency in BCD
    # run the frequency bytes through "a process" to return the frequency in kHz
    ##### refresher needed on how this works..... = jpg/may-2015
    if len(result) > 0:
        f = 0
    for k in [18, 19, 16, 17, 14, 15, 12, 13, 11, 10]:
        f = 10 * f + nib(result, k)
    freq = (float(f) / 1000)
    return "%.3f" % freq

# set new dial frequency - the frequency supplied in kHz is 1.7kHz below the nominal 
# DSC centre frequency
def set_freq(freq):
    # make a ten-digit number, with leading, zeros from the freq, in Hz
    fdig = "%010d" % int(freq * 1000)
    # convert the freq. in Hz to the necessary BCD byte value
    ##### refresher needed on how this works..... = jpg/may-2015 
    bcd = ()
    for i in (8, 6, 4, 2, 0):
        bcd += freq_bcd(int(fdig[i]), int(fdig[i + 1]))
    set_freq_val = ""
    for byte in bcd:
        set_freq_val += chr(byte)
    # Send the command
    sendStr = preamble + preamble + radio_address + controller + set_freq_cmd + set_freq_val + eom
    result = tx_rx(sendStr)
    
    # check the response for the ack byte value
    if result[4] == ack:
        return "Set Freq success"
    elif result[4] == nak:
        return "NAK received / Freq not supported"
    
        
# helper function for "set_freq()" : convert from 10-digit decimal Hz to 
# a BDC byte
##### refresher needed on how this works..... = jpg/may-2015 
def freq_bcd(d1, d2):
    return (16 * d1 + d2),

# helper function for "get_freq()" : convert from a BCD byte to a frequency
##### refresher needed on how this works..... = jpg/may-2015 
def nib(s, i):
    k = ord(s[i / 2])
    if i % 2 == 0:
        k = k >> 4
    return k & 0xf 

# serial port send/receive function to talk to Icom Transceiver        
def tx_rx(sendStr):
    
    # use Threading Lock() to prevent access to the serial port while we're using it
    lock.acquire()
    
    # ser = instance of serial for the required port/speed
    # write our command string of CiV bytes
    ser.write(sendStr)
    
    # the radio replies by echoing our sent data so we need to read from the 
    # port to get the echo
    echo = ser.read(len(sendStr))
    
    # the echo and sendStr should be identical
    if len(echo) != len(sendStr): # an error....
        return "0"
    # 
    byte = "0"
    result = ""
    
    while byte != eom: 
        # wait for the EOM marker and loop through reading byte-by-byte from the
        # serial port again. This will be the reply to our requested action (once the echo
        # has been disposed of.
        byte = ser.read()
        
        # append each read byte to the result
        result += byte
        # this finishes when new byte = eom ("\xfd")
        
    # we're finished , release the threading lock    
    lock.release()
        
    # the result is a string of bytes. The calling function will deal with them...
    return result
    
# Turn Icom TX PTT on - the IC7200 has CiV controlled PTT which simplifies the PTT operation
# For Coast Station : we set mode to "usb" and set the radio to "digi" on each PTT_ON - to 
# ensure consistent operation, even if someone has changed settings manually on the radio
def ptt_on():

    set_dial_lock()
    set_mode("usb")
    set_digi()
    
    sendStr = preamble + preamble + radio_address + controller + tx_on + eom
    
    # send the command. The result is ignored....
    result = tx_rx(sendStr)
    
    return

# Turn Icom TX PTT off    
def ptt_off():
    
    sendStr = preamble + preamble + radio_address + controller + tx_off + eom
    
    result = tx_rx(sendStr)
    return
    
    
