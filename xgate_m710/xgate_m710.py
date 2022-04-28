import time
import serial
import cwid
import id_tx_menu
import radio_functions_m710 as r1
#from icom import *
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

#r1 = Icom(n1, a1, cal1)

curr_mode = r1.get_mode()
curr_freq = str(r1.get_freq())

mode_dict = {"1" : "USB", "2" : "LSB", "3" : "AM"}


#mem_dict = {
#        "0301" : ["3773.0", "LSB"],
#        "0302" : ["3760.0", "LSB"],
#        "0303" : ["3615.0", "AM"],
#        
#        "0501" : ["5276.0","USB"], 
#        "0502" : ["5279.0","USB"], 
#        "0503" : ["5298.0","USB"],
#        "0504" : ["5301.0","USB"], 
#        "0505" : ["5304.0","USB"], 
#        "0506" : ["5317.0","AM"],
#        "0507" : ["5320.0", "USB"], 
#        "0508" : ["5333.0", "USB"], 
#        "0509" : ["5354.0", "USB"],
#        "0510" : ["5363.0", "USB"],
#        "0511" : ["5366.5", "USB"],
#        "0512" : ["5371.5", "USB"],
#        "0513" : ["5378.0", "USB"],
#        "0514" : ["5395.0", "USB"],
#        "0515" : ["5398.5", "USB"],
 #       "0516" : ["5403.5", "USB"],
 #       
 #       "0591" : ["5450.0", "USB"],
 #       "0592" : ["5505.0", "USB"],
 #       "0593" : ["10051.0", "USB"],
 #    
 ##       "0701" : ["7160.0", "LSB"],
        
 ##       }

def cleanup():
    mute_on()
    cwid.cw_id("QRT")
    mute_off()
    #ann_tx.cleanup()
    
atexit.register(cleanup)

def read_command():

    byte = ""
    result = []
    count = 0

    while byte != "#":
        byte = ser.read()
        if byte != "":
            result.append(byte)
            count += 1
            if count  > 10:
                break

    command = ''.join(result[:-1])
    
    return(command)

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
    
    timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
    status_dict["last action"] = timenow
    #if mode != "nil":
    #    status_dict["mode"] = mode
    #if freq != "nil":
    #    status_dict["freq"] = freq
    #if tt != "nil":
    #    status_dict["tt"] = tt

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

    #nr_off()
    #write_status("nr","off")

    #anf_off()
    #write_status("anf","off")

    #bandwidth_normal()
    #write_status("bandwidth","normal")

    #agc_fast()
    #write_status("agc","fast")

    #pre_off()
    #write_status("preamp","off")

    #att_off()
    #write_status("att","off")

    #comp_on()
    #write_status("comp", "on")
    
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
    print "in set_frequency() with ", freq
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

def nb_on():
    result = r1.nb_on()
    write_status("nb","on")
    write_file("Noise Blanker ON")
    return

def nb_off():
    result = r1.nb_off()
    write_status("nb","off")
    write_file("Noise Blanker OFF")
    return

#def anf_on():
#    result = r1.dsp_anf_on()
#    write_status("anf","on")
#    write_file("Auto Notch Filter ON")
#    return

#def anf_off():
#    result = r1.dsp_anf_off()
#    write_status("anf","off")
#    write_file("Auto Notch Filter OFF")
#    return

def get_snumber():
    smeter1 = r1.get_smeter()
    time.sleep(0.2)
    smeter2 = r1.get_smeter()
    time.sleep(0.2)
    smeter3 = r1.get_smeter()
    time.sleep(0.2)
    smeter4 = r1.get_smeter()
    time.sleep(0.2)
    smeter5 = r1.get_smeter()
    
    smeter = max(smeter1,smeter2,smeter3,smeter4,smeter5)


    #if smeter > -73:
    #    s_no = "S9"
    #elif smeter > -79:
    #    s_no = "S8"
    #elif smeter > -85:
    #    s_no = "S7"
    #elif smeter > -91:
    #    s_no = "S6"
    #elif smeter > -97:
    #    s_no = "S5"
    #elif smeter > -103:
    #    s_no = "S4"
    #elif smeter > -109:
    #    s_no = "S3"
    #elif smeter > -115:
    #    s_no = "S2"
    #elif smeter > -121:
    #    s_no = "S1"
    #else:
    #    s_no = "S0"
    #write_file("S Meter : %s" % s_no)
    
    return(smeter)


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

#def bandwidth_wide():
#    result = r1.bandwidth_wide()
#    write_status("bandwidth","wide")
#    write_file("IF Filter : WIDE")
#    return

#def bandwidth_normal():
#    result = r1.bandwidth_normal()
#    write_status("bandwidth","normal")
#    write_file("IF Filter : NORMAL")
#    return

#def bandwidth_narrow():
#    result = r1.bandwidth_narrow()
#    write_status("bandwidth","narrow")
#    write_file("IF Filter : NARROW")
#    return

#def comp_on():
#    result = r1.comp_on()
#    mute_on()
#    cwid.cw_id("ON")
#    mute_off()
#    write_status("comp","on")
#    write_file("TX Compression ON")
#    return

#def comp_off():
#    result = r1.comp_off()
#    mute_on()
#    cwid.cw_id("OFF")
#    mute_off()
#    write_status("comp","off")
#    write_file("TX Compression OFF")
#    return
#
def agc_on():
    result = r1.agc_on()
    write_status("agc","on")
    write_file("AGC : On")
    return

#def agc_slow():
#    result = r1.agc_slow()
#    write_status("agc","slow")
#    write_file("AGC : Slow")
#    return

def agc_off():
    result = r1.agc_off()
    write_status("agc","off")
    write_file("AGC : Off")
    return

#def pre_on():
#    result = r1.pre_on()
#    write_status("preamp","on")
#    write_file("Preamp : On")
#    return

#def pre_off():
#    result = r1.pre_off()
#    write_status("preamp","off")
#    write_file("Preamp : Off")
#    return

#def att_on():
#    result = r1.att_on()
#    write_status("att","on")
#    write_file("ATT : On")
#    return

#def att_off():
#    result = r1.att_off()
#    write_status("att","off")
#    write_file("ATT : Off")
#    return

def peek(peektime):
    write_file("Peeking on HF for %d ...."  % peektime)
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

#def comp(state):
#    if state == "1":
#        comp_on()
#    elif state == "0":
#        comp_off()
#    return

def mute_on():
    #write_file("Mute ON")
    cwid.mute_on()
    return

def mute_off():
    #write_file("Mute OFF")
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
    print "in status()" 
    saved = open('/home/gm4slv/status_dict.json')
    status_dict = json.load(saved)
    #print status_dict

    curr_freq = status_dict["freq"]
    curr_mode = status_dict["mode"]
    tt = status_dict["tt"]

    #freq = ": ".join(curr_freq)
    #freq = freq.replace('.',' decimal ')
    #mode = ": ".join(curr_mode)
    

    write_file("STATUS : Mode %s, Frequency %s, %s" % (curr_mode,curr_freq, tt))
    cwid.cw_id("%0.1f %s %s" % (float(curr_freq),curr_mode, tt))
    return

def menu():
    print "Commands are : "
    print "*1 Freq/Channel"
    print "*2 Mode"
    print "*3 RX Functions"
    print "*4 TX Power"
    print "*7 Peeki/Monitor"
    print "*8 ATU Tune"
    print "*9 Status"
    print "*99* Logout"
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

pin = "0"

write_file("X-Gate Start........................................")


#################### set up IC-7200 ##############
#

#r1.digi_off()

#r1.mod_a()

#r1.comp_off()

#r1.vfo_mode()

#r1.dial_lock_on()

#r1.nb_on()

r1.remote_on()

######################################
#

talkthrough_off()

tt_flag = 0

#write_status("mode",curr_mode)
#write_status("freq", curr_freq)
#write_status("tt", talkthrough)

setup_start_status()

mute_on()

cwid.cw_id("QRV DE GM4SLV")

#id_tx.cw_id()

#play_status()

mute_off()

login_flag = 0

#write_status(curr_mode, curr_freq, talkthrough)

try:

    while True:
   
        if login_flag == 0:
            command_one = read_command()
            #print command_one

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
                #print status[2]
                talkthrough = status[2]

                if talkthrough == "ON":
                    talkthrough_off()
                    tt_flag = 1
                else:
                    tt_flag = 0
            #print tt_flag
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
            # 3 : RX Settings
            #   : 310   = NB OFF
            #   : 311   = NB ON
            #   : 320   = AGC OFF
            #   : 321   = AGC ON
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
            #   : #92   = Menu
            #   : 93    = Full Status
            #
            # 0 : Talkthrough
            #   : 01    = Talkthrough ON
            #   : 02    = Talkthrough OFF

            try:
                if command_two == "":
                    pass
                
                elif command_two[:2] == "*1":
                    if len(command_two[2:]) == 4:
                        new_freq = float(mem_dict[command_two[2:]][0])
                        new_mode = mem_dict[command_two[2:]][1]
                        write_file("Memory Channel selected")
                        set_frequency(new_freq)
                        set_mode(new_mode)
                    else:
                        new_freq = float(command_two[2:])/10
                        print "going to set_frequency() with ",new_freq
                        set_frequency(new_freq)
                    #freq = ": ".join(curr_freq)
                    #freq = freq.replace('.','decimal')
                    #mode = ": ".join(curr_mode)

                    write_status("freq",str(new_freq))
                    
                    mute_on()
                    cwid.cw_id("i")
                    mute_off()
                    peek(3)
                    mute_on()
                    #cwid.cw_id("%s" % new_freq)
                    cwid.cw_id("e")
                    mute_off()

                elif command_two[:2] == "*2":
                    new_mode = mode_dict[command_two[2]]
                    set_mode(new_mode)
                    freq = ": ".join(curr_freq)
                    freq = freq.replace('.','decimal')
                    mode = ": ".join(curr_mode)
                    write_status("mode",new_mode)
                    mute_on()
                    cwid.cw_id("i")
                    mute_off()
                    peek(3)
                    mute_on()
                    #cwid.cw_id("%s" % new_mode)
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*01":
                    tt_flag = 1
                    freq = ": ".join(curr_freq)
                    freq = freq.replace('.','decimal')
                    mode = ": ".join(curr_mode)
                    write_status("tt","ON")
                    mute_on()
                    cwid.cw_id("TT ON %s %s" % (curr_freq, curr_mode))
                    cwid.cw_id("e")
                    mute_off()
                
                elif command_two == "*01*":
                    write_file("Force TT ON during login session")
                    talkthrough_on()
                    tt_flag = 1
                    freq = ": ".join(curr_freq)
                    freq = freq.replace('.','decimal')
                    mode = ": ".join(curr_mode)
                    write_status("tt","ON")
                    mute_on()
                    cwid.cw_id("TT ON %s %s" % (curr_freq, curr_mode))
                    cwid.cw_id("e")
                    mute_off()
        
                elif command_two == "*00":
                    talkthrough_off()
                    tt_flag = 0
                    write_status("tt","OFF")
                    mute_on()
                    cwid.cw_id("TT OFF")
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*5":
                    qsy_down()
                    time.sleep(1)
                    cwid.cw_id("i")
                
                elif command_two == "*6":
                    qsy_up()
                    time.sleep(1)
                    cwid.cw_id("i")
                    
                elif command_two == "*9":
                    mute_on()
                    play_status()
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*8":
                    mute_on()
                    cwid.cw_id( "@")
                    atu_tune()
                    cwid.cw_id("e")
                    mute_off()

                elif command_two[:2] == "*7":
                    
                    if len(command_two) > 2:

                        if command_two[2] == "*":
                            mute_on()
                            cwid.cw_id("?")
                            mute_off()
                            #monitor_state = command_two[3]
                            #monitor(monitor_state)

                        elif len(command_two) > 2:
                            peektime = int(command_two[2:])
                        
                            mute_on()
                            cwid.cw_id("i")
                            peek(peektime)
                            cwid.cw_id("e")
                            mute_off()
                    
                    else: 
                        peektime = 5
                    
                        mute_on()
                        cwid.cw_id("i")
                        peek(peektime)
                        cwid.cw_id("e")
                        mute_off()

                #elif command_two == "*311":
                #    nb_on()
                #    mute_on()
                #    cwid.cw_id("NB ON")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*310":
                #    nb_off()
                #    mute_on()
                #    cwid.cw_id("NB OFF")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*321":
                #    anf_on()
                #    mute_on()
                #    cwid.cw_id("ANF ON")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*320":
                #    anf_off()
                #    mute_on()
                #    cwid.cw_id("ANF OFF")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*331":
                #    bandwidth_narrow()
                #    mute_on()
                #    cwid.cw_id("NARROW")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*332":
                #    bandwidth_normal()
                #    mute_on()
                #    cwid.cw_id("NORMAL")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*333":
                #    bandwidth_wide()
                #    mute_on()
                #    cwid.cw_id("WIDE")
                #    cwid.cw_id("e")
                #    mute_off()
                
                #elif command_two == "*320":
                #    agc_off()
                #    mute_on()
                #    cwid.cw_id("AGC OFF")
                #    cwid.cw_id("e")
                #    mute_off()
                
                #elif command_two == "*321":
                #    agc_on()
                #    mute_on()
                #    cwid.cw_id("AGC ON")
                #    cwid.cw_id("e")
                #    mute_off()
                
                #elif command_two == "*342":
                #    agc_slow()
                #    mute_on()
                #    cwid.cw_id("SLOW")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*350":
                #    pre_off()
                #    mute_on()
                #    cwid.cw_id("OFF")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*351":
                #    pre_on()
                #    mute_on()
                #    cwid.cw_id("ON")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*360":
                #    att_off()
                #    mute_on()
                #    cwid.cw_id("OFF")
                #    cwid.cw_id("e")
                #    mute_off()

                #elif command_two == "*361":
                #    att_on()
                #    mute_on()
                #    cwid.cw_id("ON")
                #    cwid.cw_id("e")
                #    mute_off()

                elif command_two[:2] == "*4":
                    

                    new_pwr = command_two[2:]
                        #if float(new_pwr) > 80:
                        #    new_pwr = "80"
                        #    write_file("Limiting to %s" % new_pwr)
                    power = tx_pwr(new_pwr)
                    mute_on()
                    cwid.cw_id("%sW" % power)
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*91":
                    peek(5)
                    s_no = get_snumber()
                    mute_on()
                    cwid.cw_id(s_no)
                    mute_off()

                #elif command_two == "*92":
                #    menu()
                
                elif command_two == "*93":
                    mute_on()
                    id_tx_menu.cw_id()
                    cwid.cw_id("e")
                    mute_off()

                elif command_two == "*99*":
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
                    xgate_quit()

                else:
                    write_file("Command %s not understood" % command_two )
                    mute_on()
                    cwid.cw_id("?")
                    mute_off()

            except Exception as ex:
                print "exception : %s" % ex
                write_file("Exception in command_two : %s" % command_two)
                mute_on()
                cwid.cw_id("?")
                mute_off()


except KeyboardInterrupt:
    
    write_file("Program killed by keyboard interrupt.......................")
    
    xgate_quit()

