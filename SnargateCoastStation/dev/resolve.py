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
# This provides the lookup of ship MMSI via aprs.fi for the Coast Station Server in order to log
# vessels' name and callsign
#


import json
import urllib
import urllib2
import re
import time
import datetime


##################
#
# Log activity to a simple log file
#

def write_resolve_log(text):
    filename = 'reslog.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    id = "RESOLVER"
    log = ";".join((timenow, id))
    entry = ";".join((log, text))
    f.write(entry+'\r\n')
    f.close()

##################
#
# resolve_aprs() is called from the server, passing a 9-digit MMSI
# the function returns a list containing [name, call, ais_time, lat, lng]
# if the MMSI is not found the function returns None
#
## For production use I suspect we will need to find an alternative
# source of resolving MMSI>Name. 
# The ITU and Marine Traffic functions currently in YaDDNet could be incorporated
# It would also be possible to use YaDDNet itself.
#           
def resolve_aprs(mmsi):
        # the URL has a personal API Key and the mmsi variable
        # the request returns a json array with the information
        #
        url = "http://api.aprs.fi/api/get?apikey=49022.741rOwWQ5ato0Y&name="+mmsi+"&what=loc&format=json"
        
        # create an encoded URL to send from the supplied url
        req = urllib2.Request(url)
        
        # add a "User-agent" header as requested by the owner of aprs.fi
        # which indicates where/why/how his data is being used
        ####### consider changing this header to reflect the use within the Coast Station project ######
        
        
        req.add_header('User-agent', 'YaDDNet DSC (+http://gm4slv.plus.com:8000)')
        
        # delay each lookup to prevent overloading the API - this may not be needed for Coast Station project
        # as there will only be very few calls per day. 
        
        time.sleep(1)
        
        # Log it...
        write_resolve_log("")
        write_resolve_log("Looking up %s at aprs.fi" % mmsi)
        
        # get the reply from the internet
        response = urllib2.urlopen(req)

        # the reply is a json array
        # the Python json module converts this into a dictionary "data" which can be inspected to select the
        # required information
        data = json.loads(response.read())
        
        #  Our info is in the "value" of the key "entries"
        # this is another dictionary we'll call "entry".
        # The "entry" dictionary has key:value pairs for name, call, lat, long etc.
        try:
            # we aren't sure the json response has the necessary dictionary key "entries"
            # If aprs.fi decides to throttle our data it will not return a "entries" key/value
            entry =  data['entries']
        except:
            # we've been throttled 
            write_resolve_log("aprs.fi Exception in entry = data[] for %s" % mmsi)
            
            if response is not None:
                write_resolve_log("aprs.fi replied no")
                
            # APRS.FI has refused to provide data 
            # return "None" to the calling function
            return None
            
        try:
            # parse the json-derived dictionary to extract "name", "mmsi" (although we know this already)
            # lat, long and "last postition time"
            
            # the first item in the "entry" list is a dictionary called "station"
            # we can extract the values from keys in this dictionary
            station = entry[0]
            # remove commas from names (used in YaDDNet, not really needed here)
            name = station['name'].replace(',', '').strip()
            
            # we can use the returned MMSI, although we know it already, we asked for it....
            mmsi = station['mmsi']
            
            # the callsign of the vessel
            call = station['srccall']
            
            # the time (in UNIX Timestamp format) of the last recorded position in APRS.FI (this 
            # is usually older than the up to date position information available at Marine Traffic.
            lasttime = station['lasttime']
            
            # The last reported Lat and Long.
            lat = station['lat']
            lng = station['lng']
            
            # Convert the UNIX timestamp to UTC in the standard format
            ais_time = datetime.datetime.utcfromtimestamp(int(lasttime)).strftime('%Y-%m-%d %H:%M:%S')
            
            # send back a list with the requested information
            return [name, call, ais_time, lat, lng]
        
        # although we got a json reply, it doesn't contain the name/call etc.
        # we will send back "None" 
        except:
            # Log it...
            write_resolve_log("Not found at aprs.fi: %s" % mmsi)
           
            return None

            

 
  