#
#######
##  test file
#

import xmlrpclib
import time
import os

s = xmlrpclib.ServerProxy("http://laptop:7362")


#index = 0
rx_text = []
zc_flag = 0
nn_flag = 0
message_time=0

def write_file(text):
    #print "in write_file with ", text
    filename = r'parrot_log.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    f.write(text)
    f.close()


def qsp(text, user):
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
    s.text.add_tx("\n\nQSP de GM4SLV on behalf of "+user+"\n=============\n\n"+text+"\n=============\n\n"+user+" de GM4SLV kn \n  ^r")
    #print "after text add"
    timenow = time.strftime("*** Time Stamp : %Y-%m-%d %H:%M:%S :  ", time.gmtime(time.time()))
    #print timenow
    write_file("\n%s\n%s\n%s\n" % (timenow, user, text))
    return

    
while True:
    try:
        rx_length = s.text.get_rx_length()
        #i = 0
        #print "rx_length ",rx_length
        #start = int(rx_length - 256)
        #stop = int(rx_length)
        #print "Start %d, Stop %d" % (start,stop)
        for l in range(rx_length-200, rx_length):
            #print l
            rx = str(s.text.get_rx(l,1))
            #print rx
            rx_text.append(rx)
            #print rx_text
            
           #passwd = ["ZCZC","C3PO","R2D2", "ROOT"]
            user_dict = {"ZCZC" : "NOBODY", "ROOT" : "GM4SLV","C3PO": "G4VLC/P", "R2D2": "G0EZY"}
            #print "len(rx_text) ", len(rx_text)
            for i in range(len(rx_text)):
                for password in user_dict.keys():
                    if rx_text[i] == password[3] and rx_text[i-1] == password[2] and rx_text[i-2] == password[1] and rx_text[i-3] == password[0]:
                        if not zc_flag:
                            print "Found..", password
                            user = user_dict[password]
                            print "user ", user
                        zc_flag = 1
                        zc_index = i+2
                if rx_text[i] == "N" and rx_text[i-1] == "N" and rx_text[i-2] == "N" and rx_text[i-3] == "N":
                    if not nn_flag:
                        print "Found NNNN...."
                    nn_flag = 1
                    nn_index = i-3
            text =  ''.join(rx_text)
        
       
        if zc_flag == 1:
            print "found start... waiting for end  ", message_time
            if message_time < 30:
                message_time += 1
            else:
                print "Timeout waiting"
                s.text.clear_rx()
                message_time = 0
                rx_text= []
                zc_flag = 0
                nn_flag = 0
            
        else:
            rx_text=[]


        if zc_flag == 1 and nn_flag == 1 : # message complete
            print "Message complete"
            print "zc_index %d, nn_index %d" % (zc_index, nn_index)
            if zc_index < nn_index:
                message_time = 0
                print "Index correct"
                message = ''.join(rx_text[zc_index:nn_index])
                zc_flag = 0
                nn_flag = 0
                message_asc = "".join(x for x in message if (ord(x) > 31 and ord(x) < 128) or ord(x) == 13 or ord(x) == 10 or ord(x) == 9)
                
                rx_text = []
                qsp(message_asc, user)
        
        
            else:
                rx_text = []
                zc_flag = 0
                nn_flag = 0

    except:
        rx_text = []
    
    
    
    time.sleep(2)
    
    
