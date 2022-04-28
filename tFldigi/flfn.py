import xmlrpclib
import time

s = xmlrpclib.ServerProxy("http://shack:7362")


def do_qsy_tune(ttime):
    while s.main.get_trx_status() != "rx":
        trx = s.main.get_trx_status()
        print "starting while ",trx
        #s.main.rx()
        time.sleep(1)

    s.main.tune()
    time.sleep(ttime)
    trx = s.main.get_trx_status()
    print "tune? ",trx
    while s.main.get_trx_status() != "rx":
        trx = s.main.get_trx_status()
        print "ending while ",trx
        s.main.rx()
        time.sleep(1)
    trx = s.main.get_trx_status()
    print "final status ",trx
    return

def fld_qsy():
    cur_modem_carrier = s.modem.get_carrier()
    cur_dial_freq = s.main.get_frequency()
    new_dial_freq = (cur_dial_freq + cur_modem_carrier - 1500)
    s.modem.set_carrier(1500)
    s.main.set_frequency(new_dial_freq)
    return

def do_qsy(freq):
    if freq == "HOME":
        print "in do_qsy with HOME"
        do_home()
        time.sleep(2)
        do_qsy_tune(3)
        do_home()
        return freq
    else:
        print "in do_qsy with ", freq
        s.main.set_frequency(float(freq)*1000)
        s.modem.set_carrier(1500)
    
        do_qsy_tune(3)
        return freq

def do_reverse():
    s.main.toggle_reverse()
    return

def do_rxid():
    s.main.toggle_rsid()
    return

def do_txid():
    s.main.toggle_txid()
    return

def do_home():
    s.main.run_macro(14)
    return

