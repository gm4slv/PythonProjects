import xmlrpclib

s = xmlrpclib.ServerProxy("http://192.168.21.4:7362")


def get_mode():
    mode = s.modem.get_name()
    return mode

def set_mode(new_mode):
    s.modem.set_by_name(new_mode)
    return new_mode

def get_freq():
    freq = s.main.get_frequency()
    carrier = s.modem.get_carrier()
    return freq, carrier

def set_freq(freq, carrier):
    rig_f = freq - carrier
    freq = s.main.set_frequency(rig_f)
    carrier = s.modem.set_carrier(carrier)
    return freq, carrier
    
def list_modes():
    mode_list = s.modem.get_names()
    return mode_list
    
    
def start():
    choice = raw_input("1 = Get current mode\n2 = Change mode\n3 = Get Frequency\n4 = Set Centre Frequency\n5 = List Modes\nq = quit\nChoice: ")
    if choice == "1":
        mode = get_mode()
        print "\nCurrent mode: %s\n" % mode
        start()
    elif choice == "2":
        new_mode = raw_input("\nEnter mode: ")
        new_mode = set_mode(new_mode)
        mode = get_mode()
        print "\nSetting %s,\nNew Mode is %s\n" % (new_mode, mode)
        start()
    elif choice == "3":
        freq, carrier = get_freq()
        print "\nCurrent Dial Frequency is %.3fkHz\nModem carrier is %sHz\n" % (freq/1000, carrier)
        centre = (float(freq) + int(carrier))/1000
        print "Centre freq is %.3fkHz\n" % centre
        start()
    elif choice == "4":
        carrier = 1500
        freq = float(raw_input("\nEnter new centre freq (kHz): "))
        set_freq(freq * 1000, carrier)
        start()
    elif choice == "5":
        mode_list = list_modes()
        print '\n'
        print '\n'.join(str(p) for p in mode_list)
        print '\n'
        start()
        
    elif choice == "q":
        quit()
    else: 
        start()
    
start()