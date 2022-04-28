import hashlib
import json

import os

try:
    pw_file = open('passwd.txt')
    user_dict = json.load(pw_file)
except:
    user_dict = {}

    

def add_user():
    setupusername = raw_input('Username :')
    setuppassword = raw_input('Password :')
    #salt = hashlib.md5(setupusername).hexdigest()
    #salt = uuid.uuid4().hex
    salt = os.urandom(32).encode('hex')
    #salt = "qweqweqwslkdsj  sddkj slkj lks ksdjflwjlwkej lkjdsflk lkef ksdlkjfalkaslkasjlksjdf   jslkfj "
    
    setup_pass_hash = hashlib.sha256( salt + setuppassword).hexdigest()

    user_dict[setupusername] = salt+":"+setup_pass_hash
    with open('passwd.txt', 'wb') as outfile:
        json.dump(user_dict, outfile)
        
    print user_dict
    again = raw_input('Another User? ')
    if again == "y":
        add_user()
    else:
        print "goodbye"
        return
    
    
    
        
add_user()