import json
import time
import ann_tx


import RPi.GPIO as GPIO
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

TT = 11

GPIO.setup(TT,GPIO.OUT)


timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))

print timenow +  " Talkthrough watchdog enabled"
count = 0
while True:


    saved = open('/home/gm4slv/status_dict.json')
    status_dict = json.load(saved)


    tt = status_dict["tt"]
    #print tt
    #print count
    if tt == "ON":
        if count == 0:
            timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            print timenow + " Talkthrough on"
        if count > 180:
            timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            print timenow + " Timeout"
            ann_tx.ident("tt off +")
            GPIO.output(TT,False)
            status_dict["tt"] = "OFF"
            with open('/home/gm4slv/status_dict.json', 'wb') as outfile:
                json.dump(status_dict, outfile)
            count = 0
        count += 1
    else:
        if count > 0:
            timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
            print timenow + " Talkthrough off"

        count = 0
    time.sleep(10)

