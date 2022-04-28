#######
##  test file
#

import xmlrpclib
import time
import os

s = xmlrpclib.ServerProxy("http://shack:7362")


#index = 0
rx_text = []
zc_flag = 0
nn_flag = 0
#message_time=0

def write_file(text):
    filename = r'parrot_log.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    f.write(text)
    f.close()


def qsp(text):
    print "\nQSP triggered with"
    print "\nmessage: \n\n", text
    time.sleep(20)
    s.text.clear_rx()
    #wait = 0
    #while s.main.get_squelch() == 0:
    #    print "SQL Open...SLEEPING"
    #    time.sleep(1)
    #    wait += 1
    #    if wait > 60:
    #        print "sql stuck?"
    #        break
    print "PTT ON"
    s.main.tx()
    s.text.add_tx("\n\nQSP de GM4SLV \n=============\n\n"+text+"\n=============\n\nQSP de GM4SLV k \n  ^r")
    timenow = time.strftime("*** Time Stamp : %Y-%m-%d %H:%M:%S :  ", time.gmtime(time.time()))
    write_file("\r\n %s : \n\n %s\n" % (timenow, text))
    return

    
while True:
    try:
        rx_length = s.text.get_rx_length()
        #i = 0
        #print "rx_length ",rx_length
        #start = int(rx_length - 256)
        #stop = int(rx_length)
        #print "Start %d, Stop %d" % (start,stop)
        for l in range(rx_length-256, rx_length):
            #print l
            rx = str(s.text.get_rx(l,1))
            #print rx
            rx_text.append(rx)
            #print rx_text
            for i in range(len(rx_text)):         
                if rx_text[i] == "C" and rx_text[i-1] == "Z" and rx_text[i-2] == "C" and rx_text[i-3] == "Z":
                    print "Found ZCZC...."
                    zc_flag = 1
                    zc_index = i+2
                if rx_text[i] == "N" and rx_text[i-1] == "N" and rx_text[i-2] == "N" and rx_text[i-3] == "N":
                    print "Found NNNN...."
                    nn_flag = 1
                    nn_index = i-3

            text =  ''.join(rx_text)
            #print text

            
        if zc_flag == 1 and nn_flag == 1 : # message complete
            print "Message complete"
            message = ''.join(rx_text[zc_index:nn_index])
            zc_flag = 0
            nn_flag = 0
            message_asc = "".join(x for x in message if ord(x) > 32 or ord(x) < 128 or ord(x) == 13 or ord(x) == 9)
            qsp(message_asc)
            rx_text = []
            #message_time=0
        else:
            rx_text = []
            zc_flag = 0
            nn_flag = 0
            #message_time += 1
            #print "message_time ", message_time
            #print s.modem.get_id()
            
            #if message_time > 60: # 10 minutes
            #    s.text.clear_rx()
            #    s.modem.set_by_id(74)
            #    message_time = 0

    except:
        rx_text = []
    
    
    
    time.sleep(10)
    
    
