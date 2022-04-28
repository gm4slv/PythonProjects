"""
DSC Coast Station : DSC Coast Station server and client

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
# GM4SLV
# 
# Python DSC Auto-Test Responder
# 
# April/May 2015
# 
# Network administration client using TKinter
#


version = "v0.1ham"

from Tkinter import *
import ttk

from tkMessageBox import *
from tkFileDialog import *
from tkSimpleDialog  import *
from ScrolledText import *
import time
import re
import socket
import json
import hashlib
import os

import threading
import Queue

ABOUT_TEXT = "GM4SLV DSC Coast Station : DSC Coast Station client \n\n version "+ version + '''\n\n
    Copyright (C) 2015  John Pumford-Green
    gm4slv@gmail.com  

'''

# Coast Station Server host / port
#HOST, PORT = "gm4slv.plus.com", 50669
HOST, PORT = "192.168.21.4", 50669
try:
    mmsi_send = open('mmsi_send.txt')
    mmsi_list = json.load(mmsi_send)
except:
  
    mmsi_list = ["235096236"]
    
    
try:
    rx_file = open('rx_list.txt')
    rx_list = json.load(rx_file)
except:
    # if nothing alread stored on disk, we make an empty list. It'll get appended to later
    # as receivers are added on the fly from the administrator utility.
    rx_list = []

# The class for a TCP/IP connection to the Server
# Instantiated at program startup 
class Network(object):
    def __init__(self):
        # when the n1 instance is created, do nothing - we'll connect later.
        
        pass
    
    # connect to the Coast Station server at the HOST, PORT
    # make_con() is called 
    # 1) in the GUI's __INIT__
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
    
    def login(self, data):
        
        lock.acquire()
        #print "sending ", data
        self.sock.sendall(data + "\n")
        
        received = self.sock.recv(2048)
        lock.release()
        return received
        
    def connect(self, data):
        try:
        
            lock.acquire()
            #print lock
            # sendall our data to the server in a single line
            #print "sending ", data
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
        invalid_count = 1
        self.grid()
        
        
        
    
        menubar = Menu(root)
        
        menubar.add_command(label="Save...", command = self.save_current_window)
        
        menubar.add_command(label="Log download..", command=self.allsyswin)

        servermenu = Menu(menubar, tearoff=0)

        servermenu.add_command(label="List Connected Clients", command=lambda: self.list_connected())
        #servermenu.add_command(label="Show MOTD", command=lambda: self.show_motd_win())
        servermenu.add_separator()
        servermenu.add_command(label="Change Password", command=lambda: self.make_passwd_win())
        servermenu.add_separator()
        servermenu.add_command(label="Reset Message Count", command=lambda: self.reset())
        servermenu.add_separator()
        servermenu.add_command(label="Purge Syslog (>7 days)", command=lambda: self.purge_admin_7())
        servermenu.add_command(label="Purge Syslog (Logins)", command=lambda: self.purge_admin_login())
        servermenu.add_separator()
        #servermenu.add_command(label="Restart", underline=0, command= lambda: self.reboot())
        servermenu.add_command(label="Shutdown", underline=0, command= lambda: self.shutdown())
        
        menubar.add_cascade(label="Server", menu=servermenu, underline=0)
        menubar.add_command(label="About", underline=0, command=self.about)
        
        menubar.add_command(label="Quit", underline=0, command= lambda: self.callback())
        root.config(menu=menubar)
        
        self.create_widgets()
        self.make_login_win()
        self.login_win.wm_attributes("-topmost", 1)
        self.username_e.focus()
        
        
    def start_polls(self):
        
        self.fill_mmsi()
        self.fill_rx_e()
        self.fill_rx_i()
        root.focus_force()
        
        
        #self.username = askstring("Login", "This system is for authorized users only.\n\nIf you have not been provided with permission\nto access this system disconnect at once.\n\nAll activity is logged\n\nUser Name:")
        #self.password = askstring("Password", "Enter password")
        
        #self.make_con()
        
        
    
        # options for saving log files - used by file_save()
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]

        #starting the log thread
        self.log_queue = Queue.Queue(maxsize=10)
        self.log_thread_stop_event = threading.Event()
        self.poll_log_thread = threading.Thread(target=log_thread, name='Thread', args=(self.log_queue,self.log_thread_stop_event))
        self.poll_log_thread.start()
        
        
        #starting the status thread
        self.status_queue = Queue.Queue(maxsize=10)
        self.poll_thread_stop_event = threading.Event()
        self.poll_status_thread = threading.Thread(target=status_thread, name='Thread', args=(self.status_queue,self.poll_thread_stop_event))
        self.poll_status_thread.start()

        self.poll_interval = 1000

        #starting status poll()
        self.status_poll()
        
        #starting log_poll()
        self.log_poll()
        
        root.protocol("WM_DELETE_WINDOW", self.callback)
        root.lift()
        
    # called by the "Quit" menu entry
    def callback(self):
        if askyesno('Verify', 'Really quit?', default='no'):
            self.close()
            self.cleanup_on_exit()    
        else:
            pass
            
    def get_login(self):
        
        self.username = self.username_e.get()
        self.password = self.password_e.get()
        self.login_win.destroy()
        self.make_con()
        return
    
    def passwd(self):
        
        self.current_password = self.oldpass_e.get()
        self.verify_reply = n1.login("ADMIN;VERIFY;"+version+";"+token)
        #print self.verify_reply
        self.random = self.verify_reply.split(":")[0]
        self.salt = self.verify_reply.split(":")[1]
        #print self.random
        #print self.salt
        self.current_hash = hashlib.sha256(self.salt + self.current_password).hexdigest()
        self.current_value = hashlib.sha256(self.random + self.current_hash).hexdigest()
        self.verify_reply = n1.login("ADMIN;CHECK;"+self.current_value+";"+version+";"+token)
        if self.verify_reply == "verified":
            #print "password ok"
            self.newpass = self.newpass_e.get()
            self.check_new = self.ckpass_e.get()
            if self.newpass == self.check_new:
                self.new_salt = os.urandom(32).encode('hex')
                self.new_pass_hash = hashlib.sha256( self.new_salt + self.newpass).hexdigest()
                self.update_password = n1.login("ADMIN;UPDATEPW;"+self.new_salt+";"+self.new_pass_hash+";"+version+";"+token)
                showinfo("Result", "Password updated")
                 
            else:
                showinfo("Result", "Passwords don't match")
                
        else:
            showinfo("Result", "Incorrect Password")
        self.passwd_win.destroy()
        
        
    def make_login_win(self):
        try:
            self.login_win_exists = self.login_win.winfo_exists()
        except:
            self.login_win_exists = 0
            
        if self.login_win_exists == 0:   
            
            self.login_win = Toplevel(self)
            self.login_win.title("Login..")
            self.login_win.resizable(0, 0)
            self.login_win.grid()
            self.warning_l = Label(self.login_win, fg="red", text = "This system is for authorized users only.\n\nIf you have not been provided with permission\nto access this system disconnect at once.\n\nAll activity is logged\n\n")
            self.warning_l.grid(row = 0, column = 0, columnspan = 2, rowspan = 2)
            self.username_l = Label(self.login_win, text = "Username : ")
            self.username_l.grid(row = 2, column = 0)
            self.username_e = Entry(self.login_win)
            self.username_e.grid(row = 2, column = 1)
            self.password_l = Label(self.login_win, text = "Password : ")
            self.password_l.grid(row = 3, column = 0)
            self.password_e = Entry(self.login_win, show="*")
            self.password_e.grid(row = 3, column = 1)
            self.password_e.bind( '<Return>', (lambda event: self.login_b.invoke()))
            self.login_b = Button(self.login_win, text = "Login", command = lambda: self.get_login())
            self.login_b.grid(row = 4, column = 1)
            
        else:
            
            
            self.login_win.lift()
            self.login_win.focus_force()
    
    def make_passwd_win(self):
        try:
            self.passwd_win_exists = self.passwd_win.winfo_exists()
        except:
            self.passwd_win_exists = 0
            
        if self.passwd_win_exists == 0:   
            
            self.passwd_win = Toplevel(self)
            self.passwd_win.title("Login..")
            self.passwd_win.resizable(0, 0)
            self.passwd_win.grid()
            
            #self.warning_l = Label(self.login_win, text = "This system is for authorized users only.\n\nIf you have not been provided with permission\nto access this system disconnect at once.\n\nAll activity is logged\n\n")
            #self.warning_l.grid(row = 0, column = 0, columnspan = 2, rowspan = 2)
            self.oldpass_l = Label(self.passwd_win, text = "Current Password : ")
            self.oldpass_l.grid(row = 2, column = 0)
            self.oldpass_e = Entry(self.passwd_win, show="*")
            self.oldpass_e.grid(row = 2, column = 1)
            self.newpass_l = Label(self.passwd_win, text = "New Password : ")
            self.newpass_l.grid(row = 3, column = 0)
            self.newpass_e = Entry(self.passwd_win, show="*")
            self.newpass_e.grid(row = 3, column = 1)
            self.ckpass_l = Label(self.passwd_win, text = "New Password again : ")
            self.ckpass_l.grid(row = 4, column = 0)
            self.ckpass_e = Entry(self.passwd_win, show="*")
            self.ckpass_e.grid(row = 4, column = 1)
            self.passwd_b = Button(self.passwd_win, text = "Change Password", command = lambda: self.passwd())
            self.passwd_b.grid(row = 5, column = 1)
            
            
            self.ckpass_e.bind( '<Return>', (lambda event: self.passwd_b.invoke()))
            
            self.passwd_win.wm_attributes("-topmost", 1)
            self.oldpass_e.focus()
        else:
            
            
            self.login_win.lift()
            self.login_win.focus_force()
    
    def make_con(self):
       
        self.con = n1.make_con()
        if self.con:
            #print "asking for random/salt"
            self.reply = n1.login("login %s" % self.username)
            #print "reply",self.reply
    
            
            self.random, self.salt = self.reply.split(":")
            #print "random ", self.random
            #print "salt ", self.salt
            self.challenge_client(self.username, self.random, self.salt, self.password)
    
    
    def challenge_client(self, user, random, salt, client_password):
        global token
        #print "in challenge_client"
        self.client_hash = hashlib.sha256(salt + client_password).hexdigest()
        #print "client hash ", self.client_hash

        self.client_value = hashlib.sha256(random + self.client_hash).hexdigest()
        #print "client value ", self.client_value
        
        self.valid = n1.login("reply %s %s" % (self.client_value, version))
        #print "valid ",self.valid
        if "Incorrect" in self.valid:
            showinfo("Validation", self.valid)
        
        try:
            token = n1.login("alive")
            if token=="pong" or token =="":
                #sock.close()
                sys.exit(0)
            #print "got session token ", token
        except:
            #sock.close()
            sys.exit(0)
    
        if "Try again" not in self.reply: 
            #token = sock.recv(512)
            self.motd = n1.connect("ADMIN;MOTD;"+token)
            #print self.motd
            self.hello = poll_cmd("hello")
            self.snargate_reply8.set(self.hello)
            #self.show_motd_win()
            self.start_polls()
            
            
    def show_motd_win(self):
        
        try:
            self.motd_win_exists = self.motd_win.winfo_exists()
        except:
            self.motd_win_exists = 0
            
        if self.motd_win_exists == 0:   
            self.motd = poll_cmd("MOTD")#.replace('\n', '')
            self.motd_win = Toplevel(self)
            self.motd_win.title("MOTD")
            self.motd_win.resizable(0, 0)
            self.motd_win.grid()
            self.motd_var=StringVar()
            self.motd_label = Label(self.motd_win, textvariable= self.motd_var, justify=LEFT)
            self.motd_label.grid()
            self.motd_var.set(self.motd)
        else:
            self.motd = poll_cmd("MOTD")#.replace('\n', '')
            self.motd_var.set(self.motd)
            self.motd_win.wm_state('normal')
            self.motd_win.lift()
            self.motd_win.focus_force()
        
        
    def get_motd(self):
        
        self.motd_text = poll_cmd("MOTD")
        self.motd_term.config(state='normal')
        first, last = self.motd_term.yview()
        self.motd_term.delete(0.0, END)
        
        self.motd_term.insert(END, self.motd_text+"\n")
            
        #self.motd_term.yview(END)
        self.motd_term.yview_moveto(first)
        self.motd_term.config(state='disabled')
     
        #self.motd_var.set(self.motd_text)#.replace('\n',''))
        
    def close(self):
        goodbye = poll_cmd("iwantotquit")
        
    '''        
    def get_username(self):
        global id
        global invalid_count
        if invalid_count < 3:
            self.close()
            id = ""
            invalid_count += 1
            id = askstring("Try again...",  "This is attempt %d of 3.\nPlease enter a valid username.\n" % invalid_count)
            self.con = n1.make_con()
            self.welcome = poll_cmd("hello")
            self.snargate_reply8.set(self.welcome)
            if re.search("Invalid", self.welcome):
                self.get_username()
        else:
            self.close() 
            showinfo("Closing", "Too many attempts.\n\nYour IP address has been logged.")            
            self.cleanup_on_exit()
    '''
    
    def shutdown(self):
    
        self.shutdown_allowed = 1
        if self.shutdown_allowed:
            if askyesno('Confirm', 'Really Shutdown Server?\nService will not auto-restart after this action.', default='no'):
                reason = askstring('Reason', 'Please enter your reason')
                if reason != "":
                    server_reply = poll_cmd("SHUTDOWN;"+reason)
                    showinfo('Reply', 'Shutdown command issued\nServer reply : %s' % server_reply)
                else:
                    showinfo('Reason', 'No reason given, shutdown cancelled')
            else:
                showinfo('No', 'Server Shutdown has been cancelled')
                
    def reboot(self):
    
        self.shutdown_allowed = 1
        if self.shutdown_allowed:
            if askyesno('Confirm', 'Really Restart Server?', default='no'):
                reason = askstring('Reason', 'Please enter your reason')
                if reason != "":
                    server_reply = poll_cmd("REBOOT;"+reason)
                    showinfo('Reply', 'Restart command issued\nServer reply : %s' % server_reply)
                else:
                    showinfo('Reason', 'No reason given, restart cancelled')
            else:
                showinfo('No', 'Server restart has been cancelled')
    
    
    def reset(self):
        if askyesno('Confirm', 'Do you want to zero the message counts?', default='no'):
            poll_cmd("CLEAR")
            showinfo('Complete', 'Count has been reset to zero')
        else:
            showinfo('No', 'Count has not been reset')
    
    def purge_admin_7(self):
        if askyesno('Confirm', 'Purge Syslog Database of records\nmore than 7 days old?', default='no'):
            server_reply = poll_cmd("CLEARADMIN7SQL")
            showinfo('Reply', 'Purge command issued\nServer reply : %s' % server_reply)
        else:
            showinfo('No..', 'Database un-changed')
    
    def purge_admin_login(self):
        if askyesno('Confirm', 'Purge Syslog Database of login\n and connection records?', default='no'):
            server_reply = poll_cmd("CLEARADMINLOGINSQL")
            showinfo('Reply', 'Purge command issued\nServer reply : %s' % server_reply)
        else:
            showinfo('No..', 'Database un-changed')
            
    def list_connected(self):
        self.connected_list = poll_cmd("LISTCONNECTED")
        showinfo('Connected...', 'Current connections :\n %s' % self.connected_list)
    
    def handler(self):
        pass
        
    def about(self):
            showinfo("About", ABOUT_TEXT)
    
    def allsyswin(self):
    
        # test to see if the frame already exists.
        try:
            self.allsys_frame_exists = self.allsys_frame.winfo_exists()
        except:
            self.allsys_frame_exists = 0
        
        # If not we can create it and a ScrolledText widget. The text is updated automatically 
        if self.allsys_frame_exists == 0:
            self.allsys_frame = Toplevel(self,  bg = 'black', takefocus=True)
            self.allsys_frame.title("Full Log File retrieve")
            
            self.allsys_frame.resizable(0, 0)
            
            self.allsys_frame.grid() 
            self.allsysmenu = Menu(self.allsys_frame)
            self.allsysmenu.add_command(label="Save...", command= lambda: self.file_save(self.allsys_term.get(1.0, END)))
            self.allsysmenu.add_command(label="Retrieve RX/TX log...", command = lambda: self.get_allrxtx_log())
            self.allsysmenu.add_command(label="Retrieve RX log...", command = lambda: self.get_allrx_log())
            self.allsysmenu.add_command(label="Retrieve TX log...", command = lambda: self.get_alltx_log())
            self.allsysmenu.add_command(label="Retrieve Check log...", command = lambda: self.get_allcheck_log())
            self.allsysmenu.add_command(label="Retrieve MMSI log...", command = lambda: self.get_mmsi_log())
            self.allsysmenu.add_command(label="Retrieve Syslog (slow)...", command = lambda: self.get_allsys_log())

            self.allsys_frame.config(menu=self.allsysmenu)
        
            self.allsys_term = ScrolledText(self.allsys_frame, fg='blue', bg='#b0c4de', width = 120, height = 31, wrap = WORD)
            self.allsys_term.grid(row = 0, column = 0, sticky=W+E+N+S)
            self.allsys_term.insert(END, "To view the complete log click the required \"Retrieve...\" menu \nThe files may take a few seconds to appear")
            self.allsys_frame.lift()
            self.allsys_frame.focus_force()

        # Otherwise restore it from minimzation, and lift it to the top of the windows
        else:
            self.allsys_frame.wm_state('normal')
            self.allsys_frame.lift()
            self.allsys_frame.focus_force()
    
    def get_allsys_log(self):
          
        self.allsys_log = poll_cmd("GETALLADMINSQL")
        self.allsys_term.config(fg='black')
        self.allsys_term.tag_config("ADMIN", foreground="darkgreen")
        self.allsys_term.tag_config("RX", foreground="blue")
        self.allsys_term.tag_config("TX", foreground='#b50414')
        self.allsys_term.tag_config("CK", foreground='gray30')
        self.allsys_term.config(state='normal')
        self.allsys_term.delete(0.0, END)
        for line in self.allsys_log.split("\n"):
            if "Admin;" in line:
                tags = ("ADMIN", )
            elif "Received" in line:
                
                tags = ("RX", ) 
            elif "Transmit" in line: 
                tags = ("TX", )
            elif "Checklog" in line:
                tags  = ("CK",)
                
            else:
                tags = None
            self.allsys_term.insert(END, line+"\n", tags)
                
        self.allsys_term.config(state='disabled')
        self.allsys_term.yview(END)

    def get_allrxtx_log(self):
        self.allrxtx_log = poll_cmd("GETALLRXTXSQL")
        self.allsys_term.config(fg='blue')
        
        self.allsys_term.tag_config("TX", foreground='#b50414')
        self.allsys_term.tag_config("RX", foreground='blue')
        self.allsys_term.tag_config("CK", foreground='gray30')
        self.allsys_term.config(state='normal')
        self.allsys_term.delete(0.0, END)
            
        for line in self.allrxtx_log.split('\n'):

            if "; TX1" in line:
                tags = ("TX", ) 
            elif "; CK" in line:
                tags  = ("CK",)
            elif "; RX" in line:
                tags  = ("RX",)
            else:
                tags = None

            self.allsys_term.insert(END, line+"\n", tags)
                
        self.allsys_term.yview(END)
        self.allsys_term.config(state='disabled')
   
    def get_allcheck_log(self):
        self.allcheck_log = poll_cmd("GETALLCHECKSQL")
        self.allsys_term.config(fg='gray30')
        self.allsys_term.config(state='normal')
        self.allsys_term.delete(0.0, END)
        self.allsys_term.insert(END, self.allcheck_log+"\n")
  
        self.allsys_term.yview(END)
        self.allsys_term.config(state='disabled')
    
    def get_allrx_log(self):
        self.allrx_log = poll_cmd("GETALLRXSQL")
        self.allsys_term.config(fg='blue')
        self.allsys_term.config(state='normal')
        self.allsys_term.delete(0.0, END)
        self.allsys_term.insert(END, self.allrx_log+"\n")
        self.allsys_term.yview(END)
        self.allsys_term.config(state='disabled')
       
            
    def get_alltx_log(self):
        self.alltx_log = poll_cmd("GETALLTXSQL")
        self.allsys_term.config(fg='#b50414')
        self.allsys_term.config(state='normal')
        self.allsys_term.delete(0.0, END)
        self.allsys_term.insert(END, self.alltx_log+"\n")
        self.allsys_term.yview(END)
        self.allsys_term.config(state='disabled')
  
    
    def get_mmsi_log(self): 
        self.allmmsi_log = poll_cmd("GETRESOLVESQL")       
        self.allsys_term.config(fg='black')
        self.allsys_term.config(state='normal')
        self.allsys_term.delete(0.0, END)             # clear the contents of the terminal window
        self.allsys_term.insert(END, self.allmmsi_log+"\n")   # insert the new list
        self.allsys_term.yview(END)            # scroll to the bottom
        self.allsys_term.config(state='disabled')

    def save_current_window(self):
        self.current_window = self.sys_note.index(self.sys_note.select())

        if self.current_window == 0:
            self.file_save(self.sys_term.get(1.0, END))
        elif self.current_window == 1:
            self.file_save(self.rxtx_term.get(1.0, END))
        elif self.current_window == 2:
            pass
            
    # Uses tkMessageBox widget to get a file-name and saves the text sent by the calling function
    def file_save(self, text2save):
        self.f = asksaveasfile(mode='w', **self.file_opt)
        if self.f is None:
            return
        self.f.write(text2save)
        self.f.close()
        
    def fill_mmsi(self):
        for mmsi in mmsi_list:
            vals = self.to_mmsi_e.cget('values')
            if not vals:
                self.to_mmsi_e.configure(values = (mmsi, ))
            elif mmsi not in vals:
                self.to_mmsi_e.configure(values = vals + (mmsi,))
                
    def fill_rx_e(self):
        for rx in rx_list:
            vals = self.exclude_e.cget('values')
            if not vals:
                self.exclude_e.configure(values = (rx, ))
            elif rx not in vals:
                self.exclude_e.configure(values = vals + (rx,))

    def fill_rx_i(self):
        for rx in rx_list:
            vals = self.include_e.cget('values')
            if not vals:
                self.include_e.configure(values = (rx, ))
            elif rx not in vals:
                self.include_e.configure(values = vals + (rx,))

    def update_rx_e_list(self):
        widget = self.exclude_e           # get widget
        txt = widget.get()            # get current text
        vals = widget.cget('values')  # get values
        if txt != "":
            if not vals:
                widget.configure(values = (txt, ))
                rx_list.append(txt)
            elif txt not in vals:
                widget.configure(values = vals + (txt, ))
                rx_list.append(txt)
            values_to_save = widget.cget('values')
            with open('rx_list.txt', 'wb') as outfile:
                json.dump(values_to_save, outfile)
            self.fill_rx_i()
            
    def update_rx_i_list(self):
        widget = self.include_e           # get widget
        txt = widget.get()            # get current text
        vals = widget.cget('values')  # get values
        if txt != "": 
            if not vals:
                widget.configure(values = (txt, ))
                rx_list.append(txt)
            elif txt not in vals:
                widget.configure(values = vals + (txt, ))
                rx_list.append(txt)
            values_to_save = widget.cget('values')
            with open('rx_list.txt', 'wb') as outfile:
                json.dump(values_to_save, outfile)   
            self.fill_rx_e()
            
    def update_mmsi(self):
        widget = self.to_mmsi_e           # get widget
        txt = widget.get()            # get current text
        vals = widget.cget('values')  # get values
        if len(txt) == 9:
            if not vals:
                widget.configure(values = (txt, ))
            elif txt not in vals:
                widget.configure(values = vals + (txt, ))
            values_to_save = widget.cget('values')
            with open('mmsi_send.txt', 'wb') as outfile:
                json.dump(values_to_save, outfile)
            
    def create_widgets(self):

        self.sys_frame = Frame(self, borderwidth=0)    
        self.sys_frame.grid(row=2, column = 0, rowspan = 9, columnspan = 14, sticky=N+S+E+W) 
        
        self.status_frame =  Frame(self.sys_frame, borderwidth=1,relief=GROOVE, bg='#b0c4de')
        self.status_frame.grid(row = 10, column  = 0, columnspan = 14, sticky=N+S+E+W)   
        
        self.log_flag = StringVar()
        
        self.sys_note = ttk.Notebook(self.sys_frame)
        
        self.f1 = Frame(self.sys_note, bg="#b0c4de")
        self.f2 = Frame(self.sys_note, bg="#b0c4de")
        self.f3 = Frame(self.sys_note,  bg="#b0c4de")
        self.f4 = Frame(self.sys_note,  bg="#b0c4de")

        self.sys_note.add(self.f1, text='Syslog')
        self.sys_note.add(self.f2, text='RX/TX Log')  
        self.sys_note.add(self.f3, text='Controls')
        self.sys_note.add(self.f4, text='MOTD')
        
        self.sys_note.grid(row=1, column=0)
        
        self.button_1_frame = Frame(self.f3, bg="#b0c4de")
        self.button_1_frame.grid(row = 0, column = 0, columnspan=14, rowspan = 5,sticky=W+E)
        
        self.cb_frame = Frame(self.f3, bg='#b0c4de')      
        self.cb_frame.grid(row=5, column=0, columnspan = 14, sticky=N+S+E+W)
        
        self.button_3_frame = Frame(self.f3, bg="#b0c4de")
        self.button_3_frame.grid(row = 10, column = 0, columnspan=14, rowspan = 5,sticky=W+E)
        
        ######### THE TEXT AREAS ##############
        self.sys_term = ScrolledText(self.f1, takefocus=0, pady=0, borderwidth=0, fg='black', bg='#b0c4de', width = 120, height = 18, wrap = WORD, font=('sans',9,''))
        self.sys_term.grid(row = 1, column = 0, columnspan = 14,  sticky=W+E+N+S)
        
        
        self.rxtx_term = ScrolledText(self.f2, takefocus=0, pady=0, borderwidth=0,  fg='blue', bg='#b0c4de', width = 120, height = 18, wrap = WORD, font=('sans',9,''))
        self.rxtx_term.grid(row = 1, column = 0, columnspan = 14,  sticky=W+E+N+S)
        
        
        self.motd_term = ScrolledText(self.f4, takefocus=0, width=120, height=18, wrap=WORD, bg='#b0c4de', font=('courier new',9,''))
        self.motd_term.grid(row = 1, column = 0, columnspan = 14,  sticky=W+E+N+S)
        
        self.snargate_reply8 = StringVar()
        self.l_reply8 = Label(self.status_frame, anchor=SW, justify=LEFT, bg='#b0c4de', textvariable=self.snargate_reply8, width=120, font=('sans',9,''))
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
        
        self.blank = Label(self.button_1_frame,  bg='#b0c4de')
        self.blank.grid(row = 0, column = 0, columnspan = 3, padx=3, sticky=W+E)
        
        self.dsc_l = Label(self.button_1_frame, text = "Manual DSC Call" , bg='#b0c4de', font=('',9,'bold'))
        self.dsc_l.grid(row = 1, column = 0, columnspan=3)
        
        self.dscto_l = Label(self.button_1_frame, text = "To MMSI" , bg='#b0c4de')
        self.dscto_l.grid(row = 2, column = 0,padx=3, sticky = W+E)
        
        self.dscf_l = Label(self.button_1_frame, text = "Frequency" , bg='#b0c4de')
        self.dscf_l.grid(row = 2, column = 1,padx=3, sticky = W+E)
        
        self.to_mmsi_val = StringVar()
        self.to_mmsi_e = ttk.Combobox(self.button_1_frame, width=10, font=('',9,'bold'), textvariable = self.to_mmsi_val)
        self.to_mmsi_e.grid(row = 3 , column = 0, padx = 5,)
        
        self.send_freq = StringVar()
        self.freq_sp = ttk.Combobox(self.button_1_frame, font=('',9,'bold'), width=10, textvariable=self.send_freq)
        self.freq_sp.grid(row=3, column = 1)
        self.freq_sp['values']=("1996.7", "3619.7", "5373.2", "7103.7", "10147.2", "14347.7")
        self.freq_sp.current(0)
        
        self.send_cat = StringVar()
        self.cat_l = Label(self.button_1_frame, text = "Category" , bg='#b0c4de')
        self.cat_l.grid(row = 4, column = 0,padx=3, sticky = W+E)
        self.saf_r = Radiobutton(self.button_1_frame, bg='#b0c4de', text = "Routine", variable = self.send_cat, value = "rtn")
        self.saf_r.grid(row = 4, column = 1, sticky = W)
        self.saf_r = Radiobutton(self.button_1_frame,bg='#b0c4de', text = "Safety", variable = self.send_cat, value = "saf")
        self.saf_r.grid(row = 4, column = 2, sticky = W)
        self.saf_r.invoke()
        
        self.tc1 = StringVar()
        self.tc_l = Label(self.button_1_frame, text = "TC1" , bg='#b0c4de')
        self.tc_l.grid(row = 5, column = 0,padx=3, sticky = W+E)
        self.tc1_test = Radiobutton(self.button_1_frame, bg='#b0c4de', text = "Test", variable = self.tc1, value = "TEST")
        self.tc1_test.grid(row = 5, column = 1, sticky = W)
        self.tc1_j3e = Radiobutton(self.button_1_frame, bg='#b0c4de', text = "J3E", variable = self.tc1, value = "J3E TP")
        self.tc1_j3e.grid(row = 5, column = 2, sticky = W)
        self.tc1_test.invoke()
        
        # The button to send the command to generate a DSC Test call - to the MMSI and on the frequency set in the two adjacent spinboxes.
        self.go_b = Button(self.button_1_frame, text = "Send", fg='white',  bg='#6699cc',command = lambda: poll_cmd("CALL;"+self.to_mmsi_e.get()+";"+self.freq_sp.get()+";"+self.send_cat.get()+";"+self.tc1.get()))
        self.go_b.grid(row = 3, column = 3,pady=3,padx=3, sticky = E)
        self.go_b.bind('<Button-1>',  (lambda event: self.update_mmsi()))
        #
        self.blank = Label(self.button_1_frame,  bg='#b0c4de')
        self.blank.grid(row = 6, column = 0, columnspan = 3,sticky=W+E)
  
        
        ###########################################
        self.tx_state = IntVar()
        self.cb_tx_state = Checkbutton(self.cb_frame, bg='#b0c4de', text="TX Enable", variable=self.tx_state, command=lambda: self.tx_on())
        self.cb_tx_state.grid(row=0, column=0, columnspan=2, sticky=W)
        
        # A label...        
        self.cbf_l = Label(self.cb_frame, bg='#b0c4de', text="Channels allowed:")
        self.cbf_l.grid(row=1, column=0, columnspan=4, sticky=W)
    
        self.sel2 = IntVar()
        self.cb_2 = Checkbutton(self.cb_frame, text="1.6MHz", bg='#b0c4de', takefocus=0, variable=self.sel2, command=lambda: self.sel_2())
        self.cb_2.grid(row=2, column=0, sticky=W)
        
        self.sel4 = IntVar()
        self.cb_4 = Checkbutton(self.cb_frame, text="3.5MHz",  bg='#b0c4de', takefocus=0, variable=self.sel4, command=lambda: self.sel_4())
        self.cb_4.grid(row=2, column=1, sticky=W)
        
        self.sel6 = IntVar()
        self.cb_6 = Checkbutton(self.cb_frame, text="5MHz",  bg='#b0c4de', takefocus=0, variable=self.sel6, command=lambda: self.sel_6())
        self.cb_6.grid(row=2, column=2, sticky=W)
        
        self.sel8 = IntVar()
        self.cb_8 = Checkbutton(self.cb_frame, text="7MHz", bg='#b0c4de', takefocus=0,  variable=self.sel8, command=lambda: self.sel_8())
        self.cb_8.grid(row=2, column=3, sticky=W)
        
        self.sel12 = IntVar()
        self.cb_12 = Checkbutton(self.cb_frame, text="10MHz",  bg='#b0c4de', takefocus=0,  variable=self.sel12, command=lambda: self.sel_12())
        self.cb_12.grid(row=2, column=4, sticky=W)
        
        self.sel16 = IntVar()
        self.cb_16 = Checkbutton(self.cb_frame, text="14MHz",  bg='#b0c4de', takefocus=0,  variable=self.sel16, command=lambda: self.sel_16())
        self.cb_16.grid(row=2, column=5, sticky=W)
   
   
        self.blank = Label(self.cb_frame,  bg='#b0c4de')
        self.blank.grid(row = 3, column = 0, columnspan = 10, padx=3, sticky=W+E)
        #
        # The EXCLUDE RX controls
        self.rx_l = Label(self.button_3_frame, text = "Select / Deselect active receivers", bg='#b0c4de')
        self.rx_l.grid(row=0, column = 0, columnspan=2, sticky=W)
        
        # Button to send the command that will exclude the RX ID entered in the exclude_e entry box - the command get()s the current text and
        # appends it to "ADD;" for passing via send_command(). 
        self.exclude_b = Button(self.button_3_frame, text = "RX Exclude", fg='white', bg='#6699cc', command = lambda: poll_cmd("ADD;"+self.exclude_e.get()))
        self.exclude_b.grid(row = 1, column = 2, pady=2, padx=3, sticky = W+E)
        self.exclude_b.bind('<Button-1>',  (lambda event: self.update_rx_e_list()))
        #
        # the entry box, which is read by pressing either "exclude_b" or "include_b"
        self.exclude_e = ttk.Combobox(self.button_3_frame,  font=('',9,'bold'), width=20)
        self.exclude_e.grid(row = 1, column = 0, columnspan = 2, pady=2, padx=3, sticky = W)
        #self.exclude_e.bind( '<Return>', (lambda event: self.exclude_b.invoke()))
        
        
        # Button to send the command that will remove the RX ID from the exclude_list at the server. The command gets the current
        # text from the entry box and appends it to "DEL;" for passing via send_command()
        self.include_b = Button(self.button_3_frame, text = "RX Include", fg='white',bg='#6699cc', command = lambda: poll_cmd("DEL;"+self.include_e.get()))
        self.include_b.grid(row = 2, column = 2, pady=2, padx=3, sticky = W+E)
        self.include_b.bind('<Button-1>',  (lambda event: self.update_rx_i_list()))
        
        self.include_e = ttk.Combobox(self.button_3_frame, font=('',9,'bold'), width=20)
        self.include_e.grid(row = 2, column = 0, columnspan = 2, pady=2, padx=3, sticky = W)
   
    def cleanup_on_exit(self):
        """Needed to shutdown the polling thread."""
        #print 'Window closed. Cleaning up and quitting'
        self.poll_thread_stop_event.set()
        self.log_thread_stop_event.set()
        
        root.quit() #Allow the rest of the quit process to continue
    
    def cleanup_on_disconnect(self):
        """Needed to shutdown the polling thread."""
        #print 'Window closed. Cleaning up and quitting'
        #print "In cleanup on disconnect ()\n\r"
        self.poll_thread_stop_event.set()
        self.log_thread_stop_event.set()
        
        root.quit()
        
    def tx_on(self):
        self.tx_state.state = self.tx_state.get()
        if self.tx_state.state:
            poll_cmd("TXON")
        else:
            poll_cmd("TXOFF")
    
    # functions to trigger commands to the server to add or remove frequencies from the 
    # frequency_allowed list - one per band.
    # clicking to turn a freq. checkbutton ON or OFF triggers the relevant
    # function below. 
    def sel_2(self):
        # we know the status has changed - we get the new status from the associated variable.
        self.sel2.state = self.sel2.get()
        if self.sel2.state: # cb is ON - we add the freq to the server's allowed list
            poll_cmd("ADDFREQ;1996.7")
        else: # otherwise cb is OFF - we delete the freq from the server's allowed list
            poll_cmd("DELFREQ;1996.7")
            
    def sel_4(self):
        self.sel4.state = self.sel4.get()
        if self.sel4.state:
            poll_cmd("ADDFREQ;3619.7")
        else:   
            poll_cmd("DELFREQ;3619.7")    
    def sel_6(self):
        self.sel6.state = self.sel6.get()
        if self.sel6.state:
            poll_cmd("ADDFREQ;5373.2")
        else:   
            poll_cmd("DELFREQ;5373.2")       
        
    def sel_8(self):
        self.sel8.state = self.sel8.get()
        if self.sel8.state:
            poll_cmd("ADDFREQ;7103.7")
        else:   
            poll_cmd("DELFREQ;7103.7")
            
    def sel_12(self):
        self.sel12.state = self.sel12.get()
        if self.sel12.state:
            poll_cmd("ADDFREQ;10147.2")
        else:   
            poll_cmd("DELFREQ;10147.2") 
     
    def sel_16(self):
        self.sel16.state = self.sel16.get()
        if self.sel16.state:
            poll_cmd("ADDFREQ;14347.7")
        else:   
            poll_cmd("DELFREQ;14347.7") 
            
    
    def log_poll(self):
       
        if self.log_queue.qsize():
            
            self.log_reply = self.log_queue.get()
            self.log_list = self.log_reply.split("~")
            self.sys_log = self.log_list[0]
            self.rxtx_log = self.log_list[1]
            
            self.sys_term.tag_config("ADMIN", foreground="darkgreen")
            self.sys_term.tag_config("RX", foreground="blue")
            self.sys_term.tag_config("TX", foreground='#b50414')
            self.sys_term.tag_config("CK", foreground='gray30')
            self.sys_term.config(state='normal')
            first, last = self.sys_term.yview()
            self.sys_term.delete(0.0, END)
            for line in self.sys_log.split("\n"):
                if "Admin;" in line:
                    tags = ("ADMIN", )
                elif "Received" in line:
                    tags = ("RX", ) 
                elif "Transmit" in line: 
                    tags = ("TX", ) 
                elif "Checklog" in line:
                    tags = ("CK", )
                else:
                    tags = None
                self.sys_term.insert(END, line+"\n", tags)
            
            self.sys_term.yview_moveto(first)
            self.sys_term.config(state='disabled')
            #self.sys_term.yview(END)
            
            self.rxtx_term.tag_config("TX", foreground='#b50414')
            self.rxtx_term.tag_config("RX", foreground='blue')
            self.rxtx_term.tag_config("CK", foreground='gray30')
            self.rxtx_term.config(state='normal')
            first, last = self.rxtx_term.yview()
            self.rxtx_term.delete(0.0, END)
            for line in self.rxtx_log.split('\n'):
                if "; TX1" in line:
                    tags = ("TX", ) 
                elif "; CK" in line:
                    tags  = ("CK",)
                elif "; RX" in line:
                    tags  = ("RX",)
                else:
                    tags = None

                self.rxtx_term.insert(END, line+"\n", tags)
            
            self.rxtx_term.yview_moveto(first)   
            #self.rxtx_term.yview(END)
            self.rxtx_term.config(state='disabled')
            self.get_motd()
            
            
        self._poll_job_id = self.master.after(self.poll_interval * 5, self.log_poll)  
        
    def status_poll(self):
        self.timenow = time.strftime("%H:%M:%S", time.gmtime(time.time()))
        self.datenow = time.strftime("%A %d %B %Y", time.gmtime(time.time()))
        root.title("GM4SLV DSC Coast Station Client " + version + "         "+self.datenow+"  "+self.timenow+" UTC ")
        if self.status_queue.qsize():
            self.status_reply = self.status_queue.get()

            self.status_list = self.status_reply.split("~")

            if len(self.status_list) != 9:
                self.status_list=["Not Connected", "Not Connected", "Not Connected","Not Connected","Not Connected","Not Connected","Not Connected","Not Connected","Not Connected"]
            self.online = self.status_list[0]

            if re.search("online", self.online):     # check for the presence of "online" in the reply string
                self.l_reply1.configure(fg = 'darkgreen')   # set the status label text colour

            else:  # otherwise we can't reach the server.
                self.l_reply1.configure(fg = '#b50414')     # set the status label text colour
                try:
                    #print "in status_poll() going to make_con()"
                    self.recon = self.make_con()
                    if self.recon:
                        self.online = "online - reconnected - waiting for refresh"
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
                self.l_reply2.configure(fg = '#b50414') # set the status label colour
            
            self.snargate_reply2.set(self.txstate)
            
            ############
            #          
            self.ptt_state = self.status_list[2]
            
            if self.ptt_state == "PTT ON":
                self.l_reply3.configure(fg = '#b50414')
            else:
                self.l_reply3.configure(fg = 'darkgreen')
                
            self.snargate_reply3.set(self.ptt_state)
            
            #############
            #
            self.lastrx = self.status_list[3]
            self.l_reply4.configure(fg = 'blue')        
            self.snargate_reply4.set("Last RX: "+self.lastrx)
            
            self.lasttx = self.status_list[4]
            self.l_reply5.configure(fg = '#b50414')        
            self.snargate_reply5.set("Last TX: "+self.lasttx)

            self.message_count = self.status_list[5]
            self.snargate_reply6.set(self.message_count)

            self.perband = self.status_list[6]
            self.snargate_reply7.set(self.perband)
            
            self.freq_list = self.status_list[7]

            # test for the presence of each frequency in the list and select/deselect each checkbutton as necessary
            if "1996.7" in self.freq_list:
                self.cb_2.select()
            else:
                self.cb_2.deselect()
            
            if "3619.7" in self.freq_list:
                self.cb_4.select()
            else:
                self.cb_4.deselect()
           
            if "5373.2" in self.freq_list:
                self.cb_6.select()
            else:
                self.cb_6.deselect()

            if "7103.7" in self.freq_list:
                self.cb_8.select()
            else:
                self.cb_8.deselect()
            
            if "10147.2" in self.freq_list:
                self.cb_12.select()
            else:
                self.cb_12.deselect()
            
            if "14347.7" in self.freq_list:
                self.cb_16.select()
            else:
                self.cb_16.deselect()
            
            self.excluded_rx = self.status_list[8]
            self.snargate_reply9.set(self.excluded_rx)
            
        self._poll_job_id = self.master.after(self.poll_interval, self.status_poll)

def poll_cmd(cmd):
    global token
    if cmd.split(";")[0] == "ADD":
        app.exclude_e.delete(0, 'end')
        
    if cmd.split(";")[0] == "DEL": 
        app.include_e.delete(0, 'end')

    header = "ADMIN"            # All commands are prefixed with "ADMIN"
    sendcommand = header+";"+cmd+";"+version+";"+token     # build the command string - a ";" delimited string with ID as the last element

    try:
        received = n1.connect(sendcommand)      # send the command and read the returned data
        return received
    except:
        #print "no reply \r\n"
        app.cleanup_on_disconnect()
        return "Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected~Not Connected"
        
def log_thread(q, stop_event):
    while(not stop_event.is_set()):
        time.sleep(0.2)
        if q.empty():
            #print "in poll log"
            q_text=poll_cmd("GETADMINSQL")+"~"+poll_cmd("GETRXTXSQL")        
            q.put(q_text)

            
def status_thread(q, stop_event):

    while(not stop_event.is_set()):
        time.sleep(0.2)
        if q.empty():
            #print "in poll status"
            q_text=poll_cmd("POLLSTATUS")
            q.put(q_text)

if __name__ == '__main__':
    root = Tk()
    
    lock = threading.Lock()
    root.geometry("+10+10")
    root.resizable(0, 0)

    n1 = Network()
    app = Application(root)
 
    # start the GUI
    root.mainloop()
