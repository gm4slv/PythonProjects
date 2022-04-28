'''
Python TCP Server for Icom IC-M710 Marine HF SSB Transceiver

    Copyright (C) 2016  John Pumford-Green

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

from m710 import *
import SocketServer
import time
version = "v1.0"

try:
    import readline
except:
    pass

lock = threading.Lock()

radios = []

# Name of Radio to be controlled
name = "IC-M710"

# Create an instance of the M710 Radio object 
r1 = m710(name)

# Add the new radio to the list of available radios
# in this case there will only be one - this is a hang-over 
# from the older multi-radio server
radios.append(name)


print radios


def list_radios():
    radiolist = ""
    for n in range(0, len(radios)):
        r = radios[n]
        radiolist += (r + " ")
    return radiolist


def write_file(text):
    filename = 'commandlog.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
    log = " ".join((timenow, text))  # make an entry for the log by joining the timestamp with the text passed in
    f.write(log)
    f.close()


def write_con(text):
    filename = 'conlog.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
    log = " ".join((timenow, text))  # make an entry for the log by joining the timestamp with the text passed in
    f.write(log)
    f.close()


# The Server
class ThreadedRequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        # we find the current thread for the client connection just set up, to
        # use in the log file
        cur_thread = threading.currentThread()
        # log the new connection details
        write_con("Connect from %s using %s \n" % ((self.client_address[0]), cur_thread.getName()))
        # print to the server's console the new connection IP address/port
        print self.client_address
        # loop to handle client requests....
        while True:
            # using StreamRequestHandler means our input from the client
            # is  "file-like" and can be read with "file-like" commands
            # we read a line at a time, using readline()
            cmd = self.rfile.readline().lower()
            # to keep things clean, we remove any characters that aren't
            # "printable" simple ASCII
            # these are between 32 and 127 in the ASCII table
            # we look at each character, and then make a new word by
            # .join()ing each accepted character with no space in between
            asccmd = "".join(x for x in cmd if ord(x) < 128 and ord(x) > 31)
            # we make a list called "words" holding the received words which
            # will be inspected by various functions
            words = asccmd.split()
            # If a client uses sock.close() itself, to disconnect, it appears that
            # we read a continuous stream of "" on the dead
            # socket, which puts CPU to 100%.
            #
            # The "While" loop is probably responsible, but I can't see another
            # way to keep the connection up for multiple commands.
            #
            # Further connection are accepted due to the Threaded nature of the server.
            # The CPU load is unacceptable though
            # HACK ?>>>>>
            # Looking for "" and then breaking
            # the connection from the server end (even though the client has
            # gone) cures this.
            if cmd == "":
                break
            else:
                pass
            # if the words list is empty, go back and get more input
            if not words:
                continue
            # we have input....
            # filter based on the first word - these are the
            # pre-set commands the server will accept
            # the client wants to know the currently available
            # radio names - held in the variable "rnames"
            elif words[0] == "getnames":
                self.wfile.write(rnames)
            # words[-1] (the last word in the list) will always be the
            # radio name. We give the variable "my_radio" this value, for
            # identifying which radio object to apply the method to
            
            elif words[0] == "remoteon":
                my_radio = eval(words[-1])
                remote = my_radio.remote_on()
                self.wfile.write(remote)
            elif words[0] == "remoteoff":
                my_radio = eval(words[-1])
                remote = my_radio.remote_off()
                self.wfile.write(remote)
            
            elif words[0] == "tune":
                my_radio = eval(words[-1])
                tune = my_radio.tune()
                self.wfile.write(tune)
                timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
                print timenow + " : " + self.client_address[0] + " : " + tune

            elif words[0] == "dimon":
                my_radio = eval(words[-1])
                dim = my_radio.dim_on()
                self.wfile.write(dim)
            elif words[0] == "dimoff":
                my_radio = eval(words[-1])
                dim = my_radio.dim_off()
                self.wfile.write(dim)

            elif words[0] == "spon":
                my_radio = eval(words[-1])
                speaker = my_radio.speaker_on()
                self.wfile.write(speaker)
            elif words[0] == "spoff":
                my_radio = eval(words[-1])
                speaker = my_radio.speaker_off()
                self.wfile.write(speaker)

            elif words[0] == "getfreq":
                my_radio = eval(words[-1])
                freq = words[1]
                freq = my_radio.get_freq()
                self.wfile.write(freq)
            elif words[0] == "setfreq":
                my_radio = eval(words[-1])
                freq = float(words[1])
                newfreq = my_radio.set_freq(freq)
                self.wfile.write(newfreq)
                timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
                print timenow + " : " + self.client_address[0] + " : New Freq : %s " % newfreq

            elif words[0] == "getmode":
                my_radio = eval(words[-1])
                mode = my_radio.get_mode()
                self.wfile.write(mode)
            elif words[0] == "setmode":
                my_radio = eval(words[-1])
                mode = words[1]
                newmode = my_radio.set_mode(mode)
                self.wfile.write(newmode)
                timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
                print timenow + " : " + self.client_address[0] + " : New Mode : %s " % newmode
            
            elif words[0] == "getsmeter":
                my_radio = eval(words[-1])
                smeter = my_radio.get_smeter()                
                self.wfile.write(smeter)
            
            elif words[0] == "quit":
                write_con("Got quit from {}\n".format(self.client_address[0]))  # log it
                self.wfile.write("Goodbye! \r\n")  # say Goodbye
                break
            else:  # nothing in words[0] matches a pre-set command....
                write_file("Received %s\n" % words)  # log it, it's unusual
                self.wfile.write("Command not recognized\r\n")  # inform the client


class ThreadedIcomServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == '__main__':
    # define the lock to be used on the serial port access
    lock = threading.Lock()

    # address ('' = all available interfaces) to listen on, and port number
    address = ('', 9710)
    server = ThreadedIcomServer(address, ThreadedRequestHandler)
    server.allow_reuse_address = True


    # define that the server will be threaded, and will serve "forever" ie. not quit after the client disconnects
    t = threading.Thread(target=server.serve_forever)
    # start the server thread
    t.start()

    write_con(
        "Server loop running in thread: %s\n" % "".join(t.getName())) 

