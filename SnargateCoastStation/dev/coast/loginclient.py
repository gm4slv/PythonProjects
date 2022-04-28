__author__ = 'gm4slv'

# # v0.23

import socket
import hashlib
import getpass
import os
import sys

try:
    import readline
except ImportError:
    pass

import threading
import time

#print sys.argv

try:
    HOST = sys.argv[1]
except:
    HOST = "127.0.0.1"
    
PORT =  9999

def make_con():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

def challenge_client(user, random, salt):
    global token
    # ask the user for the plaintext password
    # this is the only place it ever exists
    client_password = getpass.getpass()
    # use the provided salt from the server and the user's password
    # to create the user's "salted password hash" which should match
    # the hash held in the server password file
    client_hash = hashlib.sha256(salt + client_password).hexdigest()
    #print "client_hash ", client_hash
    # use the salted password hash to calculate the challenge response
    # by hashing the provided random number and password hash
    client_value = hashlib.sha256(random + client_hash).hexdigest()
    #print "client_value ", client_value
    # send back the username and challenge result to the server
    reply = connect("reply %s" % (client_value))
    print reply
    
    try:
        token = connect("alive")
        if token=="":
            sock.close()
            sys.exit(0)
        #print "got session token ", token
    except:
        sock.close()
        sys.exit(0)
    
    if "Try again" not in reply: 
        #token = sock.recv(512)
        
        commands()
        
    else: 
        start()
    #if "incorrect" in reply:
    #    sock.close()
    #    quit(0)
        #make_con()
        #start()
        
    # the reply will be "success of fail" for the login process
    # depending on the match of challenge hashes
    #print reply
    
def commands():
    global token
    global username
    #print "we can send stuff to the server now"
    command = raw_input("Command: ")
    #print command
    if command == "q":
        sock.close()
        sys.exit(0)
        
        
    elif command == "passwd":
        reply = connect("verify "+token)
        try:
            random, salt = reply.split(":")
        except:
            quit(0)
        #print salt
        #print random
        oldpass = getpass.getpass("Current Password: ")
        oldpw_hash = hashlib.sha256(salt + oldpass).hexdigest()
        oldpwchallenge_value = hashlib.sha256(random + oldpw_hash).hexdigest()
        verify_old = connect("check %s %s" % (token, oldpwchallenge_value))
        if verify_old == "passok":
            print "Password ok"
            new_pass = getpass.getpass("New Password: ")
            while len(new_pass) < 8:
                print "Minimum of 8 characters please!"
                new_pass = getpass.getpass("New Password: ")
            
            salt = os.urandom(32).encode('hex')
            hash = hashlib.sha256(salt + new_pass).hexdigest()
            check = getpass.getpass("Re-enter new password: ")
            check_hash = hashlib.sha256(salt + check).hexdigest()
     
            if check_hash == hash:
                print "passwords ok, sending to server"
                reply = connect("new_pass "+token+" "+username+" "+salt+" "+hash)
                print reply
                # get new token
                
            else:
                print "Passwords do not match."
                commands()
        else:
            print "Password incorrect"
    else:
        #print "sending %s " % "command "+token+" "+command
        reply = connect("command "+token+" "+command)
        print reply
        
    commands()
    
def prompt():
    motd = sock.recv(1024)
    print motd
    print ""

def start():
    global username
    #data = raw_input(" " ).lower().strip()
    
    
    username = raw_input('Username: ' )
    if not username:
        username = raw_input('Username: ' )
        # send the username with the keyword "login" and read the server's reply
        # which will be a string "username:random-challenge:salt"
    reply = connect("login %s" % username)
    try:
        random, salt = reply.split(":")
    except:
        sys.exit(0)
        # split the reply into three variables
        # and pass them to the challenge calculator
    challenge_client(username, random, salt)
        
    #elif data == "q":
    ##    sock.close()
    #    quit(0)
        #reply = connect("quit" + "\n")
        
        
    


# Try to send and receive in one-go, to prevent the logging thread and the main prog
# getting the wrong receive data

def connect(data):
    try:
        lock.acquire()
        global sock
        sock.sendall(data + "\n")
        received = sock.recv(2048)
    
    finally:
        lock.release()

    return received


make_con()

lock = threading.Lock()

prompt()
start()
