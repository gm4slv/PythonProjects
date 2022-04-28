# Import the GPIO and time libraries
import RPi.GPIO as GPIO
import time
import json
import speak
import ann



GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings(False)

PTT = 7
MUTE = 22

GPIO.setup(PTT,GPIO.OUT)
GPIO.setup(MUTE,GPIO.OUT)

#GPIO.output(PTT,False)

#def ident():
#    #print GPIO.input(PTT)
#    while GPIO.input(PTT) == 1:
#        print "id_tx waiting"
#        time.sleep(0.2)    
#    cw_id()
#    return

def cw_id():
    try:
        try:
            save = open('/home/gm4slv/status_dict.json')
            status_dict = json.load(save)
        except:
            status_dict = {}

        mode = status_dict["mode"]
        #mode = ": ".join(status_dict["mode"])
        #if mode == "U S B":
        #    mode = "Upper"
        #elif mode == "L S B":
        #    mode = "Lower"
        
        freq = status_dict["freq"]

        #ann_freq = ": ".join(status_dict["freq"])
        tt = status_dict["tt"]
        #if tt == "ON":
        #    tt = "Enabled"
        #elif tt == "OFF":
        #    tt = "Disabled"
        #ann_freq = ann_freq.replace('.','decimal')
        #hour = time.strftime("%H:%M", time.gmtime(time.time()))
        #minute = time.strftime("%M", time.gmtime(time.time()))
        timenow = time.strftime("%H%M", time.gmtime(time.time()))
        
        ID = "DE GM4SLV %s UTC %s %s %s" % (timenow,freq, mode, tt)
        
        if tt != "ON":
        
            #speak.speak1("This is Golf Mike Four. Sierra. Leema. Victor. Experimental H F cross gate.")
            #speak.speak2("The time is %s UTC" % (hour))
            #speak.speak3("%s: %s." % (ann_freq,mode))
            #speak.speak4("Cross patch: is %s " % ( tt))
 
            while GPIO.input(PTT) == 1:
                time.sleep(0.5)
                #print "Waiting..."
        
            GPIO.output(MUTE,True)
            GPIO.output(PTT,True)
            time.sleep(1)
            ann.cw_play(ID)
        
            #speak.tx_status() 
            #time.sleep(1)
        
            GPIO.output(MUTE,False)
            time.sleep(5)
            GPIO.output(PTT,False)
        else:
            while GPIO.input(PTT) == 1:
                time.sleep(0.5)
                #print "Waiting..."
            GPIO.output(PTT,True)
            ann.cw_play(ID)
            GPIO.output(PTT,False)


    except KeyboardInterrupt:
        GPIO.cleanup()
    return("Success")

#GPIO.cleanup()

