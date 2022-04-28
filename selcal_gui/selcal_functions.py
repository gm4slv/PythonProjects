# CCIR 493-4 Selcal Symbol Generator / CPFSK Modulator
# Wire2waves Ltd
# March 2015
# with CW ID for use on Amateur Radio bands

version = "v0.2"

# Imports
import numpy
import pyaudio
import struct
import time
from math import *

# quick and dirty CW Ident
# words per minute
wpm = 20
# dot period
cwdit = 1.2 / wpm
# dash period
cwdah = cwdit * 3

w_amp = (2**15) - 1

# define the output audio stream for the main data
p = pyaudio.PyAudio()
cpfsk_stream = p.open(format=pyaudio.paInt16, channels=1, rate=9600, output=1)

# make a second stream for the Tune carrier & cw ident
pt = pyaudio.PyAudio()
tunestream = pt.open(format=pyaudio.paInt16, channels=1, rate=9600, output=1)

pc = pyaudio.PyAudio()
cwstream = pc.open(format=pyaudio.paInt16, channels=1, rate=9600, output=1)

# convert text to symbol value using dictionaries
fmt_symbol_dict = { "sel" : "120", "bcn" : "123" }
cat_symbol_dict = { "rtn" : "100"}
eos_symbol_dict = { "req" : "117" }


# list containing Phasing Symbols in DX/RX order. 

phasing_symbol = [ "125", "109", "125", "108", "125", "107", "125", "106", "125", "105", "125", "104" ]

# Instead of doing bit-twiddling to convert each symbol
# value to its 10-bit parity protected word, which involves padding to full 7-bits, counting zeros,
# reversing the bit order, shifting bits and "ORing" in the parity bits
# we just use a dictionary containing the conversion between symbol value and its 10-bit parity protected word
#
parity_table = { 
"00" : "0000000111", "01" : "1000000110", "02" : "0100000110", "03" : "1100000101", 
"04" : "0010000110", "05" : "1010000101", "06" : "0110000101", "07" : "1110000100",
"08" : "0001000110", "09" : "1001000101", "10" : "0101000101", "11" : "1101000100", 
"12" : "0011000101", "13" : "1011000100", "14" : "0111000100", "15" : "1111000011", 
"16" : "0000100110", "17" : "1000100101", "18" : "0100100101", "19" : "1100100100", 
"20" : "0010100101", "21" : "1010100100", "22" : "0110100100", "23" : "1110100011", 
"24" : "0001100101", "25" : "1001100100", "26" : "0101100100", "27" : "1101100011", 
"28" : "0011100100", "29" : "1011100011", "30" : "0111100011", "31" : "1111100010", 
"32" : "0000010110", "33" : "1000010101", "34" : "0100010101", "35" : "1100010100", 
"36" : "0010010101", "37" : "1010010100", "38" : "0110010100", "39" : "1110010011", 
"40" : "0001010101", "41" : "1001010100", "42" : "0101010100", "43" : "1101010011", 
"44" : "0011010100", "45" : "1011010011", "46" : "0111010011", "47" : "1111010010", 
"48" : "0000110101", "49" : "1000110100", "50" : "0100110100", "51" : "1100110011", 
"52" : "0010110100", "53" : "1010110011", "54" : "0110110011", "55" : "1110110010", 
"56" : "0001110100", "57" : "1001110011", "58" : "0101110011", "59" : "1101110010", 
"60" : "0011110011", "61" : "1011110010", "62" : "0111110010", "63" : "1111110001", 
"64" : "0000001110", "65" : "1000001101", "66" : "0100001101", "67" : "1100001100", 
"68" : "0010001101", "69" : "1010001100", "70" : "0110001100", "71" : "1110001011", 
"72" : "0001001101", "73" : "1001001100", "74" : "0101001100", "75" : "1101001011", 
"76" : "0011001100", "77" : "1011001011", "78" : "0111001011", "79" : "1111001010", 
"80" : "0000101101", "81" : "1000101100", "82" : "0100101100", "83" : "1100101011", 
"84" : "0010101100", "85" : "1010101011", "86" : "0110101011", "87" : "1110101010", 
"88" : "0001101100", "89" : "1001101011", "90" : "0101101011", "91" : "1101101010", 
"92" : "0011101011", "93" : "1011101010", "94" : "0111101010", "95" : "1111101001", 
"96" : "0000011101", "97" : "1000011100", "98" : "0100011100", "99" : "1100011011", 
"100" : "0010011100", "101" : "1010011011", "102" : "0110011011", "103" : "1110011010", 
"104" : "0001011100", "105" : "1001011011", "106" : "0101011011", "107" : "1101011010", 
"108" : "0011011011", "109" : "1011011010", "110" : "0111011010", "111" : "1111011001", 
"112" : "0000111100", "113" : "1000111011", "114" : "0100111011", "115" : "1100111010", 
"116" : "0010111011", "117" : "1010111010", "118" : "0110111010", "119" : "1110111001", 
"120" : "0001111011", "121" : "1001111010", "122" : "0101111010", "123" : "1101111001", 
"124" : "0011111010", "125" : "1011111001", "126" : "0111111001", "127" : "1111111000" 
}

cw_table = {
"A" : ".-",
"B" : "-...",
"C" : "-.-.",
"D" : "-..",
"E" : ".",
"F" : "..-.",
"G" : "--.",
"H" : "....",
"I" : "..",
"J" : ".---",
"K" : "-.-",
"L" : ".-..",
"M" : "--",
"N" : "-.",
"O" : "---",
"P" : ".--.",
"Q" : "--.-",
"R" : ".-.",
"S" : "...",
"T" : "-",
"U" : "..-",
"V" : "...-",
"W" : ".--",
"X" : "-..-",
"Y" : "--.-",
"Z" : "--..",
"1" : ".----",
"2" : "..---",
"3" : "...--",
"4" : "....-",
"5" : ".....",
"6" : "-....",
"7" : "--...",
"8" : "---..",
"9" : "----.",
"0" : "-----",
" " : "",
"/" : "-..-.",
"?" : "..--..",
"+" : ".-.-."
}

#####################
# function definitions
#

##############
#  Tone generators (not used for data, but for Tune and CW signals)
#
# Setting the "cspace" and "lspace" amplitudes (pwr) to non-zero
# will produce FSK-style CW, as used in Beacons etc,

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)#
#
# Generate a carrier to allow Auto-ATU to re-tune when changing frequency
# reduced amplitude, 3 seconds 
#
def tune_carrier(pwr):
    frequency = 1785
    length = 3
    rate = 9600
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) * (w_amp * pwr)
    tunestream.write(chunk.astype(numpy.int16).tostring())

def dash(pwr):
    frequency=1900
    length=cwdah 
    rate=9600
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) *  (w_amp * pwr)
    cwstream.write(chunk.astype(numpy.int16).tostring())    
    
def dot(pwr):
    frequency=1900
    length=cwdit
    rate=9600
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) *  (w_amp * pwr)
    cwstream.write(chunk.astype(numpy.int16).tostring())  

def cspace(pwr):
    frequency=1700
    length=cwdit
    rate=9600 
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) *  (w_amp * pwr)
    cwstream.write(chunk.astype(numpy.int16).tostring())     

def lspace(pwr):
    frequency=1700
    length=cwdah
    rate=9600
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) *  (w_amp * pwr)
    cwstream.write(chunk.astype(numpy.int16).tostring())      
#
#   
################################

def make_call(cw_table, call):
    callsign = ""
    for i in call:
        callsign += cw_table[i]
        callsign += "s"        
    return callsign
        
def cwid(call, pwr):
    callsign = make_call(cw_table, call)
    for i in callsign:
        if i == "-":
            dash(pwr)
            cspace(pwr)
        elif i == ".":
            dot(pwr)
            cspace(pwr)
        elif i == "s":
            lspace(pwr)
            
###########


# split a 4 digit Selcal into two 2-digit symbols
# resulting symbols are returned as a list
def sel_id_symbol(sel_id):
    sel_id_list = [(sel_id[i:i+2]) for i in range(0, len(sel_id), 2)]    
    return sel_id_list


# build the basic Call:
# Selcal messages are of the form:  "fmt to_id cat self_id eos eos eos"

def build_call(f_s, a_s, c_s, s_s, eos_s):

    sel_call = []
    
    sel_call.append(f_s)
    
    for i in a_s:
        sel_call.append(i)
    
    sel_call.append(c_s)

    for i in s_s:
        sel_call.append(i)

    sel_call.append(eos_s)
    
    sel_call.append(eos_s)
    sel_call.append(eos_s)
    
    return sel_call

    
    
# interleave the symbols into DX and RX sequence 
# at the same time convert between symbol value and
# 10-bit parity word by looking in the parity_table dictionary.

def interleave(parity_table, phasing, sel_list):
    
    symbol_count = len(sel_list)
    
    sel_dxrx = []
    # interleave the phasing sequence
    for p in range(0,12):
        sel_dxrx.append(parity_table[phasing[p]]) #dxrx
    
    # add dx and rx copies of the format symbol
    sel_dxrx.append(parity_table[sel_list[0]]) #dx
    sel_dxrx.append(parity_table[sel_list[0]]) #rx
    
    # add the DX copy of the the to_ID
    sel_dxrx.append(parity_table[sel_list[1]]) #dx
    
    # add another RX copy of the format symbol
    sel_dxrx.append(parity_table[sel_list[0]]) #rx
    
    # add the DX copy of the category symbol
    sel_dxrx.append(parity_table[sel_list[2]]) #dx
    
    # loop through the remaining symbols to add the RX and DX versions 
    for i in range(0,symbol_count-3):
        sel_dxrx.append(parity_table[sel_list[i]]) #rx
        sel_dxrx.append(parity_table[sel_list[i+3]]) #dx
    
    # add a final DX and RX copy of the EOS symbol
    sel_dxrx.append(parity_table[sel_list[-1]])
    sel_dxrx.append(parity_table[sel_list[-1]])    
    
    # sel_dxrx is a list of 10-bit words, as ones and noughts, for the complete message
    return sel_dxrx

    
# Make a 600-bit dotting period of alternating 1/0 in a string

# Selcal dotting periods often 6 seconds (and up to 20 seconds in some
# instances) to allow for capturing scanning radios. 
# We send 300 bits / 6 seconds for now, pending a decision to extend or reduce the dotting period.

# Append to the string each 10-bit interleaved word, to create a string of 
# ones and noughts.

# return a string of ones & noughts representing the complete message

def make_bitstream(sel_dxrx):
    sel_bitstream= "10"  * 300 # dotting
    for i in sel_dxrx:
        sel_bitstream += i
    return sel_bitstream

    
    
# DSC and Selcall use tone spacing and baud rate that prevents the use of 
# "Sunde's FSK" method to create glitch-less bit transitions.
#
# To minimize bandwidth it's necessary to use "Continuous Phase FSK" which
# has a smooth transition of the waveform at the bit boundary. The method used is time-consuming
# as we have to create each audio sample based on the phase-advance of each bit-period and 
# store them in a buffer before sending them out to the soundcard via PyAudio.
# 
# This function is courtesy of Bill Lionheart : billlionheart@gmail.com
#
# Make the CPFSK-modulated sample values, pack them into a list, and convert to a string 
# to feed PyAudio  
#

def modulate(fmsg, fcarrier, f0, f1, fsample, baud, amp):
    
    if amp > 1.0:
       amp = 1.0
       
    sel_amp =  (w_amp * amp)
    
    mlen = len(fmsg)

    mtime = mlen/baud  

    nsamp = int(round(fsample*mtime))

    deltaT = 1.0/fsample

    ph=0
    
    y = [0] * nsamp
    
    for i in range(nsamp): # i = sample number
    
        thisbit = int(floor((i/float(nsamp))* mlen)) 
        
        # "thisbit" is the index number of the data-bit being modulated,
        # the same data-bit is used for "the number of samples which occupy 1 bit period"
        
        if fmsg[thisbit]:
            f = f1 
        else:
            f = f0 
            
        # if this bit is a 1 then f = mark-freq, else f = space-freq
        
        ph +=  2*pi*(fcarrier + f)*deltaT
        
        # phase advances during sample period according the actual mark or space freq
        # when the bit changes between 1 and 0, the phase advance in deltaT is small, and
        # continuity in phase is achieved. The signal then starts to advance
        # in phase according to the new frequency appropriate the the bit (one or nought)
        #being sent.
        
        # reset phase to zero every 360 degrees
        if ph> 2*pi: 
            ph = ph - 2*pi
      
        y[i]=sel_amp*(sin(ph)) # y is an 8-bit value
        # y[i] is the current sample's amplitude - the "sin of current accumulated phase"
    
    wave_list = []
    for v in y:
        vp = struct.pack('h',v)
        wave_list.append(vp)
    wavestring = ''.join(wave_list)
    
    return wavestring
   
 
# Take the message to be sent and
# 1) interleave
# 2) make bitstream as a string
# 3) convert to list, for the CPFSK modulator function, 
# 4) calculate the sample values using the "modulate()" function
# 5) write the string of sample values to pyaudio


def transmit_sel(sel_call, pwr):
    #
    # 1) interleave the message and phasing DX and RX symbols together, and also convert to 10-bit parity words
    sel_dxrx = interleave(parity_table, phasing_symbol, sel_call) 
   
    # 2) create a string with the ones and noughts representing the full message
    sel_bitstream = make_bitstream(sel_dxrx)
    
    # 3) convert the string into a list, to feed the CPFSK modulator
    bitstream_list = [int(sel_bitstream[i:i+1]) for i in range(0, len(sel_bitstream), 1)]
    
    # 4) get a list of sample values from the CPFSK modulator
    #
    # arguments for modulate() : (source of message_bits(a list), f-centre, space_dev, mark_dev, sample_rate, baud_rate, amplitude)
    # returns a string of 8-bit signed values to feed PyAudio
    
    wave = modulate(bitstream_list, 1785, -85, +85, 9600, 100.0, pwr)
    
    # 5) make some noise...
    
    cpfsk_stream.write(wave)
    
    return


           
