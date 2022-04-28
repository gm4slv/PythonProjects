import time


print "Start", time.strftime("%H:%M:%S %a, %d %b, %Y", time.gmtime(time.time()))

while True:
    
    timenow = int(time.time())*10
    print timenow
    print timenow / 600.0
    
    if timenow % 600.0 == 0:
        timelog = time.strftime("%H:%M:%S %a, %d %b, %Y", time.gmtime(time.time()))
        print "stamp : ", timelog

    time.sleep(2)
