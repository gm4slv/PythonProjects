import json
import time
import cwid


import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


TT = 11

GPIO.setwarnings(False)

GPIO.setup(TT,GPIO.OUT)

WARN = 14 * 60
CLOSE = 15 * 60

#timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))

def write_file(text):
    filename = '/home/gm4slv/commandlog.txt'
    f = open(filename, 'a+')
    timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
    log = " ".join((timenow, text))
    print log
    f.write(log+"\n")
    f.close()
    return


write_file("++++++ Talkthrough watchdog enabled : %0.0f minute timeout period ++++++" % (CLOSE/60))

flag = 0
while True:


    saved = open('/home/gm4slv/status_dict.json')
    status_dict = json.load(saved)


    tt = status_dict["tt"]

    if tt == "ON":
        if flag == 0:
            #timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            write_file("++++++ Talkthrough on ++++++")
            t0 = time.time()
            flag = 1
        
        elapsed_time = time.time() -t0

        #print elapsed_time
        
        if elapsed_time > WARN:
        #if count > 6:
            #print "warn after ", elapsed_time
            cwid.cw_id("i i")
        
        if elapsed_time > CLOSE:
        #if count > 8:
            #timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            #print "close after ", elapsed_time
            write_file("++++++ Timeout ++++++")
            GPIO.output(TT,False)
            cwid.cw_id("de gm4slv +")
            status_dict["tt"] = "OFF"
            with open('/home/gm4slv/status_dict.json', 'wb') as outfile:
                json.dump(status_dict, outfile)
            flag = 0
        #count += 1
    else:
        if flag != 0:
            #timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            write_file("++++++ Talkthrough off ++++++")

        flag = 0
    time.sleep(20)
    
    #print "TT ",tt
    #print "flag ", flag
    
