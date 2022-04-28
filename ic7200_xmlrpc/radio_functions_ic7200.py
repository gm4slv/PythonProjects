import serial
import threading
from conf import *
import time
#sport = "COM2"
#sport = "/dev/ttyUSB0"
#print hex(ord(radio_address))

sport = "/dev/cuaU0"

sbaud = 9600

lock = threading.Lock()

ser = serial.Serial(sport, sbaud, timeout=1)

    
def dig_off():
    sendStr = preamble + preamble + radio_address + controller + digi_off_cmd + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"
    
def dig_on():
    sendStr = preamble + preamble + radio_address + controller + digi_on_cmd + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"
    
def get_dig():
    sendStr = preamble + preamble + radio_address + controller + get_dig_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    if result[6] == "\x00":
        return 0
    elif result[6] == "\x01":
        return 1

def get_pre():
    sendStr = preamble + preamble + radio_address + controller + set_pre_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    if result[6] == "\x00":
        return 0
    elif result[6] == "\x01":
        return 1
    
def get_nb():
    sendStr = preamble + preamble + radio_address + controller + set_nb_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    if result[6] == "\x00":
        return 0
    elif result[6] == "\x01":
        return 1
            
def get_nr():
    sendStr = preamble + preamble + radio_address + controller + set_nr_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    if result[6] == "\x00":
        return 0
    elif result[6] == "\x01":
        return 1
            
def get_anf():
    sendStr = preamble + preamble + radio_address + controller + set_anf_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    if result[6] == "\x00":
        return 0
    elif result[6] == "\x01":
        return 1

def get_pwrmtr():
    sendStr = preamble + preamble + radio_address + controller + get_pwrmtr_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    p1 = ord(result[7]) / 16
    p2 = ord(result[7]) % 16
    p3 = ord(result[6]) / 16
    p4 = ord(result[6]) % 16
    pwrmtr = float(100 * (10 * p3 + p4) + (10 * p1 + p2))
        
    return pwrmtr
    
def get_nr_l():
    sendStr = preamble + preamble + radio_address + controller + nr_level_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    p1 = ord(result[7]) / 16
    p2 = ord(result[7]) % 16
    p3 = ord(result[6]) / 16
    p4 = ord(result[6]) % 16
    nr_level = int(100 * (10 * p3 + p4) + (10 * p1 + p2))
    return str(nr_level)

def set_nr_l( nrl):
        
    rignrl = int(nrl)
        
    nrl1 = rignrl / 100
    nrl2 = rignrl % 100
    snrl1 = (nrl1 / 10 * 16)
    snrl2 = (nrl1 % 10)
    snrl3 =  (nrl2 / 10 * 16)
    snrl4 =  (nrl2 % 10)
    snrl = chr(snrl1+snrl2) + chr(snrl3+snrl4)
        
    sendStr = preamble + preamble + radio_address + controller + nr_level_cmd + snrl + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return get_nr_l()
    elif result[4] == nak:
        return "NAK received"

def get_pwr():
    sendStr = preamble + preamble + radio_address + controller + pwr_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    p1 = ord(result[7]) / 16
    p2 = ord(result[7]) % 16
    p3 = ord(result[6]) / 16
    p4 = ord(result[6]) % 16
    pwr = float(100 * (10 * p3 + p4) + (10 * p1 + p2))
    return int(pwr)

def set_pwr( pwr):
    rigpwr = int(pwr)
    #print "rigpwr ", rigpwr
    pwr1 = rigpwr / 100
    pwr2 = rigpwr % 100
    spwr1 = (pwr1 / 10 * 16)
    spwr2 = (pwr1 % 10)
    spwr3 =  (pwr2 / 10 * 16)
    spwr4 =  (pwr2 % 10)
    spwr = chr(spwr1+spwr2) + chr(spwr3+spwr4)
    #print "spwr ", spwr
    sendStr = preamble + preamble + radio_address + controller + pwr_cmd + spwr + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return get_pwr()
    elif result[4] == nak:
        return "NAK received"

def get_bw():
    sendStr = preamble + preamble + radio_address + controller + bw_cmd + eom
    result = tx_rx(sendStr)
    #print result
    #p1 = ord(result[7]) / 16
    #p2 = ord(result[7]) % 16
    p3 = ord(result[6]) / 16
    p4 = ord(result[6]) % 16
    pwr = float(10 * p3 + p4)
    #print "bw %f %f %f" % (pwr, p3, p4)
    return pwr
    
def set_bw(bw):
    sbw3 =  (int(bw) / 10 * 16)
    sbw4 =  (int(bw) % 10)
    sbw = chr(sbw3+sbw4)
    sendStr = preamble + preamble + radio_address + controller + bw_cmd + sbw + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return get_bw()
    elif result[4] == nak:
        return "NAK received"
            
    
def pre_on():
    sendStr = preamble + preamble + radio_address + controller + set_pre_cmd + set_pre_on + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"
    
def pre_off():
    sendStr = preamble + preamble + radio_address + controller + set_pre_cmd + set_pre_off + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"
    
def nb_on():
    sendStr = preamble + preamble + radio_address + controller + set_nb_cmd + set_nb_on + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"

def nb_off():
    sendStr = preamble + preamble + radio_address + controller + set_nb_cmd + set_nb_off + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"
    
def nr_on():
    sendStr = preamble + preamble + radio_address + controller + set_nr_cmd + set_nr_on + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"
            
def nr_off():
    sendStr = preamble + preamble + radio_address + controller + set_nr_cmd + set_nr_off + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"
            
def anf_off():
    sendStr = preamble + preamble + radio_address + controller + set_anf_cmd + set_anf_off + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"
        
def anf_on():
    sendStr = preamble + preamble + radio_address + controller + set_anf_cmd + set_anf_on + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"


def ptt_on():
    sendStr = preamble + preamble + radio_address + controller + ptt_on_cmd + eom
    result = tx_rx(sendStr)
    #print result[5]
    #print "In ptt_on()"
    if not result[4] == ack:
        return "ptt on"
    elif result[4] == nak:
        return "Error"
    
def ptt_off():
    sendStr = preamble + preamble + radio_address + controller + ptt_off_cmd + eom
    result = tx_rx(sendStr)
    #print "In ptt_off()"

    #print result[5]
    if not result[4] == ack:
        return "ptt off"
    elif result[4] == nak:
        return "Error"

def get_att():
    sendStr = preamble + preamble + radio_address + controller + set_att_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    if result[5] == "\x00":
        return 0
    elif result[5] == "\x20":
        return 1

def att_on():
    sendStr = preamble + preamble + radio_address + controller + set_att_cmd + set_att_on + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"

def att_off():
    sendStr = preamble + preamble + radio_address + controller + set_att_cmd + set_att_off + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Success"
    elif result[4] == nak:
        return "NAK received"

def set_freq( freq):
    fdig = "%010d" % int(freq * 1000)
    bcd = ()
    for i in (8, 6, 4, 2, 0):
        bcd += freq_bcd(int(fdig[i]), int(fdig[i + 1]))
    set_freq_val = ""
    for byte in bcd:
        set_freq_val += chr(byte)
    sendStr = preamble + preamble + radio_address + controller + set_freq_cmd + set_freq_val + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Set Freq success"
    elif result[4] == nak:
        return "NAK received / Freq not supported"

def get_freq():
    sendStr = preamble + preamble + radio_address + controller + get_freq_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    if len(result) > 0:
        f = 0
    for k in [18, 19, 16, 17, 14, 15, 12, 13, 10, 11]:
        f = 10 * f + nib(result, k)
    freq = (float(f) / 1000)
    #print "in get_freq() returning ", freq
    return "%.3f" % freq

def set_mode(mode):
    #print "in set_mode() with ", mode
    if mode == "LSB":
        set_mode_val = "\x00"
    elif mode == "USB":
        set_mode_val = "\x01"
    elif mode == "am":
        set_mode_val = "\x02"
    elif mode == "cw":
        set_mode_val = "\x03"
    elif mode == "rtty":
        set_mode_val = "\x04"
    elif mode == "fm":
        set_mode_val = "\x05"
    elif mode == "cw-r":
        set_mode_val = "\x07"
    elif mode == "rtty-r":
        set_mode_val = "\x08"
    elif mode == "s-am":
        set_mode_val = "\x11"
    else:
        return "Mode not recognized"
    sendStr = preamble + preamble + radio_address + controller + set_mode_cmd + set_mode_val + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Set Mode Success"
    elif result[4] == nak:
       return "NAK received / Mode not supported"

def get_mode():
    sendStr = preamble + preamble + radio_address + controller + get_mode_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    mode = ""
    if result[5] == "\x00":
        mode = "lsb"
    elif result[5] == "\x01":
        mode = "usb"
    elif result[5] == "\x02":
        mode = "am"
    elif result[5] == "\x03":
        mode = "cw"
    elif result[5] == "\x04":
        mode = "rtty"
    elif result[5] == "\x05":
        mode = "fm"
    elif result[5] == "\x08":
        mode = "rtty-r"
    elif result[5] == "\x07":
        mode = "cw-r"
    elif result[5] == "\x11":
        mode = "s-am"
    mode = mode
    return mode.upper()

def get_s():
    sendStr = preamble + preamble + radio_address + controller + get_smeter_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    sm1 = ord(result[7]) / 16
    sm2 = ord(result[7]) % 16
    sm3 = ord(result[6]) / 16
    sm4 = ord(result[6]) % 16
    s = float(100 * (10 * sm3 + sm4) + (10 * sm1 + sm2))
    return s
    
def get_swr():
    sendStr = preamble + preamble + radio_address + controller + get_swr_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    sm1 = ord(result[7]) / 16
    sm2 = ord(result[7]) % 16
    sm3 = ord(result[6]) / 16
    sm4 = ord(result[6]) % 16
    swr = float(100 * (10 * sm3 + sm4) + (10 * sm1 + sm2))
    return swr

def get_smeter():
    s = float(get_s())
    #cal = cal
    s1 = s - cal[0]
    s2 = s1 - cal[1]
    s3 = s2 - cal[2]
    s4 = s3 - cal[3]
    s5 = s4 - cal[4]
    s6 = s5 - cal[5]
    s7 = s6 - cal[6]
    if s1 <= 0:
        dbm = -123
        adj = s / cal[0] * 10
        return str(dbm + adj)
    elif s2 <= 0:
        dbm = -113
        adj = s1 / cal[1] * 10
        return str(dbm + adj)
    elif s3 <= 0:
        dbm = -103
        adj = s2 / cal[2] * 10
        return str(dbm + adj)
    elif s4 <= 0:
        dbm = -93
        adj = s3 / cal[3] * 10
        return str(dbm + adj)
    elif s5 <= 0:
        dbm = -83
        adj = s4 / cal[4] * 10
        return str(dbm + adj)
    elif s6 <= 0:
        dbm = -73
        adj = s5 / cal[5] * 10
        return str(dbm + adj)
    elif s7 <= 0:
        dbm = -63
        adj = s6 / cal[6] * 20
        return str(dbm + adj)
    else:
        dbm = -43
        adj = s7 / cal[7] * 20
        return str(dbm + adj)

def get_name():
    return model

def tune():
    print "tuning"
    curmode = get_mode().lower()
    #print "Current Mode ",curmode
    curdig = get_dig()

    curpwr = get_pwr()
    #if curpwr < 98:
    #    curpwr = curpwr + 1

    print "Current Power ", curpwr
        
    #print "Current percent power ", curpwr
    set_mode("rtty")
    set_pwr(25)
    #print "Tuning power ", get_pwr()
    #print "PTT On"
    ptt_on()
    time.sleep(2)
    swr =  get_swr()
    #print "SWR :", swr
    time.sleep(1)
    ptt_off()
    #print "PTT Off"
    set_mode(curmode)
    #print "Mode reset ",get_mode()
    set_pwr(curpwr)
    if curdig:
        dig_on()

    print "Tuned : (ref pwr : %s)" % swr
    return "Tuned : (ref pwr : %s)" % swr
        
def tx_rx(sendStr):
    lock.acquire()
    string = ""
    for byte in sendStr:
        string += hex(ord(byte))

    #print "sendStr ", string
    ser.write(sendStr)
    #print len(sendStr) 
    echo = ser.read(len(sendStr))
    #print "reply length ", len(echo)
    if len(echo) != len(sendStr):
        return "0"
    byte = "0"
    result = ""
    count = 0
    while byte != eom:
        byte = ser.read()
        #print "%#02x" % ord(byte)
        result += byte
        count += 1
        if count > 10:
            break
    lock.release()
    #print ""
    return result


def nib( s, i):
    k = ord(s[i / 2])
    if i % 2 == 0:
        k = k >> 4
    return k & 0xf


def freq_bcd( d1, d2):
    return (16 * d1 + d2),

 
