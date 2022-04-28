# Import the GPIO and time libraries
import RPi.GPIO as GPIO
import time

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
# In this case, we use BCM- the GPIO number- rather than the pin number itself.
GPIO.setmode (GPIO.BOARD)

# So that you don't need to manage non-descriptive numbers,
# set "CWID" to 4 so that our code can easily reference the correct pin.
CWID = 22
PTT = 7
TT = 11

# Because GPIO pins can act as either digital inputs or outputs,
# we need to designate which way we want to use a given pin.
# This allows us to use functions in the GPIO library in order to properly send and receive signals.
GPIO.setup(CWID,GPIO.OUT)
GPIO.setup(PTT,GPIO.OUT)
GPIO.setup(TT,GPIO.OUT)

WPM = 22

DOTPER =  1.2 /( WPM )

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

def ident(text):
    # check if VHF PTT is already active?
    if not GPIO.input(PTT):
        cw_id(text)
        return

def cw_id(text):
    
    while GPIO.input(PTT) == 1:
        time.sleep(0.2)

    try:
        #input = "GM4SLV"
        GPIO.output(PTT,True)
        time.sleep(1)
        for letter in text:
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
