# Wire2waves Ltd
# CCIR 493-4 Selcal Generator & Modulator
# Generic, non-TX GUI


from Tkinter import *
from selcal_functions import *
import threading
import Queue
import time

version = "v0.2"


class Application(Frame):
    def __init__(self, master):
        """ Initialize frame"""
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        
        # we manage the three sound-producing functions in Threads, run at startup but only produce
        # output when their Queues are set to "1"
        self.selqueue = Queue.Queue()
        self.tunequeue = Queue.Queue()
        self.cwqueue = Queue.Queue()
        self.tunequeue.put(0)
        self.selqueue.put(0)
        self.cwqueue.put(0)
        t1 = threading.Thread(target = self.tune)
        t1.setDaemon(True)
        t1.start()
        c1 = threading.Thread(target = self.send_cwid)
        c1.setDaemon(True)
        c1.start()
        d1 = threading.Thread(target = self.send_sel)
        d1.setDaemon(True)
        d1.start()
        
        
    def create_widgets(self):
        
        ###### 
        #
        # The Address Entry Fields
        self.to_l = Label(self, width = 15, text = "To ID", fg = 'red').grid(row = 0, column = 0, sticky = W)
        self.to_sel_id_e = Entry(self, width = 10, fg = 'red')
        self.to_sel_id_e.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = W)
        self.to_sel_id_e.insert(0, "3922")
        
        
        self.from_l = Label(self, width = 15, text = "Self ID", fg = 'blue').grid(row = 1, column = 0, sticky = W)
        self.from_sel_id_e = Entry(self, width = 10, fg = 'blue')
        self.from_sel_id_e.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = W)
        self.from_sel_id_e.insert(0, "3921")
        
        ###################
        #
        # The "Format" selection radio buttons
        self.fmt = StringVar()
        self.fmt_l = Label(self, width = 15, text = "Format").grid(row = 5, column = 0, sticky = W)
        self.sel_r = Radiobutton(self, text = "Sel", variable = self.fmt, value = "sel")
        self.sel_r.grid(row = 5, column = 1, sticky = W)
        self.bcn_r = Radiobutton(self, text = "Bcn", variable = self.fmt, value = "bcn")
        self.bcn_r.grid(row = 5, column = 2, sticky = W)
        #self.fmt_e = Entry(self, width = 10, fg = 'blue')
        #self.fmt_e.grid(row = 5, column = 1, padx = 5, pady = 5, sticky = W)
        #self.fmt_e.insert(0, "120")
        
        #
        # click the "SEL" radio button
        self.sel_r.invoke()
        #
        ########
        
        ######
        #
        # The "Category" selection radio buttons
        
        self.cat = StringVar()
        
        self.cat_l = Label(self, width = 15, text = "Category").grid(row = 6, column = 0, sticky = W)
        self.saf_r = Radiobutton(self, text = "Routine", variable = self.cat, value = "rtn")
        self.saf_r.grid(row = 6, column = 1, sticky = W)
        #self.cat_e = Entry(self, width = 10, fg = 'blue')
        #self.cat_e.grid(row = 6, column = 1, padx = 5, pady = 5, sticky = W)
        #self.cat_e.insert(0, "100")
        
        
        # For selcal we may require other categories, but at present only "Routine" is used
        #self.urg_r = Radiobutton(self, text = "Urgent", variable = self.cat, value = "urg")
        #self.urg_r.grid(row = 6, column = 2, sticky = W)
        #self.dis_r = Radiobutton(self, text = "Distress", variable = self.cat, value = "dis")
        #self.dis_r.grid(row = 6, column = 3, sticky = W)
        
        # click the "Safety" radio-button
        self.saf_r.invoke()
        #
        ########
        
        ####
        #
        # The "EOS" selection radio buttons
        
        self.eosv = StringVar()
        self.eos_l = Label(self, width = 15, text = "EOS").grid(row = 9, column = 0, sticky = W)
        self.req_r = Radiobutton(self, text = "REQ", variable = self.eosv, value = "req")
        self.req_r.grid(row = 9, column = 1, sticky = W)
        #self.eos_e = Entry(self, width = 10, fg = 'blue')
        #self.eos_e.grid(row = 9, column = 1, padx = 5, pady = 5, sticky = W)
        #self.eos_e.insert(0, "117")
        
        # leave these in case other EOS symbols would be useful in the future 
        #self.ack_r = Radiobutton(self, text = "ACK", variable = self.eosv, value = "ack")
        #self.ack_r.grid(row = 9, column = 2, sticky = W)
        
        #self.eos_r = Radiobutton(self, text = "EOS", variable = self.eosv, value = "eos")
        #self.eos_r.grid(row = 9, column = 3, sticky = W)
        
        # click the "REQ" radio button
        self.req_r.invoke()
        #
        ###########
        
        
        ###########
        #
        # The "do something" buttons
        
        self.go_b = Button(self, text = "Send Selcal", command = self.selqueue_on)
        self.go_b.grid(row = 10, column = 0, sticky = W+E)
        
        self.tune_b = Button(self, text = "Tune", command = self.tunequeue_on)
        self.tune_b.grid(row = 13, column = 0, sticky = W+E)
        
        self.cw_call_e = Entry(self)
        self.cw_call_e.grid(row = 14, column = 1, columnspan = 2)
        #
        # The CW Text is pre-set, but can be edited as required on the GUI
        self.cw_call_e.insert(0, "   de GM4SLV   ")
        
        self.cw_b = Button(self, text = "Send CW ->", command = self.cwqueue_on)
        self.cw_b.grid(row = 14, column = 0, sticky = W+E)
        
        ######
        #
        # The display of Selcal Symbols
        #
        
        self.sel_title = Label(self, text = "Sending Selcal Symbols: " , fg = 'blue').grid(row = 16, column = 0)
        
        sel_call_f = Frame(self, relief = GROOVE, borderwidth = 2, pady = 5)
        sel_call_f.grid(row = 17, column = 0, columnspan = 5, padx = 5, pady = 5, sticky = W+E)
        
        
        self.sel_label = StringVar()
        self.sel_l = Label(sel_call_f, textvariable = self.sel_label, fg = 'blue', height = 2, wraplength = 350, anchor = W)
        self.sel_l.grid(row = 0, column = 0)
        #
        #####
        
    
    # When a Tune is required we call tunequeue_on() which puts a "1" into the queue.
    # The queue is read by tune() which is running constantly (while True:) in a thread. 
    # If a "1" is found the tune_carrier() function is triggered
    # then tunequeue_off() will put a "0" in the queue which will inhibit any further
    # tune signals. 
    
    # Since the Tune, CWID and Selcal Transmit all run in their own threads, with their own queues
    # it's possible to do all three functions at once, and still retain an active GUI
    # this may not be "the right way" to do this, but it works...
    
    def tunequeue_on(self):
        self.tunequeue.put(1)
        
    def tunequeue_off(self):
        self.tunequeue.put(0)
        
        
    def tune(self):
        
        while True:
            t_on = self.tunequeue.get()
            if t_on == 1:   
                pwr = 0.7
                tune_carrier(pwr)
                self.tunequeue_off()
    
    
    def cwqueue_on(self):
        self.cwqueue.put(1)
    def cwqueue_off(self):
        self.cwqueue.put(0)
    
    def send_cwid(self):
        while True:
            c_on = self.cwqueue.get()
            if c_on == 1:
                pwr = 0.7
                call = self.cw_call_e.get().upper()
                cwid(call, pwr)
                self.cwqueue_off()
                
    def selqueue_on(self):
        self.selqueue.put(1)
    def selqueue_off(self):
        self.selqueue.put(0)
     
    def send_sel(self):
        
        while True:   
            go = self.selqueue.get()
            if go == 1:
                a_sel_id = self.to_sel_id_e.get()
                s_sel_id = self.from_sel_id_e.get()
                fmt = self.fmt.get()
                cat = self.cat.get()
                eos = self.eosv.get()
                pwr = 0.7
                
                # restrict to 4-digit 493-4
                if len(a_sel_id) != 4:
                    continue
                if len(s_sel_id) != 4:
                    continue
                    
                # convert the format, category and eos to the appropriate symbol values
                fmt_symbol = (fmt_symbol_dict[fmt])
                #fmt_symbol = self.fmt_e.get()
                
                cat_symbol = (cat_symbol_dict[cat])
                #cat_symbol = self.cat_e.get()
                
                eos_symbol = (eos_symbol_dict[eos])
                #eos_symbol = self.eos_e.get()
                
                # convert the 4-digit selcal IDs into two 2-digit symbols
                a_symbol = sel_id_symbol(a_sel_id)
                s_symbol = sel_id_symbol(s_sel_id)
                
                # build the call by joining the symbol values into a list
                sel_call = build_call(fmt_symbol, a_symbol, cat_symbol, s_symbol, eos_symbol)
                
                #we want the basic selcal message returned to us, to display on the GUI
                self.sel_label.set(sel_call)
                
                # turn the selcal queue off to stop further transmissions
                self.selqueue_off()
                
                # then we pass the selcal list and required "power" into "transmit_sel() which does the rest...
                transmit_sel(sel_call, pwr) 
            
       

if __name__ == '__main__':
    root = Tk()
   
    root.geometry("350x350+10+10")
    root.title("GM4SLV HF CCIR 493-4 Selcal " + version)
    root.resizable(0, 0)
    app = Application(root)
    
    
    root.mainloop()