import time
import serial
import ann_tx
import id_tx_menu
from icom import *
import atexit
import sys
import json

ser = serial.Serial(
        port='/dev/xgate',
        baudrate = 4800,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

r1 = Icom(n1, a1, cal1)

curr_mode = r1.get_mode()
curr_freq = str(r1.get_freq())

mode_dict = {"1" : "USB", "2" : "LSB", "3" : "AM"}


mem_dict = {
        "0301" : ["3773.0", "LSB"],
        "0302" : ["3760.0", "LSB"],
        "0303" : ["3615.0", "AM"],
        
        "0501" : ["5276.0","USB"], 
        "0502" : ["5279.0","USB"], 
        "0503" : ["5298.0","USB"],
        "0504" : ["5301.0","USB"], 
        "0505" : ["5304.0","USB"], 
        "0506" : ["5317.0","AM"],
        "0507" : ["5320.0", "USB"], 
        "0508" : ["5333.0", "USB"], 
        "0509" : ["5354.0", "USB"],
        "0510" : ["5363.0", "USB"],
        "0511" : ["5366.5", "USB"],
        "0512" : ["5371.5", "USB"],
        "0513" : ["5378.0", "USB"],
        "0514" : ["5395.0", "USB"],
        "0515" : ["5398.5", "USB"],
        "0516" : ["5403.5", "USB"],
        
        "0591" : ["5450.0", "USB"],
        "0592" : ["5505.0", "USB"],
        "0593" : ["10051.0", "USB"],
     
        "0701" : ["7160.0", "LSB"],
        
        }

def cleanup():
    mute_on()
    ann_tx.ident("QRT %")
    mute_off()
    ann_tx.cleanup()
    
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


def write_status(mode,freq,tt):
    
    try:
        saved = open('/home/gm4slv/status_dict.json')
        status_dict = json.load(saved)
    except:
        status_dict = {}

    if mode != "nil":
        status_dict["mode"] = mode
    if freq != "nil":
        status_dict["freq"] = freq
    if tt != "nil":
        status_dict["tt"] = tt

    with open('/home/gm4slv/status_dict.json', 'wb') as outfile:
        json.dump(status_dict, outfile)

    return


def talkthrough_on():
    global talkthrough
    talkthrough = "ON"
    write_file("Talkthrough ON")
    ann_tx.tt(True)
    return

def talkthrough_off():
    global talkthrough
    talkthrough = "OFF"
    write_file("Talkthrough OFF")
    ann_tx.tt(False)
    return

def qsy_up():
    global curr_freq
    mute_off()
    new_freq = float(curr_freq) + 0.5
    r1.set_freq(new_freq)
    curr_freq = str(new_freq)
    write_file("QSY Up to %s" % curr_freq)
    return

def qsy_down():
    global curr_freq
    mute_off()
    new_freq = float(curr_freq) - 0.5
    r1.set_freq(new_freq)
    curr_freq = str(new_freq)
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
    result = r1.tune()
    write_file("ATU Tune.... %s" % result)
    return

def nr_on():
    result = r1.dsp_nr_on()
    write_file("Noise Reduction ON")
    return

def nr_off():
    result = r1.dsp_nr_off()
    write_file("Noise Reduction OFF")
    return

def anf_on():
    result = r1.dsp_anf_on()
    write_file("Auto Notch Filter ON")
    return

def anf_off():
    result = r1.dsp_anf_off()
    write_file("Auto Notch Filter OFF")
    return

def get_snumber():
    smeter = float(r1.get_smeter())
    if smeter > -73:
        s_no = "S9"
    elif smeter > -79:
        s_no = "S8"
    elif smeter > -85:
        s_no = "S7"
    elif smeter > -91:
        s_no = "S6"
    elif smeter > -97:
        s_no = "S5"
    elif smeter > -103:
        s_no = "S4"
    elif smeter > -109:
        s_no = "S3"
    elif smeter > -115:
        s_no = "S2"
    elif smeter > -121:
        s_no = "S1"
    else:
        s_no = "S0"
    write_file("S Meter : %s" % s_no)

    return(s_no)


def tx_pwr(pwr):
    result = r1.set_pwr(pwr)
    write_file("TX Power set to %s" % pwr)
    return

def bandwidth_wide():
    result = r1.bandwidth_wide()
    write_file("IF Filter : WIDE")
    return

def bandwidth_normal():
    result = r1.bandwidth_normal()
    write_file("IF Filter : NORMAL")
    return

def bandwidth_narrow():
    result = r1.bandwidth_narrow()
    write_file("IF Filter : NARROW")
    return

def peek(peektime):
    write_file("Peeking on HF for %d ...."  % peektime)
    mute_off()
    ann_tx.ptt(peektime)
    mute_on()
    return

def mute_on():
    write_file("Mute ON")
    ann_tx.mute_on()
    return

def mute_off():
    write_file("Mute OFF")
    ann_tx.mute_off()
    return

def status():
    #global curr_freq 
    #global curr_mode
    #global talkthrough
    #global tt_flag
    
    saved = open('/home/gm4slv/status_dict.json')
    status_dict = json.load(saved)
    
    curr_freq = status_dict["freq"]
    curr_mode = status_dict["mode"]
    tt = status_dict["tt"]

    freq = ": ".join(curr_freq)
    freq = freq.replace('.',' decimal ')
    mode = ": ".join(curr_mode)
    
    #if curr_mode == "USB":
    #    mode = "upper"
    #elif mode == "LSB":
    #    mode = "lower"
    #smtr = get_snumber()
    
    #if tt == "ON":
    #    tt = "enabled"
    #else:
    #    tt = "disabled"

    write_file("STATUS : Mode %s, Frequency %s, %s" % (curr_mode,curr_freq, tt))
    #time.sleep(1)
    #ann_tx.speak_status(freq,mode,tt)
    #ann_tx.ident("%s %0.1f %s %s" % (curr_mode, float(curr_freq), smtr, tt))
    ann_tx.ident("%0.1f %s %s" % (float(curr_freq),curr_mode, tt))
    return

def menu():
    print "Commands are : "
    print "*1 Freq"
    print "*2 Mode"
    print "*3 RX Functions"
    print "*4 TX Power"
    print "*7 Peek"
    print "*8 ATU Tune"
    print "*9 Status"
    print "*99* Logout"
    #ann_tx.speak("1 Frequency : 2 Mode : 3 Receiver Functions : 4 Transmit Power : five down : six  up :  seven peek : 8 tune : 9 Status")
    return

def xgate_quit():
    write_file("Got quit command")
    talkthrough_off()
    write_status("QRT","QRT","nil")
    sys.exit(0)


######## START HERE ###############################################################################################
#
#
#

pin = "0"

write_file("X-Gate Start........................................")

#t0 = time.time()

#################### set up IC-7200 ##############
#

r1.digi_off()

r1.mod_a()

r1.comp_on()

r1.vfo_mode()

r1.dial_lock_on()

r1.nb_on()

######################################
#

talkthrough_off()

tt_flag = 0
write_status(curr_mode, curr_freq, talkthrough)

#mute_on()
ann_tx.ident("QRV DE GM4SLV")

#id_tx.cw_id()

#status()

#mute_off()

login_flag = 0

#write_status(curr_mode, curr_freq, talkthrough)

try:

    while True:
   
        if login_flag == 0:
            command_one = read_command()
        
        elif login_flag == 1:
            command_one = pin

        if command_one != pin:
            write_file("Wrong PIN")
            time.sleep(1)
            mute_on()
            ann_tx.ident("?")
            mute_off()

        else:
            time.sleep(1)
            if login_flag !=1:
                write_file("User Command login")
                
                mute_on()
                ann_tx.ident("R")
                mute_off()

                if talkthrough == "ON":
                    talkthrough_off()
                    tt_flag = 1
            
            
            #mute_on()
            
            login_flag = 1
            

            #elapsed_time = time.time() - t0
            
            command_two = read_command()
            
            write_file("Command received : %s" % command_two)
            ###################################################
            #
            # COMMANDS:
            #
            # 1 : Frequency fffff = ffff.f kHz
            #   : xxxx = channel xxxx (freq & mode combined)
            #
            # 2 : Mode 
            #   : 21 = USB
            #   : 22 = LSB
            #   : 23 = AM
            #
            # 3 : RX Settings
            #   : 310 = NR OFF
            #   : 311 = NR ON
            #   : 320 = ANF OFF
            #   : 321 = ANF ON
            #   : 331 = Bandwidth NARROW
            #   : 332 = Bandwidth NORMAL
            #   : 333 = Bandwidth WIDE
            #
            # 4 : TX Power 
            #
            # 5 : QSY Up 
            # 6 : QSY Down
            #
            # 7 : HF Peek
            #
            # 8 : ATU Tune
            #
            # 9 : Status
            #   : 9 =  CW Status
            #   : 91 = S Meter
            #   : 92 = Menu
            #   : 93 = Full Status
            #
            # 0 : Talkthrough
            #   : 01 = Talkthrough ON
            #   : 02 = Tqlkthrough OFF

            try:
                if command_two[:2] == "*1":
                    if len(command_two[2:]) == 4:
                        new_freq = float(mem_dict[command_two[2:]][0])
                        new_mode = mem_dict[command_two[2:]][1]
                        set_frequency(new_freq)
                        set_mode(new_mode)
                    else:
                        new_freq = float(command_two[2:])/10
                        set_frequency(new_freq)
                    freq = ": ".join(curr_freq)
                    freq = freq.replace('.','decimal')
                    mode = ": ".join(curr_mode)
                    #if curr_mode == "USB":
                    #    mode = "upper"
                    #elif curr_mode == "LSB":
                    #    mode = "lower"
                    #else:
                    #    mode = " : ".join(curr_mode)

                    write_status("nil",str(new_freq),"nil")
                    mute_on()
                    #ann_tx.ident("e")
                    ann_tx.ident("%s" % new_freq)
                    #ann_tx.speak("%s: %s" % (freq, mode))
                    #status()
                    ann_tx.ident("e")
                    mute_off()

                elif command_two[:2] == "*2":
                    new_mode = mode_dict[command_two[2]]
                    set_mode(new_mode)
                    freq = ": ".join(curr_freq)
                    freq = freq.replace('.','decimal')
                    mode = ": ".join(curr_mode)
                    #if curr_mode == "USB":
                    #    mode = "upper"
                    #elif curr_mode == "LSB":
                    #    mode = "lower"
                    #else:
                    #    mode = " : ".join(curr_mode)
                    #print freq
                    #print mode
                    write_status(new_mode,"nil","nil")
                    mute_on()
                    #ann_tx.ident("e")
                    ann_tx.ident("%s" % new_mode)
                    #ann_tx.speak("%s: %s" % (mode, freq))
                    #status()
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*01":
                    tt_flag = 1
                    freq = ": ".join(curr_freq)
                    freq = freq.replace('.','decimal')
                    mode = ": ".join(curr_mode)
                    #if curr_mode == "USB":
                    #    mode = "upper"
                    #elif curr_mode == "LSB":
                    #    mode = "lower"
                    #else:
                    #    mode = ": ".join(curr_mode)
                    write_status("nil","nil","ON")
                    mute_on()
                    #ann_tx.speak("Cross Gate: enabled: %s: %s" % (freq, mode))
                    #ann_tx.ident("e")
                    ann_tx.ident("TT ON %s %s" % (curr_freq, curr_mode))
                    ann_tx.ident("e")
                    mute_off()
                
                elif command_two == "*01*":
                    write_file("Force TT ON during login session")
                    talkthrough_on()
                    tt_flag = 1
                    freq = ": ".join(curr_freq)
                    freq = freq.replace('.','decimal')
                    mode = ": ".join(curr_mode)
                    #if curr_mode == "USB":
                    #    mode = "upper"
                    #elif curr_mode == "LSB":
                    #    mode = "lower"
                    #else:
                    #    mode = " : ".join(curr_mode)
                    #ann_tx.ident("TT ON %s %s" % (curr_freq, curr_mode))
                    write_status("nil","nil","ON")
                    mute_on()
                    #ann_tx.speak("Cross Gate: enabled: %s: %s" % (freq, mode))
                    #ann_tx.ident("e")
                    ann_tx.ident("TT ON %s %s" % (curr_freq, curr_mode))
                    ann_tx.ident("e")
                    mute_off()
        
                elif command_two == "*00":
                    talkthrough_off()
                    tt_flag = 0
                    write_status("nil","nil","OFF")
                    mute_on()
                    #ann_tx.speak("Cross Gate: disabled")
                    #ann_tx.ident("e")
                    ann_tx.ident("TT OFF")
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*5":
                    qsy_down()
                    #mute_on()
                    time.sleep(1)
                    ann_tx.ident("i")
                
                elif command_two == "*6":
                    qsy_up()
                    #mute_on()
                    time.sleep(1)
                    ann_tx.ident("i")
                    
                elif command_two == "*9":
                    mute_on()
                    status()
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*8":
                    mute_on()
                    atu_tune()
                    
                    #ann_tx.speak("Tuning cycle complete")
                    ann_tx.ident( "ATU")
                    ann_tx.ident("e")
                    mute_off()

                elif command_two[:2] == "*7":
                    if len(command_two) > 2:
                        peektime = int(command_two[2:])
                    else: 
                        peektime = 10
                    mute_on()
                    ann_tx.ident("i")
                    #mute_off()
                    peek(peektime)
                    #mute_on()
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*311":
                    nr_on()
                    mute_on()
                    #ann_tx.speak("Noise Reduction enabled")
                    #ann_tx.ident("e")
                    ann_tx.ident("NR ON")
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*310":
                    nr_off()
                    mute_on()
                    #ann_tx.speak("Noise Reduction disabled")
                    ann_tx.ident("NR OFF")
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*321":
                    anf_on()
                    mute_on()
                    #ann_tx.speak("Notch Filter enabled")
                    ann_tx.ident("ANF ON")
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*320":
                    anf_off()
                    mute_on()
                    #ann_tx.speak("Notch Filter disabled")
                    #ann_tx.ident("e")
                    ann_tx.ident("ANF OFF")
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*331":
                    bandwidth_narrow()
                    mute_on()
                    #ann_tx.speak("Filter: Narrow")
                    #ann_tx.ident("e")
                    ann_tx.ident("NARROW")
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*332":
                    bandwidth_normal()
                    mute_on()
                    #ann_tx.speak("Filter: Normal")
                    #ann_tx.ident("e")
                    ann_tx.ident("NORMAL")
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*333":
                    bandwidth_wide()
                    mute_on()
                    #ann_tx.speak("Filter: Wide")
                    #ann_tx.ident("e")
                    ann_tx.ident("WIDE")
                    ann_tx.ident("e")
                    mute_off()

                elif command_two[:2] == "*4":
                    new_pwr = command_two[2:]
                    tx_pwr(new_pwr)
                    mute_on()
                    #ann_tx.speak(": %s watts " % new_pwr)
                    #ann_tx.ident("e")
                    ann_tx.ident("%sW" % new_pwr)
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*91":
                    s_no = get_snumber()
                    ann_tx.ident(s_no)
            
                elif command_two == "*92":
                    menu()
                
                elif command_two == "*93":
                    mute_on()
                    id_tx_menu.cw_id()
                    ann_tx.ident("e")
                    mute_off()

                elif command_two == "*99*":
                    write_file("Logout")
                    login_flag = 0
                    mute_on()
                    ann_tx.ident("%")
                    if tt_flag == 1:
                        write_file("... returning to TT")
                        talkthrough_on()
                        tt_flag = 0
                    mute_off()
                    write_status(curr_mode, curr_freq, talkthrough)

                elif command_two == "*9999*":
                    xgate_quit()

                else:
                    write_file("Command %s not understood" % command_two )
                    mute_on()
                    ann_tx.ident("?")
                    mute_off()

            except Exception:
                write_file("Exception in command_two : %s" % command_two)
                mute_on()
                ann_tx.ident("?")
                mute_off()

            #if elapsed_time > 3600:
            #    write_file("Identify")
            #    ann_tx.ident("DE GM4SLV")
            #    t0 = time.time()

except KeyboardInterrupt:
    
    write_file("Program killed by keyboard interrupt.......................")
    
    xgate_quit()

