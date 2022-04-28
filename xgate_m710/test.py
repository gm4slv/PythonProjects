# Import the GPIO and time libraries
import RPi.GPIO as GPIO
import time


GPIO.setmode (GPIO.BOARD)

GPIO.setwarnings(False)

MUTE = 22
PTT = 7
TT = 11
CWID = 13

GPIO.setup(MUTE,GPIO.OUT)
GPIO.setup(CWID,GPIO.OUT)
GPIO.setup(PTT,GPIO.OUT)
GPIO.setup(TT,GPIO.OUT)

def ptt():
    if GPIO.input(PTT) != 1:
        GPIO.output(PTT,True)
    else:
        GPIO.output(PTT,False)
    return

def tt():
    if GPIO.input(TT) != 1:
        GPIO.output(TT,True)
    else:
        GPIO.output(TT,False)
    return

def tone():
    if GPIO.input(CWID) != 1:
        GPIO.output(CWID,True)
    else:
        GPIO.output(CWID,False)
    return

def mute():
    if GPIO.input(MUTE) != 1:
        GPIO.output(MUTE,True)
    else:
        GPIO.output(MUTE,False)
    return


def show_pins():
    print ""
    print "======================"
    print "PTT  p : ", GPIO.input(PTT)
    print "TT   t : ", GPIO.input(TT)
    print "CW   c : ", GPIO.input(CWID)
    print "Mute m : ", GPIO.input(MUTE)
    print "======================"
    print ""
    return


show_pins()

GPIO.output(PTT,False)


while True:
 

    command = raw_input("Enter command  > ")
    #print command

    if command == "p":
        ptt()
        show_pins()
    elif command == "t":
        tt()
        show_pins()
    elif command == "c":
        tone()
        show_pins()
    elif command == "m":
        mute()
        show_pins()
    elif command == "q":
        #GPIO.cleanup()
        quit()
    else:
        show_pins()


