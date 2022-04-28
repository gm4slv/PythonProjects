# # new class-based gui

from Tkinter import *
import socket
import threading
import time



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
        qrg_frame.grid(row=5, column=0, columnspan=5, rowspan=2, sticky=W)
        
        mode_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        mode_frame.grid(row=3, column=0, columnspan=5, rowspan=2, sticky=W)
        
        
        bw_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        bw_frame.grid(row=7, column=0, columnspan=5, rowspan=2, sticky=W)
        
        band_frame = Frame(radio_frame, borderwidth=2, relief=GROOVE)
        band_frame.grid(row=10, column=0, columnspan=5, rowspan=2, sticky=W)
        
        Label(radio_frame, text="Name", width=10).grid(row=0, column=0)
        Label(radio_frame, text="Freq/kHz", width=10).grid(row=0, column=1)
        Label(radio_frame, text="Mode", width=10).grid(row=0, column=2)
        Label(radio_frame, text="BW/Hz", width=10).grid(row=0, column=3)
        Label(radio_frame, text="Signal/dBm", width=10).grid(row=0, column=4)
        Label(radio_frame, text="Max/dBm", width=10, fg='red').grid(row=0, column=5)
        Label(radio_frame, text="Ave/dBm", width=10, fg='green').grid(row=0, column=6)
        Label(radio_frame, text="Min/dBm", width=10, fg='blue').grid(row=0, column=7)

        self.name_l = StringVar()
        self.l_name = Label(radio_frame, textvariable=self.name_l, width=10)
        self.l_name.grid(row=1, column=0, sticky=W)
        
        self.freq_l = StringVar()
        self.l_freq = Label(radio_frame, fg='red', textvariable=self.freq_l, width=10)
        self.l_freq.grid(row=1, column=1, sticky=E)
        
        self.mode_l = StringVar()
        self.l_mode = Label(radio_frame, textvariable=self.mode_l, width=10)
        self.l_mode.grid(row=1, column=2, sticky=E)
        
        self.bw_l = StringVar()
        self.l_bw = Label(radio_frame, textvariable=self.bw_l, width=10)
        self.l_bw.grid(row=1, column=3, sticky=E)
        
        '''
        self.e_mode = Entry(radio_frame, width=10, bg = 'white', fg = 'black', insertbackground = 'blue')
        self.e_mode.grid(row=2, column=2)
        self.e_mode.bind('<Return>', (lambda event: self.set_mode(self.num)))
        '''
        #self.e_mode = StringVar()
        
        self.modeframe_l=Label(mode_frame, text="Mode").grid(row=0, column=0)
        

        self.b_mode_usb = Button(mode_frame, text = "USB", width = 4, command = lambda: self.set_mode("usb", self.num))
        self.b_mode_usb.grid(row = 3, column = 0)
        
        self.b_mode_lsb = Button(mode_frame, text = "LSB", width = 4, command = lambda: self.set_mode("lsb", self.num))
        self.b_mode_lsb.grid(row = 3, column = 1)
        
        self.b_mode_data = Button(mode_frame, text = "RTTY", width = 4, command = lambda: self.set_mode("rtty", self.num))
        self.b_mode_data.grid(row = 3, column = 2)
        
        self.b_mode_cw = Button(mode_frame, text = "CW", width = 4, command = lambda: self.set_mode("cw", self.num))
        self.b_mode_cw.grid(row = 4, column = 0)
        
        self.b_mode_am = Button(mode_frame, text = "AM", width = 4, command = lambda: self.set_mode("am", self.num))
        self.b_mode_am.grid(row = 4, column = 1)
        
       
        self.b_tune = Button(mode_frame, text = "Tune", width = 4, command = lambda: self.atutune(self.num))
        self.b_tune.grid(row = 4, column = 2)
        
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
        self.b_bw_1k.grid(row = 8, column = 4)
        self.b_bw_2k = Button(bw_frame, text = "2000", width = 4, command = lambda: self.set_bw("24",self.num))
        self.b_bw_2k.grid(row = 8, column = 5)
        self.b_bw_2k5 = Button(bw_frame, text = "2500", width = 4, command = lambda: self.set_bw("29",self.num))
        self.b_bw_2k5.grid(row = 8, column = 6)
        self.b_bw_2k5 = Button(bw_frame, text = "2800", width = 4, command = lambda: self.set_bw("32",self.num))
        self.b_bw_2k5.grid(row = 8, column = 7)
        
        self.b_bw_2k5 = Button(bw_frame, text = "3000", width = 4, command = lambda: self.set_bw("34",self.num))
        self.b_bw_2k5.grid(row = 8, column = 8)
        
        self.band160_b = Button(band_frame, text = "160m")
        self.band160_b.grid(row = 6, column = 0,sticky=EW)
        self.band80_b = Button(band_frame, text = "80m")
        self.band80_b.grid(row = 6, column = 1)
        self.band60_b = Button(band_frame, text = "60m")
        self.band60_b.grid(row = 6, column = 2)
        self.band40_b = Button(band_frame, text = "40m")
        self.band40_b.grid(row = 6, column = 3)
        self.band30_b = Button(band_frame, text = "30m")
        self.band30_b.grid(row = 7, column = 0,sticky=EW)
        self.band20_b = Button(band_frame, text = "20m")
        self.band20_b.grid(row = 7, column = 1)
        self.band17_b = Button(band_frame, text = "17m")
        self.band17_b.grid(row = 7, column = 2)
        
        
        self.smeter_l = StringVar()
        self.l_smeter = Label(radio_frame, textvariable=self.smeter_l, width=10)
        self.l_smeter.grid(row=1, column=4, sticky=E)

        self.max_var = StringVar()
        self.l_max = Label(radio_frame, textvariable=self.max_var, width=10)
        self.l_max.grid(row=1, column=5)
        
        self.ave_var = StringVar()
        self.l_average = Label(radio_frame, textvariable=self.ave_var, width=10)
        self.l_average.grid(row=1, column=6)

        self.min_var = StringVar()
        self.l_min = Label(radio_frame, textvariable=self.min_var, width=10)
        self.l_min.grid(row=1, column=7)

        self.e_freq = Entry(radio_frame, width=10, bg = 'white', fg = 'black', insertbackground = 'blue')
        self.e_freq.grid(row=2, column=1)
        self.e_freq.focus()
        self.e_freq.bind('<Return>', (lambda event: self.set_freq(self.num)))
        
        
        
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
        
        #self.set_log = IntVar()
        #self.cb_log = Checkbutton(radio_frame, variable = self.set_log)
        #self.cb_log.grid(row = 8, column = 1, sticky = W)
        
        #self.l_log = Label(radio_frame, width = 10, text = "Log to file...")
        #self.l_log.grid(row = 8, column = 0, sticky = E)

        self.c1 = Canvas(radio_frame, width=260, height=100, bg='black')
        self.c1.grid(row=2, column=4, columnspan=4, rowspan=3)

        name = self.get_name(radio)
       

    def get_all(self):
        
        self.get_freq(self.num)
        self.get_mode(self.num)
        self.get_smeter(self.num)
        self.get_preamp(self.num)
        self.get_atten(self.num)
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
        self.qsy = float(delta)
        self.cur_freq = float(n1.connect("getfreq" + " " + radio))
        self.new_freq = self.cur_freq + self.qsy
        self.newfreq = n1.connect("setfreq" + " " + str(self.new_freq) + " " + radio)
        return
        
    def qsy_dn(self, delta, radio):
        self.qsy = float(delta)
        self.cur_freq = float(n1.connect("getfreq" + " " + radio))
        self.new_freq = self.cur_freq - self.qsy
        self.newfreq = n1.connect("setfreq" + " " + str(self.new_freq) + " " + radio)
        return

    def set_freq(self, radio):
        self.freq = str(self.e_freq.get())
        self.newfreq = n1.connect("setfreq" + " " + self.freq + " " + radio)
        self.e_freq.delete(0, END)
        return


    def get_mode(self, radio):
        self.mode = n1.connect("getmode" + " " + radio)
        self.mode_l.set(self.mode)
        return

    def set_mode(self, mode, radio):
        #self.mode = str(self.e_mode.get())
        self.newmode = n1.connect("setmode" + " " + mode + " " + radio)
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
    #w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #root.geometry("%dx%d+0+0" % (w, h))
    root.geometry("700x400")
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
    
    
    
    
