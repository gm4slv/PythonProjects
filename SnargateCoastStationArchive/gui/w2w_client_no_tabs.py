"""
Wire2waves DSC Coast Station : GMDSS DSC Coast Station server and client

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
"""
##################
#
# 
# Wire2waves Ltd
# 
# Python GMDSS Coast Station Auto-Test Responder
# 
# April/May 2015
# 
# Network administration client using TKinter
#


version = "v0.5"

from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from tkSimpleDialog  import *
from ScrolledText import *
import time
import re
import socket

import threading
import Queue

ABOUT_TEXT = "Wire2waves DSC Coast Station : GMDSS DSC Coast Station client \n\n version "+ version + '''\n\n
    Copyright (C) 2015  John Pumford-Green
    Wire2Waves Ltd
    Shetland
    john@wire2waves.co.uk
    

'''


# Coast Station Server host / port
HOST, PORT = "gm4slv.plus.com", 50669





# The class for a TCP/IP connection to the Server
# Instantiated at program startup 
class Network(object):
    def __init__(self):
        # when the n1 instance is created, do nothing - we'll connect later under
        # user control
        #self.make_con()
        #self.send_command("hello")
        pass
    
    # connect to the Coast Station server at the HOST, PORT
    # make_con() is called 
    # 1) by the user pressing the "CONNECT" button
    # 2) by an auto-reconnect mechanism driven by the regular polling of server information
    def make_con(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
        
            return self.sock
        except:
            return
    
    # the send/receive function to send a command to the server and read the reply.
    # To allow the server to send a unspecified amount of data, which may exceed the recv() buffer
    # size we prepend the data from the server by a number, delimited by a "@" character, which is 
    # the number of bytes in the full message. The initial recv() buffer is 8k, but will be increased 
    # in response to the reported message length, and receive is called until all the data is
    # transferred.
    # The recipe came from a combination of sources:
    # http://stackoverflow.com/questions/1708835/receiving-socket-python
    # for the general idea to prepend the data with a length and a delimiting character. I chose the 
    # "@" character because it is not sent by any server replies.
    # http://code.activestate.com/recipes/408859/
    # for the buffer handling in the "recv_size" method described, but substituting the simpler
    # len(message) from the first reference for the packed 4-byte method of the second.
    def connect(self, data):
        try:
        
            lock.acquire()
            #print lock
            # sendall our data to the server in a single line
            self.sock.sendall(data + "\n")
        
            # the buffer management
            # initialize a measure of total length received and a list "total_data" to hold
            # the incoming message in chunks as it's read into "buffer"
            total_len = 0
            total_data = []
            # initially we set the maximum expected message size to 64k - although this could be increased
            # when we begin taking in the data
            size = 65532
            size_data = sock_data = ''
            # buffer to append each incoming string to
            buffer = ""
            recv_size = 8192
        
            # total_len is zero at the start... it will grow as the message is read, until it is equal to 
            # the reported message size. Initially "size" = "a big number", but after the first loop we know the 
            # true payload size and "size" is reassigned this value. We keep looping until total_len (all the data
            # received so far) = the expected data payload size.
            while total_len < size:
            
                sock_data = self.sock.recv(recv_size)
                if not sock_data:
                    break
                
                # total_data is empty at the start so we do the first "find the length" and the first 
                # section of payload process... setting the recv() buffer size to match 
                # the expected length of data so that the second recv() will get all the remaining data as the 
                # TCP buffer will now be large enough.
                if not total_data:
 
                    # append the read data to the buffer
                    buffer += sock_data
                    # determine the length_str, ignore the "@" delimiter, buffer is now the remaining 
                    # data in this block
                    length_str, ignored, buffer = buffer.partition('@')
                    # the size string is converted to an integer
                    size = int(length_str)
                    # set the recv() to buffer "size" number of bytes - the expected size of the message
                    recv_size=size
                    # set a maximum limit to the size of the TCP recv() buffer.
                    if recv_size>524288:
                        recv_size = 5224288
                        
                    # add the first block ("buffer") to the list total_data[] - this is the data minus the size header
                    # from the first "8k" of data from the first recv()
                    total_data.append(buffer)
                
                   
                    # total_data already has the first buffer-full, so we do the else: clause the second time round, ignoring 
                    # the size determining process
                    # This should give us a list with all the data in two elements
                else:
                    total_data.append(sock_data)
            
                    # total_len is the length of the data received.
                    # we test it in the While statement to see if it is < the expected size. 
                    # when total_len >= size we can stop the While loop.
                total_len=sum([len(i) for i in total_data])
                #print total_len
        finally:
            lock.release()
            # our result is a join of the two elements of the total_data list
            return ''.join(total_data)
              
   
# The GUI class... 
class Application(Frame):
    def __init__(self, master):
        # The frame for the main controls and a terminal window
        Frame.__init__(self, master)
        global id
        global invalid_count
        invalid_count = 0
        self.grid()
        
        
        
            
        menubar = Menu(root)
        
        menubar.add_command(label="Save...", command = self.save_current_window)
        
        menubar.add_command(label="Log download..", command=self.allsyswin)
        
        menubar.add_command(label="About", underline=0, command=self.about)
        
        servermenu = Menu(menubar, tearoff=0)
        #servermenu.add_command(label="Login", underline=0, command=self.get_username)
        #servermenu.add_separator()
        servermenu.add_command(label="Shutdown", underline=0, command= lambda: self.shutdown())
        
        menubar.add_cascade(label="Server", menu=servermenu, underline=0)
        
        menubar.add_command(label="Quit", underline=0, command= lambda: self.callback())
        root.config(menu=menubar)
        
        
        #self.status_win()
        
        #self.button_3_frame.withdraw()
        id = askstring("Username", "Name")
        #self.get_username()
        self.create_widgets()
        #self.dsc_buttons()
        
        self.make_con()
        # options for saving log files - used by file_save()
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]
        self.log_queue = Queue.Queue(maxsize=10)
        self.log_thread_stop_event = threading.Event()
        self.poll_log_thread = threading.Thread(target=log_thread, name='Thread', args=(self.log_queue,self.log_thread_stop_event))
        self.poll_log_thread.start()
        
        
        
        self.status_queue = Queue.Queue(maxsize=10)
        self.poll_thread_stop_event = threading.Event()
        self.poll_status_thread = threading.Thread(target=status_thread, name='Thread', args=(self.status_queue,self.poll_thread_stop_event))
        self.poll_status_thread.start()

        self.poll_interval = 1000
        self.log_flag.set("sys")
        self.show()
        #self.show_rx()
        self.showsys_b.focus_set()
        self.status_poll()
        self.log_poll()
        
        root.protocol("WM_DELETE_WINDOW", self.callback)
        root.lift()
    # called by the "Quit" menu entry
    def callback(self):
        if askyesno('Verify', 'Really quit?', default='no'):
            self.close()
            
            self.cleanup_on_exit()
            #root.destroy()
        else:
            pass
    def get_username(self):
        global id
        global invalid_count
        if invalid_count < 3:
            self.close()
            id = ""
            invalid_count += 1
            id = askstring("Retry %d of 3" % invalid_count, "Try again")
        else:
            self.close() 
            showinfo("Closing", "Too many attempts")            
            self.cleanup_on_exit()
        
    def shutdown(self):
    
        self.shutdown_allowed = 1
        #self.shutdown_allowed = self.en_sd.get()
        if self.shutdown_allowed:
            if askyesno('Verify', 'Really Shutdown Server?', default='no'):
                poll_cmd("SHUTDOWN")
            else:
                showinfo('No', 'Server Shutdown has been cancelled')
                #self.cb_en_sd.deselect()
                #self.shutdown_b.configure(fg='grey')
                #self.shutdown_b.configure(state=DISABLED)
                pass
                
    def handler(self):
        pass
        
    def about(self):
            showinfo("About", ABOUT_TEXT)
            
    def show(self):
        
        if self.log_flag.get() == "sys":

            #self.rx_term.grid_remove()
            #self.tx_term.grid_remove()
            self.rxtx_term.grid_remove()
            self.mmsi_term.grid_remove()
            #self.allsys_term.grid_remove()
            self.sys_term.grid()
            
            
            
        #elif self.log_flag.get()  == "rx":
        #    self.sys_term.grid_remove()
        #    #self.tx_term.grid_remove()
        #    self.rxtx_term.grid_remove()
        #    self.mmsi_term.grid_remove()
        #    #self.allsys_term.grid_remove()
        #    #self.rx_term.grid()
            
            
            
        #elif self.log_flag.get() == "tx":
        #    self.sys_term.grid_remove()
        #    self.rx_term.grid_remove()
        #    self.rxtx_term.grid_remove()
        #    self.mmsi_term.grid_remove()
        #    #self.allsys_term.grid_remove()
        #    self.tx_term.grid()
            
            
        elif self.log_flag.get() == "rxtx":
            self.sys_term.grid_remove()
            #self.rx_term.grid_remove()
            #self.tx_term.grid_remove()
            self.mmsi_term.grid_remove()
            #self.allsys_term.grid_remove()
            self.rxtx_term.grid()
        
        elif self.log_flag.get() == "mmsi":
            self.sys_term.grid_remove()
            #self.rx_term.grid_remove()
            #self.tx_term.grid_remove()
            self.rxtx_term.grid_remove()
            #self.allsys_term.grid_remove()
            self.mmsi_term.grid()
            self.get_mmsi_log()

        #elif self.log_flag.get() == "allsys":
        #    self.sys_term.grid_remove()
        #    self.rx_term.grid_remove()
        #    self.tx_term.grid_remove()
        #    self.rxtx_term.grid_remove()
        #    self.mmsi_term.grid_remove()
        #    self.allsys_term.grid()
            
            #self.get_allsys_log() 
   
    def allsyswin(self):
    
        # test to see if the frame already exists.
        try:
            self.allsys_frame_exists = self.allsys_frame.winfo_exists()
        except:
            self.allsys_frame_exists = 0
        
        # If not we can create it and a ScrolledText widget. The text is updated automatically 
        if self.allsys_frame_exists == 0:
            self.allsys_frame = Toplevel(self,  bg = 'black', takefocus=True)
            self.allsys_frame.title("Full Log File retreive")
            
            self.allsys_frame.resizable(0, 0)
            
            self.allsys_frame.grid() 
            self.allsysmenu = Menu(self.allsys_frame)
            self.allsysmenu.add_command(label="Retrieve RX/TX log...", command = lambda: self.get_allrxtx_log())
            
            self.allsysmenu.add_command(label="Retrieve RX log...", command = lambda: self.get_allrx_log())
            self.allsysmenu.add_command(label="Retrieve TX log...", command = lambda: self.get_alltx_log())
            self.allsysmenu.add_command(label="Retrieve Syslog (slow)...", command = lambda: self.get_allsys_log())
            self.allsysmenu.add_command(label="Save...", command= lambda: self.file_save(self.allsys_term.get(1.0, END)))
            
            self.allsys_frame.config(menu=self.allsysmenu)
        
            self.allsys_term = ScrolledText(self.allsys_frame, fg='black', bg='#b0c4de', width = 120, height = 25, wrap = WORD)
            self.allsys_term.grid(row = 0, column = 0, sticky=W+E+N+S)
            self.allsys_term.insert(END, "To view the complete log click the required \"Retrieve...\" menu \nThe files may take a few seconds to appear")
            self.allsys_frame.lift()
            self.allsys_frame.focus_force()
            #self.get_allsys_log()
        # Otherwise restore it from minimzation, and lift it to the top of the windows
        else:
            self.allsys_frame.wm_state('normal')
            self.allsys_frame.lift()
            self.allsys_frame.focus_force()
            #self.get_allsys_log()
    
    
            
    def dsc_buttons(self):
    # a frame for more buttons, again held in the main application window
        self.button_3_frame = Frame(self.status_frame)
        #self.button_3_frame = Toplevel(self, bg="#b0c4de")
        #self.button_3_frame.resizable(0, 0)
        #self.button_3_frame.title("Send DSC")
        #self.button_3_frame.protocol("WM_DELETE_WINDOW", self.hide_dsc)
        self.button_3_frame.grid(row = 0, column = 10)
    
    
    def get_allsys_log(self):
        
            
        allsys_log = poll_cmd("GETALLADMINSQL")
        
        try: # in a try/except because the term may not exist if the user hasn't pressed the button, but the function is still called by poll() anyway
            self.allsys_term.delete(0.0, END)
            self.allsys_term.insert(END, allsys_log+"\n")
            self.allsys_term.yview(END)
        except:
            pass
        
    def get_allrxtx_log(self):
        allsys_log = poll_cmd("GETALLRXTXSQL")
        try: # in a try/except because the term may not exist if the user hasn't pressed the button, but the function is still called by poll() anyway
            self.allsys_term.delete(0.0, END)
            self.allsys_term.insert(END, allsys_log+"\n")
            self.allsys_term.yview(END)
        except:
            pass
            
    def get_allrx_log(self):
        
        allsys_log = poll_cmd("GETALLRXSQL")
        try: # in a try/except because the term may not exist if the user hasn't pressed the button, but the function is still called by poll() anyway
            self.allsys_term.delete(0.0, END)
            self.allsys_term.insert(END, allsys_log+"\n")
            self.allsys_term.yview(END)
        except:
            pass
            
    def get_alltx_log(self):
        allsys_log = poll_cmd("GETALLTXSQL")
        try: # in a try/except because the term may not exist if the user hasn't pressed the button, but the function is still called by poll() anyway
            self.allsys_term.delete(0.0, END)
            self.allsys_term.insert(END, allsys_log+"\n")
            self.allsys_term.yview(END)
        except:
            pass
    
    def get_mmsi_log(self):
        # not regularly polled - but uses the poll_cmd() to prevent the results being written to the main window 
        mmsi_log = poll_cmd("GETRESOLVESQL")       
        try:
            self.mmsi_term.config(state='normal')
            self.mmsi_term.delete(0.0, END)             # clear the contents of the terminal window
            self.mmsi_term.insert(END, mmsi_log+"\n")   # insert the new list
            self.mmsi_term.yview(END)            # scroll to the bottom
            self.mmsi_term.config(state='disabled')
        except:
            pass
            
    
    def save_current_window(self):
        self.current_window = self.log_flag.get()
        if self.current_window == "sys":
            self.file_save(self.sys_term.get(1.0, END))
        #elif self.current_window == "rx":
        #    self.file_save(self.rx_term.get(1.0, END))
        #elif self.current_window == "tx":
        #    self.file_save(self.tx_term.get(1.0, END))
        elif self.current_window == "rxtx":
            self.file_save(self.rxtx_term.get(1.0, END))
        elif self.current_window == "mmsi":
            self.file_save(self.mmsi_term.get(1.0, END))
        #elif self.current_window == "allsys":
        #    self.file_save(self.allsys_term.get(1.0, END))   
            
    # Uses tkMessageBox widget to get a file-name and saves the text sent by the calling function
    def file_save(self, text2save):
        self.f = asksaveasfile(mode='w', **self.file_opt)
        if self.f is None:
            return
  
        self.f.write(text2save)
        self.f.close()
        
        
    def create_widgets(self):
    
        
    
        self.sys_frame = Frame(self, borderwidth=0)    
        self.sys_frame.grid(row=2, column = 0, rowspan = 9, columnspan = 14, sticky=N+S+E+W) 
        
        self.status_frame =  Frame(self.sys_frame, borderwidth=1,relief=GROOVE, bg='#b0c4de')
        self.status_frame.grid(row = 10, column  = 0, columnspan = 14, sticky=N+S+E+W)
        
        self.cb_frame = Frame(self.status_frame, bg='#b0c4de')      
        self.cb_frame.grid(row=0, column=0, columnspan = 10, sticky=N+S+E+W)
        
        self.button_3_frame = Frame(self.status_frame, bg="#b0c4de")
        self.button_3_frame.grid(row = 0, column = 11, columnspan=3, rowspan = 10, sticky=N+S+W+E)
        
        #self.button_1_frame = Frame(self.status_frame,  bg="#b0c4de")
        #self.button_1_frame.grid(row = 8, column = 8)
        
        self.log_flag = StringVar()
        
        self.showsys_b = Radiobutton(self, text="System Log", takefocus=1, pady=0, borderwidth=0, selectcolor='#b0c4de', indicatoron = 0, variable = self.log_flag, value="sys", command= self.show)
        self.showsys_b.grid(row = 1, column = 0, sticky=W+E)
        self.showsys_b.bind( '<Return>', (lambda event: self.showsys_b.invoke()))
        
        self.showrxtx_b = Radiobutton(self, text="RX/TX Log",  takefocus=1, pady=0, borderwidth=0, selectcolor='#b0c4de', indicatoron = 0, variable = self.log_flag, value = "rxtx",  command = self.show)
        self.showrxtx_b.grid(row = 1, column = 1,  sticky=W+E)
        self.showrxtx_b.bind( '<Return>', (lambda event: self.showrxtx_b.invoke()))
        
        #self.showrx_b = Radiobutton(self, text="RX Log", pady=0, takefocus=1,  borderwidth=0, selectcolor='#b0c4de', indicatoron = 0, variable = self.log_flag, value = "rx",  command = self.show)
        #self.showrx_b.grid(row = 1, column = 2,  sticky=W+E)
        #self.showrx_b.bind( '<Return>', (lambda event: self.showrx_b.invoke()))
        
        #self.showtx_b = Radiobutton(self, text="TX Log",  pady=0,takefocus=1,  borderwidth=0, selectcolor='#b0c4de', indicatoron = 0, variable = self.log_flag, value = "tx", command = self.show)
        #self.showtx_b.grid(row = 1, column = 3, sticky=W+E)
        #self.showtx_b.bind( '<Return>', (lambda event: self.showtx_b.invoke()))
        
        
        
        self.showmmsi_b = Radiobutton(self, text="MMSI Log", pady=0,takefocus=1,  borderwidth=0,  selectcolor='#b0c4de', indicatoron = 0, variable = self.log_flag, value = "mmsi",  command = self.show)
        self.showmmsi_b.grid(row = 1, column = 2,  sticky=W+E)
        self.showmmsi_b.bind( '<Return>', (lambda event: self.showmmsi_b.invoke()))
        
        #self.showallsys_b = Radiobutton(self, text="Full Log", selectcolor='#b0c4de', indicatoron = 0, variable = self.log_flag, value = "allsys",  command = self.show)
        #self.showallsys_b.grid(row = 1, column = 6,  sticky=W+E)
        
        #self.all_get_b = Button(self, text="<Refresh", command = self.get_allsys_log)
        #self.all_get_b.grid(row=1, column = 7, sticky=W+E)
        
        self.sys_term = ScrolledText(self.sys_frame, takefocus=0, pady=0, borderwidth=0, fg='black', bg='#b0c4de', width = 120, height = 18, wrap = WORD)
        self.sys_term.grid(row = 1, column = 0, columnspan = 14,  sticky=W+E+N+S)
        
        #self.rx_term = ScrolledText(self.sys_frame, takefocus=0, pady=0, borderwidth=0, fg='blue', bg='#b0c4de',  height = 18, wrap = WORD)
        #self.rx_term.grid(row = 1, column = 0, columnspan = 12,  sticky=W+E+N+S)
        
        #self.tx_term = ScrolledText(self.sys_frame, takefocus=0, pady=0, borderwidth=0, fg='red', bg='#b0c4de', height = 18, wrap = WORD)
        #self.tx_term.grid(row = 1, column = 0, columnspan = 12,  sticky=W+E+N+S)
        
        self.rxtx_term = ScrolledText(self.sys_frame,takefocus=0, pady=0, borderwidth=0,  fg='blue', bg='#b0c4de', width = 120, height = 18, wrap = WORD)
        self.rxtx_term.grid(row = 1, column = 0, columnspan = 14,  sticky=W+E+N+S)
        
        self.mmsi_term = ScrolledText(self.sys_frame,takefocus=0, fg='darkgreen',  pady=0, borderwidth=0, bg='#b0c4de',  width = 120, height = 18, wrap = WORD)
        self.mmsi_term.grid(row = 1, column = 0, columnspan = 14,  sticky=W+E+N+S)
        
        
        #self.allsys_term = ScrolledText(self.sys_frame, fg='blue', bg='#b0c4de', width = 120, height = 35, wrap = WORD)
        #self.allsys_term.grid(row = 1, column = 0, columnspan = 10,  sticky=W+E+N+S)
        
        self.snargate_reply8 = StringVar()
        self.l_reply8 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply8, width=80, font=('sans',9,''))
        self.l_reply8.grid(row=1, column=0,  sticky=E+W)
        
        self.snargate_reply1 = StringVar()
        self.l_reply1 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply1, width=80, font=('sans',9,'bold'))
        self.l_reply1.grid(row=2, column=0,  sticky=E+W)
        
        self.snargate_reply2 = StringVar()
        self.l_reply2 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply2, width=80, font=('sans',9,'bold'))
        self.l_reply2.grid(row=3, column=0,  sticky=E+W)
        
        self.snargate_reply3 = StringVar()
        self.l_reply3 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply3, width=80, font=('sans',9,'bold'))
        self.l_reply3.grid(row=4, column=0,  sticky=E+W)
        
        self.snargate_reply4 = StringVar()
        self.l_reply4 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply4, width=80, font=('sans',9,'bold'))
        self.l_reply4.grid(row=5, column=0,  sticky=E+W)
        #self.make_con()
        
        self.snargate_reply5 = StringVar()
        self.l_reply5 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply5, width=80, font=('sans',9,'bold'))
        self.l_reply5.grid(row=6, column=0,  sticky=E+W)
        
        self.snargate_reply6 = StringVar()
        self.l_reply6 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply6, width=80, font=('sans',9,'bold'))
        self.l_reply6.grid(row=7, column=0,  sticky=E+W)
        
        self.snargate_reply7 = StringVar()
        self.l_reply7 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply7, width=80, font=('sans',9,''))
        self.l_reply7.grid(row=8, column=0,  sticky=E+W)
        
        
        
        self.snargate_reply9 = StringVar()
        self.l_reply9 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply9, font=('sans',9,''))
        self.l_reply9.grid(row=9, column=0, sticky=E+W)
        
        
        
        # A label...        
        self.cbf_l = Label(self.cb_frame, bg='#b0c4de', text="Channels allowed")
        self.cbf_l.grid(row=1, column=0, columnspan=2)
        
        # Checkbuttons to select/deselect individual channels. The boxes indicate the current state retreived from the server
        # Each button calls a function to send the necessary command depending on whether the box is selected or de-selected.
        # If another user changes the state of a band, this will be echoed on the selections of the boxes on all other connected
        # clients.
        
        # TX State : to display and control the Server TX Inhibit function
        self.tx_state = IntVar() 
        # the variable is read by the polling of get_tx_state() and indicates whether TX is Enabled/Disable. The state
        # of the CB mirrors the state of the TX Inhibit reported by the server.
        # ticking the CB will run "tx_on()" and send the istruction to the server to enable TX
        #self.cb_tx_state = Checkbutton(self.cb_frame, bg='#b0c4de', text="TX Enable", variable=self.tx_state, command=lambda: self.tx_on())
        #self.cb_tx_state.grid(row=1, column=9, columnspan=2, sticky=E)
        
        self.sel2 = IntVar()
        self.cb_2 = Checkbutton(self.cb_frame, text="2MHz", bg='#b0c4de', takefocus=0, variable=self.sel2, command=lambda: self.sel_2())
        self.cb_2.grid(row=1, column=2, sticky=E)
        
        self.sel4 = IntVar()
        self.cb_4 = Checkbutton(self.cb_frame, text="4MHz",  bg='#b0c4de', takefocus=0, variable=self.sel4, command=lambda: self.sel_4())
        self.cb_4.grid(row=1, column=3, sticky=E)
        
        self.sel6 = IntVar()
        self.cb_6 = Checkbutton(self.cb_frame, text="6MHz",  bg='#b0c4de', takefocus=0, variable=self.sel6, command=lambda: self.sel_6())
        self.cb_6.grid(row=1, column=4, sticky=E)
        
        self.sel8 = IntVar()
        self.cb_8 = Checkbutton(self.cb_frame, text="8MHz", bg='#b0c4de', takefocus=0,  variable=self.sel8, command=lambda: self.sel_8())
        self.cb_8.grid(row=1, column=5, sticky=E)
        
        self.sel12 = IntVar()
        self.cb_12 = Checkbutton(self.cb_frame, text="12MHz",  bg='#b0c4de', takefocus=0,  variable=self.sel12, command=lambda: self.sel_12())
        self.cb_12.grid(row=1, column=6, sticky=E)
        
        self.sel16 = IntVar()
        self.cb_16 = Checkbutton(self.cb_frame, text="16MHz",  bg='#b0c4de', takefocus=0,  variable=self.sel16, command=lambda: self.sel_16())
        self.cb_16.grid(row=1, column=7, sticky=E)
   
   
        ###################
        #   Called as a TopLevel window via the Menu
        #   widgets in button_3 frame
        #
        #self.dsc_l = Label(self.button_3_frame, text = "Send a DSC Test Call to Snargate" , bg='#b0c4de')
        #self.dsc_l.grid(row = 0, column = 0, columnspan=3)
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 16MHz
        self.call1_b = Button(self.button_3_frame, text = "16MHz Self Call", fg='white', bg='#6699cc', command = lambda: poll_cmd("CALL;002320204;16804.5"))
        self.call1_b.grid(row = 1, column = 0,  sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 12MHz
        self.call2_b = Button(self.button_3_frame, text = "12MHz Self Call", fg='white', bg='#6699cc', command = lambda: poll_cmd("CALL;002320204;12577.0"))
        self.call2_b.grid(row = 1, column = 1,  sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 8MHz
        self.call3_b = Button(self.button_3_frame, text = "8MHz Self Call", fg='white', bg='#6699cc', command = lambda: poll_cmd("CALL;002320204;8414.5"))
        self.call3_b.grid(row = 1, column = 2,  sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 6MHz
        self.call5_b = Button(self.button_3_frame, text = "6MHz Self Call", fg='white',  bg='#6699cc', command = lambda: poll_cmd("CALL;002320204;6312.0"))
        self.call5_b.grid(row = 2, column = 0,  sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 4MHz
        self.call4_b = Button(self.button_3_frame, text = "4MHz Self Call", fg='white', bg='#6699cc', command = lambda: poll_cmd("CALL;002320204;4207.5"))
        self.call4_b.grid(row = 2, column = 1, sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 2MHz
        self.call6_b = Button(self.button_3_frame, text = "2MHz Self Call", fg='white', bg='#6699cc', command = lambda: poll_cmd("CALL;002320204;2187.5"))
        self.call6_b.grid(row = 2, column = 2,  sticky = W+E)
        
        
        self.cb_tx_state = Checkbutton(self.button_3_frame, bg='#b0c4de', text="TX Enable", variable=self.tx_state, command=lambda: self.tx_on())
        self.cb_tx_state.grid(row=0, column=0, sticky=W)
        self.blank = Label(self.button_3_frame,  bg='#b0c4de')
        self.blank.grid(row = 4, column = 0, columnspan = 3, sticky=W+E)
        #self.dsc_l = Label(self.button_3_frame, text = "Send a DSC Test Call to another MMSI" , bg='#b0c4de')
        #self.dsc_l.grid(row = 4, column = 0, columnspan=3)
        
        self.dscto_l = Label(self.button_3_frame, text = "To MMSI" , bg='#b0c4de')
        self.dscto_l.grid(row = 5, column = 0, sticky = W+E)
        self.dscf_l = Label(self.button_3_frame, text = "Frequency" , bg='#b0c4de')
        self.dscf_l.grid(row = 5, column = 1, sticky = W+E)
        # A spinbox to select, or manually enter, target MMSIs for a DSC Test Call 
        # The list of pre-set MMSIs should be extended............ The values are read by get() called when pressing the button go_b below...
        self.to_mmsi_e = Spinbox(self.button_3_frame,width=8, wrap = True, values = ("002320001", "002320004", "002320024", "002191000", "002711000", "002241022", "003669991"), fg = 'red')
        self.to_mmsi_e.grid(row = 6, column = 0, sticky = W+E)
        
        # A spinbox to select, or manually enter, the desired frequency for a DSC Test Call
        # The value is read by get() when pressing the go_b button...
        self.freq_sp = Spinbox(self.button_3_frame,width=8, wrap = True, values = ("2187.5", "4207.5", "6312.0", "8414.5", "12577.0", "16804.5"))
        self.freq_sp.grid(row = 6, column = 1, sticky = W+E)
        
        # The button to send the command to generate a DSC Test call - to the MMSI and on the frequency set in the two adjacent spinboxes.
        self.go_b = Button(self.button_3_frame, text = "Send", fg='white',  bg='#6699cc',command = lambda: poll_cmd("CALL;"+self.to_mmsi_e.get()+";"+self.freq_sp.get()))
        self.go_b.grid(row = 6, column = 2, sticky = W+E)
        #
        self.blank = Label(self.button_3_frame,  bg='#b0c4de')
        self.blank.grid(row = 7, column = 0, columnspan = 3, sticky=W+E)
        #
        #######################
        self.reset_b = Button(self.button_3_frame, text = "Reset Message Count",fg='white', bg='#6699cc', command = lambda: poll_cmd("CLEAR"))
        self.reset_b.grid(row = 8, column = 0, columnspan=2,  sticky = W+E)
        
        
        # The EXCLUDE RX controls
        # Button to send the command that will exclude the RX ID entered in the exclude_e entry box - the command get()s the current text and
        # appends it to "ADD;" for passing via send_command(). 
        self.exclude_b = Button(self.button_3_frame, text = "RX Exclude>>", fg='white', bg='#6699cc', command = lambda: poll_cmd("ADD;"+self.exclude_e.get()))
        self.exclude_b.grid(row = 9, column = 0, sticky = W+E)
        
        #
        # the entry box, which is read by pressing either "exclude_b" or "include_b"
        self.exclude_e = Entry(self.button_3_frame,width=8)
        self.exclude_e.grid(row = 9, column = 1, sticky = W+E)
        
        # Button to send the command that will remove the RX ID from the exclude_list at the server. The command gets the current
        # text from the entry box and appends it to "DEL;" for passing via send_command()
        self.include_b = Button(self.button_3_frame, text = "<< RX Include", fg='white',bg='#6699cc', command = lambda: poll_cmd("DEL;"+self.exclude_e.get()))
        self.include_b.grid(row = 9, column = 2, sticky = W+E)
        
 
        
        
        
        
        
   
    def cleanup_on_exit(self):
        """Needed to shutdown the polling thread."""
        #print 'Window closed. Cleaning up and quitting'
        self.poll_thread_stop_event.set()
        self.log_thread_stop_event.set()
        root.quit() #Allow the rest of the quit process to continue
            
    # the connect function called by the connect button or the auto-reconnect functionality of the online() funtion.
    # two variables are set to indicate connection status for the email and re-connect processes.
    
    def make_con(self):
        
        self.con = n1.make_con()
        self.welcome = poll_cmd("hello")
        self.snargate_reply8.set(self.welcome)
        if re.search("Invalid", self.welcome):
            
            self.get_username()
        
        
    
    def close(self):
        
        poll_cmd("iwantotquit")
        
    def tx_on(self):
        self.tx_state.state = self.tx_state.get()
        if self.tx_state.state:
            poll_cmd("TXON")
        else:
            poll_cmd("TXOFF")

    
    
    def status_win(self):
        
        try:
            self.status_frame_exists = self.status_frame.winfo_exists()
        except:
            self.status_frame_exists = 0
            
        # a Toplevel frame - in its own window  - to hold the various "Status" indications (Labels)
        if self.status_frame_exists == 0:
            self.status_frame =  Toplevel(self, bg='#b0c4de')
            self.status_frame.title("Status")
        
            # we don't want to close this window, so we divert the WM close to a handler() function that simply
            # "passes"....
            self.status_frame.protocol("WM_DELETE_WINDOW", self.handler)
            self.status_frame.geometry("-30-40")
            # don't allow the frame to be resized
            self.status_frame.resizable(0, 0)
            self.status_frame.grid()
            self.status_frame.lift()
        else:
            self.status_frame.wm_state('normal')
            self.status_frame.lift()
            
    # functions to trigger commands to the server to add or remove frequencies from the 
    # frequency_allowed list - one per band.
    # clicking to turn a freq. checkbutton ON or OFF triggers the relevant
    # function below. 
    def sel_2(self):
        # we know the status has changed - we get the new status from the associated variable.
        self.sel2.state = self.sel2.get()
        if self.sel2.state: # cb is ON - we add the freq to the server's allowed list
            poll_cmd("ADDFREQ;2187.5")
        else: # otherwise cb is OFF - we delete the freq from the server's allowed list
            poll_cmd("DELFREQ;2187.5")
            
    def sel_4(self):
        self.sel4.state = self.sel4.get()
        if self.sel4.state:
            poll_cmd("ADDFREQ;4207.5")
        else:   
            poll_cmd("DELFREQ;4207.5")    
    def sel_6(self):
        self.sel6.state = self.sel6.get()
        if self.sel6.state:
            poll_cmd("ADDFREQ;6312.0")
        else:   
            poll_cmd("DELFREQ;6312.0")       
        
    def sel_8(self):
        self.sel8.state = self.sel8.get()
        if self.sel8.state:
            poll_cmd("ADDFREQ;8414.5")
        else:   
            poll_cmd("DELFREQ;8414.5")
            
    def sel_12(self):
        self.sel12.state = self.sel12.get()
        if self.sel12.state:
            poll_cmd("ADDFREQ;12577.0")
        else:   
            poll_cmd("DELFREQ;12577.0") 

            
    def sel_16(self):
        self.sel16.state = self.sel16.get()
        if self.sel16.state:
            poll_cmd("ADDFREQ;16804.5")
        else:   
            poll_cmd("DELFREQ;16804.5") 
            
    
    def show_rx(self):
        self.excluded_rx = poll_cmd("SHOW")
        self.snargate_reply9.set(self.excluded_rx)
    # Function to create the mmsi window and display the list retrieved from the server of known ship names.
    def mmsi_win(self):
        
        pass
        
    def sys_win(self):
    
        pass
        
    def allsys_win(self):
    
        pass
    
    # Same functionality as the sys window
    def rx_win(self):
    
        pass
    # Same functionality as the sys window
    def rxtx_win(self):
    
        pass
    # Same functionality as the sys window
    def tx_win(self):
    
        pass
    # set a variable to inhibit the email alert (we don't need to send an alert if we've disconnected on purpose)
    # and then send the server the necessary string to cause a remote disconnection
    def hide_dsc(self):
        self.button_3_frame.withdraw()
        
    def online(self):
    
        pass
        
    ###########
    # various functions called by poll() or poll_win()
    #
    # ptt status - is the TX transmitting?
    def get_ptt_state(self):
        
        pass
        
            
    # TX State = enabled or disabled - we need to update status label as well as the TX_STATE checkbutton
    def get_tx_state(self):
        
        pass
    
    def log_poll(self):
        if self.log_queue.qsize():
            
            self.log_reply = self.log_queue.get()
            self.log_list = self.log_reply.split("~")
            self.sys_log = self.log_list[0]
            #self.rx_log = self.log_list[1]
            #self.tx_log = self.log_list[2]
            self.rxtx_log = self.log_list[1]
            
            self.sys_term.tag_config("ADMIN", foreground="darkgreen")
            self.sys_term.tag_config("RX", foreground="blue")
            self.sys_term.tag_config("TX", foreground="red")
            self.sys_term.config(state='normal')
            self.sys_term.delete(0.0, END)
            for line in self.sys_log.split("\n"):
                if "Admin;" in line:
                    tags = ("ADMIN", )
                elif "Received" in line:
                
                    tags = ("RX", ) 
                elif "Transmit" in line: 
                    tags = ("TX", ) 
                else:
                    tags = None
                self.sys_term.insert(END, line+"\n", tags)
                
            self.sys_term.config(state='disabled')
            self.sys_term.yview(END)
            
            #self.rx_term.config(state='normal')
            #self.rx_term.delete(0.0, END)
            #self.rx_term.insert(END, self.rx_log+"\n")
            #self.rx_term.yview(END)
            #self.rx_term.config(state='disabled')
            
            #self.tx_term.config(state='normal')
            #self.tx_term.delete(0.0, END)
            #self.tx_term.insert(END, self.tx_log+"\n")
            #self.tx_term.yview(END)
            #self.tx_term.config(state='disabled')
            
            self.rxtx_term.tag_config("TX1", foreground="red")
            self.rxtx_term.config(state='normal')
            self.rxtx_term.delete(0.0, END)
            #self.rxtx_term.insert(END, rxtx_log+"\n")
            for line in self.rxtx_log.split('\n'):
                #print line
                
                tags = ("TX1", ) if "; TX1" in line else None
                #print tags
                #
                self.rxtx_term.insert(END, line+"\n", tags)
                
            self.rxtx_term.yview(END)
            self.rxtx_term.config(state='disabled')
            #self.rxtx_term.delete(0.0, END)
            #self.rxtx_term.insert(END, self.rxtx_log+"\n")
            #self.rxtx_term.yview(END)
            
            #print self.log_reply
            
        self._poll_job_id = self.master.after(self.poll_interval * 5, self.log_poll)    
    def status_poll(self):
        if self.status_queue.qsize():
            self.status_reply = self.status_queue.get()
            
           
            
            ############
            #
            self.status_list = self.status_reply.split("~")
           
            #print "################## ", self.status_list
            
            if len(self.status_list) != 9:
                self.status_list=["Not Connected", "Not Connected", "Not Connected","Not Connected","Not Connected","Not Connected","Not Connected","Not Connected","Not Connected"]
            self.online = self.status_list[0]
            #print self.online
                
            if re.search("online", self.online):     # check for the presence of "online" in the reply string
                #self.lost_comms = 0             # if the string is present we have comms, unset the lost_comms variable
                #self.count = str(self.con_count)
                self.l_reply1.configure(fg = 'darkgreen')   # set the status label text colour
            
            
                
            else:  # otherwise we can't reach the server.
                self.l_reply1.configure(fg = 'red')     # set the status label text colour
                try:
                    self.make_con()
                except:
                    self.status_list=["Not Connected", "Not Connected","Not Connected","Not Connected","Not Connected","Not Connected","Not Connected","Not Connected"]
                
            self.snargate_reply1.set(self.online)   
            ###########
            #
            self.txstate = self.status_list[1]
            if self.txstate == "TX Enabled":             # TX is allowed
                self.cb_tx_state.select()           # select (tick) the tx_state checkbutton
                self.l_reply2.configure(fg = 'darkgreen')   # set the status label colour
                
            else:                                   # TX is disabled
                self.cb_tx_state.deselect()         # deselect (untick) the tx_state checkbutton
                self.l_reply2.configure(fg = 'red') # set the status label colour
            
            self.snargate_reply2.set(self.txstate)
            
            ############
            #          
            self.ptt_state = self.status_list[2]
            
            if self.ptt_state == "PTT ON":
                self.l_reply3.configure(fg = 'red')
            else:
                self.l_reply3.configure(fg = 'darkgreen')
                
            self.snargate_reply3.set(self.ptt_state)
            
            #############
            #
            self.lastrx = self.status_list[3]
            self.l_reply4.configure(fg = 'blue')        
            self.snargate_reply4.set("Last RX: "+self.lastrx)
            
            
            
            self.lasttx = self.status_list[4]
            self.l_reply5.configure(fg = 'red')        
            self.snargate_reply5.set("Last TX: "+self.lasttx)
            
            
            
            self.message_count = self.status_list[5]
            self.snargate_reply6.set(self.message_count)
            
            
            self.perband = self.status_list[6]
            self.snargate_reply7.set(self.perband)
            
            self.freq_list = self.status_list[7]#.split(";")
            
            
            # test for the presence of each frequency in the list and select/deselect each checkbutton as necessary
            if "2187.5" in self.freq_list:
                self.cb_2.select()
            else:
                self.cb_2.deselect()
            
            if "4207.5" in self.freq_list:
                self.cb_4.select()
            else:
                self.cb_4.deselect()
           
            if "6312.0" in self.freq_list:
                self.cb_6.select()
            else:
                self.cb_6.deselect()
            
        
            if "8414.5" in self.freq_list:
                self.cb_8.select()
            else:
                self.cb_8.deselect()
            
            if "12577.0" in self.freq_list:
                self.cb_12.select()
            else:
                self.cb_12.deselect()
            
            if "16804.5" in self.freq_list:
                self.cb_16.select()
            else:
                self.cb_16.deselect()
            
            
            self.excluded_rx = self.status_list[8]
            self.snargate_reply9.set(self.excluded_rx)
            
        self._poll_job_id = self.master.after(self.poll_interval, self.status_poll)
    
            
       
        
        

def poll_cmd(cmd):
    
    if cmd.split(";")[0] == "ADD" or cmd.split(";")[0] == "DEL": 
        app.exclude_e.delete(0, 'end')
        
        
         
    header = "ADMIN"            # All commands are prefixed with "ADMIN"
    sendcommand = header+";"+cmd+";"+id     # build the command string - a ";" delimited string with ID as the last element
    
        
    try:
        #print "sending... ", sendcommand
        received = n1.connect(sendcommand)      # send the command and read the returned data
        
        return received
            
    except:
        
        return "Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected"
 
def log_thread(q, stop_event):
    
    while(not stop_event.is_set()):
        time.sleep(0.2)
        if q.empty():
            #print "In log_thread...."
            #q_text=poll_cmd("GETADMINSQL")+"~"+poll_cmd("GETRXSQL")+"~"+poll_cmd("GETTXSQL")+"~"+poll_cmd("GETRXTXSQL")
            q_text=poll_cmd("GETADMINSQL")+"~"+poll_cmd("GETRXTXSQL")
            #q_text = poll_cmd("TESTING") + "~" + poll_cmd("TXSTATE") + "~" + poll_cmd("GETPTT")+"~"+poll_cmd("LAST1")+"~"+poll_cmd("TX1")+"~"+poll_cmd("COUNT")+"~"+poll_cmd("PERBAND")+"~"+poll_cmd("POLLFREQ")
            
        
            q.put(q_text)

            
def status_thread(q, stop_event):

    while(not stop_event.is_set()):
        time.sleep(0.2)
        if q.empty():
        
            q_text=poll_cmd("POLLSTATUS")
           
            #q_text = poll_cmd("TESTING") + "~" + poll_cmd("TXSTATE") + "~" + poll_cmd("GETPTT")+"~"+poll_cmd("LAST1")+"~"+poll_cmd("TX1")+"~"+poll_cmd("COUNT")+"~"+poll_cmd("PERBAND")+"~"+poll_cmd("POLLFREQ")
            
        
            q.put(q_text)


        
if __name__ == '__main__':
    root = Tk()
    
    lock = threading.Lock()
    root.geometry("+10+10")
    root.resizable(0, 0)
   
    root.title("Wire2waves DSC Coast Station Client " + version)
    n1 = Network()
    app = Application(root)
 
    # instance of the network class - our connection to the server
    
    
    # start the GUI
    root.mainloop()
