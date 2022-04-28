import json
import time
import ann_tx


import RPi.GPIO as GPIO
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

TT = 11

GPIO.setup(TT,GPIO.OUT)


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


write_file("+++Talkthrough watchdog enabled")

count = 0
while True:


    saved = open('/home/gm4slv/status_dict.json')
    status_dict = json.load(saved)


    tt = status_dict["tt"]
    #print tt
    #print count
    if tt == "ON":
        if count == 0:
            #timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            write_file("+++Talkthrough on")
        if count > 358:
            ann_tx.ident("i i i")

        if count > 360:
            #timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            write_file("+++Timeout")
            ann_tx.ident("tt off +")
            GPIO.output(TT,False)
            status_dict["tt"] = "OFF"
            with open('/home/gm4slv/status_dict.json', 'wb') as outfile:
                json.dump(status_dict, outfile)
            count = 0
        count += 1
    else:
        if count > 0:
            #timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            write_file("+++Talkthrough off")

        count = 0
    time.sleep(10)

