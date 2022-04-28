#! /usr/bin/env python
import xmlrpclib
import radio_functions_ic7200 as radio
import time
import math
from Tkinter import *
import threading
from subprocess import call

HOST="127.0.0.1"
s = xmlrpclib.ServerProxy("http://"+HOST+":7362")


class App():
    def __init__(self, master):
        
        frame=Frame(master)
        frame.grid()

        #self.pwr_l=StringVar()
        #self.pwr_a=StringVar()

        #l_pwr = Label(frame, textvariable=self.pwr_l)
        #l_pwr.grid(column=0, row=0)
        #l_ave = Label(frame, textvariable=self.pwr_a)
        #l_ave.grid(column=0, row=1)
        

        self.control_f=Frame(frame)
        self.control_f.grid(column=0, row=0, columnspan=4)
        
        self.c=Canvas(frame, width=310, height=20, bg='black')
        self.c.grid(column=0, row=1, columnspan=5)
        

        self.c1 = Canvas(frame, width=310, height=100, bg='black')
        self.c1.grid(column=0, row=4, columnspan=5)

        self.nb=IntVar()
        self.nb_c=Checkbutton(self.control_f,text="NB", variable=self.nb, command=lambda: nb_on())
        self.nb_c.grid(row=0, column=0, sticky=EW)
        self.nb_c.deselect()

        self.anf=IntVar()
        self.anf_c=Checkbutton(self.control_f,text="ANF", variable=self.anf, command=lambda: anf_on())
        self.anf_c.grid(row=0, column=1, sticky=EW)
        
        self.dig=IntVar()
        self.dig_c=Checkbutton(self.control_f,text="Dig", variable=self.dig, command=lambda:dig_on())
        self.dig_c.grid(row=0, column=2, sticky=EW)
        self.dig_c.select()
        
        self.apc=IntVar()
        self.apc_c=Checkbutton(self.control_f, text="APC", variable=self.apc)
        self.apc_c.grid(row=0,column=3, sticky=EW)
        self.apc_c.select()

        self.pwr_l=StringVar()
        self.l_pwr=Label(self.control_f, textvariable=self.pwr_l)
        self.l_pwr.grid(row=0, column=4, sticky=EW)
        
        self.apc_l=StringVar()
        self.l_apc=Label(self.control_f, textvariable=self.apc_l)
        self.l_apc.grid(row=0, column=5, sticky=EW)


def read_target():
    target_file = open("/home/gm4slv/bin/target", "r")
    target=int(target_file.readline())
    #print "In read_target() with ", target
    return target

def nb_on():
    nb_state= app.nb.get()
    if nb_state == 1:
        radio.nb_on()
    elif nb_state == 0:
        radio.nb_off()
    return

def anf_on():
    anf_state= app.anf.get()
    if anf_state == 1:
        radio.anf_on()
    elif anf_state == 0:
        radio.anf_off()
    return

def dig_on():
    dig_state= app.dig.get()
    if dig_state == 1:
        radio.dig_on()
    elif dig_state == 0:
        radio.dig_off()
    return


def fld_trx():
    fld_trx = s.main.get_trx_status()
    global pollcnt
    if fld_trx == "tx" or fld_trx == "tune":
        pollcnt += 1
        #radio.dig_on()
        pwr_ctrl()
        radio.ptt_on()
        #poll_pwr(False)
    else:
        poll_pwr(True)
        radio.ptt_off()
        #poll_m()
        poll_bw()
        poll_f()
        poll_sm()
        pollcnt = 0
        app.apc_l.set(".")
    return

def pwr_ctrl():
    global pollcnt
    target=float(read_target())
    curpwr= float(poll_pwr(False))
    #print "pollcnt ", pollcnt
    #print "target %0.1f current %0.1f" % (target, curpwr)
    if pollcnt > 10 and app.apc.get():
        app.apc_l.set("|")
        if curpwr/target > 1.26 or curpwr > 100:
            if curpwr/target > 1.58:
                print "target %0.1f current %0.1f" % (target, curpwr)
                print "minus 2"
                app.apc_l.set("<<")
                pollcnt = 5
                call(["/home/gm4slv/bin/minus2.sh", ""])
            else:
                print "target %0.1f current %0.1f" % (target, curpwr)
                print "minus 1"
                app.apc_l.set("<")
                pollcnt = 5
                call(["/home/gm4slv/bin/minus1.sh", ""])
        elif curpwr/target < 0.79: # -1dB
            if curpwr/target < 0.63:
                print "target %0.1f current %0.1f" % (target, curpwr)
                print "plus 2"
                app.apc_l.set(">>")
                pollcnt = 5
                call(["/home/gm4slv/bin/plus2.sh", ""])
            else:
                print "target %0.1f current %0.1f" % (target, curpwr)
                print "plus 1"
                app.apc_l.set(">")
                pollcnt = 5
                call(["/home/gm4slv/bin/plus1.sh", ""])
    else:
        pass
        #app.apc_l.set("")
    return

def get_freq():
    freq = s.main.get_frequency()
    return freq
  
def set_freq(freq):
    rig_f = freq - carrier
    freq = s.main.set_frequency(rig_f)
    radio_dial = float(rig_f / 1000 )
    radio.set_freq(str(radio_dial))
    return freq
    
def get_rigmode():
    rigmode = s.rig.get_mode()
    return rigmode
   
def get_fbw():
    fbw = s.rig.get_bandwidth()
    return fbw


def poll_sm():
    smeter = radio.get_smeter()
    smeter_list.append(float(smeter))
    if len(smeter_list) > 150:
        smeter_list.pop(0)

    #print "Smeter ", smeter
    y_stretch = 1.4
    y_gap = 0
    x_stretch = 0
    x_width = 2
    x_gap = 0
    height = 100
    app.c1.delete(ALL)
    app.c1.create_line(0, 100 - (-73 + 123)*y_stretch, 310, 100 - (-73 + 123)*y_stretch, fill='red')
    app.c1.create_line(305, 100 - (-79 + 123)*y_stretch, 310, 100 - (-79 + 123)*y_stretch, fill='white')
    app.c1.create_line(0, 100 - (-85 + 123)*y_stretch, 310, 100 - (-85 + 123)*y_stretch, fill='white')
    app.c1.create_line(305, 100 - (-91 + 123)*y_stretch, 310, 100 - (-91 + 123)*y_stretch, fill='white')
    app.c1.create_line(0, 100 - (-97 + 123)*y_stretch, 310, 100 - (-97 + 123)*y_stretch, fill='white')
    app.c1.create_line(305, 100 - (-103 + 123)*y_stretch, 310, 100 - (-103 + 123)*y_stretch, fill='white')
    app.c1.create_line(0, 100 - (-109 + 123)*y_stretch, 310, 100 - (-109 + 123)*y_stretch, fill='white')
    app.c1.create_line(305, 100 - (-115 + 123)*y_stretch, 310, 100 - (-115 + 123)*y_stretch, fill='white')
    app.c1.create_line(0, 100 - (-121 + 123)*y_stretch, 310, 100 - (-121 + 123)*y_stretch, fill='white')
    t = 300
    while t > 30:
        app.c1.create_line(t, 0, t, 100, fill="white")
        t -= 60 
    seq=smeter_list
    for x, y in enumerate(seq):
        yd = y + 123
        x0 = x * x_stretch + x * x_width + x_gap
        y0 = height - (yd * y_stretch + y_gap)
        x1 = x * x_stretch + x * x_width + x_width + x_gap
        y1 = height - y_gap
        app.c1.create_rectangle(x0, y0, x1, y1, fill="yellow")
    return


def poll_f():
    fld_dial = get_freq() / 1000
    
    radio_dial = float(radio.get_freq())
    if fld_dial != radio_dial: 
        #print "Fld dial ", fld_dial
        #print "radio dial ", radio_dial
        radio.set_freq(fld_dial)
        #print "new radio freq ", radio.get_freq()

def poll_m():
    fld_rigmode = get_rigmode()
    radio_mode = radio.get_mode()
    #print "fld mode ", fld_rigmode
    #print "radio mode ", radio_mode
    if fld_rigmode != radio_mode:
        radio.set_mode(fld_rigmode)
        #print "New radio mode ", radio.get_mode()

def poll_bw():
    fld_rigbw = get_fbw()
    #print "fld_rigbw ", fld_rigbw
    bw = (int(fld_rigbw) + 400) / 100
    #print bw
    radio.set_bw(bw)
    return

def poll_pwr(clear):
    global pwrmtr_list
    rig_pwrmtr = radio.get_pwrmtr()
    pwrmtr = math.pow(float(rig_pwrmtr),1.783759) * 0.005094455
    pwrmtr = pwrmtr * 1.02

    #print "Rig %s, power %f" % (rig_pwrmtr, pwrmtr) 
    pwrmtr_list.append(pwrmtr)
    #print pwrmtr_list
    #s = pwrmtr_list
    total = 0
    for i in pwrmtr_list:
        total += i
    avepwr = (total / len(pwrmtr_list))
    maxpwr = pwrmtr_list[0]
    for i in pwrmtr_list:
        if i > maxpwr:
            maxpwr = i
    if clear:
        pwrmtr_list=[]

    if len(pwrmtr_list) > 5:
        pwrmtr_list.pop(0)
    #print "Pwr: %0.1f, ave pwr: %0.1f  maxpwr: %0.1f" % (pwrmtr, avepwr, maxpwr)
        
    #app.pwr_l.set(str(round(pwrmtr,1)))
    #app.pwr_a.set(str(round(avepwr,1)))
    app.pwr_l.set(round(maxpwr,1))
    
    app.c.delete(ALL)
    app.c.create_rectangle(avepwr*3, 15, maxpwr*3, 5, fill="red")
    app.c.create_rectangle(0, 15,avepwr*3, 5, fill="green")
    app.c.create_line(pwrmtr*3, 0, pwrmtr*3, 10, fill="yellow", width="2", dash=(2,1))
    app.c.create_line(30, 0, 30, 7, fill="white")
    app.c.create_line(60, 0, 60, 7, fill="white")
    app.c.create_line(90, 0, 90, 7, fill="white")
    app.c.create_line(120, 0, 120, 7, fill="white")
    app.c.create_line(150, 0, 150, 10, fill="white")
    app.c.create_line(180, 0, 180, 7, fill="white")
    app.c.create_line(210, 0, 210, 7, fill="white")
    app.c.create_line(240, 0, 240, 7, fill="white")
    app.c.create_line(270, 0, 270, 7, fill="white")
    app.c.create_line(300, 0, 300, 10, fill="white")

    return maxpwr

#print s.rig.get_modes()

mode_list = [ "USB" ]
bw_list = ["500", "600", "900", "1200", "1500", "1800", "2100", "2400", "2700"]

s.rig.set_bandwidths(bw_list)

s.rig.set_modes(mode_list)
s.rig.set_name("IC7200")
#radio.set_txpower("3")
#radio.dim_on()
radio.set_mode("USB")
s.rig.set_mode("USB")
#s.rig.set_bandwidth("2700")
global pwrmtr_list

pwrmtr_list=[]
smeter_list=[-123]*150
radio.nb_off()
radio.anf_off()
radio.dig_on()
global pollcnt
pollcnt = 0


def main():
    start_f=float(radio.get_freq()) * 1000
    s.main.set_frequency(start_f)
    start_bw=str((int(radio.get_bw()) * 100) - 400)
    s.rig.set_bandwidth(start_bw)

    while True:
        try:
            #radio.dig_on()
            #poll_f()
            #poll_m()
            #poll_bw()
            fld_trx()
            #    poll_pwr(False)
        except:
            pass
        #    print "exception in poll"
        time.sleep(1)

if __name__ == "__main__":
    version = "0.2"
    root=Tk()
    root.title("GM4SLV IC7200 "+ version)
    root.geometry("-100+100")
    app=App(root)

    m1 = threading.Thread(target=main)
    m1.setDaemon(True)
    m1.start()

    root.mainloop()
    


