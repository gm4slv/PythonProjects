#
#######
##  test file
#

import xmlrpclib
import time
import os
import subprocess

import flfn

s = xmlrpclib.ServerProxy("http://shack:7362")


rx_text = []
zc_flag = 0
nn_flag = 0
message_time=0

mycall = "GM4SLV"
                 
info = "GM4SLV INFO\nTest Relay\nIC-M710 50W\nInverted-L\n"
help_text = "Usage : \nZCZC\nRELAY_CALL FROM_CALL [ INFO? | HELP? | TO_CALL ]\nNNNN"

def write_file(text):
    filename = r'parrot_log.txt'
    f = open(filename, 'a+')
    f.write(text)
    f.close()

def parse_message(text):
    #print "Parsing : ", text
    header_line=text.split('\n')[0]
    message_text = "\n".join(text.split('\n')[1:])
    print "Header Line :\n", header_line
    print "Message Text : \n", message_text

    calls_list = header_line.split()
    
    if len(calls_list) > 1:
        if len(calls_list) < 4:
            
            print "Calls List ", calls_list
            
            relay_call = calls_list[0].upper()
            
            print "Relay call ", relay_call
            
            from_call = calls_list[1].upper()
            
            if len(calls_list) > 2:
                to_call = calls_list[2].upper()
            else:
                to_call = "ECHO"

            print "From ",from_call
            
            print "To ",to_call
            
            user = call_asc(from_call)

            target = call_asc(to_call)
            
            message = "\n".join(text.split('\n')[1:])
        
            if target == "INFO?":
                target = user
                user = "ECHO"
                message = info
            
            if from_call == "HELP?" or target == "HELP?":
                target = user
                user = "ECHO"
                message = help_text

            if relay_call == mycall:
                return(user,target,message)
            
            else:
                print "Wrong Relay Call"
                return("BOGUS","BOGUS","Not for Me")
        
        else:
            print "Header too long"
            return("BOGUS", "BOGUS", "Too Long")
    else:
        print "Header too short"
        return("BOGUS", "BOGUS","Too Short")

def call_asc(call):
    call_asc = "".join(x for x in call if (ord(x) > 46 and ord(x) < 58) or (ord(x) > 62 and ord(x) < 91))
    return(call_asc)



def qsp(text, snr):
    print "\nQSP triggered"
    
    timenow = time.strftime("*** Time Stamp : %Y-%m-%d %H:%M:%S :  ", time.gmtime(time.time()))
    
    user,target,message=parse_message(text)
    
    if user == "BOGUS":
        print "Ignoring"
        write_file("\n%s\nNOT RELAYED\n%s" % (timenow, text))
        subprocess.call("./log.sh")
        s.text.clear_rx()

        return

    time.sleep(10)
    s.text.clear_rx()
    
    print "PTT ON"
    
    timemsg = time.strftime("%H:%M:%S ", time.gmtime(time.time()))
    s.main.tx()
    s.text.add_tx("\n"+timemsg+"\nTo "+target+" from "+user+" via GM4SLV ("+snr+")\n\n"+message+"\n"+target+" de "+user+" via GM4SLV kn \n  ^r")
    
    timenow = time.strftime("*** Time Stamp : %Y-%m-%d %H:%M:%S :  ", time.gmtime(time.time()))
    timemsg = time.strftime("%H:%M:%S ", time.gmtime(time.time()))
    
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
        for l in range(rx_length-200, rx_length):
            rx = str(s.text.get_rx(l,1))
            rx_text.append(rx)
            
            for i in range(len(rx_text)):
                if rx_text[i] == "C" and rx_text[i-1] == "Z" and rx_text[i-2] == "C" and rx_text[i-3] == "Z":
                        
                    if not zc_flag:
                        print "Found ZCZC...."

                        modem = s.modem.get_name()
                        if modem != "RTTY":
                            stat1 = s.main.get_status1()
                        else:
                            stat1 = s.main.get_status2()

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
            #print "zc_index %d, nn_index %d" % (zc_index, nn_index)
            #print "Text  %s " % (rx_text[zc_index:nn_index])
            if zc_index < nn_index:
                message_time = 0
                print "Index correct"
                message = ''.join(rx_text[zc_index:nn_index])
                #print "Raw Message ", message
                zc_flag = 0
                nn_flag = 0

                message_asc = "".join(x for x in message if (ord(x) > 31 and ord(x) < 128) or ord(x) == 13 or ord(x) == 10 or ord(x) == 9)
                rx_text = []

                qsp(message_asc, stat1)
        
        
            else:
                rx_text = []
                zc_flag = 0
                nn_flag = 0

    except:
        rx_text = []
    
    
    
    time.sleep(2)
    
    
