import os
import time

def speak(text):
    command = "flite -voice awb -t \"" + text + "\" -o status.wav"
    os.system(command)
    return

def speakf(text):
    command = "flite -voice awb -t \"" + text + "\" -o statusf.wav"
    os.system(command)
    return

def speakm(text):
    command = "flite -voice awb -t \"" + text + "\" -o statusm.wav"
    os.system(command)
    return

def speakt(text):
    text = "Cross Gate is: %s" % (text)
    command = "flite -voice awb -t \"" + text + "\" -o statust.wav"
    os.system(command)
    return

def tx_command():
    command = "play -q -v 3 status.wav > /dev/null 2>&1"
    os.system(command)
    return

def tx_status():
    command = "play -q -v 3 statusf.wav > /dev/null 2>&1 "
    os.system(command)
    time.sleep(0.5)
    command = "play -q -v 3 statusm.wav > /dev/null 2>&1 "
    os.system(command)
    time.sleep(0.5)
    command = "play -q -v 3 statust.wav > /dev/null 2>&1 "
    os.system(command)

    return

def cw_play(text):
    if text == "?":
        text = "?k"
    text = text.replace('.','r')
    #text = text.replace('0','o')
    #text = text.replace('9','n')
    command1 = "echo \""+text+"\" | /usr/local/bin/cwwav -f 900 -w 22 -o /home/gm4slv/file.wav > /dev/null 2>&1"
    os.system(command1)
    command2 = "play -q /home/gm4slv/file.wav vol 0.35 > /dev/null 2>&1"
    os.system(command2)
    return

