import os
import time

def speak1(text):
    command = "flite -voice awb -t \"" + text + "\" -o /home/gm4slv/status1.wav"
    os.system(command)
    return


def speak2(text):
    command = "flite -voice awb -t \"" + text + "\" -o /home/gm4slv/status2.wav"
    os.system(command)
    return

def speak3(text):

    command = "flite -voice awb -t \"" + text + "\" -o /home/gm4slv/status3.wav"
    os.system(command)
    return


def speak4(text):
    command = "flite -voice awb -t \"" + text + "\" -o /home/gm4slv/status4.wav"
    os.system(command)
    return

def tx_status():
    command1 = "play -q -v 3  /home/gm4slv/status1.wav  > /dev/null 2>&1"
    command2 = "play -q -v 3  /home/gm4slv/status2.wav > /dev/null 2>&1"
    command3 = "play -q  -v 3 /home/gm4slv/status3.wav > /dev/null 2>&1"
    command4 = "play -q  -v 3  /home/gm4slv/status4.wav > /dev/null 2>&1"
    os.system(command1)
    time.sleep(0.3)
    os.system(command2)
    time.sleep(0.3)
    os.system(command3)
    time.sleep(0.3)
    os.system(command4)
    return



