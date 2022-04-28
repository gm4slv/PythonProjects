#######
##  test file
#

import xmlrpclib
import time
import os

s = xmlrpclib.ServerProxy("http://shack:7362")


index = 0
rx_text = []
zc_flag = 0
nn_flag = 0

def zc(text):
    print "doing the ZCZC function"
    print "Handling \n", text
    s.text.clear_rx()
    #time.sleep(10)
    wait = 0
    while s.main.get_squelch() == 0:
        print "SQL Open...SLEEPING"
        time.sleep(1)
        wait += 1
        if wait > 30:
            print "sql stuck?"
            break
    print "PTT ON"
    s.main.tx()
    s.text.add_tx("CQ de GM4SLV \n\nRepeated text: \n\n"+text+"de GM4SLV \n  ^r")
    

    
while True:
    try:
        rx_length = s.text.get_rx_length()
        i = 0
        print "rx_length ",rx_length
        for i in range(rx_length):
            print i
            rx = str(s.text.get_rx(i,1))
            print rx
            rx_text.append(rx)
            #print rx_text[i]
            if rx_text[i] == "C" and rx_text[i-1] == "Z" and rx_text[i-2] == "C" and rx_text[i-3] == "Z":
                print "Found ZCZC"
                zc_flag = 1
                zc_index = i+3
            if rx_text[i] == "N" and rx_text[i-1] == "N" and rx_text[i-2] == "N" and rx_text[i-3] == "N":
                nn_flag = 1
                nn_index = i-3
            text =  ''.join(rx_text)
            print text
        if zc_flag == 1 and nn_flag ==1 :
            message = ''.join(rx_text[zc_index:nn_index])
            zc_flag = 0
            nn_flag = 0
            zc(message)
            rx_text = []
        else:
            rx_text = []
            if rx_length > 1024:
                s.text.clear_rx()

    except:
        rx_text = []
    
    
    
    time.sleep(10)
    
    
