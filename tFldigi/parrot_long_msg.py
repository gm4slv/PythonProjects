#
#######
##  test file
#

import xmlrpclib
import time
import os
import subprocess

s = xmlrpclib.ServerProxy("http://shack:7362")


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

def parse_message(text):
    print text
    header=text.split('\n')[0]
    print "Header ", header
    try:
        from_call=header.split(">")[0]
        to_call=header.split(">")[1]
    except:
        from_call=header.split('\n')[0]
        to_call=from_call

    print "From ",from_call
    print "To ",to_call
    user = call_asc(from_call)

    target = call_asc(to_call)
    message = "\n".join(text.split('\n')[1:])
    return(user,target,message)

def call_asc(call):
    call_asc = "".join(x for x in call if (ord(x) > 46 and ord(x) < 58) or (ord(x) > 64 and ord(x) < 91))
    return(call_asc)



def qsp(text, snr):
    print "\nQSP triggered with"
    print "\nmessage: \n\n", text
    
    user,target,message=parse_message(text)

    time.sleep(10)
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
    s.text.add_tx("\n"+target+" de GM4SLV\n\nQSP de GM4SLV on behalf of "+user+"\n\n==== "+snr+" ====\n\nFor attn. of "+target+"\nMESSAGE BEGINS\n\n"+message+"\nMESSAGE ENDS\n\n"+target+" de "+user+" via GM4SLV kn \n  ^r")
    #print "after text add"
    timenow = time.strftime("*** Time Stamp : %Y-%m-%d %H:%M:%S :  ", time.gmtime(time.time()))
    #print timenow
    modem = s.modem.get_name()
    car = s.modem.get_carrier()
    f = s.main.get_frequency()
    rfc = (f + car) / 1000
    write_file("\n%s\n%s (%s)  Message Relayed on %0.1f for : %s\n%s\n====================\n" % (timenow, modem, snr, rfc, user, text))
    subprocess.call("./log.sh")
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
            modem = s.modem.get_name()
            if modem != "RTTY":
                stat1 = s.main.get_status1()
            else:
                stat1 = s.main.get_status2()

            print stat1
            

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
                #call_index = zc_index + 20
                
                #user = ''.join(rx_text[zc_index:call_index])
                message = ''.join(rx_text[zc_index:nn_index])
                
                zc_flag = 0
                nn_flag = 0

                #user = user.split(" ")[0]
                #target = user.split(">")[1]

                #user_asc = "".join(x for x in user if (ord(x) > 46 and ord(x) < 58) or (ord(x) > 64 and ord(x) < 91))
                #target_asc = "".join(x for x in target if (ord(x) > 46 and ord(x) < 58) or (ord(x) > 64 and ord(x) < 91))
                message_asc = "".join(x for x in message if (ord(x) > 31 and ord(x) < 128) or ord(x) == 13 or ord(x) == 10 or ord(x) == 9)
                #print "User %s" % (user_asc)
                #print "Target %s" % (target_asc)
                rx_text = []

                qsp(message_asc, stat1)
        
        
            else:
                rx_text = []
                zc_flag = 0
                nn_flag = 0

    except:
        rx_text = []
    
    
    
    time.sleep(2)
    
    
