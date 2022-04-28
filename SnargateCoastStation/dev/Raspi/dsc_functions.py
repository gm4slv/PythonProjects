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

# DSC Symbol Generator / CpFSK Modulator
# Wire2waves Ltd
# For Snargate Coast Station project
# May 2015
#
# Support functions for DSC Server
# 
# For Coast Station use - the calling function is reply() which itself uses the various dictionaries here
# to generate a symbolic version of the DSC call to be generated, and calls build_call() with these
# symbol values.
#
# build_call() takes the symbolic representation of each the DSC message elements and returns the numerical symbols, including ECC
# and the repeated FMT and EOS symbols.
#  
# transmit_call() takes the dsc_call symbols and a "power" value (0-1) to set the peak amplitude of the 
# audio output. transmit_call() uses further functions to interleave the symbols, to convert to 10-bit
# words, in 1s and 0s and then to produce a string of 16-bit sample values representing the continual-phase frequency
# shift keyed signal for sending via PyAudio to the soundcard.
#



version = "v1.0"

# Imports
import numpy
import pyaudio
import struct
import time
from math import *


# the maximum 16-bit number to be used for the audio sample amplitudes
w_amp = (2**15) - 1

# add a sample rate correction - at 9600 the rate is off, correcting by 0.9955 seems to
# produce better results.
sr_corr = 0.9955

# instance of PyAudio
p = pyaudio.PyAudio()

# convert text to DSC symbol value using dictionaries
# for Coast Station use we only use "SEL" / "SAF" / "TEST" / "NOINF" / "REQ"| "ACK" 
# other symbol values may be used in future (sort out mixed cases.....)
# in Coast Station these dictionaries are used in "reply()" to convert the text symbols into a 
# number between 0-126.
#
fmt_symbol_dict = { "area" : "102", "group" : "114", "all ships" : "116", "SEL" : "120", "sel" : "120"}
cat_symbol_dict = { "RTN" : "100" , "rtn" : "100", "SAF" : "108" , "saf" : "108", "urg" : "110", "dis" : "112" }
tc1_symbol_dict = { 
"f3e" : "100", 
"f3edup" : "101", 
"poll" : "102", 
"unable" : "104", 
"end" : "105", 
"data" : "106", 
"j3e" : "109", 
"fec" : "113", 
"arq" : "115", 
"test" : "118", 
"pos" : "121", 
"noinf" : "126",
"TEST" : "118"
}
tc2_symbol_dict = {
"no reason" : "100", 
"congestion" : "101", 
"busy" : "102", 
"queue" : "103", 
"barred" : "104", 
"no oper" : "105", 
"temp unav" : "106", 
"disabled" : "107", 
"unable channel" : "108", 
"unable mode" : "109", 
"conflict" : "110", 
"medical" : "111", 
"payphone" : "112", 
"fax" : "113", 
"NOINF" : "126"
}
eos_symbol_dict = { "REQ" : "117", "req" : "117", "ACK" : "122", "ack" : "122", "eos" : "127" }


# This is a list containing Phasing Symbols in DX/RX order. 
# elements [12] and [14] aren't used - the real DSC data is interleaved instead, but
# they are included to keep the list referencing simple

phasing_symbol = [ 125, 111, 125, 110, 125, 109, 125, 108, 125, 107, 125, 106, 125, 105, 125, 104 ]

# Instead of doing bit-twiddling to convert each symbol
# value to its 10-bit parity protected word, which involves padding to full 7-bits, counting zeros,
# reversing the bit order, shifting bits and "ORing" in the parity bits
# we just use a dictionary containing the conversion between symbol value and its 10-bit parity protected word
#
parity_table = { 
0 : "0000000111", 1 : "1000000110", 2 : "0100000110", 3 : "1100000101", 
4 : "0010000110", 5 : "1010000101", 6 : "0110000101", 7 : "1110000100",
8 : "0001000110", 9 : "1001000101", 10 : "0101000101", 11 : "1101000100", 
12 : "0011000101", 13 : "1011000100", 14 : "0111000100", 15 : "1111000011", 
16 : "0000100110", 17 : "1000100101", 18 : "0100100101", 19 : "1100100100", 
20 : "0010100101", 21 : "1010100100", 22 : "0110100100", 23 : "1110100011", 
24 : "0001100101", 25 : "1001100100", 26 : "0101100100", 27 : "1101100011", 
28 : "0011100100", 29 : "1011100011", 30 : "0111100011", 31 : "1111100010", 
32 : "0000010110", 33 : "1000010101", 34 : "0100010101", 35 : "1100010100", 
36 : "0010010101", 37 : "1010010100", 38 : "0110010100", 39 : "1110010011", 
40 : "0001010101", 41 : "1001010100", 42 : "0101010100", 43 : "1101010011", 
44 : "0011010100", 45 : "1011010011", 46 : "0111010011", 47 : "1111010010", 
48 : "0000110101", 49 : "1000110100", 50 : "0100110100", 51 : "1100110011", 
52 : "0010110100", 53 : "1010110011", 54 : "0110110011", 55 : "1110110010", 
56 : "0001110100", 57 : "1001110011", 58 : "0101110011", 59 : "1101110010", 
60 : "0011110011", 61 : "1011110010", 62 : "0111110010", 63 : "1111110001", 
64 : "0000001110", 65 : "1000001101", 66 : "0100001101", 67 : "1100001100", 
68 : "0010001101", 69 : "1010001100", 70 : "0110001100", 71 : "1110001011", 
72 : "0001001101", 73 : "1001001100", 74 : "0101001100", 75 : "1101001011", 
76 : "0011001100", 77 : "1011001011", 78 : "0111001011", 79 : "1111001010", 
80 : "0000101101", 81 : "1000101100", 82 : "0100101100", 83 : "1100101011", 
84 : "0010101100", 85 : "1010101011", 86 : "0110101011", 87 : "1110101010", 
88 : "0001101100", 89 : "1001101011", 90 : "0101101011", 91 : "1101101010", 
92 : "0011101011", 93 : "1011101010", 94 : "0111101010", 95 : "1111101001", 
96 : "0000011101", 97 : "1000011100", 98 : "0100011100", 99 : "1100011011", 
100 : "0010011100", 101 : "1010011011", 102 : "0110011011", 103 : "1110011010", 
104 : "0001011100", 105 : "1001011011", 106 : "0101011011", 107 : "1101011010", 
108 : "0011011011", 109 : "1011011010", 110 : "0111011010", 111 : "1111011001", 
112 : "0000111100", 113 : "1000111011", 114 : "0100111011", 115 : "1100111010", 
116 : "0010111011", 117 : "1010111010", 118 : "0110111010", 119 : "1110111001", 
120 : "0001111011", 121 : "1001111010", 122 : "0101111010", 123 : "1101111001", 
124 : "0011111010", 125 : "1011111001", 126 : "0111111001", 127 : "1111111000" 
}

#####################
# for Area Calls - we need a number representing the quadrant
# Not used in Coast Station at present
area_table = { "ne" : "0", "nw" : "1", "se" : "2", "sw" : "3" }


##############
#
# sine() and tune() are for single tone carrier to assist ATU tuning
# 

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)#

# Generate a carrier to allow Auto-ATU to re-tune when changing frequency
# generated at FSK centre frequency. Amplitude and length can be 
# determined by the requesting function
#
def tune_carrier(pwr, time):
    # open a stream for writing data to the soundcard
    tunestream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    frequency = 1700
    #length = 3
    length = time
    rate = 44100
    #rate = 9600 * sr_corr
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) * pwr
    #chunk = numpy.concatenate(chunks) * (w_amp * pwr)
    # write the data representing "time" seconds of carrier to the soundcard
    tunestream.write(chunk.astype(numpy.float32).tostring())
    # closed the stream after sending, so that it's possible to open another for the message.
    tunestream.stop_stream()
    tunestream.close()

# split a 9-digit MMSI into 5 2-digit symbols - add a trailing "0" to the fifth symbol
# resulting MMSI symbols are returned as a list.
def mmsi_symbol(mmsi):
    mmsi_list = [int(mmsi[i:i+2]) for i in range(0, len(mmsi), 2)]
    # replace the last symbol with a trailing 1
    mmsi_list[4] = (mmsi_list[4] * 10 + 0)
    return mmsi_list
#
# for AREA calls - create the necessary symbol
# Not needed for Coast Station at present.  
def area_symbol(area):
    area_list = [int(area[i:i+2]) for i in range(0, len(area), 2)]
    return area_list

# 
# generate the symbol coding a frequency for the message data where needed
# Not used in Coast Station at present    
def freq_symbol(dfreq):
    freq_list = [int(dfreq[i:i+2]) for i in range(0, len(dfreq), 2)] 
    return freq_list
    
# calculate the ECC by XORing the relevant message symbols
# we must loop through the MMSI and data symbol lists to 
# include each symbol in the overall calculation
def get_ecc(f_s, a_s, c_s, s_s, tc1_s, tc2_s, d_s, e_s):
    
    # if "All Ships", we ignore the a_mmsi word, it won't be transmitted, don't include it in the ECC
    # this is done be setting it to "0"
    if f_s != 116:
        a_ecc = 0
        # xor the 5 symbols of the TO mmsi together
        for i in a_s:
            a_ecc = int(i) ^ a_ecc
    else:
        a_ecc = 0
        
    s_ecc = 0
    # xor the 5 symbols of the FROM mmsi together
    for i in s_s:
        s_ecc = int(i) ^ s_ecc
    
    d_ecc = 0
    # xor the 6 symbols of the "data" section together
    for i in d_s:
        d_ecc = int(i) ^ d_ecc
    # the final ECC is done be XORing all the intermediate ECC values to the Format symbol and the EOS symbol.
    ecc = f_s ^ a_ecc ^ c_s ^ s_ecc ^ tc1_s ^ tc2_s ^ d_ecc ^ e_s
    return ecc

# build the basic DSC Call:
# "fmt fmt mmsi cat mmsi tc1 tc2 data eos ecc eos eos"
def make_dsc_call(f_s, a_s, c_s, s_s, tc1_s, tc2_s, d_s, eos_s, ecc_s):

    dsc_call = []
    # 
    # two copies of the FORMAT symbol
    dsc_call.append(f_s)
    dsc_call.append(f_s)
    
    # if "All Ships", we ignore the a_mmsi word
    # otherwise we add the 5 "TO" address symbols.
    if f_s != 116: 
        for i in a_s:
            dsc_call.append(i)
    
    # add the CATEGORY symbol
    dsc_call.append(c_s)

    # add the 5 "FROM" address symbols
    for i in s_s:
        dsc_call.append(i)
    
    # Telecommand 1 and Telecommand 2
    dsc_call.append(tc1_s)
    dsc_call.append(tc2_s)

    # the 6 DATA MESSSAGE symbols
    for i in d_s:
        dsc_call.append(i)
    
    # EOS + ECC + EOS + EOS
    dsc_call.append(eos_s)
    dsc_call.append(ecc_s)
    dsc_call.append(eos_s)
    dsc_call.append(eos_s)
    
    # a list containing the full symbols for the message, with duplication of
    # FORMAT and EOS
    return dsc_call

# interleave the dsc symbols with phasing symbols, and at the same time convert between symbol value and
# 10-bit parity word by looking in the parity_table dictionary.

def interleave(parity_table, phasing, dsc_list):
    
    symbol_count = len(dsc_list)
    
    dsc_dxrx = []
    for p in range(0,12):
        dsc_dxrx.append(parity_table[phasing[p]]) #dxrx......
    
    dsc_dxrx.append(parity_table[dsc_list[0]])  #dx
    dsc_dxrx.append(parity_table[phasing[13]])  #rx
    dsc_dxrx.append(parity_table[dsc_list[1]])  #dx
    dsc_dxrx.append(parity_table[phasing[15]])  #rx
    dsc_dxrx.append(parity_table[dsc_list[2]])  #dx
    
    for i in range(0,symbol_count-3):
        dsc_dxrx.append(parity_table[dsc_list[i]]) #rx
        dsc_dxrx.append(parity_table[dsc_list[i+3]]) #dx
        
    dsc_dxrx.append(parity_table[dsc_list[-3]]) #rx ecc
   
    return dsc_dxrx

    
# take the interleaved dxrx list (now as ones and noughts after conversion in the Parity Dictionary)
# add a 200-bit dotting period of alternating 1/0 at the beginning and then append each 1 or 0 from the interleaved 
# dsc_dxrx list. 

# return a string of ones & noughts representing the complete message

def make_bitstream(dsc_dxrx):
    dsc_bitstream= "10"  * 100 # dotting
    for i in dsc_dxrx:
        dsc_bitstream += i
    return dsc_bitstream

   
# take the ones and noughts, create CPFSK-modulated sample values, pack them into a list, 
# and convert to a string to feed PyAudio. 
# This routine is thanks to Bill Lionheart (billlionheart@gmail.com)
# Normal FSK would cause excessive bandwidth due to the abrupt phase changes
# at bit-boundaries due to there not being complete cycles of audio (mark or space)
# during a bit-period since the bit rate and frequency shifts not being simple
# ratios - eg 100Hz shift / 100 baud. DSC uses 170Hz shift and 100 baud. CPSK avoids abrupt
# jumps in amplitude / phase by gradually changing the waveform across the bit boundary.
#
def modulate(fmsg, fcarrier, f0, f1, fsample, baud, amp):
    
    if amp > 1.0:
       amp = 1.0
       
    dsc_amp =  (w_amp * amp)
    
    mlen = len(fmsg)

    mtime = mlen/baud  

    nsamp = int(round(fsample*mtime))

    deltat = 1.0/fsample

    ph=0
    
    y = [0] * nsamp
    
    for i in range(nsamp): # i = sample number
        thisbit = int(floor((i/float(nsamp))* mlen)) 
        
        # "thisbit" is the index number of the data bit being modulated,
        # the same data-bit is used for "the number of samples which occupy 1 bit period"
        
        if fmsg[thisbit]:
            f = f1 
        else:
            f = f0 
            
        # if this bit is a 1 > f = mark, else f = space
        
        ph +=  2*pi*(fcarrier + f)*deltat 
        
        # phase advances during sample period according the actual mark or space freq
        # when the bit changes between 1 and 0, the phase advance in deltat is small, and
        # continuity in phase is achieved. The signal then starts to advance
        # in phase according to the new frequency.
        
        # reset phase to zero every 360 degrees
        if ph> 2*pi: 
            ph = ph -2*pi
      
        y[i]=dsc_amp*(sin(ph)) # y is an 8-bit value
        # y[i] is the current sample's amplitude - the "sin of current accumulated phase"
    
    wave_list = []
    for v in y:
        vp = struct.pack('h',v)
        wave_list.append(vp)
    wavestring = ''.join(wave_list)
    
    return wavestring
   
 
    
# This is the starting point, called by the Main routine' reply() function with already symbolic versions of the 
# DSC message
def build_call(fmt_symbol, a_symbol, cat_symbol, s_symbol, tc1_symbol, tc2_symbol, data_symbol, eos_symbol):
    
    # calculate the ECC from the relevant message symbols
    ecc_symbol = get_ecc(fmt_symbol, a_symbol, cat_symbol, s_symbol, tc1_symbol, tc2_symbol, data_symbol, eos_symbol)
    
    # build the basic DSC message   
    dsc_call = make_dsc_call(fmt_symbol, a_symbol, cat_symbol, s_symbol, tc1_symbol, tc2_symbol, data_symbol, eos_symbol, ecc_symbol)
    
    return dsc_call

# interleave, make bitstream as a string, convert to list, for the CPFSK modulator function, calculate the samples
# and send them as a string to the soundcard....
def transmit_dsc(dsc_call, pwr):
    
    # interleave the message and phasing DX and RX symbols together, and also convert to 10-bit parity words
    dsc_dxrx = interleave(parity_table, phasing_symbol, dsc_call) 
     
    # create a string with the ones and noughts representing the full message
    dsc_bitstream = make_bitstream(dsc_dxrx)
    
    # convert the string into a list, to feed the CPFSK modulator
    bitstream_list = [int(dsc_bitstream[i:i+1]) for i in range(0, len(dsc_bitstream), 1)]
    
    
    # get a list of sample values from the CPFSK modulator
    #
    # args = (source of message_bits(a list), f-centre, space_dev, mark_dev, sample_rate, baud_rate, amplitude)
    # returns a string of 8-bit signed values to feed PyAudio   
    wave = modulate(bitstream_list, 1700, +85, -85, 9600 * sr_corr, 100.0, pwr)
    
    # open a PyAudio stream to send the calculated samples to the soundcard
    cpfsk_stream = p.open(format=pyaudio.paInt16, channels=1, rate=9600, output=1)
    # write the samples to the stream... audio is produced from the DEFAULT soundcard. (In future it would be
    # useful to select a sound card.
    cpfsk_stream.write(wave)
    
    # stop the stream and close it, ready for the next message. the Tune carrier opens another stream when necessary, and
    # they must both be closed after use.
    cpfsk_stream.stop_stream()
    cpfsk_stream.close()
    
    # return to the main program after completion of the outgoing DSC Call.
    return


           
