#!/usr/bin/env python
'''
Python NMEA Control panel for Icom IC-M710 Marine HF SSB Transceiver

    Copyright (C) 1815  John Pumford-Green

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
import json
import time
from tkSimpleDialog import *
from tkMessageBox import *
import tkFont
import subprocess

#panel_colour="DarkOliveGreen"
panel_colour="CadetBlue4"
select_colour="SteelBlue4"
#lcd_colour="darkorange4"
lcd_colour="AntiqueWhite3"
led_bg_colour="black"
led_fg_colour="red"
button_colour="slategray1"


class m710(object):
    def __init__(self, master):
        self.master = master
        
        radio.remote_on()
        
        control_frame = Frame(master,borderwidth=2, relief=GROOVE).grid()
        
        
        ### Variables...
        
        self.delta = StringVar()
        self.freq = StringVar()
        self.mode = StringVar()
        self.sp=IntVar()
        self.dim=IntVar() 
        self.txp = StringVar()
        self.remote_flag = IntVar()
        self.tune_t = IntVar()
        self.e_var=StringVar()
        self.volume = StringVar()
        self.rfgain = StringVar()
        
        
        self.freq_l = Label(control_frame, textvariable=self.freq, font=("fixed",40,"bold"), borderwidth=3, relief=SUNKEN, bg=lcd_colour, fg='grey18')
        self.freq_l.grid(row=2, column = 0,columnspan=5,padx=5, pady=5, sticky="NESW")
        
        
        
        
        delta_frame = Frame(control_frame, bg=panel_colour, borderwidth=2, relief=GROOVE)
        delta_frame.grid(row=4, column = 0, columnspan = 5, padx=3, pady=2)
        
        self.qsy1m_r = Radiobutton(delta_frame, indicatoron=0, activebackground=button_colour,bg=button_colour,  selectcolor=select_colour, height=2, width=6, text="1MHz", variable=self.delta, value="1000")
        self.qsy1m_r.grid(row = 1, column = 0, padx=3, pady=2, sticky="NESW")
        self.qsy100k_r = Radiobutton(delta_frame, indicatoron=0,activebackground=button_colour,bg=button_colour, selectcolor=select_colour, width=6, text="100kHz", variable=self.delta, value="100")
        self.qsy100k_r.grid(row = 1, column = 1, padx=3,pady=2, sticky="NEWS")
        
	self.qsy10k_r = Radiobutton(delta_frame,  indicatoron=0,activebackground=button_colour,bg=button_colour, selectcolor=select_colour, width=6,text="10kHz", variable=self.delta, value="10")
        self.qsy10k_r.grid(row = 1, column = 2, padx=3,pady=2, sticky="NESW")
        
	self.qsy5k_r = Radiobutton(delta_frame,  indicatoron=0,activebackground=button_colour,bg=button_colour, selectcolor=select_colour, width=6,text="5kHz", variable=self.delta, value="5")
        
	self.qsy5k_r.grid(row = 1, column = 3, padx=3,pady=2, sticky="NESW")

	self.qsy1k_r = Radiobutton(delta_frame,  indicatoron=0,activebackground=button_colour,bg=button_colour,  selectcolor=select_colour, width=6,text="1kHz", variable=self.delta, value="1")
        self.qsy1k_r.grid(row = 1, column = 4, padx=3,pady=2, sticky="NEWS")
        self.qsy100h_r = Radiobutton(delta_frame, indicatoron=0,activebackground=button_colour,bg=button_colour, selectcolor=select_colour, width=6, text="100Hz", variable=self.delta, value="0.1")
        self.qsy100h_r.grid(row = 1, column = 5,padx=3,pady=2, sticky="NEWS")
        
	#self.qsy10h_r = Radiobutton(delta_frame, indicatoron=0,activebackground=button_colour,bg=button_colour,  selectcolor=select_colour, width=6, text="10Hz", variable=self.delta, value="0.01")
        #self.qsy10h_r.grid(row = 1, column = 5,padx=3,pady=2, sticky="NESW")
        
        self.tunedn_b = Button(delta_frame, text = "Down", activebackground=button_colour, bg=button_colour, height=2, width = 5, command=lambda: self.down())
        self.tunedn_b.grid(row = 2 , column = 0, columnspan=3,padx=3, pady=2, sticky="NEWS")
        
        self.tuneup_b = Button(delta_frame, text = "Up",activebackground=button_colour, bg=button_colour,  height=2, width = 5, command=lambda: self.up())
        self.tuneup_b.grid(row = 2 , column = 3, columnspan=3, padx=3, pady=2, sticky="NEWS")

        mode_frame = Frame(control_frame, bg=panel_colour, borderwidth=2, relief=GROOVE)
        mode_frame.grid(row = 6, column = 0, columnspan = 5, padx=3, pady=5)
        
        
        self.usb_r = Radiobutton(mode_frame, text = "USB", activebackground=button_colour,bg=button_colour,  selectcolor=select_colour, indicatoron=0, height=2, width=6, variable = self.mode, value = "USB", command = lambda: self.new_mode("USB"))
        self.usb_r.grid(row = 1, column = 0,padx=7,pady=5, sticky="NESW")
        self.lsb_r = Radiobutton(mode_frame, text = "LSB", activebackground=button_colour,bg=button_colour, selectcolor=select_colour, indicatoron=0,height=2, width=6, variable = self.mode, value = "LSB", command = lambda: self.new_mode("LSB"))
        self.lsb_r.grid(row = 1, column = 1,padx=7,pady=5, sticky="NESW")
        self.cw_r = Radiobutton(mode_frame, text = "AM", activebackground=button_colour,bg=button_colour, selectcolor=select_colour, indicatoron=0,height=2, width=6, variable = self.mode, value = "AM", command = lambda: self.new_mode("AM"))
        self.cw_r.grid(row = 1, column = 2,padx=7,pady=5, sticky="NESW")
        self.am_r = Radiobutton(mode_frame, text = "CW", activebackground=button_colour,bg=button_colour,  selectcolor=select_colour, indicatoron=0,height=2, width=6, variable = self.mode, value = "CW", command = lambda: self.new_mode("CW"))
        self.am_r.grid(row = 1, column = 3,padx=7,pady=5, sticky="NESW")
        self.fsk_r = Radiobutton(mode_frame, text = "FSK", activebackground=button_colour,bg=button_colour,  selectcolor=select_colour, indicatoron=0,height=2, width=6, variable = self.mode, value = "FSK", command = lambda: self.new_mode("FSK"))
        self.fsk_r.grid(row = 1, column = 4,padx=7,pady=5, sticky="NESW")
        
        
        button_frame = Frame(control_frame, bg=panel_colour, borderwidth=2, relief=GROOVE)
        button_frame.grid(row = 8, column = 0, columnspan = 5, pady=5)
        
        self.sp_cb = Checkbutton(button_frame,indicatoron=0,activebackground=button_colour, bg=button_colour, selectcolor=select_colour, height=2, width=7, text = "Speaker", variable=self.sp, command = lambda:self.speaker())
        self.sp_cb.grid(row=0, column=0,padx=2,pady=2,sticky=N+S+W+E)
        
       
        self.dim_cb = Checkbutton(button_frame, indicatoron=0,activebackground=button_colour,bg=button_colour,  selectcolor=select_colour, height=2, width=5,text = "Dim", variable=self.dim, command = lambda:self.dimc())
        self.dim_cb.grid(row=0, column=3,padx=2,pady=2, sticky=N+S+W+E)
        
        self.txp_l = Label(button_frame, bg=panel_colour, fg="black", text="TX Power")
        self.txp_l.grid(row = 2, column = 0,padx=2,pady=2, sticky=N+S+W+E)
        
        self.txp3_r = Radiobutton(button_frame,activebackground=button_colour,bg=button_colour,  text = "High",selectcolor=select_colour, height=2,width=4, indicatoron=0,  variable=self.txp, value = "3", command = lambda: self.txpc("3"))
        self.txp3_r.grid(row=2, column=3,padx=2, pady=2, sticky="NSWE")
        self.txp2_r = Radiobutton(button_frame,activebackground=button_colour,bg=button_colour,  text = "Mid",selectcolor=select_colour, height=2,width=4, indicatoron=0,  variable=self.txp, value = "2", command = lambda: self.txpc("2"))
        self.txp2_r.grid(row=2, column=2,padx=2, pady=2, sticky=N+S+W+E)
        self.txp1_r = Radiobutton(button_frame, activebackground=button_colour,bg=button_colour, text = "Low",selectcolor=select_colour, height=2, width=4, indicatoron=0,  variable=self.txp, value = "1", command = lambda: self.txpc("1"))
        self.txp1_r.grid(row=2, column=1, padx=2, pady=2, sticky=N+S+W+E)
        
        self.rem_l = Label(button_frame, bg=panel_colour, fg="black", text="Remote")
        self.rem_l.grid(row = 3, column = 0,padx=2,pady=2, sticky=N+S+W+E)
        
        self.remoteon_b = Radiobutton(button_frame,activebackground=button_colour, bg=button_colour, text="On", indicatoron=0, height=2, width=4, selectcolor=select_colour, variable=self.remote_flag, value=1, command = lambda: self.remote_toggle())
        self.remoteon_b.grid(row = 3, column = 1,padx=2,pady=2, sticky=N+S+W+E)
        
        self.remoteoff_b = Radiobutton(button_frame,activebackground=button_colour, bg=button_colour, text="Off", selectcolor=select_colour, height=2, width=4,indicatoron=0, variable=self.remote_flag, value=0, command = lambda: self.remote_toggle())
        self.remoteoff_b.grid(row = 3, column = 2,padx=2,pady=2, sticky=N+S+W+E)
        
        #########
        #
        # Keypad frame
        
     
        
        key_frame = Frame(control_frame, bg=panel_colour, borderwidth=2, relief=GROOVE)
        key_frame.grid(row = 0, column = 11, rowspan = 10, sticky=N+S+W+E, padx=10, pady=2)
        
        atu_frame = Frame(key_frame, bg=panel_colour, borderwidth=2, relief=GROOVE)
        atu_frame.grid(row=5, column = 0)
        
        self.tune1_r = Radiobutton(atu_frame,indicatoron=0, bg=button_colour, selectcolor=select_colour, width=4, text = "2s", value = 2, variable=self.tune_t)
        #self.tune1_r.grid(row = 7, column = 1,padx=5,pady=5)
        self.tune5_r = Radiobutton(atu_frame,indicatoron=0, bg=button_colour, selectcolor=select_colour, width=4, text = "5s", value = 5, variable=self.tune_t)
        #self.tune5_r.grid(row = 7, column = 2,padx=5,pady=5)
        self.tune5_r.select()
        
        
        
        self.k1_b = Button(key_frame,activebackground='grey25',bg='grey25',  text="1", activeforeground="white",fg='white',  font=("fixed","13","bold"),height=3,  width=4, command=lambda: self.qsy_entry("1"))
        self.k1_b.grid(row = 1, column = 0, sticky=N+S+W+E, padx=3, pady=3)       
        self.k2_b = Button(key_frame,bg='grey25', activebackground='grey25', text="2",activeforeground="white", fg="white",  font=("fixed","13","bold"),  width=4,height=3, command=lambda: self.qsy_entry("2"))
        self.k2_b.grid(row = 1, column = 1, sticky=N+S+W+E,  padx=3, pady=3)
        self.k3_b = Button(key_frame,bg='grey25', activebackground='grey25', text="3",activeforeground="white",fg="white",  font=("fixed","13","bold"), width=4, height=3, command=lambda: self.qsy_entry("3"))
        self.k3_b.grid(row = 1, column = 2, sticky=N+S+W+E,  padx=3, pady=3)
        self.k4_b = Button(key_frame,bg='grey25',activebackground='grey25',  text="4",activeforeground="white",fg="white",  font=("fixed","13","bold"), height=3, width=4, command=lambda: self.qsy_entry("4"))
        self.k4_b.grid(row = 2, column = 0, sticky=N+S+W+E,  padx=3, pady=3)
        self.k5_b = Button(key_frame,bg='grey25',activebackground='grey25',  text="5", activeforeground="white",fg="white",  font=("fixed","13","bold"),  width=4, height=3,command=lambda: self.qsy_entry("5"))
        self.k5_b.grid(row = 2, column = 1, sticky=N+S+W+E,  padx=3, pady=3)
        self.k6_b = Button(key_frame,bg='grey25',activebackground='grey25',  text="6",activeforeground="white", fg="white",  font=("fixed","13","bold"),  width=4,height=3, command=lambda: self.qsy_entry("6"))
        self.k6_b.grid(row = 2, column = 2, sticky=N+S+W+E,  padx=3, pady=3)
        self.k7_b = Button(key_frame,bg='grey25', activebackground='grey25', text="7",activeforeground="white", fg="white",  font=("fixed","13","bold"),  height=3,  width=4, command=lambda: self.qsy_entry("7"))
        self.k7_b.grid(row = 3, column = 0, sticky=N+S+W+E,  padx=3, pady=3)
        self.k8_b = Button(key_frame,bg='grey25', activebackground='grey25', text="8",activeforeground="white", fg="white",  font=("fixed","13","bold"), height=3, width=4,command=lambda: self.qsy_entry("8") )
        self.k8_b.grid(row = 3, column = 1, sticky=N+S+W+E,  padx=3, pady=3)
        self.k9_b = Button(key_frame,bg='grey25', activebackground='grey25', text="9", activeforeground="white",fg="white",  font=("fixed","13","bold"),  width=4,height=3, command=lambda: self.qsy_entry("9"))
        self.k9_b.grid(row = 3, column = 2, sticky=N+S+W+E,  padx=3, pady=3)
        self.k0_b = Button(key_frame,bg='grey25', activebackground='grey25', text="0", activeforeground="white",fg="white",  font=("fixed","13","bold"),  height=3, width=4, command=lambda: self.qsy_entry("0"))
        self.k0_b.grid(row = 4, column = 1, sticky=N+S+W+E,  padx=3, pady=3)
        self.k0_b = Button(key_frame,bg='grey25', activebackground='grey25', text=".",activeforeground="white",  fg="white",  font=("fixed","13","bold") ,height=3, width=4, command=lambda: self.qsy_entry("."))
        self.k0_b.grid(row = 4, column = 2, sticky=N+S+W+E,  padx=3, pady=3)
        

        self.enter_b = Button(key_frame,bg=led_bg_colour,activebackground=led_bg_colour,  textvariable=self.e_var, fg=led_fg_colour,activeforeground=led_fg_colour,  font=("fixed","20","bold"),height=2,   width=5, command = lambda:self.qsy() )
        self.enter_b.grid(row = 0, column = 0, columnspan=3, sticky=N+S+W+E,  padx=2, pady=2)
        
        self.e_freq = Entry(key_frame, insertbackground='red',textvariable=self.e_var, fg='red', bg='black', width=5, font=("fixed",13,'bold'))
        
        self.voldn_b = Button(button_frame,bg=button_colour, activebackground=button_colour, height=2, text = "AF -",width=4, command=lambda: self.vol_dn())
        self.voldn_b.grid(row = 0, column = 1,padx=3, pady=2, sticky="NSWE")
        
        
        self.volup_b = Button(button_frame,bg=button_colour, activebackground=button_colour,height=2, text = "AF +", width=4, command=lambda: self.vol_up())
        self.volup_b.grid(row = 0, column = 2, padx=3, pady=2, sticky="NSWE")

        
        self.rcl_b = Button(key_frame,activebackground=button_colour,bg=button_colour,  text="Clear", height=2, width=4, command=lambda: self.clr())
        self.rcl_b.grid(row = 5, column = 1, columnspan=2,sticky=N+S+W+E, padx=2, pady=2)
        
        #self.tune_b = Button(key_frame, activeforeground="red",bg=button_colour, anchor="nw", font=("fixed","12",""), width=5, height=3, wraplength=50, text = "ATU Tune", command = lambda: self.tune())
        self.tune_b = Button(key_frame,activebackground=button_colour,bg=button_colour, anchor="nw", font=("fixed","12",""), width=5, height=3, wraplength=50, text = "ATU Tune", command = lambda: self.tune())
        self.tune_b.grid(row = 4, column = 0,padx=2,pady=2, sticky="NSWE")
       

	self.sd_b = Button(button_frame,activebackground=button_colour, bg=button_colour,width=4, height=2, text="Quit", command= lambda: self.shutdown_pi())
        self.sd_b.grid(row=3, column=3)
 
        self.mode.set(radio.get_mode())
        self.freq.set(radio.get_rxfreq())
        self.txp.set(radio.get_txpower())
        
        self.remoteon_b.invoke()
        self.dim_cb.invoke()
        self.sp_cb.invoke()
        self.volume.set(radio.get_vol())
        self.delta.set(1)
        radio.agc_on()
        radio.nb_off()
        
    def shutdown_pi(self):
        #print "shutting down"
        if askyesno('What are you doing Dave?', "Close Controller?", default='no'):
            showinfo('Ok', "Radio Control Off")
            radio.remote_off()
            if askyesno('Shutdown', "Also shutdown Pi?", default='no'):
                cmd=['/home/gm4slv/sandbox/killme.sh']
                subprocess.Popen(cmd).wait()
            else:
                self.master.destroy()
	    
        else:
            showinfo('No', "Cancelled")
        return
 
        
    def close(self):
        pass
    
    def remote_toggle(self):
        if self.remote_flag.get() == 1:
            radio.remote_on()
            self.mode.set(radio.get_mode())
            self.freq.set(radio.get_rxfreq())
            self.txp.set(radio.get_txpower())
            self.freq_l.configure(fg='grey18')
        else:
            radio.remote_off()
            self.freq.set(radio.get_rxfreq())
            self.mode.set(radio.get_mode())
            self.freq_l.configure(fg=button_colour)
            
    def clr(self):
        self.e_freq.delete(0, END)
        
    def vol_up(self):
        self.sp.set(1)
        self.speaker()
        self.cur_vol = radio.get_vol()
        self.new_vol = int(self.cur_vol) + 2
        radio.set_vol(str(self.new_vol))
        self.volume.set(radio.get_vol())
        
    def vol_dn(self):
        self.cur_vol = radio.get_vol()
        self.new_vol = int(self.cur_vol) - 2
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
        
    
    def qsy(self):
        self.enter_freq()
    
    def qsy_entry(self, text):
        self.e_freq.insert(END,text)
        
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
    
    def enter_freq(self):
        
        try:
            radio.set_txfreq(self.e_freq.get())
            radio.set_rxfreq(self.e_freq.get())
        except:
            pass
        self.freq.set(radio.get_rxfreq())
            
        self.e_freq.delete(0, END)
    

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
            
    
            
    def up(self):
        deltaf = float(self.delta.get())
        
        self.cur_freq = float(radio.get_rxfreq())
        self.new_freq = str(self.cur_freq + deltaf)
        radio.set_rxfreq(self.new_freq)
        radio.set_txfreq(self.new_freq)
        self.freq.set(radio.get_rxfreq())
        
    
    def down(self):
        deltaf = float(self.delta.get())
       
        self.cur_freq = float(radio.get_rxfreq())
        self.new_freq = str(self.cur_freq - deltaf)
        radio.set_rxfreq(self.new_freq)
        radio.set_txfreq(self.new_freq)
        self.freq.set(radio.get_rxfreq())
        
        
    def handler(self):
        radio.dim_off()
        radio.remote_off()
        
        exit(0)


    
def main():
    version = "v0.1"
    root = Tk()
    #root.geometry("780x450-0-0")
    root.wm_attributes('-topmost', 1)
    #root.attributes('-zoomed', True)
    root.attributes('-fullscreen', True)
    
    root.title("Icom IC-M710 NMEA 0183 Touchscreen " + version)
    root.configure(background=panel_colour)
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=13, weight="bold")

    app = m710(root)
    #root.protocol("WM_DELETE_WINDOW", app.handler)
    
    root.mainloop()


   
if __name__ == "__main__":
    main()
    
