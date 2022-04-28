import xmlrpclib
import radio_functions_m710 as radio
import time

s = xmlrpclib.ServerProxy("http://192.168.21.4:7362")


def get_freq():
    freq = s.main.get_frequency()
    return freq
  
def set_freq(freq):
    rig_f = freq - carrier
    freq = s.main.set_frequency(rig_f)
    radio_dial = float(rig_f / 1000 )
    radio.set_freq(str(radio_dial))
    return freq
    
def get_rigmode():
    rigmode = s.rig.get_mode()
    return rigmode
    
def poll_f():
    fld_dial = get_freq() / 1000
    radio_dial = float(radio.get_rxfreq())
    if fld_dial != radio_dial: 
        print "Fld dial ", fld_dial
        print "radio dial ", radio_dial
        radio.set_freq(fld_dial)
        print "new radio freq ", radio.get_rxfreq()

def poll_m():
    fld_rigmode = get_rigmode()
    radio_mode = radio.get_mode()
    if fld_rigmode != radio_mode:
        print "fld mode ", fld_rigmode
        print "radio mode ", radio_mode
        radio.set_mode(fld_rigmode)
        print "New radio mode ", radio.get_mode()

print s.rig.get_modes()

mode_list = [ "USB", "LSB" ]

s.rig.set_modes(mode_list)
s.rig.set_name("IC-M710")
radio.set_txpower("3")
radio.dim_on()

while True:
    try:
        poll_f()
        poll_m()
    except:
        pass
    time.sleep(0.3)
    


