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

import smtplib
from email.MIMEText import MIMEText
text_subtype = 'plain'

def send_email(content):
    SERVER = "192.168.21.20"

    FROM = "gm4slv@gm4slv.org"
    TO = ["john@wire2waves.co.uk"] # must be a list
    
    msg = MIMEText(content, text_subtype)
    msg['Subject']= "Coast Station Alert"
    msg['From']   = FROM # some SMTP servers will do this automatically, not all

    
    
    
   

    # Send the mail

    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
    

