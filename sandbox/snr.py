import xmlrpclib
import time

s = xmlrpclib.ServerProxy("http://192.168.21.101:7362")


global snrlist
snrlist=[]
global statlist
statlist=[]


def get_status():
    global snrlist
    global statlist
    
    modem = s.modem.get_name()
    if modem != "RTTY":
        stat1 = s.main.get_status1()
    else:
        stat1 = s.main.get_status2()

    #print "new stat1 ", stat1
    try:
        statlist = stat1.split(" ")
        #print statlist
    except:
        pass
        #print "problem splitting stat1"
    try:
        snr = statlist[1]
    except:
        #print "problem with statlist"
        snr=0

    #print "new snr ", snr
    if snr != "":
        try:
            snrlist.append(float(snr))
        except:
            pass
        
    #    pass
        #snrlist=[0]
    if len(snrlist)>15:
        snrlist.pop(0)    
    #print snrlist
    total = 0
    if len(snrlist)>0:
        for i in snrlist:
            total += i
            av = round((total / len(snrlist)), 1)
    else:
        av = "none"

    print snrlist
    print "snr ", snr
    print "ave ", av
    return


while True:
    get_status()
    time.sleep(1)


