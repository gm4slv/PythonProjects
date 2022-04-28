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
    command1 = "aplay -q /home/gm4slv/status1.wav"
    command2 = "aplay -q /home/gm4slv/status2.wav"
    command3 = "aplay -q /home/gm4slv/status3.wav"
    command4 = "aplay -q /home/gm4slv/status4.wav"
    os.system(command1)
    time.sleep(0.3)
    os.system(command2)
    time.sleep(0.3)
    os.system(command3)
    time.sleep(0.3)
    os.system(command4)
    return



