'''
Python NMEA Control panel for Icom IC-M710 Marine HF SSB Transceiver

    Copyright (C) 2015  John Pumford-Green

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


from Tkinter import *
import radio_functions_m710 as radio
#from mem import *
import json
import time
import tkSimpleDialog




class m710(object):
    def __init__(self, master):
        self.master = master
        
        radio.remote_on()
        try:
            mems = open('mem_list.txt')
            self.mem_list = json.load(mems)
        except:
            # 
            self.mem_list = [""] * 60
        try:
            modes = open('mode_list.txt')
            self.mode_list = json.load(modes)
        except:
            # 
            self.mode_list = ["USB"] * 60
        
        control_frame = Frame(master).grid()
        self.make_mem()
        
        Label(control_frame, text="Icom IC-M710 NMEA 0183 Controller",bg='darkgreen', fg='white', font=("",10,"bold")).grid(row = 0, column = 0, columnspan=4)
        
        
        Label(control_frame, text="Receiver", bg='darkgreen', fg='white').grid(row = 1, column = 0)
        
        self.rx_freq = StringVar()
        self.rx_l = Label(control_frame, textvariable=self.rx_freq, width = 10, bg='black', fg="green", font=("",14, "bold"))
        self.rx_l.grid(row=2, column = 0,padx=5)
        
        Label(control_frame, text="Transmitter", bg='darkgreen', fg='white').grid(row = 1, column = 2)
        
        self.store_b = Button(control_frame,bg='grey50',  text = "Store", command = lambda: self.store_mem())
        self.store_b.grid(row=2, column=1, padx=5)
        
        self.tx_freq = StringVar()
        self.tx_l = Label(control_frame, textvariable=self.tx_freq, bg='black', fg="green", font=("",14,"bold"), width = 10)
        self.tx_l.grid(row=2, column = 2,padx=5)
        
        self.e_rxfreq = Entry(control_frame, insertbackground='red', fg='red', bg='black',width=10, font=("",10,'bold'))
        self.e_rxfreq.grid(row=3, column=0)
        self.e_rxfreq.bind('<Return>', (lambda event: self.enter_rxfreq()))
        
        
        #self.simplex_l = Label(control_frame, text="Simplex")
        #self.simplex_l.grid(row = 2, column = 1)
        
        self.simplex=IntVar()
        self.simplex_cb = Checkbutton(control_frame,bg='grey50', text="Simplex", selectcolor='green', width=6, indicatoron=0, variable=self.simplex, command = lambda:self.do_simplex())
        self.simplex_cb.grid(row=3, column=1)
        
        
       
        
        self.e_txfreq = Entry(control_frame, insertbackground='red',disabledbackground='darkgreen',relief=FLAT, width=10,fg='red', bg='black',font=("",10,'bold'))
        self.e_txfreq.grid(row=3, column=2)
        self.e_txfreq.bind('<Return>', (lambda event: self.enter_txfreq()))
        
        
        
        
        delta_frame = Frame(control_frame, bg='darkgreen')
        delta_frame.grid(row=4, column = 0, columnspan = 5)
        
        self.delta = StringVar()
        self.qsy1m_r = Radiobutton(delta_frame, indicatoron=0, bg='grey50',  selectcolor='green', width=5, text="1MHz", variable=self.delta, value="1000")
        self.qsy1m_r.grid(row = 1, column = 0, padx=3)
        self.qsy100k_r = Radiobutton(delta_frame, indicatoron=0,bg='grey50', selectcolor='green', width=5, text="100kHz", variable=self.delta, value="100")
        self.qsy100k_r.grid(row = 1, column = 1, padx=3)
        self.qsy10k_r = Radiobutton(delta_frame,  indicatoron=0,bg='grey50', selectcolor='green', width=5,text="10kHz", variable=self.delta, value="10")
        self.qsy10k_r.grid(row = 1, column = 2, padx=3)
        self.qsy1k_r = Radiobutton(delta_frame,  indicatoron=0,bg='grey50', selectcolor='green', width=5,text="1kHz", variable=self.delta, value="1")
        self.qsy1k_r.grid(row = 1, column = 3, padx=3)
        self.qsy500h_r = Radiobutton(delta_frame, indicatoron=0,bg='grey50', selectcolor='green', width=5, text="500Hz", variable=self.delta, value="0.5")
        self.qsy500h_r.grid(row = 1, column = 4,padx=3)
        self.qsy100h_r = Radiobutton(delta_frame, indicatoron=0,bg='grey50', selectcolor='green', width=5, text="100Hz", variable=self.delta, value="0.1")
        self.qsy100h_r.grid(row = 1, column = 5,padx=3)
        
        
        spin_frame = Frame(control_frame, bg='darkgreen')
        spin_frame.grid(row = 5, column = 0, columnspan = 10)
        
        self.tunedn_b = Button(spin_frame, text = "Down",bg='grey50',  width = 5, command=lambda: self.down())
        self.tunedn_b.grid(row = 2 , column = 0,padx=3)
        
        self.delta_l = Label(spin_frame, bg='darkgreen', fg='white', text = "Tune", width = 6)
        self.delta_l.grid(row = 2 , column = 1,padx=3)
        
        
        self.tuneup_b = Button(spin_frame, text = "Up",bg='grey50',  width = 5, command=lambda: self.up())
        self.tuneup_b.grid(row = 2 , column = 3,padx=3)

        
        
        mode_frame = Frame(control_frame, bg='darkgreen')
        mode_frame.grid(row = 6, column = 0, columnspan = 5)
        
        self.mode = StringVar()
        
        
        self.usb_r = Radiobutton(mode_frame, text = "USB",bg='grey50',  selectcolor='green', font=("",10,'bold'), indicatoron=0, width=4, variable = self.mode, value = "USB", command = lambda: self.new_mode("USB"))
        self.usb_r.grid(row = 1, column = 0,padx=3,pady=3)
        self.lsb_r = Radiobutton(mode_frame, text = "LSB", bg='grey50', selectcolor='green', font=("",10,'bold'),indicatoron=0, width=4, variable = self.mode, value = "LSB", command = lambda: self.new_mode("LSB"))
        self.lsb_r.grid(row = 1, column = 1,padx=3,pady=3)
        self.cw_r = Radiobutton(mode_frame, text = "AM",bg='grey50', selectcolor='green', font=("",10,'bold'), indicatoron=0, width=4, variable = self.mode, value = "AM", command = lambda: self.new_mode("AM"))
        self.cw_r.grid(row = 1, column = 2,padx=3,pady=3)
        self.am_r = Radiobutton(mode_frame, text = "CW",bg='grey50',  selectcolor='green', font=("",10,'bold'),indicatoron=0, width=4, variable = self.mode, value = "CW", command = lambda: self.new_mode("CW"))
        self.am_r.grid(row = 1, column = 3,padx=3,pady=3)
        self.j2_r = Radiobutton(mode_frame, text = "J2B", bg='grey50', selectcolor='green', font=("",10,'bold'),indicatoron=0, width=4,  variable = self.mode, value = "J2B", command = lambda: self.new_mode("J2B"))
        self.j2_r.grid(row = 1, column = 4,padx=3,pady=3)
        self.fsk_r = Radiobutton(mode_frame, text = "FSK",bg='grey50', selectcolor='green', font=("",10,'bold'), indicatoron=0,width=4,  variable = self.mode, value = "FSK", command = lambda: self.new_mode("FSK"))
        self.fsk_r.grid(row = 1, column = 5,padx=3,pady=3)
        self.r3e_r = Radiobutton(mode_frame, text = "R3E",bg='grey50', selectcolor='green', font=("",10,'bold'), indicatoron=0,width=4, variable = self.mode, value = "R3E", command = lambda: self.new_mode("R3E"))
        self.r3e_r.grid(row = 1, column = 6,padx=3,pady=3)
        
        
        atu_frame = Frame(control_frame, bg='darkgreen')
        atu_frame.grid(row=7, column = 0, columnspan = 5)
        
        self.tune_b = Button(atu_frame,activebackground='red',bg='grey50',  text = "ATU Tune", command = lambda: self.tune())
        self.tune_b.grid(row = 7, column = 0,padx=5,pady=3)
        
        self.tune_t = IntVar()
        self.tune1_r = Radiobutton(atu_frame,indicatoron=0, bg='grey50', selectcolor='green', width=4, text = "2s", value = 2, variable=self.tune_t)
        self.tune1_r.grid(row = 7, column = 1,padx=3,pady=3)
        self.tune5_r = Radiobutton(atu_frame,indicatoron=0, bg='grey50', selectcolor='green', width=4, text = "5s", value = 5, variable=self.tune_t)
        self.tune5_r.grid(row = 7, column = 2,padx=3,pady=3)
       
        self.tune1_r.select()
        
        button_frame = Frame(control_frame, bg='darkgreen')
        button_frame.grid(row = 8, column = 0, columnspan = 5)
        
        self.sp=IntVar()
        self.sp_cb = Checkbutton(button_frame,indicatoron=0, bg='grey50', selectcolor='green', width=6, text = "Speaker", variable=self.sp, command = lambda:self.speaker())
        self.sp_cb.grid(row=1, column=0,padx=3,pady=3)
        
        self.sql=IntVar()
        self.sql_cb = Checkbutton(button_frame,indicatoron=0,bg='grey50',  selectcolor='green', width=5, text = "SQL", variable=self.sql, command = lambda:self.sqlc())
        self.sql_cb.grid(row=1, column=4,padx=3,pady=3)
        
        self.nb=IntVar()
        self.nb_cb = Checkbutton(button_frame, indicatoron=0, bg='grey50', selectcolor='green', width=5,text = "NB", variable=self.nb, command = lambda:self.nbc())
        self.nb_cb.grid(row=1, column=3,padx=3,pady=3)
        
        self.agc=IntVar()
        self.agc_cb = Checkbutton(button_frame, indicatoron=0,bg='grey50',  selectcolor='green', width=5,text = "AGC", variable=self.agc, command = lambda:self.agcc())
        self.agc_cb.grid(row=1, column=2,padx=3,pady=3)
       
        self.dim=IntVar()
        self.dim_cb = Checkbutton(button_frame, indicatoron=0,bg='grey50',  selectcolor='green', width=5,text = "Dim", variable=self.dim, command = lambda:self.dimc())
        self.dim_cb.grid(row=1, column=1,padx=3,pady=3)
        
        self.txp_l = Label(button_frame, bg='darkgreen', fg='white', text="TX Power")
        self.txp_l.grid(row = 2, column = 0,padx=3,pady=3)
        
        self.txp = StringVar()
        self.txp3_r = Radiobutton(button_frame,bg='grey50',  text = "High",selectcolor='green',width=4, font=("",10,'bold'), indicatoron=0,  variable=self.txp, value = "3", command = lambda: self.txpc("3"))
        self.txp3_r.grid(row=2, column=3)
        self.txp2_r = Radiobutton(button_frame,bg='grey50',  text = "Mid",selectcolor='green',width=4, font=("",10,'bold'), indicatoron=0,  variable=self.txp, value = "2", command = lambda: self.txpc("2"))
        self.txp2_r.grid(row=2, column=2)
        self.txp1_r = Radiobutton(button_frame, bg='grey50', text = "Low",selectcolor='green', width=4, font=("",10,'bold'), indicatoron=0,  variable=self.txp, value = "1", command = lambda: self.txpc("1"))
        self.txp1_r.grid(row=2, column=1)
        
        self.rem_l = Label(button_frame, bg='darkgreen', fg='white', text="Remote")
        self.rem_l.grid(row = 3, column = 0,padx=3,pady=3)
        
        self.remote_flag = IntVar()
        self.remoteon_b = Radiobutton(button_frame, bg='grey50', text="On", indicatoron=0, width=4,font=("",10,'bold'),selectcolor='green', variable=self.remote_flag, value=1, command = lambda: self.remote_toggle())
        self.remoteon_b.grid(row = 3, column = 1,padx=3,pady=3)
        
        self.remoteoff_b = Radiobutton(button_frame, bg='grey50', text="Off", selectcolor='green',font=("",10,'bold'), width=4,indicatoron=0, variable=self.remote_flag, value=0, command = lambda: self.remote_toggle())
        self.remoteoff_b.grid(row = 3, column = 2,padx=3,pady=3)
        
        #########
        #
        # Keypad frame
        
     
        
        key_frame = Frame(control_frame, bg='darkgreen')
        key_frame.grid(row = 0, column = 11, rowspan = 8, sticky=N+S+W+E, padx=10, pady=10)
        self.qsy_r_b = IntVar()
        self.rx_r = Radiobutton(key_frame,bg='grey50',  text="RX", font=("",11,"bold"), indicatoron = 0,selectcolor='green', variable = self.qsy_r_b, value = 1, width=4, command=lambda: self.qsy_rx())
        self.rx_r.grid(row = 0, column = 0, sticky=N+S+W+E)       
        self.rcl_b = Button(key_frame,bg='grey50',  text="CLR", font=("",11,"bold"), width=4, command=lambda: self.clr())
        self.rcl_b.grid(row = 0, column = 1, sticky=N+S+W+E)
        self.tx_r = Radiobutton(key_frame,bg='grey50',  text="TX", font=("",11,"bold"), indicatoron=0,selectcolor='green', variable = self.qsy_r_b, value = 0, width=4, command=lambda:self.qsy_tx())
        self.tx_r.grid(row = 0, column = 2, sticky=N+S+W+E)
        
        self.k1_b = Button(key_frame,bg='grey50',  text="1", font=("",11,"bold"), width=4, command=lambda: self.qsy_entry("1"))
        self.k1_b.grid(row = 3, column = 0, sticky=N+S+W+E)       
        self.k2_b = Button(key_frame,bg='grey50',  text="2", font=("",11,"bold"),width=4, command=lambda: self.qsy_entry("2"))
        self.k2_b.grid(row = 3, column = 1, sticky=N+S+W+E)
        self.k3_b = Button(key_frame,bg='grey50',  text="3", font=("",11,"bold"),width=4, command=lambda: self.qsy_entry("3"))
        self.k3_b.grid(row = 3, column = 2, sticky=N+S+W+E)
        self.k4_b = Button(key_frame,bg='grey50',  text="4", font=("",11,"bold"),width=4, command=lambda: self.qsy_entry("4"))
        self.k4_b.grid(row = 2, column = 0, sticky=N+S+W+E)
        self.k5_b = Button(key_frame,bg='grey50',  text="5", font=("",11,"bold"), width=4,command=lambda: self.qsy_entry("5"))
        self.k5_b.grid(row = 2, column = 1, sticky=N+S+W+E)
        self.k6_b = Button(key_frame,bg='grey50',  text="6", font=("",11,"bold"),width=4, command=lambda: self.qsy_entry("6"))
        self.k6_b.grid(row = 2, column = 2, sticky=N+S+W+E)
        self.k7_b = Button(key_frame,bg='grey50',  text="7", font=("",11,"bold"),width=4, command=lambda: self.qsy_entry("7"))
        self.k7_b.grid(row = 1, column = 0, sticky=N+S+W+E)
        self.k8_b = Button(key_frame,bg='grey50',  text="8", font=("",11,"bold"),width=4,command=lambda: self.qsy_entry("8") )
        self.k8_b.grid(row = 1, column = 1, sticky=N+S+W+E)
        self.k9_b = Button(key_frame,bg='grey50',  text="9", font=("",11,"bold"), width=4, command=lambda: self.qsy_entry("9"))
        self.k9_b.grid(row = 1, column = 2, sticky=N+S+W+E)
        self.k0_b = Button(key_frame,bg='grey50',  text="0", font=("",11,"bold"), width=4,command=lambda: self.qsy_entry("0"))
        self.k0_b.grid(row = 4, column = 0, sticky=N+S+W+E)
        self.k0_b = Button(key_frame,bg='grey50',  text=".", font=("",11,"bold"),width=4, command=lambda: self.qsy_entry("."))
        self.k0_b.grid(row = 4, column = 1, sticky=N+S+W+E)
        self.enter_b = Button(key_frame,bg='grey50',  text="Go", font=("",11,"bold"), width=4,command = lambda:self.qsy() )
        self.enter_b.grid(row = 4, column = 2, sticky=N+S+W+E)
        
        self.blank = Label(key_frame, bg='darkgreen')
        self.blank.grid(row = 5, column = 0, columnspan = 3)
        
        self.voldn_b = Button(key_frame,bg='grey50',  text = "AF -", width=4, font = ("", 11, "bold"), command=lambda: self.vol_dn())
        self.voldn_b.grid(row = 6, column = 0)
        
        self.volume = StringVar()
        self.vol_l = Label(key_frame,  bg='darkgreen', fg='white' ,textvariable = self.volume)
        self.vol_l.grid(row = 6, column = 1)
        
        self.volup_b = Button(key_frame,bg='grey50',  text = "AF +", width=4, font = ("", 11, "bold"), command=lambda: self.vol_up())
        self.volup_b.grid(row = 6, column = 2)

        self.rfdn_b = Button(key_frame,bg='grey50',  text = "RF -", width=4, font = ("", 11, "bold"), command=lambda: self.rf_dn())
        self.rfdn_b.grid(row = 7, column = 0)
        
        self.rfgain = StringVar()
        self.rfg_l = Label(key_frame, bg='darkgreen', fg='white', textvariable = self.rfgain)
        self.rfg_l.grid(row = 7, column = 1)
        
        self.rfup_b = Button(key_frame, bg='grey50', text = "RF +", width=4, font = ("", 11, "bold"), command=lambda: self.rf_up())
        self.rfup_b.grid(row = 7, column = 2)
        
        
        self.mode.set(radio.get_mode())
        self.rx_freq.set(radio.get_rxfreq())
        self.tx_freq.set(radio.get_txfreq())
        self.txp.set(radio.get_txpower())
        
        self.remoteon_b.invoke()
        self.sp_cb.invoke()
        self.agc_cb.invoke()
        #self.dim_cb.invoke()
        
        self.volume.set(radio.get_vol())
        self.rfgain.set(radio.get_rfg())
        self.delta.set(1)
        radio.agc_on()
        radio.nb_off()
        
        #self.sql_cb.invoke()
        self.simplex_cb.invoke()
        self.rx_r.invoke()
        self.qsyflag="rx"
        
        #self.store_mem(0,"5366.5")
        #print self.mem_list
        
        ############
        # Memory Channel Buttons
    def make_mem(self):
        self.mem_frame = Toplevel(bg='darkgreen')
        self.mem_frame.geometry("+0+0")
        self.mem_frame.title("Presets")
        self.mem_frame.protocol('WM_DELETE_WINDOW', self.close)
        self.mem_frame.grid()
        
        
        self.ch00_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="1: "+self.mem_list[0]+"\n"+self.mode_list[0], width=12,  command = lambda: self.memory_tune(0))
        self.ch00_b.grid(row=0, column=0,padx=3,pady=3,sticky=E+W)
        self.ch01_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="2: "+self.mem_list[1]+"\n"+self.mode_list[1], width=12,  command = lambda: self.memory_tune(1))
        self.ch01_b.grid(row=0, column=1,padx=3,pady=3,sticky=E+W)
        self.ch02_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="3: "+self.mem_list[2]+"\n"+self.mode_list[2], width=12,  command = lambda: self.memory_tune(2))
        self.ch02_b.grid(row=0, column=2,padx=3,pady=3,sticky=E+W)
        self.ch03_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="4: "+self.mem_list[3]+"\n"+self.mode_list[3],  width=12, command = lambda: self.memory_tune(3))
        self.ch03_b.grid(row=0, column=3,padx=3,pady=3,sticky=E+W)    
        self.ch04_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="5: "+self.mem_list[4]+"\n"+self.mode_list[4], width=12,command = lambda: self.memory_tune(4))
        self.ch04_b.grid(row=0, column=4,padx=3,pady=3,sticky=E+W)
        
        self.ch10_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="6: "+self.mem_list[5]+"\n"+self.mode_list[5], width=12,command = lambda: self.memory_tune(5))
        self.ch10_b.grid(row=1, column=0,padx=3,pady=3,sticky=E+W)
        self.ch11_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="7: "+self.mem_list[6]+"\n"+self.mode_list[6], width=12,command = lambda: self.memory_tune(6))
        self.ch11_b.grid(row=1, column=1,padx=3,pady=3,sticky=E+W)
        self.ch12_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="8: "+self.mem_list[7]+"\n"+self.mode_list[7], width=12,command = lambda: self.memory_tune(7))
        self.ch12_b.grid(row=1, column=2,padx=3,pady=3,sticky=E+W)
        self.ch13_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="9: "+self.mem_list[8]+"\n"+self.mode_list[8], width=12,  command = lambda: self.memory_tune(8))
        self.ch13_b.grid(row=1, column=3,padx=3,pady=3,sticky=E+W)   
        self.ch14_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="10: "+self.mem_list[9]+"\n"+self.mode_list[9],  width=12, command = lambda: self.memory_tune(9))
        self.ch14_b.grid(row=1, column=4,padx=3,pady=3,sticky=E+W)
        
        
        self.ch20_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="11: "+self.mem_list[10]+"\n"+self.mode_list[10],  width=12, command = lambda: self.memory_tune(10))
        self.ch20_b.grid(row=2, column=0,padx=3,pady=3,sticky=E+W)
        self.ch21_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="12: "+self.mem_list[11]+"\n"+self.mode_list[11], width=12,command = lambda: self.memory_tune(11))
        self.ch21_b.grid(row=2, column=1,padx=3,pady=3,sticky=E+W) 
        self.ch22_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="13: "+self.mem_list[12]+"\n"+self.mode_list[12], width=12,command = lambda: self.memory_tune(12))
        self.ch22_b.grid(row=2, column=2,padx=3,pady=3,sticky=E+W)
        self.ch23_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="14: "+self.mem_list[13]+"\n"+self.mode_list[13], width=12,command = lambda: self.memory_tune(13))
        self.ch23_b.grid(row=2, column=3,padx=3,pady=3,sticky=E+W)
        self.ch24_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="15: "+self.mem_list[14]+"\n"+self.mode_list[14], width=12,command = lambda: self.memory_tune(14))
        self.ch24_b.grid(row=2, column=4,padx=3,pady=3,sticky=E+W)
        
        
        self.ch30_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="16: "+self.mem_list[15]+"\n"+self.mode_list[15], width=12,command = lambda: self.memory_tune(15))
        self.ch30_b.grid(row=3, column=0,padx=3,pady=3,sticky=E+W)  
        self.ch31_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="17: "+self.mem_list[16]+"\n"+self.mode_list[16], width=12,command = lambda: self.memory_tune(16))
        self.ch31_b.grid(row=3, column=1,padx=3,pady=3,sticky=E+W)
        self.ch32_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="18: "+self.mem_list[17]+"\n"+self.mode_list[17], width=12,command = lambda: self.memory_tune(17))
        self.ch32_b.grid(row=3, column=2,padx=3,pady=3,sticky=E+W)
        self.ch33_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="19: "+self.mem_list[18]+"\n"+self.mode_list[18], width=12,command = lambda: self.memory_tune(18))
        self.ch33_b.grid(row=3, column=3,padx=3,pady=3,sticky=E+W)
        self.ch34_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="20: "+self.mem_list[19]+"\n"+self.mode_list[19], width=12,command = lambda: self.memory_tune(19))
        self.ch34_b.grid(row=3, column=4,padx=3,pady=3,sticky=E+W)
  
  
        self.ch40_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="21: "+self.mem_list[20]+"\n"+self.mode_list[20], width=12,command = lambda: self.memory_tune(20))
        self.ch40_b.grid(row=4, column=0,padx=3,pady=3,sticky=E+W)
        self.ch41_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="22: "+self.mem_list[21]+"\n"+self.mode_list[21], width=12,command = lambda: self.memory_tune(21))
        self.ch41_b.grid(row=4, column=1,padx=3,pady=3,sticky=E+W)
        self.ch42_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="23: "+self.mem_list[22]+"\n"+self.mode_list[22], width=12,command = lambda: self.memory_tune(22))
        self.ch42_b.grid(row=4, column=2,padx=3,pady=3,sticky=E+W)
        self.ch43_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="24: "+self.mem_list[23]+"\n"+self.mode_list[23], width=12,command = lambda: self.memory_tune(23))
        self.ch43_b.grid(row=4, column=3,padx=3,pady=3,sticky=E+W)     
        self.ch44_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="25: "+self.mem_list[24]+"\n"+self.mode_list[24], width=12,command = lambda: self.memory_tune(24))
        self.ch44_b.grid(row=4, column=4,padx=3,pady=3,sticky=E+W)

        
        self.ch50_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="26: "+self.mem_list[25]+"\n"+self.mode_list[25], width=12,command = lambda: self.memory_tune(25))
        self.ch50_b.grid(row=5, column=0,padx=3,pady=3,sticky=E+W)
        self.ch51_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="27: "+self.mem_list[26]+"\n"+self.mode_list[26], width=12,command = lambda: self.memory_tune(26))
        self.ch51_b.grid(row=5, column=1,padx=3,pady=3,sticky=E+W)
        self.ch52_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="28: "+self.mem_list[27]+"\n"+self.mode_list[27], width=12,command = lambda: self.memory_tune(27))
        self.ch52_b.grid(row=5, column=2,padx=3,pady=3,sticky=E+W)    
        self.ch53_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="29: "+self.mem_list[28]+"\n"+self.mode_list[28], width=12,command = lambda: self.memory_tune(28))
        self.ch53_b.grid(row=5, column=3,padx=3,pady=3,sticky=E+W)
        self.ch54_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="30: "+self.mem_list[29]+"\n"+self.mode_list[29], width=12,  command = lambda: self.memory_tune(29))
        self.ch54_b.grid(row=5, column=4,padx=3,pady=3,sticky=E+W)
        
        
        self.ch60_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="31: "+self.mem_list[30]+"\n"+self.mode_list[30], width=12,command = lambda: self.memory_tune(30))
        self.ch60_b.grid(row=6, column=0,padx=3,pady=3,sticky=E+W)
        self.ch61_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="32: "+self.mem_list[31]+"\n"+self.mode_list[31],  width=12, command = lambda: self.memory_tune(31))
        self.ch61_b.grid(row=6, column=1,padx=3,pady=3,sticky=E+W)  
        self.ch62_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="33: "+self.mem_list[32]+"\n"+self.mode_list[32], width=12,command = lambda: self.memory_tune(32))
        self.ch62_b.grid(row=6, column=2,padx=3,pady=3,sticky=E+W)
        self.ch63_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="34: "+self.mem_list[33]+"\n"+self.mode_list[33], width=12,command = lambda: self.memory_tune(33))
        self.ch63_b.grid(row=6, column=3,padx=3,pady=3,sticky=E+W)
        self.ch64_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="35: "+self.mem_list[34]+"\n"+self.mode_list[34], width=12,command = lambda: self.memory_tune(34))
        self.ch64_b.grid(row=6, column=4,padx=3,pady=3,sticky=E+W)
        
        self.ch70_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="36: "+self.mem_list[35]+"\n"+self.mode_list[35], width=12,command = lambda: self.memory_tune(35))
        self.ch70_b.grid(row=7, column=0,padx=3,pady=3,sticky=E+W)
        self.ch71_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="37: "+self.mem_list[36]+"\n"+self.mode_list[36], width=12,command = lambda: self.memory_tune(36))
        self.ch71_b.grid(row=7, column=1,padx=3,pady=3,sticky=E+W)
        self.ch72_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="38: "+self.mem_list[37]+"\n"+self.mode_list[37], width=12,command = lambda: self.memory_tune(37))
        self.ch72_b.grid(row=7, column=2,padx=3,pady=3,sticky=E+W)
        self.ch73_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="39: "+self.mem_list[38]+"\n"+self.mode_list[38], width=12,command = lambda: self.memory_tune(38))
        self.ch73_b.grid(row=7, column=3,padx=3,pady=3,sticky=E+W)
        self.ch74_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="40: "+self.mem_list[39]+"\n"+self.mode_list[39],  width=12, command = lambda: self.memory_tune(39))
        self.ch74_b.grid(row=7, column=4,padx=3,pady=3,sticky=E+W)
        
        self.ch80_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="41: "+self.mem_list[40]+"\n"+self.mode_list[40], width=12,  command = lambda: self.memory_tune(40))
        self.ch80_b.grid(row=8, column=0,padx=3,pady=3,sticky=E+W)
        self.ch81_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="42: "+self.mem_list[41]+"\n"+self.mode_list[41], width=12,command = lambda: self.memory_tune(41))
        self.ch81_b.grid(row=8, column=1,padx=3,pady=3,sticky=E+W)
        self.ch82_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="43: "+self.mem_list[42]+"\n"+self.mode_list[42], width=12,  command = lambda: self.memory_tune(42))
        self.ch82_b.grid(row=8, column=2,padx=3,pady=3,sticky=E+W)
        self.ch83_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="44: "+self.mem_list[43]+"\n"+self.mode_list[43], width=12,command = lambda: self.memory_tune(43))
        self.ch83_b.grid(row=8, column=3,padx=3,pady=3,sticky=E+W)    
        self.ch84_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="45: "+self.mem_list[44]+"\n"+self.mode_list[44],  width=12, command = lambda: self.memory_tune(44))
        self.ch84_b.grid(row=8, column=4,padx=3,pady=3,sticky=E+W)
        
        
        self.ch90_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="46: "+self.mem_list[45]+"\n"+self.mode_list[45], width=12,  command = lambda: self.memory_tune(45))
        self.ch90_b.grid(row=9, column=0,padx=3,pady=3,sticky=E+W)
        self.ch91_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="47: "+self.mem_list[46]+"\n"+self.mode_list[46],  width=12, command = lambda: self.memory_tune(46))
        self.ch91_b.grid(row=9, column=1,padx=3,pady=3,sticky=E+W)
        self.ch92_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="48: "+self.mem_list[47]+"\n"+self.mode_list[47], width=12,command = lambda: self.memory_tune(47))
        self.ch92_b.grid(row=9, column=2,padx=3,pady=3,sticky=E+W)
        self.ch93_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="49: "+self.mem_list[48]+"\n"+self.mode_list[48], width=12,command = lambda: self.memory_tune(48))
        self.ch93_b.grid(row=9, column=3,padx=3,pady=3,sticky=E+W)
        self.ch94_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="50: "+self.mem_list[49]+"\n"+self.mode_list[49], width=12,command = lambda: self.memory_tune(49))
        self.ch94_b.grid(row=9, column=4,padx=3,pady=3,sticky=E+W)
        
        
        self.ch100_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="51: "+self.mem_list[50]+"\n"+self.mode_list[50], width=12,command = lambda: self.memory_tune(50))
        self.ch100_b.grid(row=10, column=0,padx=3,pady=3,sticky=E+W)
        self.ch101_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="52: "+self.mem_list[51]+"\n"+self.mode_list[51], width=12,command = lambda: self.memory_tune(51))
        self.ch101_b.grid(row=10, column=1,padx=3,pady=3,sticky=E+W)  
        self.ch102_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="53: "+self.mem_list[52]+"\n"+self.mode_list[52], width=12,command = lambda: self.memory_tune(52))
        self.ch102_b.grid(row=10, column=2,padx=3,pady=3,sticky=E+W)
        self.ch103_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="54: "+self.mem_list[53]+"\n"+self.mode_list[53], width=12,command = lambda: self.memory_tune(53))
        self.ch103_b.grid(row=10, column=3,padx=3,pady=3,sticky=E+W)
        self.ch104_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="55: "+self.mem_list[54]+"\n"+self.mode_list[54], width=12,command = lambda: self.memory_tune(54))
        self.ch104_b.grid(row=10, column=4,padx=3,pady=3,sticky=E+W)
        
        self.ch110_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="56: "+self.mem_list[55]+"\n"+self.mode_list[55], width=12,command = lambda: self.memory_tune(55))
        self.ch110_b.grid(row=11, column=0,padx=3,pady=3,sticky=E+W)
        self.ch111_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="57: "+self.mem_list[56]+"\n"+self.mode_list[56], width=12,command = lambda: self.memory_tune(56))
        self.ch111_b.grid(row=11, column=1,padx=3,pady=3,sticky=E+W)
        self.ch112_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="58: "+self.mem_list[57]+"\n"+self.mode_list[57], width=12,command = lambda: self.memory_tune(57))
        self.ch112_b.grid(row=11, column=2,padx=3,pady=3,sticky=E+W)
        self.ch113_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="59: "+self.mem_list[58]+"\n"+self.mode_list[58], width=12,command = lambda: self.memory_tune(58))
        self.ch113_b.grid(row=11, column=3,padx=3,pady=3,sticky=E+W)
        self.ch114_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="60: "+self.mem_list[59]+"\n"+self.mode_list[59], width=12,command = lambda: self.memory_tune(59))
        self.ch114_b.grid(row=11, column=4,padx=3,pady=3,sticky=E+W)
        self.save_mem_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="Store memory", width=12, command = lambda: self.store_mem())
        self.save_mem_b.grid(row=12, column=0, columnspan=2, padx=3, pady=3,sticky=E+W)
        self.erase_mem_b = Button(self.mem_frame,bg='grey50',fg='white',font=("",9,"bold"), text="Erase memory", width=12, command = lambda: self.erase_mem())
        self.erase_mem_b.grid(row=12, column=3, columnspan=2, padx=3, pady=3,sticky=E+W)
        
        
    def store_mem(self):
        self.freq_store = self.rx_freq.get()
        self.mode_store = self.mode.get()
        try:
            self.mem_in = tkSimpleDialog.askinteger("Store", self.freq_store+" will be a simplex (RX/TX) channel.\nMode ("+self.mode_store+") will be stored.\n\nEnter memory location 1-60:")
            self.mem_no = self.mem_in - 1
        except:
            return
            
        self.mem_list[self.mem_no]=self.freq_store
        self.mode_list[self.mem_no]=self.mode_store
        
        with open('mem_list.txt', 'wb') as outfile:
            json.dump(self.mem_list, outfile)
            
        with open('mode_list.txt', 'wb') as outfile:
            json.dump(self.mode_list, outfile)
            
        self.mem_frame.destroy()
        self.make_mem()
    
    def erase_mem(self):
        self.mem_clear = tkSimpleDialog.askinteger("Erase", "Please enter the memory 1-60 to be erased")
        self.mem_list[self.mem_clear - 1 ]  = ""
        with open('mem_list.txt', 'wb') as outfile:
            json.dump(self.mem_list, outfile)
        self.mem_frame.destroy()
        self.make_mem()
        
    def close(self):
        pass
    
    def remote_toggle(self):
        if self.remote_flag.get() == 1:
            radio.remote_on()
            self.mode.set(radio.get_mode())
            self.rx_freq.set(radio.get_rxfreq())
            self.tx_freq.set(radio.get_txfreq())
            self.txp.set(radio.get_txpower())
            self.rx_l.configure(fg='green')
            self.tx_l.configure(fg='green')
        else:
            radio.remote_off()
            self.rx_freq.set(radio.get_rxfreq())
            self.tx_freq.set(radio.get_txfreq())
            self.mode.set(radio.get_mode())
            self.rx_l.configure(fg='grey50')
            self.tx_l.configure(fg='grey50')
            
    def clr(self):
        self.e_rxfreq.delete(0, END)
        if self.simplex.get() != 1:   
            self.e_txfreq.delete(0, END)
        
    def vol_up(self):
        self.sp.set(1)
        self.speaker()
        self.cur_vol = radio.get_vol()
        self.new_vol = int(self.cur_vol) + 5
        radio.set_vol(str(self.new_vol))
        self.volume.set(radio.get_vol())
        
    def vol_dn(self):
        self.cur_vol = radio.get_vol()
        self.new_vol = int(self.cur_vol) - 5
        radio.set_vol(str(self.new_vol))
        self.volume.set(radio.get_vol())
        
    def rf_up(self):
        self.cur_rf = radio.get_rfg()
        self.new_rf = int(self.cur_rf) + 1
        radio.set_rfg(str(self.new_rf))
        self.rfgain.set(radio.get_rfg())
        
    def rf_dn(self):
        self.cur_rf = radio.get_rfg()
        self.new_rf = int(self.cur_rf) - 1
        radio.set_rfg(str(self.new_rf))
        self.rfgain.set(radio.get_rfg())
        
    def qsy_rx(self):
        self.qsyflag="rx"
        
    def qsy_tx(self):
        self.qsyflag="tx"
        self.simplex.set(0)
        self.do_simplex()
    
    def qsy(self):
        self.enter_rxfreq()
        self.enter_txfreq()
    
    def qsy_entry(self, text):
        if self.qsyflag == "tx":
            self.e_txfreq.insert(END,text)
        else:
            self.e_rxfreq.insert(END,text)
        
    def tune(self):
        self.cur_mode = radio.get_mode()
        radio.set_mode("FSK")
        self.cur_pwr = radio.get_txpower()
        self.tune_time = int(self.tune_t.get())
        radio.set_txpower("1")
        radio.ptt_on()
        time.sleep(self.tune_time)
        radio.ptt_off()
        radio.set_mode(self.cur_mode)
        radio.set_txpower(self.cur_pwr)
    
    def enter_rxfreq(self):
        
        try:
            radio.set_rxfreq(self.e_rxfreq.get())
        except:
            pass
        self.rx_freq.set(radio.get_rxfreq())
        
        if self.simplex.get() == 1:
           
            radio.set_txfreq(self.e_rxfreq.get())
   
            self.tx_freq.set(radio.get_txfreq())
            
        self.e_rxfreq.delete(0, END)
        
    def enter_txfreq(self):
        try:
            radio.set_txfreq(self.e_txfreq.get())
        except:
            pass
        self.tx_freq.set(radio.get_txfreq())
        self.e_txfreq.delete(0, END)
    
    def memory_tune(self, index):
        #print "in memory tune with index ", index
        self.newfreq = self.mem_list[index]
        self.newmode = self.mode_list[index]
        #print "freq = ", self.newfreq
        #print "mode = ", self.newmode
        
        radio.set_rxfreq(self.newfreq)
        radio.set_txfreq(self.newfreq)
        radio.set_mode(str(self.newmode))
        
        self.rx_freq.set(radio.get_rxfreq())
        self.tx_freq.set(radio.get_txfreq())
        self.mode.set(radio.get_mode())
        
    def new_mode(self, mode):
        radio.set_mode(mode)
        self.mode.set(radio.get_mode())
    
    
    def txpc(self,p):
        radio.set_txpower(p)
        self.txp.set(radio.get_txpower())
    
    def speaker(self):
        if self.sp.get() == 1:
            radio.speaker_on()
        else:
            radio.speaker_off()
            
    def sqlc(self):
        if self.sql.get() == 1:
            radio.sql_on()
        else:
            radio.sql_off()
            
    def nbc(self):
        if self.nb.get() == 1:
            radio.nb_on()
        else:
            radio.nb_off()
    def agcc(self):
        if self.agc.get() == 1:
            radio.agc_on()
        else:
            radio.agc_off()
    
    def dimc(self):
        if self.dim.get() == 1:
            radio.dim_on()
        else:
            radio.dim_off()
            
            
    
    def do_simplex(self):
        if self.simplex.get() == 1:
            self.e_txfreq.configure(state='disabled')
            radio.set_txfreq(radio.get_rxfreq())
            self.tx_freq.set(radio.get_txfreq())
            self.qsyflag="rx"
            self.rx_r.invoke()
        else:
            self.e_txfreq.configure(state='normal')
    
    
            
    def up(self):
        deltaf = float(self.delta.get())
        
        self.cur_freq = float(radio.get_rxfreq())
        self.new_freq = str(self.cur_freq + deltaf)
        radio.set_rxfreq(self.new_freq)
        radio.set_txfreq(self.new_freq)
        self.rx_freq.set(radio.get_rxfreq())
        self.tx_freq.set(radio.get_txfreq())
        
    
    def down(self):
        deltaf = float(self.delta.get())
       
        self.cur_freq = float(radio.get_rxfreq())
        self.new_freq = str(self.cur_freq - deltaf)
        radio.set_rxfreq(self.new_freq)
        radio.set_txfreq(self.new_freq)
        self.rx_freq.set(radio.get_rxfreq())
        self.tx_freq.set(radio.get_txfreq())
        
        
    def handler(self):
        radio.dim_off()
        #radio.remote_off()
        
        exit(0)


    
def main():
    version = "v1.0"
    root = Tk()
    root.geometry("500x360")
    root.wm_attributes('-topmost', 1)
    
    root.title("M710 " + version)
    root.configure(background='darkgreen')
    app = m710(root)
    #root.protocol("WM_DELETE_WINDOW", app.handler)
    
    root.mainloop()


   
if __name__ == "__main__":
    main()
    
