# Import the GPIO and time libraries
import RPi.GPIO as GPIO
import time
import json

#####Morse code ######
CODE = {' ': ' ',
        "'": '.----.',
        '(': '-.--.-',
        ')': '-.--.-',
        ',': '--..--',
        '-': '-....-',
        '.': '.-.',
        '/': '-..-.',
        '0': '---',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '-.',
        ':': '---...',
        ';': '-.-.-.',
        '?': '..--..',
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        
       'Y': '-.--',
        'Z': '--..',
        '_': '..--.-',
        '@' : '.-.-.'}
######End of morse code######

# Set the pin designation type.
GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings(False)

CWID = 22
PTT = 7

# Because GPIO pins can act as either digital inputs or outputs,
# we need to designate which way we want to use a given pin.
# This allows us to use functions in the GPIO library in order to properly send and receive signals.
GPIO.setup(CWID,GPIO.OUT)
GPIO.setup(PTT,GPIO.OUT)

WPM = 22

DOTPER =  1.2 /( WPM )


def dot():
        GPIO.output(CWID,True)
        time.sleep(DOTPER)

        GPIO.output(CWID,False)
        time.sleep(DOTPER)

def dash():
        GPIO.output(CWID,True)
        time.sleep(3 * DOTPER)
        GPIO.output(CWID,False)
        time.sleep(DOTPER)

def ident():
    # check if VHF PTT is already active?
    #print "in ident() with ",  GPIO.input(PTT)
    while GPIO.input(PTT) == 1:
        time.sleep(0.2)    
    cw_id()
    return

def cw_id():
    try:
        try:
            save = open('status_dict.json')
            status_dict = json.load(save)
        except:
            status_dict = {}

        mode = status_dict["mode"]
        freq = status_dict["freq"]
        tt = status_dict["tt"]

        timenow = time.strftime("%H%M", time.gmtime(time.time()))
        input = "DE GM4SLV %s UTC %s %s %s" % (timenow, freq, mode, tt)
        GPIO.output(PTT,True)
        time.sleep(1)
        for letter in input:
            for symbol in CODE[letter.upper()]:
                if symbol == '-':
                    dash()
                elif symbol == '.':
                    dot()
                else:
                    time.sleep(3 * DOTPER)
            time.sleep(3 * DOTPER)
        GPIO.output(PTT,False)


    except KeyboardInterrupt:
        GPIO.cleanup()

    return("Success")
