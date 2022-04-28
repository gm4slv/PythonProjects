# GM4SLV CW Keyboard
# July 2016
#
version = "0.1"


# Imports
import numpy
import pyaudio
from math import *
import os
import sys    
import termios
import tty
import threading

# words per minute
wpm = 25
# dot period
cwdit = 1.2 / wpm
# dash period
cwdah = cwdit * 3

frequency = 650 
rate = 9600

# the maximum 16-bit number to be used for the audio sample amplitudes
w_amp = (2**15) - 1


sr_corr = 1.0

# instance of PyAudio
p = pyaudio.PyAudio()

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
"Y" : "-.--",
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
" " : " ",
"/" : "-..-.",
"?" : "..--..",
"+" : ".-.-.",
"," : "--..--",
"=" : "-...-",
"." : ".-.-.-",
"-" : "-....-",
"<" : "...-.-",
">" : "-... -.-",
"(" : "-.--.",
")" : "-.--.-",
"\"": ".-..-.",
"#" : ".-...",
"~" : "...-."
}

msg_list = []

tx_list = []

def dash(pwr, cwstream, wpm):
    
    #freqiuency=650
    length=3* 1.2/wpm 
    #rate=9600
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) *  (w_amp * pwr)
    cwstream.write(chunk.astype(numpy.int16).tostring())    
    
    
    
def dot(pwr, cwstream, wpm):
    
    #frequency=650
    length=1.2/wpm
    #rate=9600
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) *  (w_amp * pwr)
    cwstream.write(chunk.astype(numpy.int16).tostring())  
    
    
def cspace(pwr, cwstream,wpm):
    
    #frequency=1600
    length=1.2/wpm
    #rate=9600
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) *  (w_amp * pwr)
    cwstream.write(chunk.astype(numpy.int16).tostring())     
    
def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)#
   
    
def lspace(pwr, cwstream, wpm):
    
    frequency=1600
    length=3*1.2/wpm
    rate=9600
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) *  (w_amp * pwr)
    cwstream.write(chunk.astype(numpy.int16).tostring())    
    
def wspace(pwr, cwstream,wpm):
    frequency=1600
    length=1.2/wpm * 7
    rate=9600
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) *  (w_amp * pwr)
    cwstream.write(chunk.astype(numpy.int16).tostring())  
    
def make_call(cw_table, call):
    morsetext = ""
    for i in call:
        #print callsign+"\r"
        try:
            morsetext += cw_table[i]
        except:
            moresetext = ""
        #callsign += "*"        
    return morsetext
        
def cwid():
    wpm = 25
    while True:
        pwr = 0.5
        try:
            char = msg_list.pop(0)
            if char == "{":
                wpm = wpm - 1
                tx_list.append(str(wpm))
            elif char == "}":
                wpm = wpm + 1
                tx_list.append(str(wpm))
                
            tx_list.append(char)
            #print tx_list 
            
        except:
            char = " "
            
            tx_list.append(".")
        #print char
        morsechar = make_call(cw_table, char)
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=9600, output=1)
        for i in morsechar:
            if i == "-":
                dash(pwr, stream,wpm)
                cspace(0, stream,wpm)
            elif i == ".":
                dot(pwr, stream,wpm)
                cspace(0, stream,wpm)
            elif i == " ":
                lspace(0,stream,wpm)
        lspace(0,stream, wpm)
        tx_chars = "".join(tx_list)
        os.system('clear')
        print tx_chars+"\r"
        stream.stop_stream()
        stream.close() 

def send():
    text = raw_input("text")
    cwid(text,0.5)
    return
    




def getchar():
   #Returns a single character from standard input
   #import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
      
   return ch
   

def fill_msg():
    while True:
        char = getchar().upper()
        if char == "$":
            os._exit(0)
        msg_list.append(char)
    
t1 = threading.Thread(target = fill_msg)
t1.setDaemon(True)
t1.start()
print "Speed = %d wpm. Press $ to quit" % wpm 
cwid()

