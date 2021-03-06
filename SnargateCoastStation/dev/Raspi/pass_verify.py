import time
import hashlib
import os
import json



valid_users = {}
# server_login

def make_challenge(user):

    try:
        pw_file = open('passwd.txt')
        user_dict = json.load(pw_file)
    except:
        user_dict = {}
        
    if user in user_dict:
        salt = user_dict[user].split(":")[0]
    else:
        salt = os.urandom(32).encode('hex')
        
    random = os.urandom(32).encode('hex')
    challenge = random+":"+salt
    print "in make_challenge()\n\r %s %s" % (user, challenge)
    return (salt, challenge, random)  
    
    
def compare_challenge(user, reply, random):

    try:
        pw_file = open('passwd.txt')
        user_dict = json.load(pw_file)
    except:
        user_dict = {}
        
    try:
        secret = user_dict[user].split(":")[1]
    except:
        secret = ""
    server_value = hashlib.sha256(random + secret).hexdigest()
    client_value = reply
    
    if client_value == server_value:
        
        return True
    else:   
        return False

def login(server_id, client_id, user):

    my_token = make_token(server_id, client_id)
    
    valid_users[client_id]=user+":"+my_token
    
    return my_token


def make_token(server_id, client_id):

    token = hashlib.md5(server_id + client_id).hexdigest()
    return token
    
def check_token(server_token, token):
   
    if server_token == token:
        return True
    else:
        return False

def check_message(client_id, client_token):
  
    if client_id in valid_users:
        username = valid_users[client_id].split(":")[0]    
        server_token = valid_users[client_id].split(":")[1]
        tokenok = check_token(server_token,client_token )
        #print "Client valid"
        if tokenok:
            #print "token ok %s" % client_token
            return True#(username)
            #print "Token ok %s, user = %s" % (client_token,username)
        else:
            return False
            #print "Token mismatch for user %s" % username
    else:
        return False
        #print "Invalid client_id"

def updatepw(username, new_salt, new_pass_hash):
    try:
        pw_file = open('passwd.txt')
        user_dict = json.load(pw_file)
    except:
        user_dict = {}
        
    try:
        user_dict[username] = new_salt+":"+new_pass_hash
        
        with open('passwd.txt', 'wb') as outfile:
            json.dump(user_dict, outfile)
            
        return True
        
    except:
    
        return False
    
        
        
def logout(client_id):
    if client_id in valid_users:
        del valid_users[client_id]
        
def list_users():
    users_online = ""
    for k,v in valid_users.items():
        users_online += v.split(":")[0]+" ("+k+"), "
    return users_online