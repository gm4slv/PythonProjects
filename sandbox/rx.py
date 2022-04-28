import xmlrpclib
import time
import os

s = xmlrpclib.ServerProxy("http://192.168.21.107:7362")
rx_text = ""
n = 0
index = s.text.get_rx_length()


os.system('cls' if os.name == 'nt' else 'clear')

    
while True:
    if len(rx_text) > 2000:
        rx_text = rx_text[500:]
    try:
        rx_length = s.text.get_rx_length()
        rx_new =  str(s.text.get_rx(index,rx_length - index))
        index = rx_length
    except:
        print "Exception"
        #pass
        #rx_text = ""
    if rx_new == "empty rx buffer!":
        rx_new = ""
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    
    rx_new_asc = "".join(x for x in rx_new if (ord(x) > 31 and ord(x) < 128 ) or ord(x) == 9 or ord(x) == 10 or ord(x) == 13) 
    
    rx_text = rx_text + rx_new_asc

    
    if len(rx_new_asc) > 0:
        print rx_text
    #    print len(rx_text)
    time.sleep(2)
     
    
