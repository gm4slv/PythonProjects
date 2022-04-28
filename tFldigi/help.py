import readline
import xmlrpclib
import time

s = xmlrpclib.ServerProxy("http://shack:7362")

def get_text():
    text = raw_input(">: ")
    #print text
    return text

def do_sql():
    s.main.toggle_squelch()
    return

def do_tune():
    trx = s.main.get_trx_status()
    #print trx
    if trx != "tune":
        #print "TUNE ON"
        s.main.tune()
    else:
        #print "TUNE OFF"
        s.main.rx()
    return

def fld_qsy():
    cur_modem_carrier = s.modem.get_carrier()
    cur_dial_freq = s.main.get_frequency()
    new_dial_freq = (cur_dial_freq + cur_modem_carrier - 1500)
    s.modem.set_carrier(1500)
    s.main.set_frequency(new_dial_freq)
    return

def set_call():
    call = raw_input("Enter Callsign: ")
    s.log.set_call(call)
    return
def do_qsy():
    freq = raw_input("Enter Freq: ")
    s.rig.set_frequency(float(freq)*1000)
    s.modem.set_carrier(1500)
    return
def do_bw():
    bw_list =  s.rig.get_bandwidths()
    print "  ".join(bw_list)
    bw = raw_input("Select Bandwidth: ")
    if bw in bw_list:
        s.rig.set_bandwidth(bw)
        print "Bandwidth selected : %s" % s.rig.get_bandwidth()
    else:
        print "not recognized"
        print "Bandwidth selected : %s" % s.rig.get_bandwidth()
    return

def do_mode_change():
    modem_list= s.modem.get_names()
    
    modes=len(modem_list)
    count = 0
    while count < modes:

        print "\t".join(modem_list[count:count+5])
        count += 5
                

    #mode = raw_input("Select Mode: ")
    
    #if mode in modem_list:
    #    s.modem.set_by_name(mode)
    #    print "Modem selected : %s" % s.modem.get_name()
    #else :
     #   print "not recognized"
     #   print "Modem selected : %s" % s.modem.get_name()
    return

def do_reverse():
    s.main.toggle_reverse()
    return

def do_rxid():
    s.main.toggle_rsid()
    return

def do_txid():
    s.main.toggle_txid()
    return

def prompt():
    print "!qsy     = Enter new freq. in kHz"
    print "!net     = Move to centre 1500Hz"
    print "!mode    = Choose new data modem"
    print "!tx      = Transmit"
    print "!tune    = Toggle Tune"
    print "!rx      = Receive"
    print "!home    = Return to 60m / 5368kHz"
    print "!rxid    = Toggle RxID"
    print "!txid    = Toggle TxID"
    print "!rev     = Toggle modem reverse setting"
    print "!sql     = Toggle Squelch"
    print "!bw      = Choose new IF Bandwidth"
    print ""
    print "!cq      = Send CQ Macro"
    print "!call    = Enter callsign"
    print "!ans     = Send ANS Macro"
    print "!qso     = Send QSO Start of Over Macro"
    print "!kn      = Send KN End of Over Macro"
    print "!sk      = Send SK End of QSO Macro"
    print "!ry      = Send RY Testing Macro"
    print "!clr     = Clear Log Fields"
    print ""
    print "!5       = Select  5W TX power Macro"
    print "!10      = Select 19W TX power Macro"
    print "!50      = Select 50W TX power Macro"
    print "!100     = Select 100W TX power Macro"
    print ""
    print "!help    = Display this menu"
    print "!Q       = QUIT"
    return


def tx():
    tx_text = get_text()
    if tx_text == "":
        #f = s.rig.get_frequency()/1000
        #trx = s.main.get_trx_status()
        #modem = s.modem.get_name()
        #r = s.main.get_reverse()
        #stat = s.main.get_status1()
        #sql = s.main.get_squelch()
        
        # if r == 1:
        #     rev = "Rev"rx
        #else:
        #    rev = "Nor"

        #if sql == 0:
        #    sq = "Open"
        #else:
        #    sq = "Closed"

        #print "%0.1f %s %s %s %s %s" % (f, trx, stat, modem, rev, sq)
        s.text.add_tx("\n")
        
        return

    elif tx_text == "!help":
        prompt()
    #elif tx_text == "!tx":
    #    s.main.tx()
    #elif tx_text == "!rx":
    #    s.text.add_tx("^r")
    #elif tx_text == "!tune":
    #    do_tune()
    #elif tx_text == "!call":
    #    set_call()
    #elif tx_text == "!rev":
    #    do_reverse()
    #elif tx_text == "!rxid":
    #    do_rxid()
    #elif tx_text == "!txid":
    #    do_txid()
    #elif tx_text == "!sql":
    #    do_sql()
    #elif tx_text == "!bw":
    #    do_bw()
    #elif tx_text == "!home":
    #    rev=s.main.get_reverse()
    #    s.modem.set_by_id(73)
    #    if rev == 1:
    #        #print "REV ", rev
    #        s.main.toggle_reverse()
    #    s.main.run_macro(14)

    #elif tx_text=="!cq":
    #    s.main.run_macro(0)
    #elif tx_text=="!ans":
    #    s.main.run_macro(1)

    #elif tx_text=="!qso":
    #    s.main.run_macro(2)
    #elif tx_text=="!kn":
    #    s.main.run_macro(3)
    #elif tx_text=="!sk":
    #    s.main.run_macro(4)
    #elif tx_text=="!ry":
    #    s.main.run_macro(6)
    #elif tx_text == "!5":
    #    s.main.run_macro(20)
    #elif tx_text == "!10":
    #    s.main.run_macro(21)
    #    
    #elif tx_text == "!50":
    #    s.main.run_macro(22)
    #elif tx_text == "!100":
    #    s.main.run_macro(23)
    #elif tx_text == "!qsy":
    #    do_qsy()
    #elif tx_text == "!net":
    #    fld_qsy()
    elif tx_text == "!mode":
        do_mode_change()
    elif tx_text == "!Q":
        quit()
    else:
    #    #s.main.tx()
    #    s.text.add_tx("\n"+tx_text)
        return

prompt()

while True:
    tx()
    time.sleep(1)


