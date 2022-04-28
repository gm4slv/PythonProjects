# # new class-based gui

from Tkinter import *
import socket
import threading
import time
import tkFont


class Network(object):
    def __init__(self):
        self.sock = self.make_con()
        
    def make_con(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("192.168.21.105", 9999))
        return self.sock

    def connect(self, data):
        try:
            lock.acquire()
            self.sock.sendall(data + "\n")
            self.received = self.sock.recv(2048)
        finally:
            lock.release()
            return self.received
            
class Dash(object):
    def __init__(self, master):
        self.master = master
        
        self.s = (n1.sock.getsockname())
        self.p = (n1.sock.getpeername())
        

        
        dash_frame = Toplevel(master, borderwidth = 2, relief = GROOVE, bg = 'black')
        dash_frame.title("Server")
        dash_frame.protocol("WM_DELETE_WINDOW", self.handler)
        dash_frame.resizable(0, 0)
        dash_frame.geometry("350x150-10+10")
        dash_frame.grid()
        
        self.utc_time = StringVar()
        Label(dash_frame, textvariable = self.utc_time, fg = 'green', bg = 'black').grid(row = 0, column = 0, sticky = W)
        
        Label(dash_frame, text = self.s, bg = 'black', fg = 'white').grid(row = 1, column = 0, sticky = W)
        
        Label(dash_frame, text = " < --- > ", bg = 'black', fg = 'white').grid(row = 1, column = 1)
        
        Label(dash_frame, text = self.p, bg = 'black', fg = 'white').grid(row = 1, column = 2, sticky = E)
         
        #self.server_msg_l = StringVar()
        #Label(dash_frame, textvariable = self.server_msg_l, fg = 'yellow', bg = 'black').grid(row = 2, column = 0, columnspan = 3, sticky = W)
        
        q_button = Button(dash_frame, text = "Quit", command = lambda: close())
        q_button.grid(row = 3, column = 0, sticky = W)
    
    def handler(self):
        pass
        
    def up_dash(self):
        #self.server_msg = n1.connect("ident")
        #self.server_msg_l.set(self.server_msg)
        self.utc_time.set(time.strftime("%d/%m/%Y %H:%M", time.gmtime(time.time())))
        return

class nRadio(object):
    def __init__(self, master, radio):
        self.master = master
        
        self.radio = radio
        self.num = "".join(("r", self.radio))
       
        
        radio_frame = Frame(master, borderwidth=2, relief=GROOVE)
        
        radio_frame.grid()
        self.smeter_list = []
        
        qrg_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        qrg_frame.grid(row=8, column=4, columnspan=5, rowspan=2, sticky=W)
        
        mode_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        mode_frame.grid(row=3, column=0, columnspan=4, rowspan=5, sticky=EW)
        
        
        bw_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        bw_frame.grid(row=8, column=0, columnspan=4, rowspan=4, sticky=EW)
        
        #band_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        #band_frame.grid(row=10, column=0, columnspan=5, rowspan=2, sticky=W)
        
        log_frame = Frame(master, relief=GROOVE)
        log_frame.grid(row=0, column=1, sticky=NSEW)
        
        mem_frame = Frame(log_frame, borderwidth=2, relief=GROOVE)
        mem_frame.grid(row=0, column=0, columnspan=8, rowspan=14, sticky=NSEW)
        
        mem_frame2 = Frame(log_frame, borderwidth=2, relief=GROOVE)
        mem_frame2.grid(row=15, column=0, columnspan=8, rowspan=10, sticky=NSEW)
        
        mem_frame3 = Frame(mem_frame2, borderwidth=2, relief=GROOVE)
        mem_frame3.grid(row=0, column=6, columnspan=5, rowspan=11, sticky=NSEW)

        #Label(radio_frame, text="Name", width=10).grid(row=0, column=0)
        #Label(radio_frame, text="Freq/kHz", width=10).grid(row=0, column=0, sticky=EW)
        Label(radio_frame, text="Mode", width=10).grid(row=0, column=1, sticky=EW)
        Label(radio_frame, text="BW/Hz", width=10).grid(row=0, column=2)
        Label(radio_frame, text="Signal/dBm", width=10).grid(row=0, column=3)
        Label(radio_frame, text="Max/dBm", width=10, fg='red').grid(row=0, column=4)
        Label(radio_frame, text="Ave/dBm", width=10, fg='green').grid(row=0, column=5)
        Label(radio_frame, text="Min/dBm", width=10, fg='blue').grid(row=0, column=6)

        self.name_l = StringVar()
        self.l_name = Label(radio_frame, textvariable=self.name_l, width=10)
        self.l_name.grid(row=0, column=0)
        
        self.freq_l = StringVar()
        self.l_freq = Label(radio_frame, fg='red', textvariable=self.freq_l, width=10)
        self.l_freq.grid(row=1, column=0, sticky=EW)
       
        self.e_freq = Entry(radio_frame, width=10, bg = 'white', fg = 'black', insertbackground = 'blue')
        self.e_freq.grid(row=2, column=0, sticky=EW)
        self.e_freq.focus()
        self.e_freq.bind('<Return>', (lambda event: self.set_freq(self.num)))
        
        
        self.scrollbar = Scrollbar(radio_frame)
        #self.scrollbar.grid()

        self.freq_list = Text(radio_frame, width = 50, bg='white', yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.freq_list.yview)
        self.scrollbar.grid(row=15, rowspan = 10, column=8, sticky=NS)
        self.freq_list.grid(row = 15, rowspan=10, columnspan=8, column = 0, sticky=NSEW)
        
        self.write_b = Button(radio_frame, text="save", command = lambda: self.write_log())
        self.write_b.grid(row = 26, column=7)
        self.clear_b = Button(radio_frame, text="clear", command = lambda: self.clear_log())
        self.clear_b.grid(row = 26, column=6)
        self.ins_b = Button(radio_frame, text="stamp", command = lambda: self.ins_log())
        self.ins_b.grid(row = 26, column=5)
        
        self.loginf_l = Label(radio_frame, text="callsign , identity , comments")
        self.loginf_l.grid(row = 26, column =0, columnspan=4)

        self.mode_l = StringVar()
        self.l_mode = Label(radio_frame, textvariable=self.mode_l, width=10)
        self.l_mode.grid(row=1, column=1, sticky=W)
        
        self.bw_l = StringVar()
        self.l_bw = Label(radio_frame, textvariable=self.bw_l, width=10)
        self.l_bw.grid(row=1, column=2, sticky=W)
        
        '''
        self.e_mode = Entry(radio_frame, width=10, bg = 'white', fg = 'black', insertbackground = 'blue')
        self.e_mode.grid(row=2, column=2)
        self.e_mode.bind('<Return>', (lambda event: self.set_mode(self.num)))
        '''
        #self.e_mode = StringVar()
        
        self.modeframe_l=Label(mode_frame, text="Mode").grid(row=0, column=0)
        

        self.b_mode_usb = Button(mode_frame, text = "USB", width = 4, command = lambda: self.set_mode("usb", self.num))
        self.b_mode_usb.grid(row = 1, column = 0)
        
        self.b_mode_lsb = Button(mode_frame, text = "LSB", width = 4, command = lambda: self.set_mode("lsb", self.num))
        self.b_mode_lsb.grid(row = 1, column = 1)
        
        self.b_mode_am = Button(mode_frame, text = "AM", width = 4, command = lambda: self.set_mode("am", self.num))
        self.b_mode_am.grid(row = 1, column = 2)
        
        
        self.b_mode_cwr = Button(mode_frame, text = "CW", width = 4, command = lambda: self.set_mode("cw-r", self.num))
        self.b_mode_cwr.grid(row = 1, column = 3)
    
        
        self.b_mode_data = Button(mode_frame, text = "RTTY", width = 4, command = lambda: self.set_mode("rtty", self.num))
        self.b_mode_data.grid(row = 1, column = 4)
        
       
        #self.b_tune = Button(mode_frame, text = "Tune", width = 4, command = lambda: self.atutune(self.num))
        #self.b_tune.grid(row = 4, column = 2)
        
        self.qrgframe_l=Label(qrg_frame, text="VFO Up/Down (Hz)").grid(row=0, column=0, columnspan=2)
        
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
        
        self.bwframe_l=Label(bw_frame, text="IF Bandwidth (Hz)").grid(row=0, column=0, columnspan=2)
        self.b_bw_50h = Button(bw_frame, text = "50", width = 4, command = lambda: self.set_bw("00",self.num))
        self.b_bw_50h.grid(row = 8, column = 0)
        self.b_bw_150h = Button(bw_frame, text = "150", width = 4, command = lambda: self.set_bw("02",self.num))
        self.b_bw_150h.grid(row = 8, column = 1)
        self.b_bw_250h = Button(bw_frame, text = "250", width = 4, command = lambda: self.set_bw("04",self.num))
        self.b_bw_250h.grid(row = 8, column = 2)
        self.b_bw_500h = Button(bw_frame, text = "500", width = 4, command = lambda: self.set_bw("09",self.num))
        self.b_bw_500h.grid(row = 8, column = 3)
        self.b_bw_1k = Button(bw_frame, text = "1000", width = 4, command = lambda: self.set_bw("14",self.num))
        self.b_bw_1k.grid(row = 9, column = 0)
        self.b_bw_2k = Button(bw_frame, text = "2000", width = 4, command = lambda: self.set_bw("24",self.num))
        self.b_bw_2k.grid(row = 9, column = 1)
        self.b_bw_2k5 = Button(bw_frame, text = "2500", width = 4, command = lambda: self.set_bw("29",self.num))
        self.b_bw_2k5.grid(row = 9, column = 2)
        self.b_bw_2k5 = Button(bw_frame, text = "2800", width = 4, command = lambda: self.set_bw("32",self.num))
        self.b_bw_2k5.grid(row = 9, column = 3)
        
        self.b_bw_2k5 = Button(bw_frame, text = "3000", width = 4, command = lambda: self.set_bw("34",self.num))
        self.b_bw_2k5.grid(row = 9, column = 4)
        
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 0, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 0, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 0, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 0, column = 3, sticky=EW)
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 0, column = 4, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 1, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 1, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 1, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 1, column = 3, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 1, column = 4, sticky=EW)
        self.mem103_b.grid(row = 2, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 2, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 2, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 2, column = 3, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 2, column = 4, sticky=EW)
        self.mem103_b.grid(row = 3, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 3, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 3, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 3, column = 3, sticky=EW)
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 3, column = 4, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 4, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 4, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 4, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 4, column = 3, sticky=EW)
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 4, column = 4, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 5, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 5, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 5, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 5, column = 3, sticky=EW)
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 5, column = 4, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 6, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 6, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 6, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 6, column = 3, sticky=EW)
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 6, column = 4, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 7, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 7, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 7, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 7, column = 3, sticky=EW)
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 7, column = 4, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 8, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 8, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 8, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 8, column = 3, sticky=EW)
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 8, column = 4, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 9, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 9, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 9, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 9, column = 3, sticky=EW)
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 9, column = 4, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 10, column = 0, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 10, column = 1, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 10, column = 2, sticky=EW)
        self.mem103_b = Button(mem_frame3, text = "Spare", command = lambda: self.set_mem("s", self.num))
        self.mem103_b.grid(row = 10, column = 3, sticky=EW)
        self.mem05_l = Label(mem_frame3, text="Spare")
        self.mem05_l.grid(row = 10, column = 4, sticky=EW)
        #self.mem102_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem102_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem102_b.grid(row = 7, column = 7, sticky=EW)
        #self.mem103_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem103_b.grid(row = 7, column = 8, sticky=EW)
        #self.mem104_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem104_b.grid(row = 10, column = 4, sticky=EW)
        
        
        self.mem00_b = Button(mem_frame, fg='red', text = "2182",  command = lambda: self.set_mem("2182.0", self.num))
        self.mem00_b.grid(row = 0, column = 0, sticky=EW)
        self.mem01_b = Button(mem_frame, text = "1770", command = lambda: self.set_mem("1770.0", self.num))
        self.mem01_b.grid(row = 0, column = 1, sticky=EW)
        self.mem02_b = Button(mem_frame, text = "1743",  command = lambda: self.set_mem("1743.0", self.num))
        self.mem02_b.grid(row = 0, column = 2, sticky=EW)
        self.mem03_b = Button(mem_frame, text = "2226", command = lambda: self.set_mem("2226.0", self.num))
        self.mem03_b.grid(row = 0, column = 3, sticky=EW)
        self.mem04_b = Button(mem_frame, text = "1925",  command = lambda: self.set_mem("1925.0", self.num))
        self.mem04_b.grid(row = 0, column = 4, sticky=EW)
        self.mem10_b = Button(mem_frame, text = "1880", command = lambda: self.set_mem("1880.0", self.num))
        self.mem10_b.grid(row = 0, column = 5, sticky=EW)
        self.mem11_b = Button(mem_frame, text = "1883", command = lambda: self.set_mem("1883.0", self.num))
        self.mem11_b.grid(row = 0, column = 6, sticky=EW)
        self.mem12_b = Button(mem_frame, text = "2596", command = lambda: self.set_mem("2596.0", self.num))
        self.mem12_b.grid(row = 0, column = 7, sticky=EW)
        #self.mem05_l = Label(mem_frame, text="Marine")
        #self.mem05_l.grid(row = 0, column = 8, sticky=EW)

        #self.mem13_b = Button(mem_frame, text = "2226", command = lambda: self.set_mem("2226.0", self.num))
        #self.mem13_b.grid(row = 1, column = 0, sticky=EW)
        #self.mem14_b = Button(mem_frame, text = "2659", command = lambda: self.set_mem("2659.0", self.num))
        #self.mem14_b.grid(row = 1, column = 1, sticky=EW)
        self.mem15_l = Label(mem_frame, text="Marine")
        self.mem15_l.grid(row = 0, column = 9, sticky=EW)
        
        self.mem20_b = Button(mem_frame, text = "2275",  command = lambda: self.set_mem("2275.0", self.num))
        self.mem20_b.grid(row = 8, column = 0, sticky=EW)
        self.mem21_b = Button(mem_frame, text = "3338",  command = lambda: self.set_mem("3338.0", self.num))
        self.mem21_b.grid(row = 8, column = 1, sticky=EW)
        self.mem22_b = Button(mem_frame, text = "4438",  command = lambda: self.set_mem("4438.0", self.num))
        self.mem22_b.grid(row = 8, column = 2, sticky=EW)
        self.mem23_b = Button(mem_frame, text = "4440",  command = lambda: self.set_mem("4440.0", self.num))
        self.mem23_b.grid(row = 8, column = 3, sticky=EW)
        self.mem24_b = Button(mem_frame, text = "4550", command = lambda: self.set_mem("4550.0", self.num))
        self.mem24_b.grid(row = 8, column = 4, sticky=EW)
        #self.mem25_l = Label(mem_frame, text="Cadet")
        #self.mem25_l.grid(row = 2, column = 5, sticky=EW)
        
        self.mem30_b = Button(mem_frame, text = "4858", command = lambda: self.set_mem("4858.0", self.num))
        self.mem30_b.grid(row = 8, column = 5, sticky=EW)
        self.mem31_b = Button(mem_frame, text = "4920", command = lambda: self.set_mem("4920.0", self.num))
        self.mem31_b.grid(row = 8, column = 6, sticky=EW)
        self.mem32_b = Button(mem_frame, fg='red', text = "5345",  command = lambda: self.set_mem("5345.0", self.num))
        self.mem32_b.grid(row = 8, column = 7,sticky=EW)
        self.mem33_b = Button(mem_frame, text = "5808",  command = lambda: self.set_mem("5805.0", self.num))
        self.mem33_b.grid(row = 8, column = 8, sticky=EW)
        #self.mem34_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("sp", self.num))
        #self.mem34_b.grid(row = 3, column = 4, sticky=EW)
        self.mem35_l = Label(mem_frame, text="Cadet")
        self.mem35_l.grid(row = 8, column = 9, sticky=EW)

        self.mem40_b = Button(mem_frame, text = "4724",  command = lambda: self.set_mem("4724.0", self.num))
        self.mem40_b.grid(row = 4, column = 0, sticky=EW)
        self.mem41_b = Button(mem_frame, text = "6739",  command = lambda: self.set_mem("6739.0", self.num))
        self.mem41_b.grid(row = 4, column = 1, sticky=EW)
        self.mem42_b = Button(mem_frame, text = "8992",  command = lambda: self.set_mem("8992.0", self.num))
        self.mem42_b.grid(row = 4, column = 2, sticky=EW)
        self.mem43_b = Button(mem_frame,fg='red', text = "11175", command = lambda: self.set_mem("11175.0", self.num))
        self.mem43_b.grid(row = 4, column = 3, sticky=EW)
        self.mem44_b = Button(mem_frame, text = "13200", command = lambda: self.set_mem("13200.0", self.num))
        self.mem44_b.grid(row = 4, column = 4, sticky=EW)
        #self.mem45_l = Label(mem_frame, text="HFGCS")
        #self.mem45_l.grid(row = 4, column = 5, sticky=EW)
       
        self.mem50_b = Button(mem_frame, text = "15016",  command = lambda: self.set_mem("15016.0", self.num))
        self.mem50_b.grid(row = 4, column = 5, sticky=EW)
        self.mem51_b = Button(mem_frame, text = "6712", command = lambda: self.set_mem("6712.0", self.num))
        self.mem51_b.grid(row = 4, column = 6, sticky=EW)
        #self.mem52_b = Button(mem_frame, text = "9016", command = lambda: self.set_mem("9016.0", self.num))
        #self.mem52_b.grid(row = 4, column = 7, sticky=EW)
        #self.mem53_b = Button(mem_frame, text = "9019", command = lambda: self.set_mem("9019.0", self.num))
        #self.mem53_b.grid(row = 4, column = 8, sticky=EW)
        #self.mem54_b = Button(mem_frame, text = "11220", command = lambda: self.set_mem("11220.0", self.num))
        #self.mem54_b.grid(row = 5, column = 4, sticky=EW)
        self.mem55_l = Label(mem_frame, text="HFGCS")
        self.mem55_l.grid(row = 4, column = 9, sticky=EW)
        
        self.mem60_b = Button(mem_frame, fg = 'red', text = "4742", command = lambda: self.set_mem("4742.0", self.num))
        self.mem60_b.grid(row = 5, column = 0, sticky=EW)
        self.mem61_b = Button(mem_frame, text = "5702",  command = lambda: self.set_mem("5702.0", self.num))
        self.mem61_b.grid(row = 5, column = 1, sticky=EW)
        self.mem62_b = Button(mem_frame, text = "8980",  command = lambda: self.set_mem("8980.0", self.num))
        self.mem62_b.grid(row = 5, column = 2, sticky=EW)
        self.mem63_b = Button(mem_frame, text = "9022", command = lambda: self.set_mem("9022.0", self.num))
        self.mem63_b.grid(row = 5, column = 3, sticky=EW)
        self.mem64_b = Button(mem_frame, text = "9028", command = lambda: self.set_mem("9028.0", self.num))
        self.mem64_b.grid(row = 5, column = 4, sticky=EW)
        #self.mem65_l = Label(mem_frame, text="DHFCS")
        #self.mem65_l.grid(row = 5, column = 5, sticky=EW)
        
        self.mem70_b = Button(mem_frame, text = "9031", command = lambda: self.set_mem("9031.0", self.num))
        self.mem70_b.grid(row = 5, column = 5, sticky=EW)
        self.mem71_b = Button(mem_frame,fg='red', text = "11247", command = lambda: self.set_mem("11247.0", self.num))
        self.mem71_b.grid(row = 5, column = 6, sticky=EW)
        self.mem72_b = Button(mem_frame, text = "13257", command = lambda: self.set_mem("13257.0", self.num))
        self.mem72_b.grid(row = 5, column = 7, sticky=EW)
        self.mem73_b = Button(mem_frame, text = "18018", command = lambda: self.set_mem("18018.0", self.num))
        self.mem73_b.grid(row = 5, column = 8, sticky=EW)
        #self.mem74_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("sp", self.num))
        #self.mem74_b.grid(row = 7, column = 4, sticky=EW)
        self.mem75_l = Label(mem_frame, text="DHFCS")
        self.mem75_l.grid(row = 5, column = 9, sticky=EW)
        
        self.mem80_b = Button(mem_frame, text = "3023", command = lambda: self.set_mem("3023.0", self.num))
        self.mem80_b.grid(row = 6, column = 0, sticky=EW)
        self.mem81_b = Button(mem_frame, text = "3226", command = lambda: self.set_mem("3226.0", self.num))
        self.mem81_b.grid(row = 6, column = 1, sticky=EW)
        self.mem82_b = Button(mem_frame, text = "4718", command = lambda: self.set_mem("4718.0", self.num))
        self.mem82_b.grid(row = 6, column = 2, sticky=EW)
        self.mem83_b = Button(mem_frame,fg='red', text = "5680", command = lambda: self.set_mem("5680.0", self.num))
        self.mem83_b.grid(row = 6, column = 3, sticky=EW)
        self.mem84_b = Button(mem_frame, text = "5699", command = lambda: self.set_mem("5699.0", self.num))
        self.mem84_b.grid(row = 6, column = 4, sticky=EW)
        self.mem85_l = Label(mem_frame, text="SAR")
        self.mem85_l.grid(row = 6, column = 9, sticky=EW)
        
        self.mem90_b = Button(mem_frame, text = "4925", command = lambda: self.set_mem("4925.0", self.num))
        self.mem90_b.grid(row = 7, column = 0, sticky=EW)
        self.mem91_b = Button(mem_frame, text = "5206",  command = lambda: self.set_mem("5206.0", self.num))
        self.mem91_b.grid(row = 7, column = 1, sticky=EW)
        self.mem92_b = Button(mem_frame, text = "5399.5", command = lambda: self.set_mem("5399.5", self.num))
        self.mem92_b.grid(row = 7, column = 2, sticky=EW)
        self.mem93_b = Button(mem_frame, text = "6992.5", command = lambda: self.set_mem("6992.5", self.num))
        self.mem93_b.grid(row = 7, column = 3, sticky=EW)
        self.mem94_b = Button(mem_frame, text = "7714", command = lambda: self.set_mem("7714.0", self.num))
        self.mem94_b.grid(row = 7, column = 4, sticky=EW)
        #self.mem95_l = Label(mem_frame, text="Spare")
        #self.mem95_l.grid(row = , column = 5, sticky=EW)
        
        self.mem100_b = Button(mem_frame, text = "9230", command = lambda: self.set_mem("9230.0", self.num))
        self.mem100_b.grid(row = 7, column = 5, sticky=EW)
        #self.mem101_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem101_b.grid(row = 7, column = 6, sticky=EW)
        #self.mem102_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem102_b.grid(row = 7, column = 7, sticky=EW)
        #self.mem103_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem103_b.grid(row = 7, column = 8, sticky=EW)
        #self.mem104_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem104_b.grid(row = 10, column = 4, sticky=EW)
        self.mem105_l = Label(mem_frame, text="Cadet")
        self.mem105_l.grid(row = 7, column = 9, sticky=EW)
        
        self.mem110_b = Button(mem_frame, text = "4247", command = lambda: self.set_mem("4247.0", self.num))
        self.mem110_b.grid(row = 2, column = 0, sticky=EW)
        self.mem111_b = Button(mem_frame, text = "6477.5", command = lambda: self.set_mem("6477.5", self.num))
        self.mem111_b.grid(row = 2, column = 1, sticky=EW)
        self.mem112_b = Button(mem_frame, text = "8642.0", command = lambda: self.set_mem("8642.0", self.num))
        self.mem112_b.grid(row = 2, column = 2, sticky=EW)
        self.mem113_b = Button(mem_frame, text = "12808.5", command = lambda: self.set_mem("12808.5", self.num))
        self.mem113_b.grid(row = 2, column = 3, sticky=E)
        self.mem114_b = Button(mem_frame, text = "17016.8", command = lambda: self.set_mem("17016.8", self.num))
        self.mem114_b.grid(row = 2, column = 4, sticky=E)
        
        self.mem120_b = Button(mem_frame, text = "22477.5", command = lambda: self.set_mem("22477.5", self.num))
        self.mem120_b.grid(row = 2, column = 5, sticky=EW)
        #self.mem121_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem121_b.grid(row = 2, column = 6, sticky=EW)
        #self.mem122_b = Button(mem_frame, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem122_b.grid(row = 2, column = 7, sticky=EW)

        self.mem115_l = Label(mem_frame, text="KPH")
        self.mem115_l.grid(row = 2, column = 9, sticky=EW)

        self.mem123_b = Button(mem_frame, text = "5276",  command = lambda: self.set_mem("5276.0", self.num))
        self.mem123_b.grid(row = 9, column = 0, sticky=EW)
        self.mem124_b = Button(mem_frame, text = "5279", command = lambda: self.set_mem("5279.0", self.num))
        self.mem124_b.grid(row = 9, column = 1, sticky=EW)
        #self.mem125_l = Label(mem_frame, text="Ham")
        #self.mem125_l.grid(row = 9, column = 2, sticky=EW)
        
        self.mem130_b = Button(mem_frame, text = "5298", command = lambda: self.set_mem("5298.0", self.num))
        self.mem130_b.grid(row = 9, column = 2, sticky=EW)
        self.mem131_b = Button(mem_frame, text = "5301", command = lambda: self.set_mem("5301.0", self.num))
        self.mem131_b.grid(row = 9, column = 3, sticky=EW)
        self.mem132_b = Button(mem_frame, text = "5317", command = lambda: self.set_mem("5317.0", self.num))
        self.mem132_b.grid(row = 9, column = 4, sticky=EW)
        self.mem133_b = Button(mem_frame, text = "5333", command = lambda: self.set_mem("5333.0", self.num))
        self.mem133_b.grid(row = 9, column = 5, sticky=EW)
        self.mem134_b = Button(mem_frame, text = "5354", command = lambda: self.set_mem("5354.0", self.num))
        self.mem134_b.grid(row = 9, column = 6, sticky=EW)
        
        self.mem140_b = Button(mem_frame, text = "5371.5", command = lambda: self.set_mem("5371.5", self.num))
        self.mem140_b.grid(row = 9, column = 7, sticky=EW)
        self.mem141_b = Button(mem_frame, text = "5379", command = lambda: self.set_mem("5379.0", self.num))
        self.mem141_b.grid(row = 9, column = 8, sticky=EW)
        self.mem145_l = Label(mem_frame, text="Ham")
        self.mem145_l.grid(row = 9, column = 9, sticky=EW)
        
        self.mem142_b = Button(mem_frame, text = "5395", command = lambda: self.set_mem("5395.0", self.num))
        self.mem142_b.grid(row = 10, column = 0, sticky=EW)
        self.mem143_b = Button(mem_frame, text = "5398.5", command = lambda: self.set_mem("5398.5", self.num))
        self.mem143_b.grid(row = 10, column = 1, sticky=EW)
        self.mem144_b = Button(mem_frame, text = "5403.5", command = lambda: self.set_mem("5403.5", self.num))
        self.mem144_b.grid(row = 10, column = 2, sticky=EW)
        self.mem144_b = Button(mem_frame, text = "3615", command = lambda: self.set_mem("3615.0", self.num))
        self.mem144_b.grid(row = 10, column = 3, sticky=EW)

        self.mem135_l = Label(mem_frame, text="Ham")
        self.mem135_l.grid(row = 10, column = 9, sticky=EW)
        
        self.mem80_b2 = Button(mem_frame2, text = "5450", command = lambda: self.set_mem("5450.0", self.num))
        self.mem80_b2.grid(row = 10, column = 0, sticky=EW)
        self.mem81_b2 = Button(mem_frame2, text = "11253", command = lambda: self.set_mem("11253.0", self.num))
        self.mem81_b2.grid(row = 10, column = 1, sticky=EW)
        self.mem82_b2 = Button(mem_frame2, text = "5505", command = lambda: self.set_mem("5505.0", self.num))
        self.mem82_b2.grid(row = 10, column = 2, sticky=EW)
        self.mem83_b2 = Button(mem_frame2, text = "8957", command = lambda: self.set_mem("8957.0", self.num))
        self.mem83_b2.grid(row = 10, column = 3, sticky=EW)
        self.mem84_b2 = Button(mem_frame2, text = "13264", command = lambda: self.set_mem("13264.0", self.num))
        self.mem84_b2.grid(row = 10, column = 4, sticky=EW)
        self.mem85_l2 = Label(mem_frame2, text="Volmet")
        self.mem85_l2.grid(row = 10, column = 5, sticky=EW)
        
        self.mem90_b2 = Button(mem_frame2, text = "3485", command = lambda: self.set_mem("3485.0", self.num))
        self.mem90_b2.grid(row = 11, column = 0, sticky=EW)
        self.mem91_b2 = Button(mem_frame2, text = "6604", command = lambda: self.set_mem("6604.0", self.num))
        self.mem91_b2.grid(row = 11, column = 1, sticky=EW)
        self.mem92_b2 = Button(mem_frame2, text = "10051", command = lambda: self.set_mem("10051.0", self.num))
        self.mem92_b2.grid(row = 11, column = 2, sticky=EW)
        self.mem93_b2 = Button(mem_frame2, text = "13270", command = lambda: self.set_mem("13270.0", self.num))
        self.mem93_b2.grid(row = 11, column = 3, sticky=EW)
        #self.mem94_b2 = Button(mem_frame2, text = "Spare", command = lambda: self.set_mem("s", self.num))
        #self.mem94_b2.grid(row = 9, column = 4, sticky=EW)
        self.mem95_l2 = Label(mem_frame2, text="Volmet")
        self.mem95_l2.grid(row = 11, column = 5, sticky=EW)
        
        self.mem30_b2 = Button(mem_frame2, text = "3016", command = lambda: self.set_mem("3016.0", self.num))
        self.mem30_b2.grid(row = 3, column = 0, sticky=EW)
        self.mem31_b2 = Button(mem_frame2, text = "5598", command = lambda: self.set_mem("5598.0", self.num))
        self.mem31_b2.grid(row = 3, column = 1, sticky=EW)
        self.mem32_b2 = Button(mem_frame2, text = "8906", command = lambda: self.set_mem("8906.0", self.num))
        self.mem32_b2.grid(row = 3, column = 2, sticky=EW)
        self.mem33_b2 = Button(mem_frame2, text = "13306", command = lambda: self.set_mem("13306.0", self.num))
        self.mem33_b2.grid(row = 3, column = 3, sticky=EW)
        self.mem34_b2 = Button(mem_frame2, text = "17946", command = lambda: self.set_mem("17946.0", self.num))
        self.mem34_b2.grid(row = 3, column = 4, sticky=EW)
        self.mem35_l2 = Label(mem_frame2, text="NAT-A")
        self.mem35_l2.grid(row = 3, column = 5, sticky=EW)
        
        self.mem40_b2 = Button(mem_frame2, text = "2899", command = lambda: self.set_mem("2899.0", self.num))
        self.mem40_b2.grid(row = 4, column = 0, sticky=EW)
        self.mem41_b2 = Button(mem_frame2, text = "5616", command = lambda: self.set_mem("5616.0", self.num))
        self.mem41_b2.grid(row = 4, column = 1, sticky=EW)
        self.mem42_b2 = Button(mem_frame2, text = "8864", command = lambda: self.set_mem("8864.0", self.num))
        self.mem42_b2.grid(row = 4, column = 2, sticky=EW)
        self.mem43_b2 = Button(mem_frame2, text = "13291", command = lambda: self.set_mem("13291.0", self.num))
        self.mem43_b2.grid(row = 4, column = 3, sticky=EW)
        self.mem44_b2 = Button(mem_frame2, text = "17946", command = lambda: self.set_mem("17946.0", self.num))
        self.mem44_b2.grid(row = 4, column = 4, sticky=EW)
        self.mem45_l2 = Label(mem_frame2, text="NAT-B")
        self.mem45_l2.grid(row = 4, column = 5, sticky=EW)
        
        self.mem50_b2 = Button(mem_frame2, text = "2872", command = lambda: self.set_mem("2872.0", self.num))
        self.mem50_b2.grid(row = 5, column = 0, sticky=EW)
        self.mem51_b2 = Button(mem_frame2, text = "5649", command = lambda: self.set_mem("5649.0", self.num))
        self.mem51_b2.grid(row = 5, column = 1, sticky=EW)
        self.mem52_b2 = Button(mem_frame2, text = "8879", command = lambda: self.set_mem("8879.0", self.num))
        self.mem52_b2.grid(row = 5, column = 2, sticky=EW)
        self.mem53_b2 = Button(mem_frame2, text = "11336", command = lambda: self.set_mem("11336.0", self.num))
        self.mem53_b2.grid(row = 5, column = 3, sticky=EW)
        self.mem54_b2 = Button(mem_frame2, text = "13306", command = lambda: self.set_mem("13306.0", self.num))
        self.mem54_b2.grid(row = 5, column = 4, sticky=EW)
        self.mem55_l2 = Label(mem_frame2, text="NAT-C")
        self.mem55_l2.grid(row = 5, column = 5, sticky=EW)
        
        self.mem60_b2 = Button(mem_frame2, text = "2971", command = lambda: self.set_mem("2971.0", self.num))
        self.mem60_b2.grid(row = 6, column = 0, sticky=EW)
        self.mem61_b2 = Button(mem_frame2, text = "4675", command = lambda: self.set_mem("4675.0", self.num))
        self.mem61_b2.grid(row = 6, column = 1, sticky=EW)
        self.mem62_b2 = Button(mem_frame2, text = "8891", command = lambda: self.set_mem("8891.0", self.num))
        self.mem62_b2.grid(row = 6, column = 2, sticky=EW)
        self.mem63_b2 = Button(mem_frame2, text = "11279", command = lambda: self.set_mem("11279.0", self.num))
        self.mem63_b2.grid(row = 6, column = 3, sticky=EW)
        self.mem64_b2 = Button(mem_frame2, text = "13291", command = lambda: self.set_mem("13291.0", self.num))
        self.mem64_b2.grid(row = 6, column = 4, sticky=EW)
        self.mem65_l2 = Label(mem_frame2, text="NAT-D")
        self.mem65_l2.grid(row = 6, column = 5, sticky=EW)
        
        self.mem00_b2 = Button(mem_frame2, text = "3491", command = lambda: self.set_mem("3491.0", self.num))
        self.mem00_b2.grid(row = 0, column = 0, sticky=EW)
        self.mem01_b2 = Button(mem_frame2, text = "5583", command = lambda: self.set_mem("5583.0", self.num))
        self.mem01_b2.grid(row = 0, column = 1, sticky=EW)
        self.mem02_b2 = Button(mem_frame2, text = "6667", command = lambda: self.set_mem("6667.0", self.num))
        self.mem02_b2.grid(row = 0, column = 2, sticky=EW)
        self.mem03_b2 = Button(mem_frame2, text = "10021", command = lambda: self.set_mem("10021.0", self.num))
        self.mem03_b2.grid(row = 0, column = 3, sticky=EW)
        self.mem04_b2 = Button(mem_frame2, text = "10036", command = lambda: self.set_mem("10036.0", self.num))
        self.mem04_b2.grid(row = 0, column = 4, sticky=EW)
        self.mem05_l2 = Label(mem_frame2, text="1/1E")
        self.mem05_l2.grid(row = 0, column = 5, sticky=EW)
        
        self.mem10_b2 = Button(mem_frame2, text = "2890", command = lambda: self.set_mem("2890.0", self.num))
        self.mem10_b2.grid(row = 1, column = 0, sticky=EW)
        self.mem11_b2 = Button(mem_frame2, text = "5484", command = lambda: self.set_mem("5484.0", self.num))
        self.mem11_b2.grid(row = 1, column = 1, sticky=EW)
        self.mem12_b2 = Button(mem_frame2, text = "5568", command = lambda: self.set_mem("5568.0", self.num))
        self.mem12_b2.grid(row = 1, column = 2, sticky=EW)
        self.mem13_b2 = Button(mem_frame2, text = "6550", command = lambda: self.set_mem("6550.0", self.num))
        self.mem13_b2.grid(row = 1, column = 3, sticky=EW)
        self.mem14_b2 = Button(mem_frame2, text = "6595", command = lambda: self.set_mem("6595.0", self.num))
        self.mem14_b2.grid(row = 1, column = 4, sticky=EW)
        self.mem15_l2 = Label(mem_frame2, text="1B")
        self.mem15_l2.grid(row = 1, column = 5, sticky=EW)
        
        self.mem20_b2 = Button(mem_frame2, text = "2893", command = lambda: self.set_mem("2893.0", self.num))
        self.mem20_b2.grid(row = 2, column = 0, sticky=EW)
        self.mem21_b2 = Button(mem_frame2, text = "4666", command = lambda: self.set_mem("4666.0", self.num))
        self.mem21_b2.grid(row = 2, column = 1, sticky=EW)
        self.mem22_b2 = Button(mem_frame2, text = "6544", command = lambda: self.set_mem("6544.0", self.num))
        self.mem22_b2.grid(row = 2, column = 2, sticky=EW)
        self.mem23_b2 = Button(mem_frame2, text = "8840", command = lambda: self.set_mem("8840.0", self.num))
        self.mem23_b2.grid(row = 2, column = 3, sticky=EW)
        #self.mem24_b2 = Button(mem_frame2, text = "Spare", command = lambda: self.set_mem("sp", self.num))
        #self.mem24_b2.grid(row = 2, column = 4, sticky=EW)
        self.mem25_l2 = Label(mem_frame2, text="1C")
        self.mem25_l2.grid(row = 2, column = 5, sticky=EW)
        
        self.mem70_b2 = Button(mem_frame2, text = "2962", command = lambda: self.set_mem("2962.0", self.num))
        self.mem70_b2.grid(row = 7, column = 0, sticky=EW)
        self.mem71_b2 = Button(mem_frame2, text = "6628", command = lambda: self.set_mem("6628.0", self.num))
        self.mem71_b2.grid(row = 7, column = 1, sticky=EW)
        self.mem72_b2 = Button(mem_frame2, text = "8825", command = lambda: self.set_mem("8825.0", self.num))
        self.mem72_b2.grid(row = 7, column = 2, sticky=EW)
        self.mem73_b2 = Button(mem_frame2, text = "11309", command = lambda: self.set_mem("11309.0", self.num))
        self.mem73_b2.grid(row = 7, column = 3, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "13254", command = lambda: self.set_mem("13254", self.num))
        self.mem74_b2.grid(row = 7, column = 4, sticky=EW)
        self.mem75_l2 = Label(mem_frame2, text="NAT-E")
        self.mem75_l2.grid(row = 7, column = 5, sticky=EW)
        
        self.mem70_b2 = Button(mem_frame2, text = "3476", command = lambda: self.set_mem("3476.0", self.num))
        self.mem70_b2.grid(row = 8, column = 0, sticky=EW)
        self.mem71_b2 = Button(mem_frame2, text = "6622", command = lambda: self.set_mem("6622.0", self.num))
        self.mem71_b2.grid(row = 8, column = 1, sticky=EW)
        self.mem72_b2 = Button(mem_frame2, text = "8831", command = lambda: self.set_mem("8831.0", self.num))
        self.mem72_b2.grid(row = 8, column = 2, sticky=EW)
        self.mem73_b2 = Button(mem_frame2, text = "13291", command = lambda: self.set_mem("13291.0", self.num))
        self.mem73_b2.grid(row = 8, column = 3, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "17946", command = lambda: self.set_mem("17946.0", self.num))
        self.mem74_b2.grid(row = 8, column = 4, sticky=EW)
        self.mem75_l2 = Label(mem_frame2, text="NAT-F")
        self.mem75_l2.grid(row = 8, column = 5, sticky=EW)
        
        self.mem70_b2 = Button(mem_frame2, text = "3491", command = lambda: self.set_mem("3491.0", self.num))
        self.mem70_b2.grid(row = 9, column = 0, sticky=EW)
        self.mem71_b2 = Button(mem_frame2, text = "6667", command = lambda: self.set_mem("6667.0", self.num))
        self.mem71_b2.grid(row = 9, column = 1, sticky=EW)
        #self.mem72_b2 = Button(mem_frame2, text = "8831", command = lambda: self.set_mem("8831.0", self.num))
        #self.mem72_b2.grid(row = 9, column = 2, sticky=EW)
        #self.mem73_b2 = Button(mem_frame2, text = "13291", command = lambda: self.set_mem("13291.0", self.num))
        #self.mem73_b2.grid(row = 9, column = 3, sticky=EW)
        #self.mem74_b2 = Button(mem_frame2, text = "17946", command = lambda: self.set_mem("17946.0", self.num))
        #self.mem74_b2.grid(row = 9, column = 4, sticky=EW)
        self.mem75_l2 = Label(mem_frame2, text="NAT-H")
        self.mem75_l2.grid(row = 9, column = 5, sticky=EW)
        
        self.mem70_b2 = Button(mem_frame2, text = "2944", command = lambda: self.set_mem("2944.0", self.num))
        self.mem70_b2.grid(row =13, column = 0, sticky=EW)
        self.mem71_b2 = Button(mem_frame2, text = "3446", command = lambda: self.set_mem("3446.0", self.num))
        self.mem71_b2.grid(row = 13, column = 1, sticky=EW)
        self.mem72_b2 = Button(mem_frame2, text = "4651", command = lambda: self.set_mem("4651.0", self.num))
        self.mem72_b2.grid(row = 13, column = 2, sticky=EW)
        self.mem73_b2 = Button(mem_frame2, text = "5460", command = lambda: self.set_mem("5460.0", self.num))
        self.mem73_b2.grid(row = 13, column = 3, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "5481", command = lambda: self.set_mem("5481.0", self.num))
        self.mem74_b2.grid(row = 13, column = 4, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "5559", command = lambda: self.set_mem("5559.0", self.num))
        self.mem74_b2.grid(row = 13, column = 5, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "5577", command = lambda: self.set_mem("5577.0", self.num))
        self.mem74_b2.grid(row = 13, column = 6, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "6547", command = lambda: self.set_mem("6547.0", self.num))
        self.mem74_b2.grid(row = 13, column = 7, sticky=EW)
        self.mem75_l2 = Label(mem_frame2, text="10E")
        self.mem75_l2.grid(row = 13, column = 9, sticky=EW)
        
        self.mem70_b2 = Button(mem_frame2, text = "2887", command = lambda: self.set_mem("2887.0", self.num))
        self.mem70_b2.grid(row =14, column = 0, sticky=EW)
        self.mem71_b2 = Button(mem_frame2, text = "5550", command = lambda: self.set_mem("5550.0", self.num))
        self.mem71_b2.grid(row = 14, column = 1, sticky=EW)
        self.mem72_b2 = Button(mem_frame2, text = "6577", command = lambda: self.set_mem("6577.0", self.num))
        self.mem72_b2.grid(row = 14, column = 2, sticky=EW)
        self.mem73_b2 = Button(mem_frame2, text = "8918", command = lambda: self.set_mem("8918.0", self.num))
        self.mem73_b2.grid(row = 14, column = 3, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "11396", command = lambda: self.set_mem("11396.0", self.num))
        self.mem74_b2.grid(row = 14, column = 4, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "13297", command = lambda: self.set_mem("13297.0", self.num))
        self.mem74_b2.grid(row = 14, column = 5, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "17907", command = lambda: self.set_mem("17907.0", self.num))
        self.mem74_b2.grid(row = 14, column = 6, sticky=EW)
        #self.mem74_b2 = Button(mem_frame2, text = "6547", command = lambda: self.set_mem("6547.0", self.num))
        #self.mem74_b2.grid(row = 14, column = 7, sticky=EW)
        self.mem75_l2 = Label(mem_frame2, text="CAR-A")
        self.mem75_l2.grid(row = 14, column = 9, sticky=EW)
        
        self.mem70_b2 = Button(mem_frame2, text = "3455", command = lambda: self.set_mem("3455.0", self.num))
        self.mem70_b2.grid(row =15, column = 0, sticky=EW)
        self.mem71_b2 = Button(mem_frame2, text = "5520", command = lambda: self.set_mem("5529.0", self.num))
        self.mem71_b2.grid(row = 15, column = 1, sticky=EW)
        self.mem72_b2 = Button(mem_frame2, text = "6586", command = lambda: self.set_mem("6586.0", self.num))
        self.mem72_b2.grid(row = 15, column = 2, sticky=EW)
        self.mem73_b2 = Button(mem_frame2, text = "8846", command = lambda: self.set_mem("8946.0", self.num))
        self.mem73_b2.grid(row = 15, column = 3, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "11330", command = lambda: self.set_mem("11330.0", self.num))
        self.mem74_b2.grid(row = 15, column = 4, sticky=EW)
        self.mem74_b2 = Button(mem_frame2, text = "17907", command = lambda: self.set_mem("17907.0", self.num))
        self.mem74_b2.grid(row = 15, column = 5, sticky=EW)
        #self.mem74_b2 = Button(mem_frame2, text = "6547", command = lambda: self.set_mem("6547.0", self.num))
        #self.mem74_b2.grid(row = 14, column = 7, sticky=EW)
        self.mem75_l2 = Label(mem_frame2, text="CAR-B")
        self.mem75_l2.grid(row = 15, column = 9, sticky=EW)
        
        self.smeter_l = StringVar()
        self.l_smeter = Label(radio_frame, textvariable=self.smeter_l, width=10)
        self.l_smeter.grid(row=1, column=3, sticky=W)

        self.max_var = StringVar()
        self.l_max = Label(radio_frame, textvariable=self.max_var, width=10)
        self.l_max.grid(row=1, column=4, sticky=W)
        
        self.ave_var = StringVar()
        self.l_average = Label(radio_frame, textvariable=self.ave_var, width=10)
        self.l_average.grid(row=1, column=5, sticky=W)

        self.min_var = StringVar()
        self.l_min = Label(radio_frame, textvariable=self.min_var, width=10)
        self.l_min.grid(row=1, column=6, sticky=W)

        
        
        
        self.pre = IntVar()
        self.cb_pre = Checkbutton(mode_frame, variable=self.pre, command=lambda: self.preamp_onoff(self.num))
        self.cb_pre.grid(row=10, column=1, sticky=E)

        self.l_pre = Label(mode_frame, width=10, text="Preamp")
        self.l_pre.grid(row=10, column=0, columnspan=2, sticky=W)

        self.att = IntVar()
        self.cb_att = Checkbutton(mode_frame, variable=self.att, command=lambda: self.att_onoff(self.num))
        self.cb_att.grid(row=11, column=1, sticky=E)
        
        self.l_att = Label(mode_frame, width=10, text="Att")
        self.l_att.grid(row=11, column=0,columnspan=2, sticky=W)
        
        
        self.nb = IntVar()
        self.cb_nb = Checkbutton(mode_frame, variable=self.nb, command=lambda: self.nb_onoff(self.num))
        self.cb_nb.grid(row=12, column=1, sticky=E)

        self.l_nb = Label(mode_frame, width=10, text="NB")
        self.l_nb.grid(row=12, column=0, columnspan=2, sticky=W)

        
        #self.set_log = IntVar()
        #self.cb_log = Checkbutton(radio_frame, variable = self.set_log)
        #self.cb_log.grid(row = 8, column = 1, sticky = W)
        
        #self.l_log = Label(radio_frame, width = 10, text = "Log to file...")
        #self.l_log.grid(row = 8, column = 0, sticky = E)

        self.c1 = Canvas(radio_frame, width=260, height=100, bg='black')
        self.c1.grid(row=2, column=4, columnspan=4, rowspan=3)

        name = self.get_name(radio)
    
    
    def write_log(self):
        #print "in write_file"
        self.filename = r'logfile.txt'
        self.f = open(self.filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
        timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        self.f.write("\n\nLog saved at : " + timenow + "==================\n")
        ## loop over lines in current text widget:
        self.newlog = self.freq_list.get("1.0", END)
        self.newlog_list = self.newlog.split("\n")
        for x in self.newlog_list:
            if len(x) > 1:
                #print x
                time_freq_text = x.split(":")
                #print time_freq_text
                log_date = time_freq_text[0].strip()
                log_time = time_freq_text[1].strip()
                log_freq = "%07.1f" % float(time_freq_text[2])
                text_list = time_freq_text[3].split(",")
                if len(text_list) > 3:
                    #print text_list
                    log_mode = text_list[0].strip()
                    log_call = text_list[1].strip()
                    log_ident = text_list[2].strip()
                    log_comment = text_list[3].strip()
                    
                    self.f.write("\n" + log_freq + "  " + log_call + ":" + " " + log_ident + " " + log_time + " " + log_mode + " " + log_comment + " (" + log_date + ") (JPG)") 
        self.f.close()
        self.clear_log()

        return

    def clear_log(self):
        self.freq_list.delete('1.0', END)
        timenow = time.strftime("%d%b%y : %H%M", time.gmtime(time.time()))
        self.freq_list.insert(END, "\n" + timenow +" : " + self.freq + " : " + self.mode + " , " )
        self.freq_list.see(END)
        self.freq_list.mark_set("insert", END)
        return
    
    def ins_log(self):
        #self.freq_list.delete('1.0', END)
        timenow = time.strftime("%d%b%y : %H%M", time.gmtime(time.time()))
        self.freq_list.insert(END, "\n" + timenow +" : " + self.freq + " : "  + self.mode + " , " )
        self.freq_list.see(END)
        self.freq_list.mark_set("insert", END)
        return

    def get_all(self):
        
        self.get_freq(self.num)
        self.get_mode(self.num)
        self.get_smeter(self.num)
        self.get_preamp(self.num)
        self.get_atten(self.num)
        self.get_nb(self.num)
        self.graph_points()       
        self.avg()
        self.max()
        self.min()
        self.get_bw(self.num)
        
        if self.set_log.get() == 1:
            if int(time.time()) % 10.0 == 0:
                self.write_file()
        return
        
        
    def get_bw(self, radio):
        self.bw = float(n1.connect("getbw" + " " + radio))
        #print self.bw
        
        if self.bw < 10:
            self.bwhz = 50 * (self.bw + 1)
        else:
            self.bwhz = 100 * (self.bw - 4)
            
        self.bw_l.set(int(self.bwhz))
        return
        
    def set_bw(self, bw, radio):
        self.new_bw = n1.connect("setbw" + " " + bw + " " + radio)
        
        return
        
    
        
    def get_freq(self, radio):

        self.freq = n1.connect("getfreq" + " " + radio)
        self.freq_l.set(self.freq)
        return
        
    def atutune(self, radio):
        self.tune = n1.connect("tune" + " " + radio)
        return

    def qsy_up(self, delta, radio):
        timenow = time.strftime("%d%b%y : %H%M", time.gmtime(time.time()))
        self.qsy = float(delta)
        self.cur_freq = float(n1.connect("getfreq" + " " + radio))
        self.new_freq = self.cur_freq + self.qsy
        self.newfreq = n1.connect("setfreq" + " " + str(self.new_freq) + " " + radio)
        self.get_freq(self.num)
        self.freq_list.insert(END, "\n" + timenow +" : " + self.freq + " : " + self.mode + " , " )
        self.freq_list.see(END)
        self.freq_list.mark_set("insert", END)
        return
        
    def qsy_dn(self, delta, radio):
        timenow = time.strftime("%d%b%y : %H%M", time.gmtime(time.time()))
        self.qsy = float(delta)
        self.cur_freq = float(n1.connect("getfreq" + " " + radio))
        self.new_freq = self.cur_freq - self.qsy
        self.newfreq = n1.connect("setfreq" + " " + str(self.new_freq) + " " + radio)
        self.get_freq(self.num)
        self.freq_list.insert(END, "\n" + timenow +" : " + self.freq + " : " + self.mode + " , " )
        self.freq_list.see(END)
        self.freq_list.mark_set("insert", END)
        return

    def set_freq(self, radio):
        self.freq = str(self.e_freq.get())
        timenow = time.strftime("%d%b%y : %H%M", time.gmtime(time.time()))
        try: 
            float(self.freq)
            self.newfreq = n1.connect("setfreq" + " " + self.freq + " " + radio)
            self.e_freq.delete(0, END)
            self.get_freq(self.num)
            self.freq_list.insert(END, "\n" + timenow +" : " + self.freq + " : "  + self.mode + " , " )
            self.freq_list.see(END)
            self.freq_list.mark_set("insert", END)
        except ValueError:
            self.e_freq.delete(0, END)
        return

    def set_mem(self, freq, radio):
        timenow = time.strftime("%d%b%y : %H%M", time.gmtime(time.time()))
        try:
            float(freq)
            self.newfreq = n1.connect("setfreq" + " " + freq + " " + radio)
            self.get_freq(self.num)
            self.freq_list.insert(END, "\n" + timenow +" : " + self.freq + " : " + self.mode + " , "  )
            self.freq_list.see(END)
            self.freq_list.mark_set("insert", END)
        except ValueError:
            pass
        return

    def get_mode(self, radio):
        self.mode = n1.connect("getmode" + " " + radio)
        if self.mode == "CW-R":
            self.mode = "CW"
        self.mode_l.set(self.mode)
        return

    def set_mode(self, mode, radio):
        #self.mode = str(self.e_mode.get())
        self.newmode = n1.connect("setmode" + " " + mode + " " + radio)
        timenow = time.strftime("%d%b%y : %H%M", time.gmtime(time.time()))
        #self.mode = str(self.e_mode.get())
        if mode == "cw-r":
            mode = "cw"
        self.freq_list.insert(END, "\n" + timenow +" : " + self.freq + " : " + mode.upper() + " , "  )
        #self.e_mode.delete(0, END)
        return

    def get_smeter(self, radio):
        self.smeter = n1.connect("getsmeter" + " " + radio)
        self.smeter_l.set(self.smeter)
        self.smeter_list.append(float(self.smeter))
        if len(self.smeter_list) > 120:
            self.smeter_list.pop(0)
        return

    def avg(self):
        s = self.smeter_list
        total = 0
        for i in s:
            total += i
        self.av = round((total / len(s)), 1)
        self.ave_var.set(str(self.av))
        self.c1.create_line(0, 100 - (self.av + 123 + 5), 310, 100 - (self.av + 123 + 5), fill="green")
        return self.av

    def min(self):
        s = self.smeter_list
        self.mn = s[0]
        for i in s:
            if i < self.mn:
                self.mn = i
        self.min_var.set(str(self.mn))
        self.c1.create_line(0, 100 - (self.mn + 123 + 5), 310, 100 - (self.mn + 123 + 5), fill="blue")
        return self.mn

    def max(self):
        s = self.smeter_list
        self.mx = s[0]
        for i in s:
            if i > self.mx:
                self.mx = i
        self.max_var.set(str(self.mx))
        self.c1.create_line(0, 100 - (self.mx + 123 + 5), 310, 100 - (self.mx + 123 + 5), fill="red")
        return self.mx

    def get_preamp(self, radio):
        self.preamp = n1.connect("getpreamp" + " " + radio)
        if self.preamp == "1":
            self.cb_pre.select()
        elif self.preamp == "0":
            self.cb_pre.deselect()
        return

    def preamp_onoff(self, radio):
        self.prestate = self.pre.get()
        if self.prestate:
            n1.connect("preampon" + " " + radio)
        else:
            n1.connect("preampoff" + " " + radio)
        return

    def att_onoff(self, radio):
        self.attstate = self.att.get()
        if self.attstate:
            n1.connect("atton" + " " + radio)
        else:
            n1.connect("attoff" + " " + radio)
        return

    def nb_onoff(self, radio):
        self.nbstate = self.nb.get()
        if self.nbstate:
            n1.connect("nbon" + " " + radio)
        else:
            n1.connect("nboff" + " " + radio)
        return

    def get_nb(self, radio):
        self.nblank = n1.connect("getnb" + " " + radio)
        if self.nblank == "1":
            self.cb_nb.select()
        elif self.nblank == "0":
            self.cb_nb.deselect()
        return

    def get_atten(self, radio):
        self.atten = n1.connect("getatt" + " " + radio)
        if self.atten == "1":
            self.cb_att.select()
        elif self.atten == "0":
            self.cb_att.deselect()
        return

    def get_name(self, radio):
        self.all_names = n1.connect("listradios")
        self.radios = self.all_names.split()
        self.name = self.radios[int(radio) - 1]
        self.name_l.set(self.name)
        return

    def graph_points(self):
        seq = self.smeter_list
        y_stretch = 1
        y_gap = 5
        x_stretch = 0
        x_width = 2
        x_gap = 2
        height = 100
        self.c1.delete(ALL)
        self.c1.create_line(0, 100 - (-73 + 123 + 5), 310, 100 - (-73 + 123 + 5), fill='white')
        for x, y in enumerate(seq):
            yd = y + 123
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = height - (yd * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = height - y_gap
            self.c1.create_rectangle(x0, y0, x1, y1, fill="yellow")

    def write_file(self):
        self.filename = self.name+".txt"
        self.f = open(self.filename, 'a+')
        timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
        log = " ".join((timenow, self.name, self.mode, self.freq, self.smeter, self.preamp, self.atten, "\r\n"))
        self.f.write(log)
        self.f.close()


def main():
    #loops = 0
    while True:
        try:
            nRadio1.get_all()
        except:
            pass
        try:
            nRadio2.get_all()
        except:
            pass
        try:
            nRadio3.get_all()
        except:
            pass
        try:
            nRadio4.get_all()
        except:
            pass
        #d1.up_dash()
        #loops += 1
        #print threading.currentThread().name, loops
        time.sleep(0.5)

def close():
    n1.connect("quit")
    root.destroy()
    
    
if __name__ == "__main__":
    version = "v0.1"
    lock = threading.Lock()
    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=8)
    
    root.option_add("*Font", default_font)
    
    
    #root.geometry("1300x690")
    root.title("GM4SLV IC-7200 Controller " + version)
    #root.withdraw()
    n1 = Network()
    radio_count = 1
    #radio_count = int(n1.connect("count"))
    if radio_count > 0:
        nRadio1 = nRadio(root, "1")
    if radio_count > 1:
        nRadio2 = nRadio(root, "2")
    if radio_count > 2:
        nRadio3 = nRadio(root, "3")
    if radio_count > 3:
        nRadio4 = nRadio(root, "4")
        
    #d1 = Dash(root)
    
    #print threading.currentThread().name
    m1 = threading.Thread(target = main)
    m1.setDaemon(True)
    m1.start()

    root.mainloop()
    
    
    
    
