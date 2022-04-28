import xmlrpclib
import time

s = xmlrpclib.ServerProxy("http://192.168.21.107:7362")


global snrlist
snrlist=[0]
global statlist
statlist=[0]
global count
count=0
global n
n=1
global p
p=0
global plast
plast=[]


def getmma(n,p,pm):
    
    pm = (((n-1)*pm)+p)/n
    
    return pm


def get_status():
    global plast
    global p
    global n
    global count
    global snrlist
    global statlist
    f = s.main.get_frequency()
    car = s.modem.get_carrier()
    rfc = f + car
    trx = s.main.get_trx_status().upper()
    modem = s.modem.get_name()
    bw = s.rig.get_bandwidth()
    r = s.main.get_reverse()
    
    
    
    #### SNR AVERAGING
    ##
    if modem != "RTTY":
        stat1 = s.main.get_status1()
    else:
        stat1 = s.main.get_status2()
    
    
    try:
        statlist = stat1.rsplit(" ")
    except:
        pass
    
    try:
        snr = statlist[-2]
    except:
        snr="--"

    if snr != "":
        try:
            snrlist.append(float(snr))
        except:
            pass
        
    if len(snrlist)>60:
        snrlist.pop(0)    
    
    
   
    #if len(snrlist)>0:
    #    for i in snrlist:
    #        total += i
    #        av = round((total / len(snrlist)), 1)
    #else:
    #    av = "none"
    
    ####
    # Calculate Modified Moving Average of the 60-second averages
    #
    
    if snr != "--": # snr is set to "--" when it's not possible to split the status1 value - ie when there's no signal
        try:
            s1 = float(snr)
        except:
            pass

    else: # when there's no signal we hold the current value and reset the sample count to 1
        s1 = p
        n = 1
        plast=[]

    p = getmma(n,s1,p) # get the MMA s1 = new value, p = last MMA
    n +=1 # increment the sample count
    # limit to 10 minutes
    if n > 60:

        plast.append(round(p,1))
        if len(plast)>5:
            plast.pop(0)
        n = 1
    
    
    total = 0
    if len(plast) > 1:
        for i in plast:
            total += i
            av = round((total / len(plast)),1)
    else:
        av = "--"

    ### max / min
    ##

    mx = snrlist[0]
    for i in snrlist:
        if i > mx:
            mx = i

    mn = snrlist[0]
    for i in snrlist:
        if i < mn:
            mn = i

    #print "max %s / min %s" % (mx,mn)

    #print snrlist
    #print "snr ", snr
    #print "ave ", av
    
    #print snrlist
    stat2 = s.main.get_status2()
    rid = s.main.get_rsid()
    tid = s.main.get_txid()
    sql = s.main.get_squelch()
    if r == 1:
        rev = "Rev"
    else:
        rev = "Nor"
    
    if rid == 1:
        rxid = "RxID"
    else:
        rxid = "R---"
    
    if tid == 1:
        txid = "TxID"
    else:
        txid = "T---"
    #if sql == 1:
    #    snrlist=[]
    #print sql
    #else:
    #   sq = "Closed"
    count += 1
    if count == 1:
        star = " \\"
    elif count == 2:
        star = " /"
        count = 0 
    
    if trx == "RX":
        print "%s %0.3f %s %0.3f %s %s %s %s %s %s %d %s (%s < snr < %s) %0.1f %s %s" % (star, f/1000, car, rfc/1000 , bw, trx, modem, rev, rxid, txid, sql, snr,mn, mx, p, plast, av)
    
    return


while True:
    get_status()
    time.sleep(1)


