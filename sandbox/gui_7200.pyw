#! /usr/bin/env python

from Tkinter import *
import socket
import threading
import time
import math
import xmlrpclib
import tkFont

HOST="raspi"

s = xmlrpclib.ServerProxy("http://"+HOST+":7362")

class Network(object):
    def __init__(self):
        self.sock = self.make_con()
        
    def make_con(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, 9999))
        return self.sock

    def connect(self, data):
        try:
            lock.acquire()
            self.sock.sendall(data + "\n")
            self.received = self.sock.recv(2048)
        finally:
            lock.release()
            return self.received

class nRadio(object):
    def __init__(self, master, radio):

        self.master = master        
        self.radio = radio
        
        self.num = "".join(("r", self.radio))
        
        self.smeter_list = [-123]*150
        self.pwrmtr_list = []
        
        try:
            self.fld_mode_on()
        except:
            pass
        
        ######################################################################
        #####
        ###   Here starts the GUI
        #
        
        radio_frame = Frame(master, borderwidth=2, relief=GROOVE)
        radio_frame.grid(columnspan=6)
        
        #####
        ### Data_frame : freq / last tuned / TX power setting / power meter
        #
        data_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        data_frame.grid(row=0, column=0, rowspan=3, sticky=EW)
        
        Label(data_frame, text="Freq/kHz", width=10).grid(row=0, column=0, sticky=W)
        Label(data_frame, text="Last Tuned", width=10).grid(row=0, column=1, sticky=W)
        Label(data_frame, text="Av. Power", width=10).grid(row=0, column=2, sticky=W)
        Label(data_frame, text="Pk. Power", width=10).grid(row=0, column=3, sticky=W)
        
        self.freq_l = StringVar()
        self.l_freq = Label(data_frame, fg='red', textvariable=self.freq_l, width=10)
        self.l_freq.grid(row=1, column=0, sticky=W)
        
        self.e_freq = Entry(data_frame, width=10, bg = 'white', fg = 'black', insertbackground = 'blue')
        self.e_freq.grid(row=2, column=0)
        self.e_freq.focus()
        self.e_freq.bind('<Return>', (lambda event: self.set_freq(self.num)))
        
        self.b_tune = Button(data_frame, text = "Tune", command = lambda: self.atutune(self.num))
        self.b_tune.grid(row = 2, column = 1)
        
        self.b_qsy = Button(data_frame, text = "QSY", command = lambda: self.fld_qsy())
        self.b_qsy.grid(row = 2, column = 2)
        
        self.b_home = Button(data_frame, text = "Home", command = lambda: self.home(self.num))
        self.b_home.grid(row = 2, column = 3)
        
        self.last_tuned_l = StringVar()
        self.l_last_tuned = Label(data_frame, textvariable=self.last_tuned_l, width=10)
        self.l_last_tuned.grid(row=1, column=1, sticky=W)
        self.last_tuned_l.set("0")
        
        self.pwrmtr_l = StringVar()
        self.l_pwrmtr = Label(data_frame, textvariable=self.pwrmtr_l, width=10)
        self.l_pwrmtr.grid(row=1, column=2, sticky=W)
        
        self.maxpwr_l = StringVar()
        self.l_maxpwr = Label(data_frame, textvariable=self.maxpwr_l, width=10)
        self.l_maxpwr.grid(row=1, column=3, sticky=W)
        
        self.c2 = Canvas(data_frame, width=310, height=15, bg='black')
        self.c2.grid(row=3, column=0, columnspan=4)   
        
        #####
        ### Mode_frame : mode selection radio butons
        #
        mode_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        mode_frame.grid(row=3, column=0, rowspan=3, sticky=EW)
        
        self.mode_l = StringVar()
        
        self.rb_mode_usb = Radiobutton(mode_frame, text="USB", variable=self.mode_l, value="USB", command = lambda: self.set_mode("usb", self.num))
        self.rb_mode_usb.grid(row=3, column = 0)
        
        self.rb_mode_lsb = Radiobutton(mode_frame, text="LSB", variable=self.mode_l, value="LSB", command=lambda: self.set_mode("lsb", self.num))
        self.rb_mode_lsb.grid(row=3, column=1)
        
        self.rb_mode_data = Radiobutton(mode_frame, text="RTTY", variable=self.mode_l, value="RTTY", command=lambda: self.set_mode("rtty", self.num))
        self.rb_mode_data.grid(row=3, column=2)
        
        self.rb_mode_cw = Radiobutton(mode_frame, text="CW", variable=self.mode_l, value="CW", command=lambda: self.set_mode("cw", self.num))
        self.rb_mode_cw.grid(row=3, column=3)
        
        self.rb_mode_am = Radiobutton(mode_frame, text="AM", variable=self.mode_l, value="AM", command=lambda: self.set_mode("am", self.num))
        self.rb_mode_am.grid(row=3, column=4)
        
        #####
        ### Controls_frame : pre-amp etc
        #
        controls_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        controls_frame.grid(row=6, column=0, rowspan = 3, sticky=EW)
         
        self.l_pre = Label(controls_frame, width=3, text="Pre")
        self.l_pre.grid(row=1, column=0, sticky=W)
        self.pre = IntVar()
        self.cb_pre = Checkbutton(controls_frame, variable=self.pre, command=lambda: self.preamp_onoff(self.num))
        self.cb_pre.grid(row=2, column=0, sticky=W)

        self.l_att = Label(controls_frame,width=3,text="Att")
        self.l_att.grid(row=1, column=1, sticky=W)
        self.att = IntVar()
        self.cb_att = Checkbutton(controls_frame, variable=self.att, command=lambda: self.att_onoff(self.num))
        self.cb_att.grid(row=2, column=1, sticky=W)
        
        self.l_nb = Label(controls_frame,width=3, text="NB")
        self.l_nb.grid(row=1, column=2, sticky=W)
        self.nb = IntVar()
        self.cb_nb = Checkbutton(controls_frame, variable=self.nb, command=lambda: self.nb_onoff(self.num))
        self.cb_nb.grid(row=2, column=2, sticky=W)
        
        self.l_anf = Label(controls_frame,width=3, text="ANF")
        self.l_anf.grid(row=1, column=3, sticky=W)
        self.anf = IntVar()
        self.cb_anf = Checkbutton(controls_frame, variable=self.anf, command=lambda: self.anf_onoff(self.num))
        self.cb_anf.grid(row=2, column=3, sticky=W)
        
        self.l_nr = Label(controls_frame,width=3, text="NR")
        self.l_nr.grid(row=1, column=4, sticky=W)
        self.nr = IntVar()
        self.cb_nr = Checkbutton(controls_frame, variable=self.nr, command=lambda: self.nr_onoff(self.num))
        self.cb_nr.grid(row=2, column=4, sticky=W)
        
        
        self.l_dig = Label(controls_frame,width=3, text="Dig")
        self.l_dig.grid(row=1, column=5, sticky=W)
        self.digv = IntVar()
        self.cb_dig = Checkbutton(controls_frame, variable=self.digv, command=lambda: self.dig_onoff(self.num))
        self.cb_dig.grid(row=2, column=5, sticky=W)
        
        self.l_ptt = Label(controls_frame,width=3,text="PTT")
        self.l_ptt.grid(row=1, column=6, sticky=W)
        self.pttvar = IntVar()
        self.cb_ptt = Checkbutton(controls_frame, variable=self.pttvar, command=lambda: self.ptt_onoff(self.num))
        self.cb_ptt.grid(row=2, column=6, sticky=W)
        
        
        
        self.nr_l = StringVar()
        self.l_nr_l = Label(controls_frame, text="NR Level")
        self.l_nr_l.grid(row=3, column=0, columnspan=2)
        self.rb_nr_1 = Radiobutton(controls_frame, text = "1", variable=self.nr_l, value="24", command = lambda: self.set_nr_l(self.num))
        self.rb_nr_1.grid(row=3, column=2)
        self.rb_nr_2 = Radiobutton(controls_frame, text = "2", variable=self.nr_l, value="40", command = lambda: self.set_nr_l(self.num))
        self.rb_nr_2.grid(row=3, column=3)
        self.rb_nr_3 = Radiobutton(controls_frame, text = "3", variable=self.nr_l, value="56", command = lambda: self.set_nr_l(self.num))
        self.rb_nr_3.grid(row=3, column=4)
        self.rb_nr_4 = Radiobutton(controls_frame, text = "4", variable=self.nr_l, value="72", command = lambda: self.set_nr_l(self.num))
        self.rb_nr_4.grid(row=3, column=5)
        self.rb_nr_5 = Radiobutton(controls_frame, text = "5", variable=self.nr_l, value="88", command = lambda: self.set_nr_l(self.num))
        self.rb_nr_5.grid(row=3, column=6)
        self.rb_nr_6 = Radiobutton(controls_frame, text = "6", variable=self.nr_l, value="104", command = lambda: self.set_nr_l(self.num))
        self.rb_nr_6.grid(row=3, column=7, sticky=W)
        self.rb_nr_7 = Radiobutton(controls_frame, text = "7", variable=self.nr_l, value="120", command = lambda: self.set_nr_l(self.num))
        self.rb_nr_7.grid(row=3, column=8, sticky=W)
        #####
        ### Bandwidth_frame : bandwidth selection Radio Buttons
        #
        bw_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        bw_frame.grid(row=9, column=0,rowspan=3, sticky=EW)
        
        self.bwframe_l=Label(bw_frame, text="IF Bandwidth (Hz)")
        self.bwframe_l.grid(row=0, column=0, columnspan=2)
        
        self.bw_l = StringVar()
        
        self.rb_bw_0 = Radiobutton(bw_frame, text="50", variable=self.bw_l, value = "50", command = lambda: self.set_bw("00",self.num))
        self.rb_bw_0.grid(row = 8, column = 0)
        
        self.rb_bw_1 = Radiobutton(bw_frame, text="150", variable=self.bw_l, value = "150", command = lambda: self.set_bw("02",self.num))
        self.rb_bw_1.grid(row = 8, column = 1)
   
        self.rb_bw_2 = Radiobutton(bw_frame, text="300", variable=self.bw_l, value = "300", command = lambda: self.set_bw("05",self.num))
        self.rb_bw_2.grid(row = 8, column = 2)
                
        self.rb_bw_3 = Radiobutton(bw_frame, text="600", variable=self.bw_l, value = "600", command = lambda: self.set_bw("10",self.num))
        self.rb_bw_3.grid(row = 8, column = 3)
         
        self.rb_bw_4 = Radiobutton(bw_frame, text="900", variable=self.bw_l, value = "900", command = lambda: self.set_bw("13",self.num))
        self.rb_bw_4.grid(row = 8, column = 4)

        self.rb_bw_5 = Radiobutton(bw_frame, text="1k2", variable=self.bw_l, value = "1200", command = lambda: self.set_bw("16",self.num))
        self.rb_bw_5.grid(row = 8, column = 5)

        self.rb_bw_6 = Radiobutton(bw_frame, text="1k5", variable=self.bw_l, value = "1500", command = lambda: self.set_bw("19",self.num))
        self.rb_bw_6.grid(row = 9, column = 0)
        
        self.rb_bw_7 = Radiobutton(bw_frame, text="1k8", variable=self.bw_l, value = "1800", command = lambda: self.set_bw("22",self.num))
        self.rb_bw_7.grid(row = 9, column = 1)
        
        self.rb_bw_8 = Radiobutton(bw_frame, text="2k1", variable=self.bw_l, value = "2100", command = lambda: self.set_bw("25",self.num))
        self.rb_bw_8.grid(row = 9, column = 2)
        
        self.rb_bw_9 = Radiobutton(bw_frame, text="2k4", variable=self.bw_l, value = "2400", command = lambda: self.set_bw("28",self.num))
        self.rb_bw_9.grid(row = 9, column = 3)
        
        self.rb_bw_10 = Radiobutton(bw_frame, text="2k7", variable=self.bw_l, value = "2700", command = lambda: self.set_bw("31",self.num))
        self.rb_bw_10.grid(row = 9, column = 4)
        
        self.rb_bw_11 = Radiobutton(bw_frame, text="3k0", variable=self.bw_l, value = "3000", command = lambda: self.set_bw("34",self.num))
        self.rb_bw_11.grid(row = 9, column = 5)
        
        #####
        ### Qrg_frame : quick qsy up/down buttons
        #
        qrg_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        qrg_frame.grid(row=12, column=0, rowspan=3, sticky=EW)
        
        self.qrgframe_l=Label(qrg_frame, text="VFO Up/Down (Hz)")
        self.qrgframe_l.grid(row=0, column=0, columnspan=2)
        
        self.b_freq_up = Button(qrg_frame, text = "+1000", width = 4, command = lambda: self.qsy_up("1.00",self.num))
        self.b_freq_up.grid(row = 5, column = 0)
        
        self.b_freq_dn = Button(qrg_frame, text = "-1000", width = 4, command = lambda: self.qsy_dn("1.00",self.num))
        self.b_freq_dn.grid(row = 6, column = 0)
        
        self.b_freq_up = Button(qrg_frame, text = "+500", width = 4, command = lambda: self.qsy_up("0.500",self.num))
        self.b_freq_up.grid(row = 5, column = 1)
        
        self.b_freq_dn = Button(qrg_frame, text = "-500", width = 4, command = lambda: self.qsy_dn("0.500",self.num))
        self.b_freq_dn.grid(row = 6, column = 1)
        
        self.b_freq_up = Button(qrg_frame, text = "+100", width = 4, command = lambda: self.qsy_up("0.100",self.num))
        self.b_freq_up.grid(row = 5, column = 2)
        
        self.b_freq_dn = Button(qrg_frame, text = "-100", width = 4, command = lambda: self.qsy_dn("0.100",self.num))
        self.b_freq_dn.grid(row = 6, column = 2)
        
        self.b_freq_up = Button(qrg_frame, text = "+10", width = 4, command = lambda: self.qsy_up("0.010",self.num))
        self.b_freq_up.grid(row = 5, column = 3)
        
        self.b_freq_dn = Button(qrg_frame, text = "-10", width = 4, command = lambda: self.qsy_dn("0.010",self.num))
        self.b_freq_dn.grid(row = 6, column = 3)
        
        self.b_freq_up = Button(qrg_frame, text = "+1", width = 4, command = lambda: self.qsy_up("0.001",self.num))
        self.b_freq_up.grid(row = 5, column = 4)
        
        self.b_freq_dn = Button(qrg_frame, text = "-1", width = 4, command = lambda: self.qsy_dn("0.001",self.num))
        self.b_freq_dn.grid(row = 6, column = 4)
        
        #####
        ### Power_frame : TX Power setting radio buttons
        #
        power_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        power_frame.grid(row=15, column=0, rowspan=2, sticky=EW)
        
        self.pwr_l = StringVar()
       
        self.pwrbutton_l=Label(power_frame, text="TX Power (Watts)").grid(row=0, column=0, columnspan=2)
        self.pwr_1_rb = Radiobutton(power_frame, text = "1W", variable = self.pwr_l, value = "2", command = lambda: self.set_pwr("2", self.num))
        self.pwr_1_rb.grid(row=8, column = 0)
        
        self.pwr_10_rb = Radiobutton(power_frame, text = "10W", variable = self.pwr_l, value = "25", command = lambda: self.set_pwr("25", self.num))
        self.pwr_10_rb.grid(row=8, column = 1)
        
        self.pwr_25_rb = Radiobutton(power_frame, text = "20W", variable = self.pwr_l, value = "63", command = lambda: self.set_pwr("63", self.num))
        self.pwr_25_rb.grid(row=8, column = 2)
       
        self.pwr_50_rb = Radiobutton(power_frame, text = "50W", variable = self.pwr_l, value = "127", command = lambda: self.set_pwr("127", self.num))
        self.pwr_50_rb.grid(row=8, column = 3)
       
        self.pwr_100_rb = Radiobutton(power_frame, text = "100W", variable = self.pwr_l, value = "255", command = lambda: self.set_pwr("255", self.num))
        self.pwr_100_rb.grid(row=8, column = 4)
     
        #####
        ### Signal_frame : S-Meter readings / graph
        # 
        signal_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        signal_frame.grid(row=18, column=0, rowspan=5, sticky=EW)
        
        Label(signal_frame, text="Signal/dBm", width=10).grid(row=0, column=0)
        Label(signal_frame, text="S No.", width=10).grid(row=0, column=1)
        Label(signal_frame, text="dBm/Hz", width=10).grid(row=0, column=2)
       
        Label(signal_frame, text="Min/dBm", width=10, fg='blue').grid(row=2, column=0)
        Label(signal_frame, text="Ave/dBm", width=10, fg='green').grid(row=2, column=1)
        Label(signal_frame, text="Max/dBm", width=10, fg='red').grid(row=2, column=2)
        #Label(signal_frame, text="QSB/dB", width=10).grid(row=2, column=3)
        
        self.smeter_l = StringVar()
        self.l_smeter = Label(signal_frame, textvariable=self.smeter_l, width=10)
        self.l_smeter.grid(row=1, column=0)

        self.max_var = StringVar()
        self.l_max = Label(signal_frame, textvariable=self.max_var, width=10)
        self.l_max.grid(row=3, column=2)
        
        self.ave_var = StringVar()
        self.l_average = Label(signal_frame, textvariable=self.ave_var, width=10)
        self.l_average.grid(row=3, column=1)

        self.min_var = StringVar()
        self.l_min = Label(signal_frame, textvariable=self.min_var, width=10)
        self.l_min.grid(row=3, column=0)
        
        #self.qsb_var = StringVar()
        #self.l_min = Label(signal_frame, textvariable=self.qsb_var, width=10)
        #self.l_min.grid(row=3, column=3)
        
        self.sdens_var = StringVar()
        self.l_sdens = Label(signal_frame, textvariable=self.sdens_var, width=10)
        self.l_sdens.grid(row=1, column=2)
    
        self.sno_var = StringVar()
        self.l_sno_var = Label(signal_frame, textvariable=self.sno_var, width=10)
        self.l_sno_var.grid(row=1, column=1)
    
        self.c1 = Canvas(signal_frame, width=310, height=100, bg='black')
        self.c1.grid(row=4, column=0, columnspan=4, rowspan=3)
        
        self.fld_l = StringVar()
        self.l_fld = Label(master, textvariable=self.fld_l)
        self.l_fld.grid(row=26, column=0, columnspan=3)

    ##############################################################################
    #####   Functions
    ###
    #
    
    ##### 
    ###   get_ functions
    #
    def get_all(self):
        self.fldigi_state = 0
        self.get_freq(self.num)
        self.get_mode(self.num)
        if not self.pttvar.get():
            self.get_smeter(self.num)
            self.graph_points() 
        self.get_pwr(self.num)
        self.get_preamp(self.num)
        self.get_nb(self.num)
        self.get_anf(self.num)
        self.get_nr(self.num)
        self.get_nr_l(self.num)
        self.get_atten(self.num)
        self.avg()
        self.smax()
        self.smin()
        #self.qsb()
        self.get_bw(self.num)
        self.sig_density()
        self.peak_hold()
        try:
            self.fld_poll()
            self.fldigi_state +=1
        except:
            pass
        self.get_dig(self.num)
        self.get_pwrmtr(self.num)
        if self.fldigi_state:
            if self.digv.get() != 1:
                if self.mode_l.get() != "CW" and self.mode_l.get() != "RTTY":
                    self.cb_dig.select()
                    self.dig_onoff(self.num)
                else:
                    pass
            else:
                pass
            self.cb_dig.config(state=DISABLED)
            self.cb_ptt.config(state=DISABLED)
            self.fld_l.set("Fldigi connected")
            self.l_fld["fg"]="green"
        else:
            self.cb_ptt.config(state=NORMAL)
            self.cb_dig.config(state=NORMAL)
            self.fld_l.set("Fldigi not connected")
            self.l_fld["fg"]="red"
        return

    def get_anf(self, radio):
        self.anfstate = n1.connect("getanf" + " " + radio)
        if self.anfstate == "1":
            self.cb_anf.select()
        elif self.anfstate == "0":
            self.cb_anf.deselect()
        return

    def get_atten(self, radio):
        self.atten = n1.connect("getatt" + " " + radio)
        if self.atten == "1":
            self.cb_att.select()
        elif self.atten == "0":
            self.cb_att.deselect()
        return
    
    def get_bw(self, radio):
        self.bw = float(n1.connect("getbw" + " " + radio))
        if self.bw < 10:
            self.bwhz = 50 * (self.bw + 1)
        else:
            self.bwhz = 100 * (self.bw - 4)
        self.bw_l.set(int(self.bwhz))
        return
        
    def get_dig(self, radio):
        self.digstate = n1.connect("getdig" + " " + radio)
        if self.digstate == "1":
            self.cb_dig.select()
        elif self.digstate == "0":
            self.cb_dig.deselect()
        return
    
    def get_freq(self, radio):

        self.freq = n1.connect("getfreq" + " " + radio)
        self.freq_l.set(self.freq)
        if 100 * abs((float(self.freq) - float(self.last_tuned_l.get())) / float(self.freq)) > 1.3:
            self.l_last_tuned["fg"]="red"
            self.l_freq["fg"]="red"
        else:
            self.l_last_tuned["fg"]="green"
            self.l_freq["fg"]="green"
        return
            
    def get_mode(self, radio):
        self.mode = n1.connect("getmode" + " " + radio)
        self.mode_l.set(self.mode)
        return

    def get_nb(self, radio):
        self.nblank = n1.connect("getnb" + " " + radio)
        if self.nblank == "1":
            self.cb_nb.select()
        elif self.nblank == "0":
            self.cb_nb.deselect()
        return
        
    def get_nr(self, radio):
        self.nrstate = n1.connect("getnr" + " " + radio)
        if self.nrstate == "1":
            self.cb_nr.select()
        elif self.nrstate == "0":
            self.cb_nr.deselect()
        return
        
    def get_nr_l(self, radio):
        self.nrlevel = n1.connect("getnrl" + " " + radio)
        #print "NR Level ", self.nrlevel
        self.nr_l.set(self.nrlevel)
        #self.pwr_l.set(self.pwr)
        return
    
    def get_preamp(self, radio):
        self.preamp = n1.connect("getpreamp" + " " + radio)
        if self.preamp == "1":
            self.cb_pre.select()
        elif self.preamp == "0":
            self.cb_pre.deselect()
        return
    
    def get_pwr(self, radio):
        self.pwr = n1.connect("getpwr" + " " + radio)
        self.pwr_l.set(self.pwr)
        return
        
    def get_pwrmtr(self, radio):
        self.rig_pwrmtr = n1.connect("getpwrmtr" + " " + radio)
        self.pwrmtr = math.pow(float(self.rig_pwrmtr),1.783759) * 0.005094455
        self.pwrmtr = self.pwrmtr * 1.02
        # correct for freq response - roughly 10% out away from 60m
        pwr_freq = float(self.freq_l.get())
        if pwr_freq < 3800 or pwr_freq > 5900:
            self.pwrmtr = self.pwrmtr * 1.1
        self.pwrmtr_list.append(self.pwrmtr)
        s = self.pwrmtr_list
        total = 0
        for i in s:
            total += i
        self.avepwr = round((total / len(s)), 1)
        self.pwrmtr_l.set(self.avepwr)
        self.maxpwr = s[0]
        for i in s:
            if i > self.maxpwr:
                self.maxpwr = i
        self.maxpwr_l.set(str(round(self.maxpwr,1)))
        
        if len(self.pwrmtr_list) > 5:
            self.pwrmtr_list.pop(0)
        
        self.c2.delete(ALL)
        self.c2.create_rectangle(self.avepwr*3, 15, self.maxpwr*3, 5, fill="red")
        self.c2.create_rectangle(0, 15, self.avepwr*3, 5, fill="green")
        self.c2.create_line(self.pwrmtr*3, 0, self.pwrmtr*3, 10, fill="yellow", width="2", dash=(2,1))
        self.c2.create_line(30, 0, 30, 7, fill="white")
        self.c2.create_line(60, 0, 60, 7, fill="white")
        self.c2.create_line(90, 0, 90, 7, fill="white")
        self.c2.create_line(120, 0, 120, 7, fill="white")
        self.c2.create_line(150, 0, 150, 10, fill="white")
        self.c2.create_line(180, 0, 180, 7, fill="white")
        self.c2.create_line(210, 0, 210, 7, fill="white")
        self.c2.create_line(240, 0, 240, 7, fill="white")
        self.c2.create_line(270, 0, 270, 7, fill="white")
        self.c2.create_line(300, 0, 300, 10, fill="white")
        
        return
        
    def get_smeter(self, radio):
        self.smeter = n1.connect("getsmeter" + " " + radio)
        self.smeter_list.append(float(self.smeter))
        self.smeter_l.set(self.smeter)
        if len(self.smeter_list) > 150:
            self.smeter_list.pop(0)
        return
    
    def home(self, radio):
        home_freq = "5366.5"
        home_mode = "USB"
        self.newfreq = n1.connect("setfreq" + " " + home_freq + " " + radio)
        try:
            self.fld_set_freq(home_freq)
        except:
            pass
        
        try:
            self.fld_set_rigmode(home_mode)
        except:
            pass
        
        return
        
    ##### 
    ###   set_ functions
    #
    
    def set_bw(self, bw, radio):
        self.new_bw = n1.connect("setbw" + " " + bw + " " + radio)
        return
    
    def set_freq(self, radio):
        self.freq = str(self.e_freq.get())
        self.newfreq = n1.connect("setfreq" + " " + self.freq + " " + radio)
        self.e_freq.delete(0, END)
        try:
            self.fld_set_freq(self.freq)
        except:
            pass
        self.e_freq.delete(0, END)
        return
        
    def set_mode(self, mode, radio):
        self.newmode = n1.connect("setmode" + " " + mode + " " + radio)
        try:
            self.fld_set_rigmode(mode)
        except:
            pass
        return

    def set_nr_l(self, radio):
        nrl = self.nr_l.get()
        self.newnrl = n1.connect("setnrl" + " " + nrl + " " + radio)
        return

    def set_pwr(self, pwr, radio):
        self.newpwr = n1.connect("setpwr" + " " + pwr + " " + radio)
        return

    
    #####
    ###   various other functions
    #
    
    def atutune(self, radio):
        self.last_tuned_l.set(self.freq_l.get())
        self.tune = n1.connect("tune" + " " + radio)
        self.l_last_tuned["fg"]="green"
        return
    
    def avg(self):
        s = self.smeter_list[-30:]
        total = 0
        for i in s:
            total += i
        self.av = round((total / len(s)), 1)
        self.ave_var.set(str(self.av))
        self.c1.create_line(240, 100 - (self.av + 123)*1.4, 310, 100 - (self.av + 123)*1.4, fill="green", width="2", dash=(5,3))
        return self.av
    
    def graph_points(self):
        seq = self.smeter_list
        y_stretch = 1.4
        y_gap = 0
        x_stretch = 0
        x_width = 2
        x_gap = 0
        height = 100
        self.c1.delete(ALL)
        self.c1.create_line(0, 100 - (-73 + 123)*y_stretch, 310, 100 - (-73 + 123)*y_stretch, fill='white')
        self.c1.create_line(305, 100 - (-79 + 123)*y_stretch, 310, 100 - (-79 + 123)*y_stretch, fill='white')
        self.c1.create_line(0, 100 - (-85 + 123)*y_stretch, 310, 100 - (-85 + 123)*y_stretch, fill='white')
        self.c1.create_line(305, 100 - (-91 + 123)*y_stretch, 310, 100 - (-91 + 123)*y_stretch, fill='white')
        self.c1.create_line(0, 100 - (-97 + 123)*y_stretch, 310, 100 - (-97 + 123)*y_stretch, fill='white')
        self.c1.create_line(305, 100 - (-103 + 123)*y_stretch, 310, 100 - (-103 + 123)*y_stretch, fill='white')
        self.c1.create_line(0, 100 - (-109 + 123)*y_stretch, 310, 100 - (-109 + 123)*y_stretch, fill='white')
        self.c1.create_line(305, 100 - (-115 + 123)*y_stretch, 310, 100 - (-115 + 123)*y_stretch, fill='white')
        self.c1.create_line(0, 100 - (-121 + 123)*y_stretch, 310, 100 - (-121 + 123)*y_stretch, fill='white')
        t = 300
        while t > 30:
            self.c1.create_line(t, 0, t, 100, fill="white")
            t -= 60
        
        for x, y in enumerate(seq):
            yd = y + 123
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = height - (yd * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = height - y_gap
            self.c1.create_rectangle(x0, y0, x1, y1, fill="yellow")
        return
   
    def peak_hold(self):
        s_last = self.smeter_list[-3:]
        
        #print s_5
        self.mhold = s_last[0]
        
        for i in s_last:
            if i > self.mhold:
                self.mhold = i
        #print "maxHold ", self.mhold
        if self.mhold > -53:
            self.sno = "S9+20"
        elif self.mhold > -63:
            self.sno = "S9+10"
        elif self.mhold > -73:
            self.sno = "S9"
        elif self.mhold > -79:
            self.sno = "S8"
        elif self.mhold > -85:
            self.sno = "S7"
        elif self.mhold > -91:
            self.sno = "S6"
        elif self.mhold > -97:
            self.sno = "S5"
        elif self.mhold > -103:
            self.sno = "S4"
        elif self.mhold > -109:
            self.sno = "S3"
        elif self.mhold > -115:
            self.sno = "S2"
        elif self.mhold > -121:
            self.sno = "S1"
        else:
            self.sno = "S0"
        #print self.sno
        self.sno_var.set(str(self.sno))
        return
    
    def qsb(self):
        maxs = float(self.max_var.get())
        mins = float(self.min_var.get())
        qsb = maxs - mins
        self.qsb_var.set(str(qsb))
        return
        
    def qsy_dn(self, delta, radio):
        self.qsy = float(delta)
        self.cur_freq = float(n1.connect("getfreq" + " " + radio))
        self.new_freq = self.cur_freq - self.qsy
        self.newfreq = n1.connect("setfreq" + " " + str(self.new_freq) + " " + radio)
        try:
            self.fld_qsy_freq((self.cur_freq - self.qsy)*1000)
        except:
            pass
        return

    def qsy_up(self, delta, radio):
        self.qsy = float(delta)
        self.cur_freq = float(n1.connect("getfreq" + " " + radio))
        self.new_freq = self.cur_freq + self.qsy
        self.newfreq = n1.connect("setfreq" + " " + str(self.new_freq) + " " + radio)
        try:
            self.fld_qsy_freq((self.cur_freq + self.qsy)*1000)
        except:
            pass
        return
    
    def sig_density(self):
        nbandw = float(self.bw_l.get())
        s_average = float(self.ave_var.get())
        bwl = 10 * math.log(nbandw,10)
        s_dens = round(s_average-bwl,1)
        self.sdens_var.set(str(s_dens))
        return
        
    def smax(self):
        s = self.smeter_list[-30:]
        self.mx = s[0]
        for i in s:
            if i > self.mx:
                self.mx = i
        self.max_var.set(str(self.mx))
        self.c1.create_line(240, 100 - (self.mx + 123)*1.4, 310, 100 - (self.mx + 123)*1.4, fill="red", width="2",dash=(5,3))
        return self.mx
                
    def smin(self):
        s = self.smeter_list[-30:]
        self.mn = s[0]
        for i in s:
            if i < self.mn:
                self.mn = i
        self.min_var.set(str(self.mn))
        self.c1.create_line(240, 100 - (self.mn + 123)*1.4, 310, 100 - (self.mn + 123)*1.4, fill="blue", width="2", dash=(5,3))
        return self.mn
        
        
    #####
    ###   onoff functions
    #
    
    def anf_onoff(self, radio):
        self.anfstate = self.anf.get()
        if self.anfstate:
            n1.connect("anfon" + " " + radio)
        else:
            n1.connect("anfoff" + " " + radio)
        return
    
    def att_onoff(self, radio):
        self.attstate = self.att.get()
        if self.attstate:
            n1.connect("atton" + " " + radio)
        else:
            n1.connect("attoff" + " " + radio)
        return
    
    def dig_onoff(self, radio):
        self.digistate = self.digv.get()
        if self.digistate:
            n1.connect("digon" + " " + radio)
        else:
            n1.connect("digoff" + " " + radio)
        return
    
    def nb_onoff(self, radio):
        self.nbstate = self.nb.get()
        if self.nbstate:
            n1.connect("nbon" + " " + radio)
        else:
            n1.connect("nboff" + " " + radio)
        return
        
    def nr_onoff(self, radio):
        self.nrstate = self.nr.get()
        if self.nrstate:
            n1.connect("nron" + " " + radio)
        else:
            n1.connect("nroff" + " " + radio)
        return
    
    def preamp_onoff(self, radio):
        self.prestate = self.pre.get()
        if self.prestate:
            n1.connect("preampon" + " " + radio)
        else:
            n1.connect("preampoff" + " " + radio)
        return
        
    def ptt_onoff(self,radio):
        self.pttstate = self.pttvar.get()
        print "in ptt_onoff() with ", self.pttstate
        if self.pttstate:
            n1.connect("ptton" + " " + radio)
            # and Stop snr collection - set a flag to be
            # tested by something running via get_all()
            
        else:
            n1.connect("pttoff" + " " + radio)
            # and reset snr record and Start collection.
        return
    
    
    ###### 
    ###  XMLRPC Stuff........
    #
        
    def fld_get_freq(self):
        ffreq = s.main.get_frequency()
        return ffreq
    
    def fld_get_rigmode(self):
        frigmode = s.rig.get_mode()
        return frigmode  
    
    def fld_mode_on(self):
        if s.rig.get_modes():
            mode_list = [ "USB", "LSB" , "RTTY", "CW", "AM"]
            s.rig.set_modes(mode_list)
        return

    def fld_poll(self):
        s.rig.set_name("IC-7200")
        fld_dial = self.fld_get_freq() / 1000
        radio_dial = float(self.freq_l.get())
        if fld_dial != radio_dial: 
            self.newfreq = n1.connect("setfreq" + " " + str(fld_dial) + " " +self.num)
        fld_rigmode = self.fld_get_rigmode()
        radio_mode = self.mode_l.get()
        if fld_rigmode != radio_mode:
            self.set_mode(fld_rigmode, self.num)
        self.fld_trx()
        return
        
    def fld_qsy_freq(self, newfreq):
        s.main.set_frequency(newfreq)
        return
    
    def fld_qsy(self):
        try:
            cur_modem_carrier = s.modem.get_carrier()
            cur_dial_freq = s.main.get_frequency()
            new_dial_freq = (cur_dial_freq + cur_modem_carrier - 1500)
            s.modem.set_carrier(1500)
            s.main.set_frequency(new_dial_freq)
            
        except:
            pass
        return

    def fld_set_freq(self, freq):
        ffreq = float(freq) * 1000
        s.main.set_frequency(ffreq)
        return
        
    def fld_set_rigmode(self, mode):
        s.rig.set_mode(mode.upper())
        return
        
    def fld_trx(self):
        fld_trx = s.main.get_trx_status()
        
        if fld_trx == "tx":
            self.pttstate = self.pttvar.get()
            if self.pttstate != 1:
                self.cb_ptt.select()
                self.ptt_onoff(self.num)
        else:
            self.pttstate = self.pttvar.get()
            if self.pttstate != 0:
                self.cb_ptt.deselect()
                self.ptt_onoff(self.num)
        return

############################################################
#####
###
#

def main():
    while True:
        nRadio1.get_all()
        time.sleep(0.5)

    
if __name__ == "__main__":
    
    version = "v0.2"
    lock = threading.Lock()
    
    root = Tk()
    root.geometry("320x530")
    root.title("GM4SLV IC-7200 " + version)
    
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=8)

    n1 = Network()
    radio_count = 1
    
    nRadio1 = nRadio(root, "1")
    
    m1 = threading.Thread(target = main)
    m1.setDaemon(True)
    m1.start()
    
    root.mainloop()
    
    
    
    
