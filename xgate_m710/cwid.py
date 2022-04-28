import RPi.GPIO as GPIO
import time

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
        '+' : '.-.-.',
        '%' : '...-.-',
        '@' : '.-...'
        
        }
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

WPM = 22

DOTPER =  1.2 /( WPM )

def cleanup():
    GPIO.cleanup()
    return

def ptt(peek):
    while GPIO.input(PTT) == 1:
        #time.sleep(0.2)
        return
    GPIO.output(PTT,True)
    time.sleep(peek)
    GPIO.output(PTT,False)
    return

def monitor(onoff):
    if onoff == "ON":
        GPIO.output(PTT,True)
        GPIO.output(MUTE,False)
        cw_noptt_id("e")
    elif onoff == "OFF":
        cw_noptt_id("e")
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


def cw_noptt_id(text):
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


def cw_id(text):
    
    if GPIO.input(PTT) == 1:
        cw_noptt_id(text)
    else:
    #while GPIO.input(PTT) == 1:
    #    return
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

    return
