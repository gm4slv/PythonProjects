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
    
PORT =  50669

version = "v2.0c"

def make_con():
    global sock
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

def challenge_client(user, random, salt, client_password):
    global token
    # ask the user for the plaintext password
    # this is the only place it ever exists
    #client_password = getpass.getpass()
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
    reply = connect("reply %s %s" % (client_value, version))
    print reply
    
    try:
        token = connect("alive")
        if token=="pong" or token =="":
            sock.close()
            sys.exit(0)
        print "got session token ", token
    except:
        sock.close()
        sys.exit(0)
    
    if "Try again" not in reply: 
        #token = sock.recv(512)
        motd = connect("ADMIN;MOTD;"+version+";"+token)
        print motd
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
    #global password
    #print "we can send stuff to the server now"
    command = raw_input("Command: ")
    #print command
    if command == "q":
        sock.close()
        sys.exit(0)
        
    elif command == "passwd":
        current_password = getpass.getpass("Current Password : ")
        random, salt = connect("ADMIN;VERIFY;"+version+";"+token).split(":")
        current_hash = hashlib.sha256(salt + current_password).hexdigest()
        current_value = hashlib.sha256(random + current_hash).hexdigest()
        verify_reply = connect("ADMIN;CHECK;"+current_value+";"+version+";"+token)
        if verify_reply == "verified":
            new_password = getpass.getpass("New Password : ")
            check_new = getpass.getpass("Re-enter New Password : ")
            if check_new == new_password:
                new_salt = os.urandom(32).encode('hex')
                new_pass_hash = hashlib.sha256( new_salt + new_password).hexdigest()
                update_password = connect("ADMIN;UPDATEPW;"+new_salt+";"+new_pass_hash+";"+version+";"+token)
                print update_password

            else:
                print "Passwords don't match"
        else:
            print "Incorrect password"        
    else:
        #while True:
        reply = connect("ADMIN;"+command+";"+version+";"+token)
            
        print reply
            #time.sleep(10)
            
        
    commands()
    
def prompt():
    print "prompt"
    
def start():
    global username
    #global password
    #data = raw_input(" " ).lower().strip()
    
    
    username = raw_input('Username: ' )
    if not username:
        username = raw_input('Username: ' )
        # send the username with the keyword "login" and read the server's reply
        # which will be a string "username:random-challenge:salt"
    password = getpass.getpass('Password: ')
    reply = connect("login %s" % username)
    print reply
    
    try:
        random, salt = reply.split(":")
    except:
        print reply
        #sys.exit(0)
        # split the reply into three variables
        # and pass them to the challenge calculator
    
    challenge_client(username, random, salt, password)
      
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
        received = sock.recv(8192)
        
    finally:
        lock.release()

    return received


make_con()

lock = threading.Lock()

prompt()
start()
