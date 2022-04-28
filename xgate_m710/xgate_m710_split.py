#!/usr/bin/python


import time
import serial
import cwid
import id_tx_menu
import radio_functions_m710 as r1
import atexit
import sys
import json

from mem import *

ser = serial.Serial(
        port='/dev/xgate',
        baudrate = 4800,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

curr_mode = r1.get_mode()
curr_freq = str(r1.get_freq())

mode_dict = {"1" : "USB", "2" : "LSB", "3" : "AM"}



def cleanup():
    mute_on()
    cwid.cw_id("QRT")
    mute_off()
    
atexit.register(cleanup)

def read_command():

    byte = ""
    result = []
    count = 0

    while byte != "#":
       
        heartbeat = "Alive"
        
        byte = ser.read()
        
        heartbeat_file("%s : %s" % (heartbeat, byte))

        if byte != "":
            result.append(byte)
            count += 1
            if count  > 10:
                break

    command = ''.join(result[:-1])
    
    return(command)

def heartbeat_file(text):
    filename = '/home/gm4slv/heartbeat.txt'
    f = open(filename, 'a+')
    timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
    log = " ".join((timenow, text))
    #print log
    f.write(log+"\n")
    f.close()
    return

def write_file(text):
    filename = '/home/gm4slv/commandlog.txt'
    f = open(filename, 'a+')
    timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
    log = " ".join((timenow, text))
    print log
    f.write(log+"\n")
    f.close()
    return


def write_status(key,value):
    
    try:
        saved = open('/home/gm4slv/status_dict.json')
        status_dict = json.load(saved)
    except:
        status_dict = {}

    status_dict[key] = value

    with open('/home/gm4slv/status_dict.json', 'wb') as outfile:
        json.dump(status_dict, outfile)

    return

def setup_start_status():
    start_freq = r1.get_freq()
    write_status("freq",start_freq)
    
    talkthrough_off()
    write_status("tt","OFF")
    
    start_mode = r1.get_mode()
    write_status("mode", start_mode)
    
    pwr = r1.get_txpower()
    
    if pwr == "1":
        pwr = "15"
    elif pwr == "2":
        pwr = "50"
    elif pwr == "3":
        pwr = "100"
    
    write_status("txpwr",pwr)

    write_status("user","false")
    return

def talkthrough_on():
    global talkthrough
    talkthrough = "ON"
    write_file("Talkthrough ON")
    cwid.tt(True)
    return

def talkthrough_off():
    global talkthrough
    talkthrough = "OFF"
    write_file("Talkthrough OFF")
    cwid.tt(False)
    return

def qsy_up():
    global curr_freq
    mute_off()
    new_freq = float(curr_freq) + 0.5
    r1.set_freq(new_freq)
    curr_freq = str(new_freq)
    write_status("freq",curr_freq)
    write_file("QSY Up to %s" % curr_freq)
    return

def qsy_down():
    global curr_freq
    mute_off()
    new_freq = float(curr_freq) - 0.5
    r1.set_freq(new_freq)
    curr_freq = str(new_freq)
    write_status("freq",curr_freq)
    write_file("QSY Down to %s" % curr_freq)
    return

def set_frequency(freq):
    global curr_freq
    r1.set_freq(freq)
    curr_freq = str(freq)
    write_file("New Frequency %s" % curr_freq)
    return

def set_mode(mode):
    global curr_mode
    r1.set_mode(mode)
    curr_mode = mode
    write_file("New Mode %s" % curr_mode)
    return

def atu_tune():
    result = r1.atu_tune()
    write_file("ATU Tune.... %s" % result)
    return

def get_snumber():
    smeter1 = r1.get_smeter()
    time.sleep(0.5)
    smeter2 = r1.get_smeter()
    time.sleep(0.5)
    smeter3 = r1.get_smeter()
    time.sleep(0.5)
    smeter4 = r1.get_smeter()
    time.sleep(0.5)
    smeter5 = r1.get_smeter()
    
    smeter = max(smeter1,smeter2,smeter3,smeter4,smeter5)

    if float(smeter) < 5:
        smeter = float(smeter) * 2
    else:
        smeter = 9

    return(str( "%0.0f" % smeter))


def tx_pwr(pwr):
    result = r1.set_txpower(pwr)
    pwr = r1.get_txpower()
    
    if pwr == "1":
        pwr = "15"
    elif pwr == "2":
        pwr = "50"
    elif pwr == "3":
        pwr = "100"

    write_status("txpwr",pwr)
    write_file("TX Power set to %s" % pwr)
    return(pwr)

def peek(peektime):
    write_file("Peeking on HF for %d seconds...."  % peektime)
    mute_off()
    cwid.ptt(peektime)
    mute_on()
    return

def monitor(state):
    if state == "1":
        state = "ON"
    elif state == "0":
        state = "OFF"
    write_file("Monitoring HF "+state)
    write_status("monitor", state)    
    cwid.monitor(state)
    return

def mute_on():
    cwid.mute_on()
    return

def mute_off():
    cwid.mute_off()
    return

def get_status():
    saved = open('/home/gm4slv/status_dict.json')
    status_dict = json.load(saved)
    
    curr_freq = status_dict["freq"]
    curr_mode = status_dict["mode"]
    tt = status_dict["tt"]
    return(curr_freq, curr_mode, tt)

def play_status():
    saved = open('/home/gm4slv/status_dict.json')
    status_dict = json.load(saved)

    curr_freq = status_dict["freq"]
    curr_mode = status_dict["mode"]
    tt = status_dict["tt"]

    write_file("STATUS : Mode %s, Frequency %s, %s" % (curr_mode,curr_freq, tt))
    cwid.cw_id("%0.1f %s %s" % (float(curr_freq),curr_mode, tt))
    return

def xgate_quit():
    write_file("Got quit command")
    talkthrough_off()
    write_status("tt","QRT")
    sys.exit(0)


######## START HERE ###############################################################################################
#
#
#
#starttime = time.time()
starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))

write_status("xGate startup",starttime)
pin = "0"


write_file("X-Gate Start........................................")

r1.remote_on()

######################################
#

talkthrough_off()

tt_flag = 0

setup_start_status()

mute_on()

cwid.cw_id("QRV DE GM4SLV")

mute_off()

login_flag = 0

try:

    while True:
        
        print "heartbeat"

        if login_flag == 0:
            command_one = read_command()

        elif login_flag == 1:
            command_one = pin

        if command_one != pin:
            if command_one != "":
                write_file("Wrong PIN")
                time.sleep(1)
                mute_on()
                cwid.cw_id("?")
                mute_off()
            else:
                pass

        else:
            time.sleep(1)
            if login_flag !=1:
                write_file("User login")
                write_status("user","Login")    
                mute_on()
                cwid.cw_id("R")
                mute_off()
                status = get_status()
                talkthrough = status[2]

                if talkthrough == "ON":
                    talkthrough_off()
                    tt_flag = 1
                else:
                    tt_flag = 0
            login_flag = 1
            

            command_two = read_command()
            if command_two != "": 
                write_file("Command received : %s" % command_two)
            ###################################################
            #
            # COMMANDS:
            #
            # 1 : Frequency/Channel
            #   : 1fffff    = ffff.f kHz
            #   : 1xxxx     = channel xxxx (freq & mode combined)
            #
            # 2 : Mode 
            #   : 21    = USB
            #   : 22    = LSB
            #   : 23    = AM
            #
            # 4 : TX Power
            #   : 4xx   = xx Watts
            #
            # 5 : QSY Up 0.5kHz
            # 6 : QSY Down 0.5kHz
            #
            # 7 : HF Peek/Monitor
            #   : 7     = Peek 5 seconds
            #   : 7xx   = Peek xx seconds
            #   : 7*1   = Start Monitor HF
            #   : 7*0   = Stop Monitor HF
            #
            # 8 : ATU Tune
            #
            # 9 : Status
            #   : 9     = Status
            #   : 91    = S Meter
            #   : 93    = Full Status
            #
            # 0 : Talkthrough
            #   : 01    = Talkthrough ON
            #   : 02    = Talkthrough OFF

            try:
                if command_two == "":
                    pass
                
                elif command_two[:2] == "*1":
                    write_file("Frequency / Memory")
                    if len(command_two[2:]) == 4:
                        new_freq = float(mem_dict[command_two[2:]][0])
                        new_mode = mem_dict[command_two[2:]][1]
                        write_file("Memory Channel selected %s" % mem_dict[command_two[2:]])
                        set_frequency(new_freq)
                        set_mode(new_mode)
                        write_status("freq",str(new_freq))
                        write_status("mode",new_mode)
                    else:
                        new_freq = float(command_two[2:])/10
                        set_frequency(new_freq)
                        write_status("freq",str(new_freq))

                    
                    mute_on()
                    cwid.cw_id("e")
                    mute_off()

                elif command_two[:2] == "*2":
                    write_file("Mode")
                    new_mode = mode_dict[command_two[2]]
                    set_mode(new_mode)
                    write_status("mode",new_mode)
                    mute_on()
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*01":
                    write_file("Talkthrough On")
                    tt_flag = 1
                    write_status("tt","ON")
                    mute_on()
                    cwid.cw_id("TT ON %s %s" % (curr_freq, curr_mode))
                    cwid.cw_id("e")
                    mute_off()
                
                elif command_two == "*01*":
                    write_file("Force TT ON during login session")
                    talkthrough_on()
                    tt_flag = 1
                    write_status("tt","ON")
                    mute_on()
                    cwid.cw_id("TT ON %s %s" % (curr_freq, curr_mode))
                    cwid.cw_id("e")
                    mute_off()
        
                elif command_two == "*00":
                    write_file("Talkthrough Off")
                    talkthrough_off()
                    tt_flag = 0
                    write_status("tt","OFF")
                    mute_on()
                    cwid.cw_id("TT OFF")
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*5":
                    write_file("QSY down")
                    qsy_down()
                    time.sleep(1)
                    cwid.cw_id("i")
                
                elif command_two == "*6":
                    write_file("QSY up")
                    qsy_up()
                    time.sleep(1)
                    cwid.cw_id("i")
                    
                elif command_two == "*9":
                    write_file("Play status")
                    mute_on()
                    play_status()
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*8":
                    write_file("ATU Tune")
                    mute_on()
                    cwid.cw_id( "@")
                    atu_tune()
                    cwid.cw_id("e")
                    mute_off()

                elif command_two[:2] == "*7":
                    
                    if len(command_two) > 2:

                        if command_two[2] == "*":
                            write_file("Monitor...")
                            monitor_state = command_two[3]
                            monitor(monitor_state)

                        elif len(command_two) > 2:
                            write_file("Peek...")
                            peektime = int(command_two[2:])
                            mute_on()
                        
                            cwid.cw_id("i")
                            peek(peektime)
                            cwid.cw_id("e")
                            mute_off()
                    
                    else: 
                        write_file("Peek...")
                        peektime = 5
                    
                        mute_on()
                        cwid.cw_id("i")
                        peek(peektime)
                        cwid.cw_id("e")
                        mute_off()

                elif command_two[:2] == "*4":
                    write_file("TX Power")

                    new_pwr = command_two[2:]
                    power = tx_pwr(new_pwr)
                    mute_on()
                    cwid.cw_id("%sW" % power)
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*91":
                    write_file("S Meter")
                    s_no = get_snumber()
                    cwid.cw_id(s_no)
                    write_file("S-meter S%s" % s_no)
                
                elif command_two == "*93":
                    write_file("Send Ident")
                    mute_on()
                    id_tx_menu.cw_id()
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*99*":
                    write_file("Logout")
                    login_flag = 0
                    mute_on()
                    cwid.cw_id("+")
                    if tt_flag == 1:
                        write_file("... enabling TT")
                        talkthrough_on()
                        tt_flag = 0
                    mute_off()
                    write_status("mode",curr_mode)
                    write_status("freq", curr_freq)
                    write_status("tt", talkthrough)
                    write_status("user","Logout")
                    write_file("Logout :  %s %s %s" % (curr_freq, curr_mode, talkthrough))

                elif command_two == "*9999*":
                    write_file("Shutdown")
                    xgate_quit()

                else:
                    write_file("Command %s not understood" % command_two )
                    mute_on()
                    cwid.cw_id("?")
                    mute_off()

            except Exception as ex:
                write_file("Exception in command_two : %s" % command_two)
                mute_on()
                cwid.cw_id("?")
                mute_off()


except KeyboardInterrupt:
    
    write_file("Program killed by keyboard interrupt.......................")
    
    xgate_quit()

