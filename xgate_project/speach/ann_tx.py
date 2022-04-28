import RPi.GPIO as GPIO
import time
import ann

GPIO.setmode (GPIO.BOARD)

PTT = 7
TT = 11
MUTE = 22

GPIO.setwarnings(False)

GPIO.setup(PTT,GPIO.OUT)
GPIO.setup(TT,GPIO.OUT)
GPIO.setup(MUTE,GPIO.OUT)

def cleanup():
    GPIO.cleanup()
    return

def ptt(peek):
    GPIO.output(PTT,True)
    time.sleep(peek)
    GPIO.output(PTT,False)
    return

def tt(tt):
    GPIO.output(TT,tt)
    return

def mute_on():
    GPIO.output(MUTE,True)
    return

def mute_off():
    GPIO.output(MUTE,False)
    return

def speak(text):
    #make wav
    ann.speak(text)
    while GPIO.input(PTT) == 1:
        time.sleep(0.2)
        print "ann_tx Waiting"
    
    GPIO.output(PTT,True)
    time.sleep(1)
    ann.tx_command()
    GPIO.output(PTT,False)
    return

def speak_status(freq,mode,tt):
    #make wav
    ann.speakf(freq)
    ann.speakm(mode)
    ann.speakt(tt)
    while GPIO.input(PTT) == 1:
        time.sleep(0.2)
        print "ann_tx Waiting"
    
    GPIO.output(PTT,True)
    time.sleep(1)
    ann.tx_status()
    GPIO.output(PTT,False)
    return


def ident(text):
    
    while GPIO.input(PTT) == 1:
        time.sleep(0.2)
        print "ann_tx Waiting"

    try:
        #GPIO.output(MUTE,True)
        GPIO.output(PTT,True)
        #time.sleep(1)

        ann.cw_play(text)        
        
        #GPIO.output(MUTE,False)
        GPIO.output(PTT,False)


    except KeyboardInterrupt:
        GPIO.cleanup()

    return("Success")
