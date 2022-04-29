import xmlrpclib
import time
import os

s = xmlrpclib.ServerProxy("http://192.168.21.107:7362")
rx_text = ""
n = 0
index = 0
count = 0

def get_status():
    
    try:
        status = s.main.get_status1()
    except:
        status = "Fldigi Offline"
    return status

def get_mode():
    
    try:
        mode = s.modem.get_name()
    except:
        mode = "Fldigi Offline"
    return mode
    
def get_freq():
    try:
        freq = s.main.get_frequency()
        carrier = s.modem.get_carrier()
        centre = (float(freq) + int(carrier))/1000
    except:
        centre = 0.0
    return centre
    
def write_file(text):
    print "in write_file() with ", text
    text_asc = "".join(x for x in text if (ord(x) > 31 and ord(x) < 128) or ord(x) == 13 or ord(x) == 10 or ord(x) == 9)
    filename = r'/var/www/html/pages/gm4slv_fldigi.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    f.write(text_asc)
    f.close()
    return

def stamp_file():
    mode = get_mode()
    centre = get_freq()
    status = get_status()
    timenow = time.strftime("*** Time Stamp : %Y-%m-%d %H:%M :  ", time.gmtime(time.time()))
    #print mode
    write_file("\r\n\n%s *** Modem : %s : Centre Freq : %.3f *** SNR : %s \r\n\n" % (timenow, mode, centre, status))

def tail(n):
    filename = r'/var/www/html/pages/gm4slv_fldigi.txt'
    tailfile = r'/var/www/html/pages/gm4slv_tail.txt'
    fin = open(filename, 'r')
    list = fin.readlines()
    fin.close()
    tail_list = list[-n:]
    fout = open(tailfile, "w")
    fout.writelines(tail_list)
    fout.close()

    
while True:
    '''
    try:
        rx_length = s.text.get_rx_length()
        rx_text = str(s.text.get_rx(index,rx_length - index))
        index = rx_length
    except:
        rx_text = ""
    '''
    rx_length = s.text.get_rx_length()
    print "rxl ", rx_length
    print "index ", index
    print "getting %d, %d" % (index, rx_length - index)
    rx_text = str(s.text.get_rx(index,rx_length - index))
    index = rx_length
    if rx_text == "empty rx buffer!":
        rx_text = ""
    #s.text.clear_rx()
    #os.system('cls' if os.name == 'nt' else 'clear')
    print  rx_text
    
    
    
    write_file(rx_text)
    tail(100)
    
    count += 1

    if count == 180:
        # hourly 180 * 20 secs = 3600 secs = 60 mins
        stamp_file()
        count = 0
    time.sleep(20)
    
    
