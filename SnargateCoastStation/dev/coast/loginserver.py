import json
import uuid
import hashlib
import threading
import SocketServer
import os

import time

valid_users = {}  
server_id = os.urandom(8).encode('hex')
  
# The Server.... still a bit vague...
class ThreadedRequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        try:
            pw_file = open('passwd.txt')
            self.user_dict = json.load(pw_file)
        except:
            self.user_dict = {}

        # we find the current thread for the client connection just set up, to
        # use in the log file
        cur_thread = threading.currentThread()
        # log the new connection details
        print "request ", self.request
        print "socket", server.socket
        
        # print to the server's console the new connection IP address/port
        print self.client_address
        
        self.count = 0
        self.wfile.write("This is a Private System.\r\nPlease disconnect if not authorized.\r\n\nOtherwise, enter your credentials at the prompts.\r\n")
        
        # loop to handle client requests....
        while True:

            # using StreamRequestHandler means our input from the client
            # is  "file-like" and can be read with "file-like" commands
            # we read a line at a time, using readline()
            
            # client_id is used to create individual session tokens for authenticated clients. 
            # using IP address & port to identify each client
            self.client_id = ":".join( str(x) for x in self.client_address)
            #print self.client_id
            
            cmd = self.rfile.readline().lower().rstrip()
            
            if not cmd:
                print "client %s gone" % self.client_id
                if self.client_id in valid_users:
                    del valid_users[self.client_id]
                print valid_users
                break

            words = cmd.split()

            if not words:
                continue


            # User wants to login - take username and send to server_login()
            # which handles creating the challenge
            if words[0] == "login":
                
                print "login"
                # words[1] is the provided username
                print "call login(%s)" % words[1]
                # send the username to "server_login" which 
                # then extracts the local copy
                # of the password hash, and its salt (not known to the 
                # client until we send it to them)
                self.username = words[1]        
                self.server_login(self.username)
            
            # the client sends back it's challenge response as words[1]
            elif words[0] == "reply":

                self.reply = words[1]
                
                # if user is known we get their pass-hash from the dictionary
                if self.username in self.user_dict:
                    self.secret = self.user_dict[self.username].split(":")[1]
                # otherwise we use an empty pass-hash
                else:
                    self.secret = ""
                
                # 
                self.valid = self.compare_results(self.reply, self.random, self.secret, self.username)
                
                if not self.valid:
                    print "count ", self.count
                    self.count += 1
                    if self.count == 3:
                        self.wfile.write("Too many attempts... goodbye")
                        break
                    
                    else:
                        self.wfile.write("Unsuccessful. Attempts used : %d. Try again..." % self.count)
            
         
                else:
                    self.count = 0
                    valid_users[self.client_id] = self.username
                    print valid_users
                    print "login ok"
                    self.token = hashlib.md5(server_id+self.client_id).hexdigest()
                    print "client session token ", self.token
                    self.wfile.write("Hello %s, Welcome to GM4SLV\r\n\nCommands:\r\nshow = list the connected users\r\npasswd = change password\r\nhelp = show the command list\r\nq = quit" % self.username)
            
            # after the login reply is received the client sends "alive" and gets
            # his session token (if login has been successful) or "yes" if he's trying again
            # this is used to force the client to die if we "break" due to excessive failures
            # he tries to revc() the "alive" reply and fails to recv, and quits
            # if he's been successful he gets his session token.
            
            elif words[0] == "alive":
                if hasattr(self, 'token'):
                    self.wfile.write(self.token)
                else:
                    self.wfile.write("yes")
                    
                    
            elif words[0] == "verify":
                self.c_token = words[1]
                
                self.check_token = hashlib.md5(server_id+self.client_id).hexdigest()
                
                    
                if self.c_token == self.check_token:
                    if self.username in self.user_dict:
        
                        self.salt = self.user_dict[self.username].split(":")[0]
            
                    else:
                        self.salt = os.urandom(32).encode('hex')
                
                    self.random = os.urandom(32).encode('hex')
       
                    self.wfile.write(self.random+":"+self.salt)
                
                else:
                    print "Invalid token in verify"
                    self.wfile.write("Invalid")
                    break
                
                
            elif words[0] == "check":
                self.c_token = words[1]
                
                self.check_token = hashlib.md5(server_id+self.client_id).hexdigest()
                
                self.oldchallenge = words[2]
                self.secret = self.user_dict[self.username].split(":")[1]
                
                if self.c_token == self.check_token:
                    print "checking old - token ok"
                    oldok = self.compare_results(self.oldchallenge, self.random, self.secret, self.username)
                    print "old password ", oldok
                    if oldok:
                        self.wfile.write("passok")
                    else:
                        self.wfile.write("fail")
                        
                else:
                    print "Invalid token in check"
                    self.wfile.write("Invalid")
                    break
                
            elif words[0] == "new_pass":
                self.c_token = words[1]
                
                self.check_token = hashlib.md5(server_id+self.client_id).hexdigest()
                
                print "new check ", self.check_token
                print "user token", self.c_token
                setupusername = words[2]
                salt = words[3]
                setup_pass_hash = words[4]
                print "user ", setupusername
                print "new salt ", salt
                print "new hash ", setup_pass_hash
                
                if self.c_token == self.check_token:
                    print "token ok"
                    self.user_dict[setupusername] = salt+":"+setup_pass_hash
                
                    with open('passwd.txt', 'wb') as outfile:
                        json.dump(self.user_dict, outfile)
                    self.wfile.write("Success : password updated")
                    

                else:
                    print "Invalid token in new_pass"
                    self.wfile.write("Invalid")
                    break
                    
            
            
            
            elif words[0] == "command": 
            
                self.c_token = words[1]
                
                self.check_token = hashlib.md5(server_id+self.client_id).hexdigest()
                
                print "new check ", self.check_token
                print "user token", self.c_token
             
                
                if len(words) > 2:
                    
                    
                    if words[2] == "show":
                        userlist = ""
                        
                        if self.c_token == self.check_token:
                            print "token verified"
                            for v,k in valid_users.items():
                                userlist += k+" : "+v+"\r\n"
                            self.wfile.write("\r\nLogged in users :\r\n%s" % (userlist))
                        else:
                            print "Invalid token in show"
                            self.wfile.write("Invalid")
                            break
                    
                    elif words[2] == "help":
                        if self.c_token == self.check_token:
                            print "token verified"
                            self.wfile.write("Commands:\r\nshow : list connected users\r\npasswd : change password\r\nhelp : this menu\r\nq : quit")
                        else:
                            print "Invalid token in help"
                            self.wfile.write("Invalid")
                            break
                            
                    else:
                   
                        print cmd
                        
                        if self.c_token == self.check_token:
                            print "token verified"
                            self.wfile.write("You said %s " % (" ".join(words[2:])))
                        else:
                            print "Invalid token in you-said.."
                            self.wfile.write(" Invalid")
                            time.sleep(1)
                            break
                else:
                    print cmd
                    
                    if self.c_token == self.check_token:
                        print "token verified"
                        self.wfile.write("empty command ")
                    else:
                        print "Invalid token in empty command"
                        self.wfile.write("Client Invalid")
                        time.sleep(1)
                        break
            else:
                if hasattr(self, 'username'):
                    self.check_token = hashlib.md5(server_id+self.client_id).hexdigest()
                else:
                    print "Invalid User - no username at the bottom of the list"
                    self.wfile.write("Client Invalid")
                    time.sleep(1)
                    break
                
    def server_login(self, server_username):
    
        if server_username in self.user_dict:
            self.salt = self.user_dict[server_username].split(":")[0]          
        else:
            self.salt = os.urandom(32).encode('hex')
              
        # make up the one-time random challenge
        self.random = os.urandom(32).encode('hex')
        
        
        # send the random-challenge and the user's salt
        self.wfile.write(self.random+":"+self.salt)
        

    
    def compare_results(self, reply, random, secret, username):
        server_value = hashlib.sha256(random + secret).hexdigest()
        client_value = reply
        print server_value
        print client_value
        if client_value == server_value:
            
            return True
        else:
            
            return False
        
    '''
    def challenge_client(self, random, salt):
        
        self.wfile.write(random+":"+salt)
        #client_password = raw_input('password')
        client_hash = hashlib.md5(salt + client_password).hexdigest()
        print "client_hash ", client_hash
        client_value = hashlib.md5(random + client_hash).hexdigest()
        print "client_value ", client_value
        return client_value
    '''

    
class ThreadedIcomServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == '__main__':
    # define the lock to be used on the serial port access
    lock = threading.Lock()

    # address ('' = all available interfaces) to listen on, and port number
    address = ('', 9999)
    server = ThreadedIcomServer(address, ThreadedRequestHandler)
    server.allow_reuse_address = True
    
    # define that the server will be threaded, and will serve "forever" ie. not quit after the client disconnects
    t = threading.Thread(target=server.serve_forever)
    #t.daemon = True
    
    t.start()

   
