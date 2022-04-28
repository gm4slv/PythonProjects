'''
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
'''
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



version = "v0.9 pre 1"


from Tkinter import *
from tkMessageBox import *
from ScrolledText import *
import time
import re
import socket

import threading

import alert

ABOUT_TEXT = "Wire2waves DSC Coast Station : GMDSS DSC Coast Station client \n\n version "+ version + '''\n\n
    Copyright (C) 2015  John Pumford-Green
    Wire2Waves Ltd
    Shetland
    john@wire2waves.co.uk
    

'''
# Coast Station Server host / port
HOST, PORT = "gm4slv.plus.com", 50669

# Global Variables for the Email Alert trigger
email_flag = 0
lost_contact = 0

# The class for a TCP/IP connection to the Server
# Instantiated at program startup 
class Network(object):
    def __init__(self):
        # when the n1 instance is created, do nothing - we'll connect later under
        # user control
        pass
    
    # connect to the Coast Station server at the HOST, PORT
    # make_con() is called 
    # 1) by the user pressing the "CONNECT" button
    # 2) by an auto-reconnect mechanism driven by the regular polling of server information
    def make_con(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        
        return self.sock
    
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
       
        
        # our result is a join of the two elements of the total_data list
        return ''.join(total_data)
              
   
# The GUI class... 
class Application(Frame):
    def __init__(self, master):
        # The frame for the main controls and a terminal window
        Frame.__init__(self, master)
        self.grid()
        
        # a variable to track if we've been connected to the server - used to
        # manage the Alert email - we don't want to send an email due to "loss contact"
        # if we haven't even connected yet. More below....
        self.connected = 0
        
        # a frame for check_buttons etc. this is a frame within the main application window.
        self.cb_frame = Frame(self)      
        self.cb_frame.grid(row=0, column=0, sticky=NSEW)
        
        
        
        # another frame for more buttons, again held in the main application window
        self.button_1_frame = Frame(self)
        self.button_1_frame.grid(row = 1, column = 0, sticky=NSEW)
        
        # a frame to hold the terminal screen, held in the main appliction window
        self.term_frame = Frame(self)
        self.term_frame.grid(row=10, column=0, columnspan=2)
        
        self.status_win()
        
        self.dsc_buttons()
        self.button_3_frame.withdraw()
        
        self.rx_buttons()
        self.button_1_frame.withdraw()
        
        # run the widget creation function
        self.create_widgets()
        
        # deselct the SHUTDOWN ALLOW checkbutton
        self.cb_en_sd.deselect()
        
        # deselct the "Send Email" checkbutton
        self.cb_email.deselect()
        
       
        
        
        # start polling - this calls poll() once, and then poll is re-triggered, after a delay, from the command
        # in the last line of poll()
        self.poll() 
    
    # the handler to ignore Status Window closure attempts
    def handler(self):
        #print "ABOUT W2W"
        pass
    
    def delete_window(self, w):
        w.destroy()
    
    def about(self):
        self.about_frame = Toplevel(self, borderwidth = 2)
        self.about_frame.title("About W2W Coast Station")
        #admin_frame.protocol("WM_DELETE_WINDOW", self.handler)
        self.about_frame.resizable(0, 0)
        #self.mmsi_frame.geometry("900x500-10+10")
        self.about_frame.grid()
        
        self.about_l = Label(self.about_frame, text = ABOUT_TEXT)
        self.about_l.grid(row = 0, column = 0, columnspan = 5)
        
        self.close_b = Button(self.about_frame, text="OK", command = lambda: self.delete_window(self.about_frame))
        self.close_b.grid(row = 1, column = 2, sticky=W+E)
    
    def rx_buttons(self):
    # a frame for more buttons, again held in the main application window
        self.button_1_frame = Toplevel(self)
        self.button_1_frame.resizable(0, 0)
        self.button_1_frame.title("RX Exclude")
        self.button_1_frame.protocol("WM_DELETE_WINDOW", self.handler)
        self.button_1_frame.grid()
    
    def dsc_buttons(self):
    # a frame for more buttons, again held in the main application window
        self.button_3_frame = Toplevel(self)
        self.button_3_frame.resizable(0, 0)
        self.button_3_frame.title("Send DSC")
        self.button_3_frame.protocol("WM_DELETE_WINDOW", self.handler)
        self.button_3_frame.grid()
        
        
    # create all the buttons, checkboxes, labels etc....
    def create_widgets(self):
    
        menubar = Menu(root)
        
        logmenu = Menu(menubar, tearoff=0)
        logmenu.add_command(label="Status", command=self.status_win)
        logmenu.add_command(label="RX/TX", command=self.rxtx_win)
        logmenu.add_command(label="Syslog", command=self.sys_win)
        logmenu.add_separator()
        logmenu.add_command(label="RX", command=self.rx_win)
        logmenu.add_command(label="TX", command=self.tx_win)
        logmenu.add_command(label="MMSI", command=self.mmsi_win)
        
        
        menubar.add_cascade(label="Logs", menu=logmenu)
        
        menubar.add_command(label="Send DSC", command= lambda: self.button_3_frame.deiconify())
        menubar.add_command(label="RX Exclude", command= lambda: self.button_1_frame.deiconify())
        menubar.add_command(label="About", command=self.about)
        menubar.add_command(label="Quit", command= lambda: self.callback())
        #menubar.add_command(label="About", command=self.about)
        
        #menubar.add_command(label="About", command=self.about)
        root.config(menu=menubar)
        
        ###################################
        ###############################
    
        
        
        #######################
        #
        #   Widgets in the cb_frame
        #
        # TX State : to display and control the Server TX Inhibit function
        self.tx_state = IntVar() 
        # the variable is read by the polling of get_tx_state() and indicates whether TX is Enabled/Disable. The state
        # of the CB mirrors the state of the TX Inhibit reported by the server.
        # ticking the CB will run "tx_on()" and send the istruction to the server to enable TX
        self.cb_tx_state = Checkbutton(self.cb_frame, text="TX Enable", variable=self.tx_state, command=lambda: self.tx_on())
        self.cb_tx_state.grid(row=0, column=0, columnspan=2, sticky=E)
        
        
        # Enable Shutdown Command : to activate the adjacent button, allowing a "SHUTDOWN" command to be sent to the server
        self.en_sd = IntVar()
        # The variable is used to fire off "sd_but()" which will activate the SHUTDOWN button when this CB is ticked.
        # This is just a safety feature to enforce a two-step process to send a Server Shutdown request.
        self.cb_en_sd = Checkbutton(self.cb_frame, text="Allow Shutdown", variable=self.en_sd, command= lambda: self.sd_but())
        self.cb_en_sd.grid(row=0, column = 2, columnspan=2)
        
        # The button that fires off shutdown() which sends the command to the Coast Station server to initiate a shutdown.
        # The button is initially "DISABLED" and only becomes "ACTIVE" after running "sd_but()" - by ticking the "cb_en_sd" 
        self.shutdown_b = Button(self.cb_frame, state=DISABLED, fg='grey', text = "Shutdown", command = lambda: self.shutdown())
        self.shutdown_b.grid(row = 0, column = 4, sticky = W+E)
        
        # Enable email alerts to be sent to System Administrator
        self.email_enable = IntVar()
        # When this variable is set an alert email will be sent if contact is lost with the remote
        # Coast Station server, and another is sent when contact is restored.
        self.cb_email = Checkbutton(self.cb_frame, text = "Enable Email Alert", variable = self.email_enable)
        self.cb_email.grid(row=0, column = 5, columnspan = 2, sticky=W)
        
        # User Name entry box : id_e.get() is used to send the contents with each message to the server
        # an incorrect Username will lead to disconnection.
        self.id_e = Entry(self.cb_frame, width = 10)
        self.id_e.grid(row=0, column = 8, sticky=E)
        
        # bind the <Return> key, when pressed with the cursor in the User Name entry box, to the make_con()
        # function - so that a simple keypress after typing User Name will initiate connection - alternatively
        # the adjacent "CONNECT" button can be pressed with the mouse.
        #self.id_e.bind( '<Return>', (lambda event: self.connect()))
        
        # Label
        self.id_l = Label(self.cb_frame, text="User ID >")
        self.id_l.grid(row=0, column=7, sticky=W, ipadx=5)
        
        self.con=IntVar()
        self.con_cb = Checkbutton(self.cb_frame, text="Connect", variable=self.con, command = lambda: self.make_con())
        self.con_cb.grid(row=0, column = 9)
        
        # Connect button - fires off "make_con()" when pressed.
        #self.recon_b = Button(self.cb_frame, text = "Connect", command = lambda: self.make_con())
        #self.recon_b.grid(row=0, column = 9, sticky=W+E)
        
        # Disconnect button - fires off close() when pressed - close() sends a specific 
        # string to the server to initiate a server-side disconnection.
        #self.dis_b = Button(self.cb_frame, text = "Disconnect", command = lambda: self.close())
        #self.dis_b.grid(row=1, column = 9, sticky=W+E)
        
        # A label...  
        self.cbf_l = Label(self.cb_frame, text="Channels allowed")
        self.cbf_l.grid(row=1, column=0, columnspan=2)
        
        # Checkbuttons to select/deselect individual channels. The boxes indicate the current state retreived from the server
        # Each button calls a function to send the necessary command depending on whether the box is selected or de-selected.
        # If another user changes the state of a band, this will be echoed on the selections of the boxes on all other connected
        # clients.
        
        self.sel2 = IntVar()
        self.cb_2 = Checkbutton(self.cb_frame, text="2MHz", variable=self.sel2, command=lambda: self.sel_2())
        self.cb_2.grid(row=1, column=2, sticky=E)
        
        self.sel4 = IntVar()
        self.cb_4 = Checkbutton(self.cb_frame, text="4MHz", variable=self.sel4, command=lambda: self.sel_4())
        self.cb_4.grid(row=1, column=3, sticky=E)
        
        self.sel6 = IntVar()
        self.cb_6 = Checkbutton(self.cb_frame, text="6MHz", variable=self.sel6, command=lambda: self.sel_6())
        self.cb_6.grid(row=1, column=4, sticky=E)
        
        self.sel8 = IntVar()
        self.cb_8 = Checkbutton(self.cb_frame, text="8MHz", variable=self.sel8, command=lambda: self.sel_8())
        self.cb_8.grid(row=1, column=5, sticky=E)
        
        self.sel12 = IntVar()
        self.cb_12 = Checkbutton(self.cb_frame, text="12MHz", variable=self.sel12, command=lambda: self.sel_12())
        self.cb_12.grid(row=1, column=6, sticky=E)
        
        self.sel16 = IntVar()
        self.cb_16 = Checkbutton(self.cb_frame, text="16MHz", variable=self.sel16, command=lambda: self.sel_16())
        self.cb_16.grid(row=1, column=7, sticky=E)
        
        #
        #
        #####################
        
        '''
        #############
        #
        #   widgets in button_1 frame
        #
        # opens the Syslog window - via sys_win() creates a Toplevel frame with a ScrolledText widget to display 
        # the Server "syslog". The syslog data is continually retrieved by the poll() function, whether or
        # not a Syslog window is open.
        self.syssql_b = Button(self.button_1_frame, text = "System Log", command = lambda:self.sys_win() )
        self.syssql_b.grid(row = 1, column = 0, sticky = W+E)
        
        # opens the RX Log window - via rx_win() creates a Toplevel frame with a ScrolledText widget to display 
        # the Server "rxlog". The "rxlog" data is continually retrieved by the poll() function, whether or
        # not a RX Log window is open.
        self.rxsql_b = Button(self.button_1_frame, text = "RX Log", command = lambda:self.rx_win()) 
        self.rxsql_b.grid(row = 1, column = 1, sticky = W+E)
        
        # opens the RX Log window - via tx_win() creates a Toplevel frame with a ScrolledText widget to display 
        # the Server "txlog". The "txlog" data is continually retrieved by the poll() function, whether or
        # not a TX Log window is open.
        self.txsql_b = Button(self.button_1_frame, text = "TX Log", command = lambda:self.tx_win())
        self.txsql_b.grid(row = 1, column = 2, sticky = W+E)
        
        # opens the RX/TX Log window - via rxtx_win() creates a Toplevel frame with a ScrolledText widget to display 
        # the Server "rxtxlog". The "rxtxlog" data is continually retrieved by the poll() function, whether or
        # not a RXTX Log window is open.
        self.rxtxsql_b = Button(self.button_1_frame, text = "RX/TX Log", command = lambda:self.rxtx_win())
        self.rxtxsql_b.grid(row = 1, column = 3, sticky = W+E)
        
        # opens the MMSI Log window - via mmsi_win() creates a Toplevel frame with a ScrolledText widget to display 
        # the Server "mmsi log". The MMSI log data is requested once, when the window is created
        self.ressql_b = Button(self.button_1_frame, text = "MMSI Log", command = lambda: self.mmsi_win())
        self.ressql_b.grid(row = 1, column = 4, sticky = W+E)
        
        '''
        # The EXCLUDE RX controls
        # Button to send the command that will exclude the RX ID entered in the exclude_e entry box - the command get()s the current text and
        # appends it to "ADD;" for passing via send_command(). 
        self.exclude_b = Button(self.button_1_frame, text = "RX Exclude>>", command = lambda: self.send_command("ADD;"+self.exclude_e.get()))
        self.exclude_b.grid(row = 0, column = 0, sticky = W+E)
        #
        # the entry box, which is read by pressing either "exclude_b" or "include_b"
        self.exclude_e = Entry(self.button_1_frame, width = 20)
        self.exclude_e.grid(row = 0, column = 1, columnspan = 2,  sticky = W+E)
        
        # Button to send the command that will remove the RX ID from the exclude_list at the server. The command gets the current
        # text from the entry box and appends it to "DEL;" for passing via send_command()
        self.include_b = Button(self.button_1_frame, text = "<< RX Include", command = lambda: self.send_command("DEL;"+self.exclude_e.get()))
        self.include_b.grid(row = 0, column = 3, sticky = W+E)
        
        # Button to send the command that will return the currently excluded RX IDs from the server. The returns from the commands sent are
        # shown in a ScrolledText widget "terminal".... below (somewhere)
        self.show_b = Button(self.button_1_frame, text = "Show Excluded RX", command = lambda: self.send_command("SHOW"))
        self.show_b.grid(row = 1, column = 0, sticky = W+E)
        
        self.hide_rx_b = Button(self.button_1_frame, text="Hide", command = lambda:self.button_1_frame.withdraw())
        self.hide_rx_b.grid(row = 1, column = 2)
        ###################
        #
        #   widgets in button_3 frame
        #
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 16MHz
        self.call1_b = Button(self.button_3_frame, text = "16MHz Self Call", command = lambda: self.send_command("CALL;002320204;16804.5"))
        self.call1_b.grid(row = 0, column = 0, sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 12MHz
        self.call2_b = Button(self.button_3_frame, text = "12MHz Self Call", command = lambda: self.send_command("CALL;002320204;12577.0"))
        self.call2_b.grid(row = 0, column = 1, sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 8MHz
        self.call3_b = Button(self.button_3_frame, text = "8MHz Self Call", command = lambda: self.send_command("CALL;002320204;8414.5"))
        self.call3_b.grid(row = 0, column = 2, sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 6MHz
        self.call5_b = Button(self.button_3_frame, text = "6MHz Self Call", command = lambda: self.send_command("CALL;002320204;6312.0"))
        self.call5_b.grid(row = 2, column = 0, sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 4MHz
        self.call4_b = Button(self.button_3_frame, text = "4MHz Self Call", command = lambda: self.send_command("CALL;002320204;4207.5"))
        self.call4_b.grid(row = 2, column = 1, sticky = W+E)
        
        # Button to send the command to generate a DSC Test Call addressed to ourselves, on 2MHz
        self.call6_b = Button(self.button_3_frame, text = "2MHz Self Call", command = lambda: self.send_command("CALL;002320204;2187.5"))
        self.call6_b.grid(row = 2, column = 2, sticky = W+E)
       
        # A spinbox to select, or manually enter, target MMSIs for a DSC Test Call 
        # The list of pre-set MMSIs should be extended............ The values are read by get() called when pressing the button go_b below...
        self.to_mmsi_e = Spinbox(self.button_3_frame, width = 10, wrap = True, values = ("002320001", "002320004", "002320024", "002191000", "002711000", "002241022", "003669991"), fg = 'red')
        self.to_mmsi_e.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = W+E)
        
        # A spinbox to select, or manually enter, the desired frequency for a DSC Test Call
        # The value is read by get() when pressing the go_b button...
        self.freq_sp = Spinbox(self.button_3_frame, width = 10, wrap = True, values = ("2187.5", "4207.5", "6312.0", "8414.5", "12577.0", "16804.5"))
        self.freq_sp.grid(row = 3, column = 1, sticky = W+E)
        
        # The button to send the command to generate a DSC Test call - to the MMSI and on the frequency set in the two adjacent spinboxes.
        self.go_b = Button(self.button_3_frame, text = "<< Send DSC", command = lambda: self.send_command("CALL;"+self.to_mmsi_e.get()+";"+self.freq_sp.get()))
        self.go_b.grid(row = 3, column = 2, sticky = W+E)
        #
        self.d_hide_b = Button(self.button_3_frame, text="Hide", command = lambda:self.button_3_frame.withdraw())
        self.d_hide_b.grid(row = 7, column = 2)
        #
        #
        #######################
        
        #######################
        #
        # widget in the term_frame
        #
        # A ScrolledText widget to mimic a greenscreen Terminal - displays commands and replies to/from the Coast Station server
        self.command_reply = StringVar()
        self.reply = Label(master=self.term_frame, fg='blue', textvariable=self.command_reply, width = 70, height = 2, anchor=W)
        self.reply.grid(row = 0, column = 0, sticky=W+E)
       
        
       
        ######################
        #
        #   widgets (labels) in the Status Frame
        # Each label text is set via a textvariable which is set in the relevant function called by the repeating poll() function
        # See the individual functions for details of the text and colour changes. The labels are simply numbered 1 - 7, the meaning
        # of each is determined by the function that sets the textvariable.
        self.snargate_reply1 = StringVar()
        self.l_reply1 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='azure2', height=1, textvariable=self.snargate_reply1, width=80, font=('',9,'bold'))
        self.l_reply1.grid(row=0, column=0,  sticky=E+W)
        
        self.snargate_reply3 = StringVar()
        self.l_reply3 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='azure2', height=1, textvariable=self.snargate_reply3, width=80, font=('',9,'bold'))
        self.l_reply3.grid(row=1, column=0,   sticky=E+W)
        
        self.snargate_reply2 = StringVar()
        self.l_reply2 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='azure2', height=1, textvariable=self.snargate_reply2, width=80, font=('',9,'bold'))
        self.l_reply2.grid(row=2, column=0,   sticky=E+W)
 
        
        self.snargate_reply4 = StringVar()
        self.l_reply4 = Label(self.status_frame, anchor=SW, justify=LEFT,bg='azure2',  fg='blue', height=1, textvariable=self.snargate_reply4, width=80, font=('',9,'bold'))
        self.l_reply4.grid(row=3, column=0,   sticky=E+W)
        
        self.snargate_reply5 = StringVar()
        self.l_reply5 = Label(self.status_frame, anchor=SW, justify=LEFT,bg='azure2', fg='red', height=1, textvariable=self.snargate_reply5, width=80, font=('',9,'bold'))
        self.l_reply5.grid(row=4, column=0,  sticky=E+W)
        
        self.snargate_reply6 = StringVar()
        self.l_reply6 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='azure2', height=1, textvariable=self.snargate_reply6, width=80, font=('',9,'bold'))
        self.l_reply6.grid(row=5, column=0,   sticky=E+W)
        
        self.snargate_reply7 = StringVar()
        self.l_reply7 = Label(self.status_frame, anchor=SW, justify=LEFT,bg='azure2', height=1, textvariable=self.snargate_reply7, width=80)
        self.l_reply7.grid(row=6, column=0,   sticky=E+W)
        
        # button to reset the message count, by sending a command to the server.
        self.reset_b = Button(self.status_frame, text = "Reset Message Count", command = lambda: self.send_command("CLEAR"))
        self.reset_b.grid(row = 7, column = 0, sticky = W)
        
        self.hide_b = Button(self.status_frame, text="Hide", command = lambda:self.status_frame.withdraw())
        self.hide_b.grid(row = 7, column = 2, sticky=W+E)
    

    def callback(self):
        if askyesno('Verify', 'Really quit?', default=NO):
            root.destroy()
        else:
            showinfo('No', 'Quit has been cancelled')
    # the connect function called by the connect button or the auto-reconnect functionality of the online() funtion.
    # two variables are set to indicate connection status for the email and re-connect processes.
    def make_con(self):
        self.con_ok = self.con.get()
        if self.con_ok:
        
            n1.make_con()
            self.connected=1
            self.lost_comms=0
            self.send_command("hello")
            
        else:
            self.close()
    
    def status_win(self):
        
        try:
            self.status_frame_exists = self.status_frame.winfo_exists()
        except:
            self.status_frame_exists = 0
            
        # a Toplevel frame - in its own window  - to hold the various "Status" indications (Labels)
        if self.status_frame_exists == 0:
            self.status_frame =  Toplevel(self, borderwidth = 3, relief = GROOVE, bg='azure2')
            self.status_frame.title("Status")
        
            # we don't want to close this window, so we divert the WM close to a handler() function that simply
            # "passes"....
            self.status_frame.protocol("WM_DELETE_WINDOW", self.handler)
            self.status_frame.geometry("-30-40")
            # don't allow the frame to be resized
            self.status_frame.resizable(0, 0)
            self.status_frame.grid()
        else:
            self.status_frame.wm_state('normal')
            self.status_frame.lift()
            
    
    # Function to create the mmis window and display the list retrieved from the server of known ship names.
    def mmsi_win(self):
        
        # test to see if the frame already exists. 
        try:
            self.mmsi_frame_exists = self.mmsi_frame.winfo_exists()
        except:
            self.mmsi_frame_exists = 0
        
        # If not we can create it and a ScrolledText widget and then call get_mmsi_log() to display
        # the mmsi data
        if self.mmsi_frame_exists == 0:
            self.mmsi_frame = Toplevel(self, borderwidth = 2, relief = GROOVE)
            self.mmsi_frame.title("MMSI List")
            #admin_frame.protocol("WM_DELETE_WINDOW", self.handler)
            self.mmsi_frame.resizable(0, 0)
            #self.mmsi_frame.geometry("900x500-10+10")
            self.mmsi_frame.grid() 
        
            self.mmsi_term = ScrolledText(self.mmsi_frame, fg='blue',bg='azure2', width = 50, height = 31, wrap = WORD)
            self.mmsi_term.grid(row = 0, column = 0, sticky=W+E)
            self.get_mmsi_log()
            
        # Otherwise we can just get_mmsi_log(),  restore it from minimzation, and lift it to the top of the windows
        else:
            self.get_mmsi_log()
            # get_mmsi_log() will retrieve the data and controls writing it to the ScrolledText widget.
            self.mmsi_frame.wm_state('normal')
            self.mmsi_frame.lift()
        
    def sys_win(self):
    
        # test to see if the frame already exists.
        try:
            self.sys_frame_exists = self.sys_frame.winfo_exists()
        except:
            self.sys_frame_exists = 0
        
        # If not we can create it and a ScrolledText widget. The text is updated automatically 
        if self.sys_frame_exists == 0:
            self.sys_frame = Toplevel(self, borderwidth = 2, relief = GROOVE, bg = 'black')
            self.sys_frame.title("System Log")
            
            self.sys_frame.resizable(0, 0)
            
            self.sys_frame.grid() 
        
            self.sys_term = Text(self.sys_frame, fg='blue', bg='azure2', width = 120, height = 31, wrap = WORD)
            self.sys_term.grid(row = 0, column = 0, sticky=W+E+N+S)
        
        # Otherwise restore it from minimzation, and lift it to the top of the windows
        else:
            self.sys_frame.wm_state('normal')
            self.sys_frame.lift()
    
    # Same functionality as the sys window
    def rx_win(self):
    
        try:
            self.rx_frame_exists = self.rx_frame.winfo_exists()
        except:
            self.rx_frame_exists = 0
        
        if self.rx_frame_exists == 0:
        
            self.rx_frame = Toplevel(self, bg='azure2')
            self.rx_frame.title("RX Log")
            
            self.rx_frame.resizable(0, 0)
            
            self.rx_frame.grid() 
        
            self.rx_term = ScrolledText(self.rx_frame, fg='blue',bg='azure2', width = 100, height = 31, wrap = WORD, font=('courier new',10,''))
            self.rx_term.grid(row = 0, column = 0, sticky=W+E)
            self.get_rx_log()
            
            
        else:
            self.rx_frame.wm_state('normal')
            self.rx_frame.lift()
            self.get_rx_log()
            
    # Same functionality as the sys window
    def rxtx_win(self):
    
        try:
            self.rxtx_frame_exists = self.rxtx_frame.winfo_exists()
        except:
            self.rxtx_frame_exists = 0
        
        if self.rxtx_frame_exists == 0:
        
            self.rxtx_frame = Toplevel(self, borderwidth = 2, relief = GROOVE, bg = 'black')
            self.rxtx_frame.title("RX/TX Log")
            
            self.rxtx_frame.resizable(0, 0)
            
            self.rxtx_frame.grid() 
        
            self.rxtx_term = Text(self.rxtx_frame, fg='blue', bg='azure2', width = 120, height = 31, wrap = WORD, font=('courier new',10,''))
            self.rxtx_term.grid(row = 0, column = 0, sticky=W+E)
        
        else:
            self.rxtx_frame.wm_state('normal')
            self.rxtx_frame.lift()
    
    
    # Same functionality as the sys window
    def tx_win(self):
    
        try:
            self.tx_frame_exists = self.tx_frame.winfo_exists()
        except:
            self.tx_frame_exists = 0
        
        if self.tx_frame_exists == 0:
        
            self.tx_frame = Toplevel(self, borderwidth = 2, relief = GROOVE, bg = 'black')
            self.tx_frame.title("TX Log")
            
            self.tx_frame.resizable(0, 0)
            
            self.tx_frame.grid() 
        
            self.tx_term = ScrolledText(self.tx_frame, fg='red', bg='azure2', width = 100, height = 31, wrap = WORD, font=('courier new',10,''))
            self.tx_term.grid(row = 0, column = 0, sticky=W+E)
            self.get_tx_log()
        else:
            self.tx_frame.wm_state('normal')
            self.tx_frame.lift()
            self.get_tx_log()
    
    # set a variable to inhibit the email alert (we don't need to send an alert if we've disconnected on purpose)
    # and then send the server the necessary string to cause a remote disconnection
    def close(self):
        self.connected = 0
        self.send_command("iwantotquit")
        
        
    # Function to control the activation of the SHUTDOWN button and change the text colour
    # based on the state of the en_sd variable, which is set via the Enable Shutdown checkbutton. This function sd_but() 
    # is called when the checkbutton is changed by the user.
    def sd_but(self):
        # get the current value of the variable attached to the checkbutton - is it "ON" of "OFF"
        self.sd_ok = self.en_sd.get()
        
        if self.sd_ok: # cb is ON - we want to enable the Shutdown button
            self.shutdown_b.configure(fg='red')
            self.shutdown_b.configure(state=NORMAL)
        else: # otherwise cb is OFF - we want to disable the Shutdown button
            self.shutdown_b.configure(fg='grey')
            self.shutdown_b.configure(state=DISABLED)
    
    # functions to trigger commands to the server to add or remove frequencies from the 
    # frequency_allowed list - one per band.
    # clicking to turn a freq. checkbutton ON or OFF triggers the relevant
    # function below. 
    def sel_2(self):
        # we know the status has changed - we get the new status from the associated variable.
        self.sel2.state = self.sel2.get()
        if self.sel2.state: # cb is ON - we add the freq to the server's allowed list
            self.send_command("ADDFREQ;2187.5")
        else: # otherwise cb is OFF - we delete the freq from the server's allowed list
            self.send_command("DELFREQ;2187.5")
            
    def sel_4(self):
        self.sel4.state = self.sel4.get()
        if self.sel4.state:
            self.send_command("ADDFREQ;4207.5")
        else:   
            self.send_command("DELFREQ;4207.5")    
    def sel_6(self):
        self.sel6.state = self.sel6.get()
        if self.sel6.state:
            self.send_command("ADDFREQ;6312.0")
        else:   
            self.send_command("DELFREQ;6312.0")       
        
    def sel_8(self):
        self.sel8.state = self.sel8.get()
        if self.sel8.state:
            self.send_command("ADDFREQ;8414.5")
        else:   
            self.send_command("DELFREQ;8414.5")
            
    def sel_12(self):
        self.sel12.state = self.sel12.get()
        if self.sel12.state:
            self.send_command("ADDFREQ;12577.0")
        else:   
            self.send_command("DELFREQ;12577.0") 

            
    def sel_16(self):
        self.sel16.state = self.sel16.get()
        if self.sel16.state:
            self.send_command("ADDFREQ;16804.5")
        else:   
            self.send_command("DELFREQ;16804.5")       

    def tx_on(self):
        self.tx_state.state = self.tx_state.get()
        if self.tx_state.state:
            self.send_command("TXON")
        else:
            self.send_command("TXOFF")

    # function to remotely shutdown the Coast Station server. Called by the shutdown button - we check if the enable_shutdown checkbutton
    # is enabled (although it must be, if the Shutdown button was active.... belt and braces....)
    def shutdown(self):
    
        
        self.shutdown_allowed = self.en_sd.get()
        if self.shutdown_allowed:
            if askyesno('Verify', 'Really Shutdown Server?', default=NO):
                self.send_command("SHUTDOWN")
            else:
                showinfo('No', 'Server Shutdown has been cancelled')
                self.cb_en_sd.deselect()
                self.shutdown_b.configure(fg='grey')
                self.shutdown_b.configure(state=DISABLED)
            
      
    
    # the "ping" function to confirm communication with the Coast Station Server.
    # Called as part of the regular poll() sequence. This function controls the display of 
    # status text, controls the email alert, controls the auto-reconnect functionality. Various
    # variables are used to determine the neccesary actions.
    ################# it might be worth checking for exraneous tests..... ################
    def online(self):
    
        global lost_contact # a counter of how many polls have failed in sequence ....
        global email_flag # we have sent an email already - don't send another one....
        
        # "TESTING" sent to the server will return a string "User xxx: Coast Station Online"
        online = self.poll_cmd("TESTING")
        
        if re.search("online", online):     # check for the presence of "online" in the reply string
            self.lost_comms = 0             # if the string is present we have comms, unset the lost_comms variable
            
            self.l_reply1.configure(fg = 'darkgreen')   # set the status label text colour
            self.snargate_reply1.set(online)            # set the status label text to the returned text string from the server 
            
        else:  # otherwise we can't reach the server.
            self.l_reply1.configure(fg = 'red')     # set the status label text colour
            self.snargate_reply1.set(online)        # set the status label text (?)
            self.lost_comms = 1                     # set the lost_comms variable.
            
            if self.lost_comms == 1 and self.connected == 1:    # we've lost comms, but we were connected (i.e. we haven't disconnected on purpose)
                self.l_reply1.configure(fg = 'red')             # set the status label text colour     
                self.snargate_reply1.set("Lost Comms")          # set the status label text to "Lost Comms" - overwriting anything that may be there already
            elif self.connected == 0:                           # we have "lost comms" BUT we weren't connected (eg we've disconnected)
                self.snargate_reply1.set("")                    # set the status label text to blank "" and don't bother with the rest of the function
                
            
            # decide to send email and to reconnect..... 
            if self.connected == 1:                 # we WERE connected before comms was lost
                
                if self.lost_comms == 1:            # we lost comms
                    self.snargate_reply1.set("Lost Comms")  # set the status text to "Lost Comms"
                    
                    
                    if lost_contact > 30:           # after 30 sucessive lost_contacts we check the email_enable checkbutton variable
                        self.email_allow = self.email_enable.get()
                        
                        
                        if self.email_allow:        # if emails are allowed....
                            
                            if email_flag == 0:     # check to see if we've already sent one  0 = not sent
                                
                                alert.send_email("No Contact from Snargate") # call alert.send_email() with the text to be sent in the body
                                email_flag = 1      # set the "sent email" flag to inhibit further alerts - we don't want to send on every second....
                                
                    try: # reconnect - if successful we send email....
                        # we've lost comms - we can call make_con() and attempt to reconnect
                        self.make_con()
                        self.email_allow = self.email_enable.get()  # if emails are allowed...
                        if self.email_allow:
                
                            if email_flag == 1:         # we sent one already - a FAIL email
                                alert.send_email("Snargate comms Restored") # so we send a "restored" email
                                email_flag = 0          # clear the sent email flag, ready for the next event

                            lost_contact = 0            # reset the "lost contact poll failure" counter
                    except: # we can't reconnect....
                        lost_contact += 1               # increment the "lost contact poll failure" counter - we set a trigger level (30) above
                        
                        
                        
            else: # we weren't connected anyway so we ignore all the email and reconnect funtionality
                pass
        
    ###########
    # various functions called by poll()
    #
    # ptt status - is the TX transmitting?
    def get_ptt_state(self):
        # poll_cmd = send the command to the server and use the response to
        # set a label text (i.e. don't update the greenscreen terminal ScrolledText widget)
        
        ptt_state = self.poll_cmd("GETPTT")
        # insepect the reply and set colour and text of status Label
        if ptt_state == "PTT ON":
            self.l_reply2.configure(fg = 'red')
        else:
            self.l_reply2.configure(fg = 'darkgreen')
            
        # check the "lost comms" and "connected" variables
        # and set the label text appropriate to the current status
        if self.lost_comms == 1 and self.connected == 1: # we had comms and have lost it....
            self.l_reply2.configure(fg = 'red')
            self.snargate_reply2.set("Lost Comms")
            
        elif self.connected == 0:                       # we aren't connected (on purpose)
            self.snargate_reply2.set("")
            
        else:    
            self.snargate_reply2.set(ptt_state)         # we're connected - set the text   
            
    # TX State = enabled or disabled - we need to update status label as well as the TX_STATE checkbutton
    def get_tx_state(self):
        txstate = self.poll_cmd("TXSTATE")
        if txstate == "TX Enabled":             # TX is allowed
            self.cb_tx_state.select()           # select (tick) the tx_state checkbutton
            self.l_reply3.configure(fg = 'darkgreen')   # set the status label colour
            
        else:                                   # TX is disabled
            self.cb_tx_state.deselect()         # deselect (untick) the tx_state checkbutton
            self.l_reply3.configure(fg = 'red') # set the status label colour
        
        # check the "lost comms" and "connected" variables
        # and set the label text appropriate to the current status
        
        if self.lost_comms == 1 and self.connected == 1:
            self.l_reply3.configure(fg = 'red')
            self.snargate_reply3.set("Lost Comms")
        elif self.connected == 0:
            self.snargate_reply3.set("")    
        else:    
            self.snargate_reply3.set(txstate)
    
    # same procedure as the previous functions.....
    def get_last_rx_message(self):
        last_message = self.poll_cmd("LAST1")
        
        #if re.search("ACK", last_message):
        #    self.l_reply4.configure(fg = 'blue')
        #else:
        #    self.l_reply4.configure(fg = 'red')
        
        if self.lost_comms == 1 and self.connected == 1:
            self.l_reply4.configure(fg = 'red')
            self.snargate_reply4.set("Lost Comms")
        elif self.connected == 0:
            self.snargate_reply4.set("")
        else:    
            self.l_reply4.configure(fg = 'blue')        
            self.snargate_reply4.set(last_message)
            
            
        if self.lost_comms == 1 and self.connected == 1:
            self.l_reply4.configure(fg = 'red')
            self.snargate_reply4.set("Lost Comms")
        elif self.connected == 0:
            self.snargate_reply4.set("")    
        else: 
            self.l_reply4.configure(fg = 'blue')
            self.snargate_reply4.set(last_message)
    
    def get_last_tx_message(self):
        last_tx = self.poll_cmd("TX1")
        #if re.search("ACK", last_tx):
        #    self.l_reply5.configure(fg = 'blue')
        #else:
        #    self.l_reply5.configure(fg = 'red')
        
        if self.lost_comms == 1 and self.connected == 1:
            self.l_reply5.configure(fg = 'red')
            self.snargate_reply5.set("Lost Comms")
        elif self.connected == 0:
            self.snargate_reply5.set("")
        else:    
            self.l_reply5.configure(fg = 'red')
            self.snargate_reply5.set(last_tx)
            
        if self.lost_comms == 1 and self.connected == 1:
            self.l_reply5.configure(fg = 'red')
            self.snargate_reply5.set("Lost Comms")
        elif self.connected == 0:
            self.snargate_reply5.set("")    
        else:
            self.l_reply5.configure(fg = 'red')
            self.snargate_reply5.set(last_tx)
    
    def get_message_count(self):
        message_count = self.poll_cmd("COUNT")
        
        if self.lost_comms == 1 and self.connected == 1:
            self.l_reply6.configure(fg = 'red')
            self.snargate_reply6.set("Lost Comms")
        elif self.connected == 0:
            self.snargate_reply6.set("")
        else:    
            self.l_reply6.configure(fg = 'black')
            self.snargate_reply6.set(message_count)
            
    def get_message_per_band(self):
        message_per_band = self.poll_cmd("PERBAND")
        if self.lost_comms == 1 and self.connected == 1:
            self.l_reply7.configure(fg = 'red')
            self.snargate_reply7.set("Lost Comms")
        elif self.connected == 0:
            self.snargate_reply7.set("")
        else:    
            self.l_reply7.configure(fg = 'black')
            self.snargate_reply7.set(message_per_band)
        
        
    # this function retrieves the currently allowd frequencies from the server and
    # selects/deselects the appropriate frequency checkbuttons
    
    def get_freq_list(self):
        # the allowed frequencies are in a string with ";" delimiters
        # split it into a list
        freq_list = self.poll_cmd("POLLFREQ").split(";")
        
        # test for the presence of each frequency in the list and select/deselect each checkbutton as necessary
        if "2187.5" in freq_list:
            self.cb_2.select()
        else:
            self.cb_2.deselect()
            
        if "4207.5" in freq_list:
            self.cb_4.select()
        else:
            self.cb_4.deselect()
           
        if "6312.0" in freq_list:
            self.cb_6.select()
        else:
            self.cb_6.deselect()
        
        
        if "8414.5" in freq_list:
            self.cb_8.select()
        else:
            self.cb_8.deselect()
            
        if "12577.0" in freq_list:
            self.cb_12.select()
        else:
            self.cb_12.deselect()
           
        if "16804.5" in freq_list:
            self.cb_16.select()
        else:
            self.cb_16.deselect()
    
    # this function is called by the mmsi_win() function, and retrieves the data from the "resolve" database
    def get_mmsi_log(self):
        # not regularly polled - but uses the poll_cmd() to prevent the results being written to the main window terminal
        mmsi_log = self.poll_cmd("GETRESOLVESQL")       
        try: 
            self.mmsi_term.delete(0.0, END)             # clear the contents of the terminal window
            self.mmsi_term.insert(END, mmsi_log+"\n")   # insert the new list
            self.mmsi_term.yview(END)                   # scroll to the bottom
        except:
            pass
    
    # function called regularly by poll() to retrieve the system log data and update the sys_term TopLevel window
    def get_sys_log(self):
        sys_log = self.poll_cmd("GETADMINSQL")
        try: # in a try/except because the term may not exist if the user hasn't pressed the button, but the function is still called by poll() anyway
            self.sys_term.insert(END, sys_log+"\n")
            self.sys_term.yview(END)
        except:
            pass
    
    # function called regularly by poll() to retrieve the RX/TX log data and update the rxtx_term TopLevel window       
    def get_rxtx_log(self):
        
        rxtx_log = self.poll_cmd("GETRXTXSQL")
        
        try:# in a try/except because the term may not exist if the user hasn't pressed the button, but the function is still called by poll() anyway
            self.rxtx_term.tag_config("TX1", foreground="red")
            for line in rxtx_log.split('\n'):   
                tags = ("TX1", ) if ": TX1" in line else None
                print tags
                self.rxtx_term.insert(END, line+"\n", tags)
                self.rxtx_term.yview(END)
        except:
        #    print "exception"
            pass
    # function called regularly by poll() to retrieve the RX log data and update the rx_term TopLevel window       
    def get_rx_log(self):
        rx_log = self.poll_cmd("GETRXSQL")
        try: # in a try/except because the term may not exist if the user hasn't pressed the button, but the function is still called by poll() anyway
            self.rx_term.delete(0.0, END)
            self.rx_term.insert(END, rx_log+"\n")
            self.rx_term.yview(END)
        except:
            pass
    
    # function called regularly by poll() to retrieve the TX log data and update the tx_term TopLevel window
    def get_tx_log(self):
        tx_log = self.poll_cmd("GETTXSQL")
        
        try: # in a try/except because the term may not exist if the user hasn't pressed the button, but the function is still called by poll() anyway
            self.tx_term.delete(0.0, END)
            self.tx_term.insert(END, tx_log+"\n")
            self.tx_term.yview(END)
        except:
            pass
    
    # routine polling of status information. Called in the __init__ of the App class intially and then called again at completion, with 
    # a delay of 1 second, durin which time applicaiton control returns to the user
    
    def poll(self):
        ##############  why aren't these in the relevant get_XX_log() functions?
        # delete the last retrieved text from the windows (in try: because the windows may not exist if the user hasn't pressed the button 
        # to create them
        try:
            self.sys_term.delete(0.0, END)
        except:
            pass
        #try:
        #    self.rx_term.delete(0.0, END)
        #except:
        #    pass
        #try:
        #    self.tx_term.delete(0.0, END)
        #except:
        #    pass
        try:
            self.rxtx_term.delete(0.0, END)
        except:
            pass
        ###############################
        #
        # the "ping" function
        self.online()
        
        # get the sys log and display it if the window has been created
        self.get_sys_log()
        
        # get the rx log and display it if the window has been created
        #self.get_rx_log()
        
        # get the rxtx log and display it if the window has been created
        self.get_rxtx_log()
        
        # get the tx log and display it if the window has been created
        #self.get_tx_log()
        
        # get ptt state - set status text as necessary
        self.get_ptt_state()
        
        # get tx state - set status text AND checkbutton as necessary
        self.get_tx_state()
        
        # get last rx message and set status text as necessary
        self.get_last_rx_message()    
        
        # get last tx message and set status text as necessary
        self.get_last_tx_message()
        
        # get total message count and set status text as necessary
        self.get_message_count()
        
        # get individual band message counts and set status text as necessary
        self.get_message_per_band()
        
        # get allowed frequency list and select/deselect freq. checkbuttons as necessary
        self.get_freq_list()
            
        # use the after() method to schedule another poll() in 1000ms
        self.master.after(1000, self.poll)
        
        
    # function to send requests to the server and return it to the calling function (not displayed on the 
    # main window terminal screen. This is mainly called by functions controlled by poll()
    def poll_cmd(self, cmd):
        
        id = self.id_e.get()        # id is read from the id_e entry box
        header = "ADMIN"            # All commands are prefixed with "ADMIN"
        sendcommand = header+";"+cmd+";"+id     # build the command string - a ";" delimited string with ID as the last element
        
        try:
            received = n1.connect(sendcommand)      # send the command and read the returned data
            return received
            
        except:
            return "Not Connected"
        
    
    # send a command and display the returned data on the main window terminal screen   
    def send_command(self, command):
       
        # if we're sending an "ADD" or "DEL" command (exclude/include an RX ID)
        # we clear the RX ID Entry box - looks better if it clears once sent....
        if command.split(";")[0] == "ADD" or command.split(";")[0] == "DEL": 
            self.exclude_e.delete(0, 'end')
        
        # get the ID from the UserName entry box
        id = self.id_e.get()    
        header = "ADMIN"  
        sendcommand = header+";"+command+";"+id             # build the command string 
        
        
        
        
        try:
            print "SENDING ", sendcommand
            received = n1.connect(sendcommand)      # send the command and read the reply
           
        except:
            print "Timeout"
            self.command_reply.set("ADMIN > NO REPLY FROM COAST")
            # we constrain the number of lines in the scrolling text widget....
            #numlines = float(self.reply.index('end - 1 line').split('\n')[0])
            #if numlines > 2.0: # too many
            #    deletelines = numlines-2  # delete enough to retain 200          
            #    self.reply.delete(0.0, deletelines)
            
            return
        
        
        
        #self.reply.insert(END, "ADMIN > "+command+"\n") # "print" the command on the terminal widget
        self.command_reply.set(received)           # "print" the reply on the terminal widget
        #self.reply.yview(END)                           # scroll to the bottom
        
        
        
        # we constrain the number of lines in the scrolling text widget....
        #numlines = float(self.reply.index('end - 1 line').split('\n')[0])
        #if numlines > 2: # too many
        ##    deletelines = numlines-2  # delete enough to retain 200          
         #   self.reply.delete(0.0, deletelines)
        
        return received
    
    

if __name__ == '__main__':
    root = Tk()
    
    lock = threading.Lock()
    root.geometry("+10+10")
    root.resizable(0, 0)
    root.title("Wire2waves DSC Coast Station " + version)
    
    app = Application(root)
    # insance of the network class - our connection to the server
    n1 = Network()
    
    # start the GUI
    root.mainloop()
