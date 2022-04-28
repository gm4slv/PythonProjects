"""
GM4SLV X-Gate controller

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
"""
###############################
#
# Reads 4 GPIO lines, controlled by DTMF decoder module in 
# the X-Gate and sends CiV commands to Icom radio to change
# frequency & mode as required.
# 

import RPi.GPIO as GPIO
import time
from memory import *
from icom import *
import atexit
import os


# Instance of an Icom Radio
# n1, a1, cal1 are defined in conf.py (imported into icom.py)
r1 = Icom(n1,a1,cal1)

# These define the QSY frequency hop when "Bit 4" is set
# On normal bands we jump a "few" SSB channels, on 60m we move 0.5kHz, perhaps
# to align with a non-standard dial freq. selection, but not moving out of
# the selected bandlet.
qsy_non60m = 3.5
qsy_60m = -0.5

# To prevent ATU Tune carriers each time we change freq. we keep
# track of the last freq. the ATU Tune function was called
# and then calculate the "percent change from last tuned"
# and only call tune() if we've moved > 1.5% of the last tuned
# frequency. This will give a retune if a significant jump
# on 160m, 80m or 60m but not within any other band. A jump between bands will
# always give a retune.
atu_last_tune = 30000.0

# Channels are set by reading 4 GPIO lines
# which represent a 3-bit number 0-7 (8 channels)
# and an additional bit for "QSY" within the selected channel
#
# The bits are set by setting the relevant
# DTMF controlled output 3/4/5/6 via UHF
# eg
# channel2 0010 = 3-off, 4-off, 5-on, 6-off
# channel6 0110 = 3-off, 4-on, 5-on, 6-off
# channel6 + QSY 1110 = 3-on, 4-on, 5-on, 6-off
#
# Channel frequency & mode is stored in memory.py
#
# bit_one = LSB in the 3-bit channel number (from DTMF "6")
#
# bit_four = "QSY a few kHz"
#
# this is to make visualising the bits easier looking at a row of 
# keys on a DTMF keyboard. For the first 8 channels (0-7) only row "4/5/6" is needed
# and to go to the next 8 (8-15) digit "3" is turned ON (3*)

bit_one_pin = 26
bit_two_pin = 19
bit_three_pin = 13
bit_four_pin = 6

# Setup the GPIO lines needed as INPUTS, with Pull-up to 
# allow for the DTMF board open-collector outputs to pull them
# down to set each bit are required
GPIO.setmode(GPIO.BCM)
GPIO.setup(bit_one_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(bit_two_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(bit_three_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(bit_four_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)



def cleanup():
    print "exiting..."
    print "Resetting frequency...%s, %s " % (r1.set_freq(start_freq), r1.get_freq())
    print "Resetting mode....%s, %s " % (r1.set_mode(start_mode), r1.get_mode())
    print "DSP NR Turn off... ", r1.dsp_nr_off()
    print "DSP ANF Turn off... ",r1.dsp_anf_off()
    print "Dial Lock Turn off...", r1.dial_lock_off()
    print "Backlight Turn on...", r1.backlight_on()
    GPIO.cleanup()

atexit.register(cleanup)

# read_pins() is called repeatedly to poll the GPIO lines and
# to convert the n-bits into a channel number (0-7)

def read_pins():
    channel = 0
    
    bit_one = GPIO.input(bit_one_pin)
    bit_two = GPIO.input(bit_two_pin)
    bit_three = GPIO.input(bit_three_pin)
    bit_four = GPIO.input(bit_four_pin)
    
    if not bit_one:
        channel += 1
    
    if not bit_two:
        channel += 2
    
    if not bit_three:
        channel += 4
    
    if not bit_four:
        qsy = True
    else:
        qsy = False

    return channel,qsy

# change_freq() is called when a channel change is required
# it calls the Icom set_freq() method with the required frequency 
# in kHz
def change_freq(freq):
    print "Setting HF Freq.... ", freq
    freq = float(freq)
    r1.set_freq(freq)
    return

# change_mode() is called when a channel change is required
# it calls the Icom set_mode() method with the required mode
def change_mode(mode):
    print "Setting HF mode.... ", mode
    r1.set_mode(mode)
    return

# Two variables used to keep track of the current freq & mode
# as we only want to force a change if either freq or mode
# are different when a new channel number is required

old_freq = "0"
old_mode = "0"

# #### THERE SEEMS TO BE A BUG ### 
# Occasionally on first running the serial write/read
# fails - only on the first write. The exception (unable to get the current freq/mode)
# is caught and we quit(). It seems that once we're up and running the serial comms 
# works fine.... 
try:
    old_freq = r1.get_freq()
    old_mode = r1.get_mode()
    start_freq = float(old_freq)
    start_mode = old_mode
    print "=" * 40
    print "Startup : Freq %s, Mode %s" % (old_freq, old_mode)
    print "=" * 40
    print ""
    print "Initializing HF Radio....."
    print "DSP NR Turn on...", r1.dsp_nr_on()
    print "DSP ANF Turn on...", r1.dsp_anf_on()
    print "Backlight Turn off...", r1.backlight_off()
    print "Dial Lock Turn on...", r1.dial_lock_on()
    print "Digi mode Turn off...", r1.digi_off()
    print "Speech Compression on....", r1.comp_on() 
    print "Setting Full Power...", r1.set_pwr(100)
    print r1.tune()
    atu_last_tune = float(start_freq)
    print "=" * 40
    print ""

except:
    print "Error startup!"
    os._exit(0)

# The Polling loop
# 1) Read the pins > channel number N
# 2) convert channel number into a variable "channelN" and retreive
# the freq & mode (each channel variable is a list ["freq", "mode"] )
# 3) check for a change in either freq or mode and call set_freq and set_mode if
# either are different from the current values, otherwise do nothing
# 4) update the curr_freq and curr_mode variables with the new values
# 5) sleep
# 6) repeat
try:

    while True:
        channel,qsy = read_pins()
        #print "channel# : ", channel
        memch = "channel" + str(channel)
        freq = eval(memch)[0]
        mode = eval(memch)[1]
        freqn = float(freq)
        if qsy:
            if freqn < 5250 or freqn > 5410:
                freq = format(freqn + qsy_non60m, '0.3f')
            else:
                freq = format(freqn + qsy_60m, '0.3f')

    
        #print "Channel %s : Freq %s, mode %s" % (channel, freq, mode)
        if freq != old_freq or mode != old_mode:
            print "*" * 40
            timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            print "%s : Channel : %d / QSY : %s " % (timenow, channel, qsy)
            #print "setting frequency to ", freq
            change_freq(freq)
            change_mode(mode)
            print "Last ATU Tune Freq : %0.3f" % atu_last_tune
            # do we retune ATU? More than 5% change since last ATU Tune = Yes
            delta = 100 * abs(float(atu_last_tune) - float(freq)) / atu_last_tune
            if delta  > 1.5:
                print "Large freq change : %0.3f percent " % delta
                print r1.tune()
                atu_last_tune = float(freq)
            else:
                print "Small freq change : %0.3f percent " % delta
        
            old_freq = freq
            old_mode = mode
        
            curr_freq = r1.get_freq()
            curr_mode = r1.get_mode()
            #curr_smeter = float(r1.get_smeter())
            print "*" * 40
            print "Retuned : Freq %s, Mode %s" % (curr_freq, curr_mode)
            print "*" * 40    
            print ""

        else:
            pass


        time.sleep(10)
except KeyboardInterrupt:
    
    print ""
    print "Goodbye...."
    print ""
    time.sleep(2)
    quit()

GPIO.cleanup()




