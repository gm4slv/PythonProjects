# Import the GPIO and time libraries
import RPi.GPIO as GPIO
import time
import json
#import ann
import cwid


GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings(False)

PTT = 7
MUTE = 22

GPIO.setup(PTT,GPIO.OUT)
GPIO.setup(MUTE,GPIO.OUT)


def cw_id():

    save = open('/home/gm4slv/status_dict.json')
    status_dict = json.load(save)

    mode = status_dict["mode"]
        
    freq = status_dict["freq"]

    tt = status_dict["tt"]
        
    ID = "DE GM4SLV %s %s %s" % (freq, mode, tt)
    ID2 = "DE GM4SLV %s %s" % (freq, mode)
    #print mode
    #print freq
    #print tt
    #print ID
    #print GPIO.input(PTT)

    if tt != "ON":
 
        #while GPIO.input(PTT) == 1:
        #    time.sleep(0.5)
        #    #print "Waiting..."
        
        #GPIO.output(MUTE,True)
        ##GPIO.output(PTT,True)
        #time.sleep(1)
        #cwid.cw_id(ID)
        
        #GPIO.output(PTT,True)
        #GPIO.output(MUTE,False)
        #time.sleep(5)
        #GPIO.output(PTT,False)
        return

    else:
        #while GPIO.input(PTT) == 1:
        #    time.sleep(0.5)
            #print "Waiting..."
        #GPIO.output(PTT,True)
        cwid.cw_noptt_id(ID2)
        #GPIO.output(PTT,False)
    
    return


