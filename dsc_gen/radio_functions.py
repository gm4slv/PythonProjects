# serial port for Icom Rig Control
# imported into the GUI version that includes
# direct radio control



import serial


version = "v1.0"


sport = 'COM7'
ser = serial.Serial(sport, 9600, timeout=1)

# icom CiV hex-codes
preamble = "\xfe"
controller = "\xe0"
eom = "\xfd"
ack = "\xfb"
nak = "\xfa"
radio_address = "\x76" # IC-7200
tx_on = "\x1c" + "\x00" + "\x01"
tx_off = "\x1c" + "\x00" + "\x00"
set_freq_cmd = "\x05"
get_freq_cmd = "\x03"
set_mode_cmd = "\x06"
set_dig_cmd = "\x1a" + "\x04" + "\x01" + "\x03"
ack = "\xfb"
nak = "\xfa"

def set_mode(mode):
        
    if mode == "usb":
        set_mode_val = "\x01"
        
    else:
        return "Mode not recognized"
    sendStr = preamble + preamble + radio_address + controller + set_mode_cmd + set_mode_val + eom
    result = tx_rx(sendStr)
    if result[4] == ack:
        return "Set Mode Success"
    elif result[4] == nak:
        return "NAK received / Mode not supported"

def set_digi():
    sendStr = preamble + preamble + radio_address + controller + set_dig_cmd + eom
        
    result = tx_rx(sendStr)
    return 
            
# get current dial frequency from Icom transceiver
def get_freq():
    sendStr = preamble + preamble + radio_address + controller + get_freq_cmd + eom
    result = tx_rx(sendStr)
    if not result:
        return "0"
    if len(result) > 0:
        f = 0
    for k in [18, 19, 16, 17, 14, 15, 12, 13, 11, 10]:
        f = 10 * f + nib(result, k)
    freq = (float(f) / 1000)
    return "%.3f" % freq

# set new dial frequency on Icom transceiver
def set_freq(freq):
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

# helper function for "set_freq()"
def freq_bcd(d1, d2):
    return (16 * d1 + d2),

# helper function for "get_freq()"
def nib(s, i):
    k = ord(s[i / 2])
    if i % 2 == 0:
        k = k >> 4
    return k & 0xf 

# serial port send/receive function to talk to Icom Transceiver        
def tx_rx(sendStr):
       
    ser.write(sendStr)
    echo = ser.read(len(sendStr))
    if len(echo) != len(sendStr):
        return "0"
    byte = "0"
    result = ""
    count = 0
    while byte != eom:
        byte = ser.read()
        result += byte
        
    return result

# Turn Icom TX PTT on - the IC7200 has CiV controlled PTT which simplifies the PTT operation
def ptt_on():
    sendStr = preamble + preamble + radio_address + controller + tx_on + eom
    result = tx_rx(sendStr)
    return

# Turn Icom TX PTT off    
def ptt_off():
    sendStr = preamble + preamble + radio_address + controller + tx_off + eom
    result = tx_rx(sendStr)
    return
    
    
