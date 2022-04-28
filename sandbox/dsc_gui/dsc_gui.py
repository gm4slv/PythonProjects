# Wire2waves Ltd
# DSC Generator & Modulator
# Generic, non-TX GUI


from Tkinter import *
from dsc_functions import *
import threading
import Queue
import time

version = "v1.3/cw"


class Application(Frame):
    def __init__(self, master):
        """ Initialize frame"""
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.dscqueue = Queue.Queue()
        self.tunequeue = Queue.Queue()
        self.cwqueue = Queue.Queue()
        self.tunequeue.put(0)
        self.dscqueue.put(0)
        self.cwqueue.put(0)
        t1 = threading.Thread(target = self.tune)
        t1.setDaemon(True)
        t1.start()
        c1 = threading.Thread(target = self.send_cwid)
        c1.setDaemon(True)
        c1.start()
        d1 = threading.Thread(target = self.send_dsc)
        d1.setDaemon(True)
        d1.start()
        
        
    def create_widgets(self):
        
        ###### Normal GUI Widgets
        #
        self.to_l = Label(self, width = 15, text = "To MMSI", fg = 'red').grid(row = 0, column = 0, sticky = W)
        self.to_mmsi_e = Entry(self, width = 10, fg = 'red')
        self.to_mmsi_e.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = W)
        self.to_mmsi_e.insert(0, "111111111")
        
        
        self.from_l = Label(self, width = 15, text = "Self MMSI", fg = 'blue').grid(row = 1, column = 0, sticky = W)
        self.from_mmsi_e = Entry(self, width = 10, fg = 'blue')
        self.from_mmsi_e.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = W)
        self.from_mmsi_e.insert(0, "333333333")
        
        ###################
        area_f = Frame(self, relief = GROOVE, borderwidth = 2, pady = 5)
        area_f.grid(row = 3, column = 0, columnspan = 5, padx = 5, pady = 5, sticky = W+E)
        
        self.ns = StringVar()
        self.ew = StringVar()
        
        self.area_l = Label(area_f, width = 15, text = "Top Left",).grid(row = 2, column = 0, sticky = W)
        
        self.area_lat_e = Entry(area_f, width = 4, fg = 'red')
        self.area_lat_e.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = W)
        self.area_lat_e.insert(0, "00")
        
        self.area_n_r = Radiobutton(area_f, variable = self.ns, text = "N", value = "n")
        self.area_n_r.grid(row = 2, column = 2)
        self.area_s_r = Radiobutton(area_f, variable = self.ns, text = "S", value = "s")
        self.area_s_r.grid(row = 2, column = 3)
        self.area_n_r.invoke()
       
        
        self.area_lon_e = Entry(area_f, width = 4, fg = 'red')
        self.area_lon_e.grid(row = 2, column = 4, padx = 5, pady = 5, sticky = W)
        self.area_lon_e.insert(0, "00")
        
        self.area_w_r = Radiobutton(area_f, variable = self.ew, text = "W", value = "w")
        self.area_w_r.grid(row = 2, column = 5)
        self.area_s_r = Radiobutton(area_f, variable = self.ew, text = "E", value = "e")
        self.area_s_r.grid(row = 2, column = 6)
        self.area_s_r.invoke()
        
        self.area_l = Label(area_f, width = 15, text = "Sides",).grid(row = 3, column = 0, sticky = W)
        self.area_ns_e = Entry(area_f, width = 4, fg = 'red')
        self.area_ns_e.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = W)
        self.area_ns_l = Label(area_f, width = 7, text = 'N --> S').grid(row = 3, column = 2)
        
        self.area_we_e = Entry(area_f, width = 4, fg = 'red')
        self.area_we_e.grid(row = 3, column = 4, padx = 5, pady = 5, sticky = W)
        self.area_we_l = Label(area_f, width = 7, text = 'W --> E').grid(row = 3, column = 5)
        
        freq_f = Frame(self, relief = GROOVE, borderwidth = 2, pady = 5)
        freq_f.grid(row = 4, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = W+E)
        
        self.dtxfreq_l = Label(freq_f, width = 15, text = "TX freq",).grid(row = 0, column = 0, sticky = W)
        self.dtxfreqk_e = Entry(freq_f, width = 8, fg = 'red', justify = RIGHT)
        self.dtxfreqk_e.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = E)
        self.dtxfreqk_e.insert(0, "12345")
        Label(freq_f, width = 1, text = ".").grid(row = 0, column = 2)
        self.dtxfreqh_e = Entry(freq_f, width = 2, fg = 'red')
        self.dtxfreqh_e.grid(row = 0, column = 3, padx = 5, pady = 5, sticky = W)
        self.dtxfreqh_e.insert(0, "0")
        
        self.drxfreq_l = Label(freq_f, width = 15, text = "RX freq",).grid(row = 1, column = 0, sticky = W)
        self.drxfreqk_e = Entry(freq_f, width = 8, fg = 'red',  justify = RIGHT)
        self.drxfreqk_e.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = E)
        self.drxfreqk_e.insert(0, "12345")
        Label(freq_f, width = 1, text = ".").grid(row = 1, column = 2)
        self.drxfreqh_e = Entry(freq_f, width = 2, fg = 'red')
        self.drxfreqh_e.grid(row = 1, column = 3, padx = 5, pady = 5, sticky = W)
        self.drxfreqh_e.insert(0, "0")
        
        self.freq_var = IntVar()
        self.freq_used = Checkbutton(freq_f, text = "Include?", variable = self.freq_var)
        self.freq_used.grid(row = 2, column = 1)
        
        self.fmt = StringVar()
        self.fmt_l = Label(self, width = 15, text = "Format").grid(row = 5, column = 0, sticky = W)
        self.sel_r = Radiobutton(self, text = "Sel", variable = self.fmt, value = "sel")
        self.sel_r.grid(row = 5, column = 1, sticky = W)
        self.all_r = Radiobutton(self, text = "All Ships", variable = self.fmt, value = "all ships")
        self.all_r.grid(row = 5, column = 2, sticky = W)
        self.area_r = Radiobutton(self, text = "Area", variable = self.fmt, value = "area")
        self.area_r.grid(row = 5, column = 3, sticky = W)
        self.group_r = Radiobutton(self, state=DISABLED, text = "Group", variable = self.fmt, value = "group")
        self.group_r.grid(row = 5, column = 4, sticky = W)
        
        self.sel_r.invoke()
        
        self.cat = StringVar()
        
        self.cat_l = Label(self, width = 15, text = "Category").grid(row = 6, column = 0, sticky = W)
        self.saf_r = Radiobutton(self, text = "Routine", variable = self.cat, value = "rtn")
        self.saf_r.grid(row = 6, column = 1, sticky = W)
        self.saf_r = Radiobutton(self, text = "Safety", variable = self.cat, value = "saf")
        self.saf_r.grid(row = 6, column = 2, sticky = W)
        self.urg_r = Radiobutton(self, text = "Urgency", variable = self.cat, value = "urg")
        #self.urg_r = Radiobutton(self, state=DISABLED, text = "Urgency", variable = self.cat, value = "urg")
        self.urg_r.grid(row = 6, column = 3, sticky = W)
        self.dis_r = Radiobutton(self, text = "Distress", variable = self.cat, value = "dis")
        #self.dis_r = Radiobutton(self, state=DISABLED, text = "Distress", variable = self.cat, value = "dis")
        self.dis_r.grid(row = 6, column = 4, sticky = W)
        
        self.saf_r.invoke()
        
        
        self.tc1_var = StringVar()
        self.tc1_l = Label(self, width = 15, text = "TC1").grid(row = 7, column = 0, sticky = W)
        self.tc1_sp = Spinbox(self, width = 15, textvariable = self.tc1_var, readonlybackground = 'white', state = "readonly", values = ("test", "f3e", "f3edup", "poll", "unable", "end", "data", "j3e", "fec", "arq", "test", "pos", "noinf"), wrap = True)
        self.tc1_sp.grid(row = 7, column = 1, columnspan = 3, sticky = W)
        
        
        self.tc2_var = StringVar()
        self.tc2_l = Label(self, width = 15, text = "TC2").grid(row = 8, column = 0, sticky = W)
        self.tc2_sp = Spinbox(self, width = 15, readonlybackground = 'white', textvariable = self.tc2_var, state = "readonly", values = ("noinf", "no reason", "congestion", "busy", "queue", "barred", "no oper", "temp unav", "disabled", "unable channel", "unable mode", "conflict", "medical", "payphone", "fax", "noinf"), wrap = True)
        self.tc2_sp.grid(row = 8, column = 1, columnspan = 3, sticky = W)
        
        self.eosv = StringVar()
        self.eos_l = Label(self, width = 15, text = "EOS").grid(row = 9, column = 0, sticky = W)
        self.req_r = Radiobutton(self, text = "REQ", variable = self.eosv, value = "req")
        self.req_r.grid(row = 9, column = 1, sticky = W)
        self.ack_r = Radiobutton(self, text = "ACK", variable = self.eosv, value = "ack")
        self.ack_r.grid(row = 9, column = 2, sticky = W)
        self.eos_r = Radiobutton(self, text = "EOS", variable = self.eosv, value = "eos")
        self.eos_r.grid(row = 9, column = 3, sticky = W)
        self.req_r.invoke()
        
        
        self.go_b = Button(self, text = "Send DSC", command = self.dscqueue_on)
        self.go_b.grid(row = 10, column = 0, sticky = W+E)
        
        
        self.tune_b = Button(self, text = "Tune", command = self.tunequeue_on)
        self.tune_b.grid(row = 13, column = 0, sticky = W+E)
        
        '''
        self.sendcw = IntVar()
        self.cw_cb = Checkbutton(self, text = "CWID", variable = self.sendcw)
        self.cw_cb.grid(row = 10, column = 1)
        self.cw_cb.deselect()
        '''
        
        self.cw_call_e = Entry(self)
        self.cw_call_e.grid(row = 14, column = 1, columnspan = 2)
        self.cw_call_e.insert(0, "qtc")
        
        self.cw_b = Button(self, text = "Send CW ->", command = self.cwqueue_on)
        self.cw_b.grid(row = 14, column = 0, sticky = W+E)
        
        self.test_b = Button(self, text = "Setup Test Call", command = self.test)
        self.test_b.grid(row = 15, column = 0, sticky = W+E)
        
        self.dsc_title = Label(self, text = "Sending DSC Symbols: " , fg = 'blue').grid(row = 16, column = 0)
        
        dsc_call_f = Frame(self, relief = GROOVE, borderwidth = 2, pady = 5)
        dsc_call_f.grid(row = 17, column = 0, columnspan = 5, padx = 5, pady = 5, sticky = W+E)
        
        
        self.dsc_label = StringVar()
        self.dsc_l = Label(dsc_call_f, textvariable = self.dsc_label, fg = 'blue', height = 3, wraplength = 350, anchor = W)
        self.dsc_l.grid(row = 0, column = 0)
        ####
        
        
    def test(self):
        eos_symbol = 127
        cat_symbol = 108
        fmt_symbol = 120
        tc1_symbol = 118
        tc2_symbol = 126
        self.eosv.set("req")
        self.cat.set("saf")
        self.fmt.set("sel")
        self.tc1_var.set("test")
        self.tc2_var.set("noinf")
        self.freq_var.set(False)
        
        
    def tunequeue_on(self):
        print "tune queue on"
        self.tunequeue.put(1)
    def tunequeue_off(self):
        print "tune queue off"
        self.tunequeue.put(0)
        
        
    def tune(self):
        
        while True:
            t_on = self.tunequeue.get()
            if t_on == 1:
                
                pwr = 0.7
                tune_carrier(pwr)
                self.tunequeue_off()
    
    
    def cwqueue_on(self):
        print "cw queue on"
        self.cwqueue.put(1)
    def cwqueue_off(self):
        print "cw queue off"
        self.cwqueue.put(0)
    
    def send_cwid(self):
        while True:
            c_on = self.cwqueue.get()
            if c_on == 1:
                
                pwr = 0.7
                #sendcw = self.sendcw.get()
                #print "sendcw ", sendcw
                #if sendcw:
                call = self.cw_call_e.get().upper()
                cwid(call, pwr)
                self.cwqueue_off()
                #else:
                #    return
            
    def dscqueue_on(self):
        print "txqueue On"
        self.dscqueue.put(1)
    def dscqueue_off(self):
        print "txqueue Off"
        self.dscqueue.put(0)
     
    def send_dsc(self):
        
        while True:
            #time.sleep(1)
            go = self.dscqueue.get()
            
            if go == 1:
        
                a_mmsi = self.to_mmsi_e.get()
                s_mmsi = self.from_mmsi_e.get()
                fmt = self.fmt.get()
                cat = self.cat.get()
                tc1 = self.tc1_sp.get()
                tc2 = self.tc2_sp.get()
                eos = self.eosv.get()
                ns = self.ns.get()
                ew = self.ew.get()
                pwr = 0.7
                quadrant = area_table[ns + ew]
                area = quadrant + self.area_lat_e.get().rjust(2,'0') + self.area_lon_e.get().rjust(3,'0') + self.area_ns_e.get().rjust(2,'0') + self.area_we_e.get().rjust(2, '0')
                dtxfreqk = self.dtxfreqk_e.get().rjust(5, '0')
                drxfreqk = self.drxfreqk_e.get().rjust(5, '0')
                dtxfreqh = self.dtxfreqh_e.get().rjust(1,'0')
                drxfreqh = self.drxfreqh_e.get().rjust(1, '0')
                print "freq info ", dtxfreqk + dtxfreqh + drxfreqk + drxfreqh
       
                try:
                    dfreq = int(dtxfreqk + dtxfreqh + drxfreqk + drxfreqh)
                    dfreq = str(dtxfreqk + dtxfreqh + drxfreqk + drxfreqh)
                except:
                    return
        
        
                if len(a_mmsi) != 9:
                    continue
                if len(s_mmsi) != 9:
                    continue
        
                fmt_symbol = int(fmt_symbol_dict[fmt])
                cat_symbol = int(cat_symbol_dict[cat])
                tc1_symbol = int(tc1_symbol_dict[tc1])
                tc2_symbol = int(tc2_symbol_dict[tc2])
                eos_symbol = int(eos_symbol_dict[eos])

                # convert the MMSI 9-digits into a list of 2-digit symbols
                if fmt_symbol == 102:# if  "Area"
                    
                    a_symbol = area_symbol(area)
                    print dfreq
                    if len(dfreq) > 12:
                        continue
                    data_symbol = freq_symbol(dfreq)
                    print data_symbol
                    eos_symbol = 127
                    cat_symbol = 108
                    tc1_symbol = 109
                    self.freq_var.set(True)
                    self.eosv.set("eos")
                    self.cat.set("saf")
                    self.tc1_var.set("j3e")
                    s_symbol = mmsi_symbol(s_mmsi)
                   
                    
                    dsc_call = build_call(fmt_symbol, a_symbol, cat_symbol, s_symbol, tc1_symbol, tc2_symbol, data_symbol, eos_symbol)
               
                    self.dsc_label.set(dsc_call)
                    self.dscqueue_off()
                    transmit_dsc(dsc_call, pwr) 
                    continue
                    #return
                    
                else:
                    a_symbol = mmsi_symbol(a_mmsi)
                    data_symbol = [ 126, 126, 126, 126, 126, 126 ]
        
            
        

            # hard-coded Data symbols
            # if "All Ships" - set freq to 12345.6/12345.6
                if fmt_symbol == 116:
                    
            
                    if len(dfreq) > 12:
                        continue
                    data_symbol = freq_symbol(dfreq)
                    eos_symbol = 127
                    cat_symbol = 108
                    tc1_symbol = 109
                    self.freq_var.set(True)
                    self.tc1_var.set("j3e")
                    self.eosv.set("eos")
                    self.cat.set("saf")
                    s_symbol = mmsi_symbol(s_mmsi)
                    self.dscqueue.put(0)
                    
                    dsc_call = build_call(fmt_symbol, a_symbol, cat_symbol, s_symbol, tc1_symbol, tc2_symbol, data_symbol, eos_symbol)
               
                    self.dsc_label.set(dsc_call)
                    self.dscqueue_off()
                    transmit_dsc(dsc_call, pwr) 
                    continue
                # otherwise, set data to "no info" 
                else:
                    data_symbol = [ 126, 126, 126, 126, 126, 126 ]
            
                if (tc1_symbol == 109) or (tc1_symbol == 106) or (tc1_symbol == 113) or (tc1_symbol == 115) or (self.freq_var.get() == True):
                    if len(dfreq) > 12:
                        continue
                    self.freq_var.set(True)
                    data_symbol = freq_symbol(dfreq)
            
                s_symbol = mmsi_symbol(s_mmsi)
                
                
                    
                    
                    
        
               
                
        
                dsc_call = build_call(fmt_symbol, a_symbol, cat_symbol, s_symbol, tc1_symbol, tc2_symbol, data_symbol, eos_symbol)
               
                self.dsc_label.set(dsc_call)
                self.dscqueue_off()
                transmit_dsc(dsc_call, pwr) 
            #return
       

if __name__ == '__main__':
    root = Tk()
   
    root.geometry("500x550+10+10")
    root.title("GM4SLV MF/HF DSC " + version)
    root.resizable(0, 0)
    app = Application(root)
    
    
    root.mainloop()
