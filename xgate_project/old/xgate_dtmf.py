import time
import serial
import cwid
import cw_ident as speak
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


def cleanup():
    print "Goodbye"
    cwid.cw_id("QRT 73")
    cwid.cleanup()
    #GPIO.cleanup()


atexit.register(cleanup)

def read_command():

    byte = ""
    result = []
    count = 0



    while byte != "#":
        byte = ser.read()
        if byte != "":
            #if byte == "*":
            #    byte = "."
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

    status_dict["mode"] = mode
    status_dict["freq"] = freq
    status_dict["tt"] = tt

    with open('/home/gm4slv/status_dict.json', 'wb') as outfile:
        json.dump(status_dict, outfile)

    return



def talkthrough_on():
    global talkthrough
    #print "old t/t ", talkthrough
    #print "setting GPIO output ON"
    talkthrough = "ON"
    write_file("Talkthrough ON")
    cwid.tt(True)
    return

def talkthrough_off():
    global talkthrough
    #print "old t/t ", talkthrough
    #print "setting GPIO output OFF"
    talkthrough = "OFF"
    write_file("Talkthrough OFF")
    cwid.tt(False)
    return

def set_frequency(freq):
    global curr_freq
    #print "old freq", curr_freq
    #print "setting new frequency %f" % freq
    r1.set_freq(freq)
    curr_freq = str(freq)
    write_file("New Frequency %s" % curr_freq)
    #print "new freq ", curr_freq
    return

def set_mode(mode):
    global curr_mode
    #print "old mode ", curr_mode
    #print "setting new mode %s" % mode
    r1.set_mode(mode)
    curr_mode = mode
    write_file("New Mode %s" % curr_mode)
    #print "new mode ", curr_mode
    return

def atu_tune():
    #print "tuning...."
    result = r1.tune()
    write_file("ATU Tune.... %s" % result)
    #print result
    return

def nr_on():
    #print "Noise Reduction ON"
    result = r1.dsp_nr_on()
    #print result
    write_file("Noise Reduction ON")
    return

def nr_off():
    #print "Noise Reduction OFF"
    result = r1.dsp_nr_off()
    #print result
    write_file("Noise Reduction OFF")
    return

def anf_on():
    #print "Notch ON"
    result = r1.dsp_anf_on()
    #print result
    write_file("Auto Notch Filter ON")
    return

def anf_off():
    #print "Notch OFF"
    result = r1.dsp_anf_off()
    #print result
    write_file("Auto Notch Filter OFF")
    return

def get_snumber():
    smeter = float(r1.get_smeter())
    #print "S Meter....", smeter
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
    #print "S-No.  ", s_no
    write_file("S Meter : %s" % s_no)

    return(s_no)


def tx_pwr(pwr):
    #print "Setting new power"
    result = r1.set_pwr(pwr)
    #print result
    write_file("TX Power set to %s" % pwr)
    return

def bandwidth_wide():
    #print "Setting filter to WIDE"
    result = r1.bandwidth_wide()
    #print result
    write_file("IF Filter : WIDE")
    return

def bandwidth_normal():
    #print "Setting filter to NORMAL"
    result = r1.bandwidth_normal()
    #print result
    write_file("IF Filter : NORMAL")
    return

def bandwidth_narrow():
    #print "Setting filter to NARROW"
    result = r1.bandwidth_narrow()
    #print result
    write_file("IF Filter : NARROW")
    return

def peek(peektime):
    write_file("Peeking on HF for %d ...."  % peektime)
    cwid.ptt(peektime)
    return

def status():
    global curr_freq 
    global curr_mode
    global talkthrough
    global tt_flag
    #print "Mode ", curr_mode
    #print "Freq ", curr_freq
    #print "TT ", talkthrough
    smtr = get_snumber()
    #print "Sending status information"
    if tt_flag == 1:
        tt = "ON"
    else:
        tt = "OFF"
    write_file("STATUS : Mode %s, Frequency %0.1f, %s , %s" % (curr_mode, float(curr_freq), smtr, tt))
    time.sleep(1)
    cwid.cw_id("%s %0.1f %s %s" % (curr_mode, float(curr_freq), smtr, tt))
    return

def menu():
    print "Commands are : "
    print "*1 ATU Tune"
    print "*2 Peek"
    print "*3x NR"
    print "*4x ANF"
    print "*8x Filter"
    print "*Axxx Power"
    print "Axxxxxx Frequency"
    cwid.cw_id("1 ATU / 2 PEEK / 3 NR / 4 ANF / 8 BW / A PWR @")
    return

def xgate_quit():
    write_file("Got quit command")
    talkthrough_off()
    write_status("QRT","","")
    #tx_pwr(0)
    sys.exit(0)


######## START HERE


pin = "0"

write_file("X-Gate Start.........................................................")

t0 = time.time()


r1.digi_off()

talkthrough_off()

tt_flag = 0

cwid.cw_id("QRV DE GM4SLV")

status()

login_flag = 0

write_status(curr_mode, curr_freq, talkthrough)

try:

    while True:
   
        if login_flag == 0:
            command_one = read_command()
        #print command_one
        
        elif login_flag == 1:
            command_one = pin

        if command_one != pin:
            #print "Sending ?"
            write_file("Wrong PIN")
            time.sleep(1)
            cwid.cw_id("?")
        else:
            #print "Sending R"
            time.sleep(1)
            if login_flag !=1:
                write_file("User Command login")
                cwid.cw_id("R")
                if talkthrough == "ON":
                    talkthrough_off()
                    tt_flag = 1
            
            login_flag = 1

            elapsed_time = time.time() - t0
            #print elapsed_time
            command_two = read_command()
            write_file("Command received : %s" % command_two)
            ###################################################
            #
            # COMMANDS:
            #
            # 1 : Frequency
            # 2 : Mode 
            #   : 21 = USB
            #   : 22 = LSB
            #   : 23 = AM
            # 3 : RX Settings
            #   : 31 = NR
            #   : 32 = ANF
            #   : 33 = Bandwidth
            # 4 : TX Power 
            # 5 : 
            # 6 : 
            # 7 : HF Peek
            # 8 : ATU Tune
            # 9 : Status
            # 0 : TALKTHROUGH

            try:
                if command_two[:2] == "*1":
                    new_freq = float(command_two[2:])/10
                    #print "Setting frequency to %0.1f" % new_freq
                    set_frequency (new_freq)
                    cwid.cw_id("R")

                elif command_two[:2] == "*2":
                    new_mode = mode_dict[command_two[2]]
                    #print "Setting Mode to %s" % new_mode
                    set_mode(new_mode)
                    cwid.cw_id("R")

                elif command_two == "*01":
                    #print "Talkthrough to ON"
                    #talkthrough_on()
                    tt_flag = 1
                    cwid.cw_id("TT ON %s %s" % (curr_freq, curr_mode))
                
                elif command_two == "*01*":
                    write_file("Force TT ON during login session")
                    #print "Talkthrough to ON"
                    talkthrough_on()
                    tt_flag = 1
                    cwid.cw_id("TT ON %s %s" % (curr_freq, curr_mode))
        
                elif command_two == "*00":
                    #print "Talkthrough to OFF"
                    talkthrough_off()
                    cwid.cw_id("TT OFF")
                    tt_flag = 0

                elif command_two == "*9":
                    #print "Sending Status"
                    status()

                elif command_two == "*8":
                    #print "ATU TUNE!"
                    atu_tune()
                    cwid.cw_id("R")
            
                elif command_two[:2] == "*7":
                    if len(command_two) > 2:
                        peektime = int(command_two[2:])
                    else: 
                        peektime = 10

                    #print "peeking on HF...."
                    peek(peektime)
            
                elif command_two == "*311":
                    #print "NR to ON"
                    nr_on()
                    cwid.cw_id("NR ON")

                elif command_two == "*310":
                    #print "NR to OFF"
                    nr_off()
                    cwid.cw_id("NR OFF")
            
                elif command_two == "*321":
                    #print "ANF to ON"
                    anf_on()
                    cwid.cw_id("ANF ON")

                elif command_two == "*320":
                    #print "ANF to OFF"
                    anf_off()
                    cwid.cw_id("ANF OFF")
            
                elif command_two == "*331":
                    #print "Filter to NARROW"
                    bandwidth_narrow()
                    cwid.cw_id("NARROW")
            
                elif command_two == "*332":
                    #print "Filter to NORMAL"
                    bandwidth_normal()
                    cwid.cw_id("NORMAL")
            
                elif command_two == "*333":
                    #print "Filter to WIDE"
                    bandwidth_wide()
                    cwid.cw_id("WIDE")
            
            
            
                elif command_two[:2] == "*4":
                    new_pwr = command_two[2:]
                    #print "New Power ", new_pwr
                    tx_pwr(new_pwr)
                    cwid.cw_id("R")

                elif command_two == "*91":
                    s_no = get_snumber()
                    #print "S Meter ", s_no
                    cwid.cw_id(s_no)
            
                elif command_two == "*92":
                    menu()
                
                elif command_two == "*93":
                    cwid.cw_id("e")
                    speak.cw_id()

                elif command_two == "*99*":
                    write_file("Logout")
                    login_flag = 0
                    cwid.cw_id("@")
                    if tt_flag == 1:
                        write_file("We were in TT prior... returning to TT")
                        talkthrough_on()
                        tt_flag = 0
                    write_status(curr_mode, curr_freq, talkthrough)

                elif command_two == "*9999*":
                    xgate_quit()

                else:
                    write_file("Command %s not understood" % command_two )
                    #print "not understood"
                    cwid.cw_id("?")


            except Exception:
                write_file("Exception in command_two : %s" % command_two)
                cwid.cw_id("?")
                #print "Sending QTC?"
            #break
            #if tt_flag == 1:
            #    write_file("We were in TT prior... returning to TT")
            #    talkthrough_on()
            #    tt_flag = 0


            # send ID if this command executed > 5 minutes since the last ID was sent.
            if elapsed_time > 900:
                write_file("Identify")
                cwid.cw_id("DE GM4SLV")
                t0 = time.time()

except KeyboardInterrupt:
    #print "Killed"
    write_file("Program killed by keyboard interrupt.......................")
    
    xgate_quit()
    ser.close()




