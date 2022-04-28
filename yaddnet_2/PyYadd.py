# development version for new Ship Resolution process

import re
#from new_coast_dict import *
#from mid_dict import *
import json #, pickle
from class_dict import *
import time
from resolve import *
import socket

import pysql

import sys

reload(sys)
sys.setdefaultencoding("windows-1252")


rx_not_for_snargate= ["KPC6NDB1", "KPC6NDB2", "KPC6NDB3", "KPC6NDB4", "KPC6NDB5", "KPC6NDB6", "Don"]

#specials_list = [ "219015591", "237673000", "237673100", "219055000", "228040600", "258999039", "235899980", "219000333", "258999189", "219000559", "219000022", "219016306", "219020185", "235899982", "258999089", "258999139", "258999209", "258999229" ]

def send_to_coast(data):
        
        HOST, PORT = "192.168.21.151", 50669
        #HOST1, PORT = "192.168.21.107", 50669
        # SOCK_DGRAM is the socket type to use for UDP sockets
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.bind(('',50661))
        # As you can see, there is no connect() call; UDP has no connections.
        # Instead, data is directly sent to the recipient via sendto().
        sock.sendto(data, (HOST, PORT))
        #sock.sendto(data, (HOST1, PORT))
	return

def send_to_mirror(data,port):

        host = "192.168.21.105"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (host, port))
        return


def make_dsc_call(dsc_message, line):
    print "+++++++++++++++++ IN PyYaDD"
    #write_file(line+"\r\n")
    raw_dsc_message = dsc_message
    dsc_list = line.split(';')
    #print dsc_list
    datetime = dsc_list[0]
    rx_id = dsc_list[1]
    rx_freq = dsc_list[2]
    fmt = dsc_list[3]
    to_mmsi_raw = dsc_list[4]
    cat = dsc_list[5]
    from_mmsi_raw = dsc_list[6]
    tc1 = dsc_list[7]
    tc2 = dsc_list[8]
    freq = dsc_list[9]
    pos = dsc_list[10]
    eos = dsc_list[11]
    ecc = dsc_list[12].split()[-1]
    to_mmsi_list = to_mmsi_raw.split(',')
    from_mmsi_list = from_mmsi_raw.split(',')
    
    ######
    # Bridge to Coast Station Server - only send "SEL" messages, exclude certain receivers
    #
    # UPDATE 25/7/15 : filter and send only messages to/from Snargate 002320204 to reduce traffic
    # once Snargate is remotely sited.
    #
    if ecc == "OK":
    
        if any("~" in s for s in dsc_list):
                print "Parity Error..."
        else:
            if fmt == "SEL":

                ufrom = from_mmsi_list[1]
                uto = to_mmsi_list[1]
        
                
        
                if rx_id not in rx_not_for_snargate:
                    if (uto == "002320204" or ufrom == "002320204"):
                        udp_message = rx_id+";"+rx_freq+";"+fmt+";"+uto+";"+cat+";"+ufrom+";"+tc1+";"+tc2+";"+freq+";"+pos+";"+eos+";"+ecc
                        send_to_coast(udp_message)
    
              
    
            
    # Deal with special cases
    
    if to_mmsi_list[0] == "SHIP": 
        print "TESTING FOR SPECIALS in TO..........................." 
        
        to_special_name = pysql.check_special(to_mmsi_list[1])
        
        if to_special_name != None:
        #if to_mmsi_list[1] in specials_list:
            to_mmsi_list[0] = "COAST"
            pysql.load_logger("LOGGER", "Found a special: %s" % to_mmsi_list[1])
        else:
            pass


    if from_mmsi_list[0] == "SHIP":
        print "TESTING FOR SPECIALS in FROM.........................."
        
        from_special_name = pysql.check_special(from_mmsi_list[1])

        if from_special_name != None:
        #if from_mmsi_list[1] in specials_list:
            from_mmsi_list[0] = "COAST"
            pysql.load_logger("LOGGER", "Found a special: %s" % from_mmsi_list[1])
        else:
            pass

        '''
        # Sailor Examiner            
        if to_mmsi_list[1] == "219015591":     
            to_mmsi_list[0] = "COAST"
            pysql.load_logger("LOGGER", "Found Sailor Examiner")
        # Piraeus    
        if to_mmsi_list[1] == "237673000":       
            to_mmsi_list[0] = "COAST"
            pysql.load_logger("LOGGER", "Found Piraeus")
        # Skagen Skipperskole            
        if to_mmsi_list[1] == "219055000":     
            to_mmsi_list[0] = "COAST"
            pysql.load_logger("LOGGER", "Found Skagen Skipperskole")
            
    if from_mmsi_list[0] == "SHIP":
        print "TESTING FOR SPECIALS in FROM..........................."     
        if from_mmsi_list[1] == "219015591":
            from_mmsi_list[0] = "COAST"
            pysql.load_logger("LOGGER", "Found Sailor Examiner")            
        # Pireaus             
        if from_mmsi_list[1] == "237673000":
            from_mmsi_list[0] = "COAST"   
            pysql.load_logger("LOGGER", "Found Piraeus")
        '''
        
    if to_mmsi_list[0] == "COAST":
        print "Testing for 000000000 in TO"
        if to_mmsi_list[1] == "000000000":       
            to_mmsi_list[0] = "SHIP"
        
    if from_mmsi_list[0] == "COAST":
        print "Testing for 000000000 in FROM"
        if from_mmsi_list[1] == "000000000":       
            from_mmsi_list[0] = "SHIP"
            
    else:
        pass
        
    #if len(to_mmsi_list[1]) != 9:
    #   write_log("Illegal TO MMSI Length: %s" % to_mmsi_list[1])
    #	pysql.load_logger("PyYadd","Illegal TO MMSI Length: %s" % to_mmsi_list[1])
    #    nul = "nul"
    #    return nul
    #if len(from_mmsi_list[1]) != 9:
    #    pysql.load_logger("PyYadd", "Illegal FROM MMSI Length: %s" % from_mmsi_list[1])
    #    nul = "nul"
     #   return nul
    ###
    
    ###
    ## TO TO TO TO TO 
    ##
    if to_mmsi_list[0] == "COAST":
        print "We have coast"
        to_mmsi = to_mmsi_list[1]
        print "Coast TO MMSI: ", to_mmsi
        to_type = "COAST" 
        raw_to_mmsi = to_mmsi
            
        try:
            name = pysql.check_coast(to_mmsi)
            ############################
            # COAST STATION LOOKUP HERE
            ############################
            #name = new_coast_dict[to_mmsi]
            ############################
            # CHANGE TO SQL QUERY 
            #
            # name = pysql.check_coast(to_mmsi)
            #
            # What happens if not found?
            # at the moment the TRY/EXCEPT handles
            # failure to find in the DICTIONARY
            # Need to think about an if/else for handling return from pysql.check_coast()
            #
            ############################
            if not name:
                name = "Not Found"
            else:
                pass
            print "TO Name : ", name
            
            #if to_mmsi in specials_list:
            
            if pysql.check_special(to_mmsi) != None:

            #if to_mmsi == "219015591" or to_mmsi == "237673000" or to_mmsi == "219055000":
                mid = to_mmsi[0:3]
            else:              
                mid = to_mmsi[2:5]
            print "TO mid ", mid
            
            ctry = pysql.check_mid(mid)
            if not ctry:
                ctry = "UNK"
            else:
                pass

            ###########################
            # MID to COUNTRY CONVERSION HERE
            ###########################
            #ctry = mid_dict[mid]
            ###########################
            # CHANGE TO SQL QUERY
            ###########################


            ### for newlog
            to_mid = mid
            to_ctry = ctry
            to_name = name

            to_newlog = to_mmsi
            #to_mmsi = "<font color=green>COAST %s</font><br>%s<br>%s" % (to_mmsi, name, ctry)
            #to_mmsi2 = "<font color=green>COAST %s</font><br>%s<br>%s" % (to_newlog, name, ctry)

            #print "resolved to mmsi " ,to_mmsi
        except:
            pysql.load_logger("PyYaDD", "Exception in TO COAST : %s" % raw_dsc_message)
            try:
                mid = to_mmsi[2:5]
                
                
                ctry = pysql.check_mid(mid)
                if not ctry:
                    ctry = "UNK"
                else:
                    pass
                
                ###########################
                # MID TO COUNTRY CONVERSION HERE
                ###########################
                #ctry = mid_dict[mid]
                ###########################
                # CHANGE TO SQL QUERY
                ###########################

                ### for newlog
                to_mid = mid
                to_ctry = ctry
                to_name = "UNID"

                to_newlog = to_mmsi
                #to_mmsi = "<font color=green>COAST %s</font><br>UNID<br>%s" % (to_mmsi, ctry)
                #to_mmsi2 = "<font color=green>COAST %s</font><br>UNID<br>%s" % (to_newlog, ctry)
                #print "UNID TO MMSI :" ,to_mmsi
            except:
                ### for newlog
                to_mid = "UNK"
                to_ctry = "UNK"
                to_name = "UNID"

                to_newlog = to_mmsi
                #to_mmsi = "COAST, %s, UNID" % to_mmsi
                #to_mmsi2 = "COAST, %s, UNID" % to_mmsi
                #print "last resort to mmsi ", to_mmsi
                
       
            
    elif to_mmsi_list[0] == "SHIP":
        to_mmsi = to_mmsi_list[1]
        to_type = "SHIP"
        raw_to_mmsi = to_mmsi
        #print "To MMSI", to_mmsi
        if "~" not in to_mmsi and to_mmsi[0] != "0":
            #print "no parity errors"
            to_name_call = resolve_mmsi(to_mmsi)
            print "Name", to_name_call
            #write_log("To Ship  : %s" % name_call)
        else:
            to_name_call = to_mmsi
        try:
            mid = to_mmsi[0:3]
            #print mid
            
            ctry = pysql.check_mid(mid)
            if not ctry:
                ctry = "UNK"
            else:
                pass

            ##############################
            # MID TO COUNTRY CONVERSION HERE
            ##############################
            #ctry = mid_dict[mid]
            ##############################
            # CHANGE TO SQL QUERY
            ##############################


            #print ctry

            ### for newlog
            to_mid = mid
            to_ctry = ctry
            to_name = to_name_call

            to_newlog = to_mmsi
            #to_mmsi = "<font color=brown>SHIP "+to_mmsi+"</font><br><a href=\"http://www.marinetraffic.com/en/ais/details/ships/mmsi:"+to_mmsi+"\">%s</a><br>%s" % ( to_name_call, ctry)
            #to_mmsi2 = "<font color=brown>SHIP "+to_newlog+"</font><br><a href=\"http://www.marinetraffic.com/en/ais/details/ships/mmsi:"+to_newlog+"\">%s</a><br>%s" % ( to_name_call, ctry)
            #print to_mmsi2
        except:
            pysql.load_logger("PyYaDD", "Exception in TO SHIP : %s" % raw_dsc_message)
            ### for newlog
            to_mid = "UNK"
            to_ctry = "UNK"
            to_name = "UNID"

            to_newlog = to_mmsi
            to_mmsi = "SHIP, %s, UNID" % to_mmsi
            to_mmsi2 = "SHIP, %s, UNID" % to_newlog
    

    else:
        to_newlog = to_mmsi_raw
        to_mmsi = to_mmsi_raw
        to_mmsi2 = to_newlog
        
        raw_to_mmsi = to_mmsi_raw
        if fmt == "ALL":
            to_type = "ALL"
            to_mid = ""
            to_ctry = ""
            raw_to_mmsi = ""
            to_name = "ALL SHIPS"
        elif fmt == "AREA":
            to_type = "AREA"
            to_mid = ""
            to_ctry = ""
            to_name = "AREA"
        else:
            to_type = ""
            to_mid = "UNK"
            to_ctry = "UNK"
            to_name = "UNID"


    ######### GROUP GROUP #####################
    #
    #
    if to_mmsi_list[0] == "GROUP":
        to_type = "GROUP"
        to_mmsi = to_mmsi_list[1]
        raw_to_mmsi = to_mmsi
        print "We have TO GROUP"
        try:
            mid = to_mmsi[1:4]
            print mid
            ctry = pysql.check_mid(mid)
            if not ctry:
                ctry = "UNK"
            else:
                pass
            
            ############################
            # MID TO COUNTRY CONVERSION HERE
            ############################
            #ctry = mid_dict[mid]
            ############################
            # CHANGE TO SQL QUERY
            ############################


            ### for newlog
            to_mid = mid
            to_ctry = ctry
            to_name = to_mmsi

            to_newlog = to_mmsi
            #to_mmsi = "<font color=blue>GROUP %s</font><br>%s<br>%s" % (to_mmsi, to_mmsi, ctry)
            #to_mmsi2 = "<font color=blue>GROUP %s</font><br>%s<br>%s" % (to_newlog, to_newlog, ctry)
        except:
            pysql.load_logger("PyYaDD", "Exception in TO GROUP : %s" % raw_dsc_message)

            ### for newlog
            to_mid = "UNK"
            to_ctry = "UNK"
            to_name = to_mmsi

            to_newlog = to_mmsi
            #to_mmsi = "GROUP, %s, UNID" % to_mmsi
            #to_mmsi2 = "GROUP, %s, UNID" % to_newlog
            
            
    ####
    ###
    ## FROM FROM FROM FROM
    ##
    ##

    if from_mmsi_list[0] == "COAST":
        from_type = "COAST"
        print "We have coast"
        from_mmsi = from_mmsi_list[1]
        raw_from_mmsi = from_mmsi
        print "COAST FROM MMSI :", from_mmsi
        try:
            name = pysql.check_coast(from_mmsi)
            ############################
            # COAST STATION LOOKUP HERE
            ############################
            #name = new_coast_dict[from_mmsi]
            ############################
            #
            ############################
            if not name:
                name = "Not Found"
            else:
                pass

            print "FROM Name :", name
            if pysql.check_special(from_mmsi) != None:
            
                #if from_mmsi in specials_list:
            #if from_mmsi == "219015591" or from_mmsi == "237673000" or from_mmsi == "219055000":
                mid = from_mmsi[0:3]
            else:              
                mid = from_mmsi[2:5]
                
            print "From MID :", mid
            
            ctry = pysql.check_mid(mid)
            if not ctry:
                ctry = "UNK"
            else:
                pass

            ###########################
            # MID TO COUNTRY CONVERSION
            ###########################
            #ctry = mid_dict[mid]
            ###########################
            #
            ###########################

            ### for newlog
            from_mid = mid
            from_ctry = ctry
            from_name = name

            from_newlog = from_mmsi
            #from_mmsi = "<font color=green>COAST %s</font><br>%s<br>%s" % (from_mmsi, name, ctry)
            #from_mmsi2 = "<font color=green>COAST %s</font><br>%s<br>%s" % (from_newlog, name, ctry)
            #print "Resolved FROM MMSI :" , from_mmsi
        except:
            pysql.load_logger("PyYadd", "Exception in FROM COAST : %s" % raw_dsc_message)
            try:
                mid = from_mmsi[2:5]
                
                ctry = pysql.check_mid(mid)
                if not ctry:
                    ctry = "UNK"
                else:
                    pass
                
                ###########################
                # MID TO COUNTRY CONVERSION
                ###########################
                #ctry = mid_dict[mid]
                ###########################
                #
                ###########################

                ### for newlog
                from_mid = mid
                from_ctry = ctry
                from_name = "UNID"

                from_newlog = from_mmsi
                #from_mmsi = "<font color=green>COAST %s</font><br>UNID<br>%s" % (from_mmsi, ctry)
                #from_mmsi2 = "<font color=green>COAST %s</font><br>UNID<br>%s" % (from_newlog, ctry)
                #print "UNID From MMSI :" , from_mmsi
            except:
                ### for newlog
                from_mid = "UNK"
                from_ctry = "UNK"
                from_name = "UNID"

                from_newlog = from_mmsi
                #from_mmsi = "COAST, %s, UNID" % from_mmsi
                #from_mmsi2 = "COAST, %s, UNID" % from_newlog
                #print "Last resort from mmsi :", from_mmsi

    elif from_mmsi_list[0] == "SHIP":
        from_type = "SHIP"
        from_mmsi = from_mmsi_list[1]
        raw_from_mmsi = from_mmsi
        print "From MMSI", from_mmsi
        if "~" not in from_mmsi and from_mmsi[0] != "0":
            #print "no parity errors %s" % from_mmsi
            from_name_call = resolve_mmsi(from_mmsi)
            print "Name", from_name_call
            #write_log("From Ship: %s" % name_call)
        else:
            from_name_call = from_mmsi
            
        try:
            mid = from_mmsi[0:3]
                
            ctry = pysql.check_mid(mid)
            if not ctry:
                ctry = "UNK"
            else:
                pass
            #print from_mmsi, mid
            ###########################
            # MID TO COUNTRY CONVERSION
            ###########################
            #ctry = mid_dict[mid]
            ###########################
            #
            ###########################

            ### for newlog
            from_mid = mid
            from_ctry = ctry
            from_name = from_name_call

            #print ctry
            from_newlog = from_mmsi 
            #from_mmsi = "<font color=brown>SHIP "+from_mmsi+"</font><br><a href=\"http://www.marinetraffic.com/en/ais/details/ships/mmsi:"+from_mmsi+"\">%s</a><br>%s" % ( from_name_call, ctry)
            #from_mmsi2 = "<font color=brown>SHIP "+from_newlog+"</font><br><a href=\"http://www.marinetraffic.com/en/ais/details/ships/mmsi:"+from_newlog+"\">%s</a><br>%s" % ( from_name_call, ctry)
            #print from_mmsi2
        except:
            pysql.load_logger("PyYadd", "Exception in FROM SHIP : %s" % raw_dsc_message) 
            ### for newlog
            from_mid = "UNK"
            from_ctry = "UNK"
            from_name = "UNID"

            from_newlog = from_mmsi
            #from_mmsi = "SHIP, %s, UNID" % from_mmsi
            #from_mmsi2 = "SHIP, %s, UNID" % from_newlog
    
    else:
        ### for newlog
        from_mid = "UNK"
        from_ctry = "UNK"
        from_name = "UNID"

        from_mmsi = from_mmsi_raw
        raw_from_mmsi = from_mmsi
        from_mmsi2 = from_mmsi_raw
        from_type = "UNK"
    ######### GROUP GROUP #####################
    #
    #
    if from_mmsi_list[0] == "GROUP":
        from_type = "GROUP"
        from_mmsi = from_mmsi_list[1]
        raw_from_mmsi = from_mmsi
        print "We have TO GROUP"
        try:
            mid = from_mmsi[1:4]
            #print mid
            
            ctry = pysql.check_mid(mid)
            if not ctry:
                ctry = "UNK"
            else:
                pass
            
            ###########################
            # MID TO COUNTRY CONVERSION
            ###########################
            #ctry = mid_dict[mid]
            ##########################
            #
            ###########################
           
            ### for newlog
            from_mid = mid
            from_ctry = ctry
            from_name = from_mmsi

            from_newlog = from_mmsi
            #from_mmsi = "<font color=blue>GROUP %s</font><br>%s<br>%s" % (from_mmsi, from_mmsi, ctry)
            #from_mmsi2 = "<font color=blue>GROUP %s</font><br>%s<br>%s" % (from_newlog, from_newlog, ctry)
        except:
            pysql.load_logger("PyYadd", "Exception in FROM GROUP : %s" % raw_dsc_message)
            ### for newlog
            from_mid = "UNK"
            from_ctry = "UNK"
            from_name = from_mmsi

            from_newlog = from_mmsi
            #from_mmsi = "GROUP, %s, UNID" % from_mmsi
            #from_mmsi2 = "GROUP, %s, UNID" % from_newlog
            
            
            
    
    #print "from %s" % from_mmsi
    #print "to %s" % to_mmsi
    new_dsc_call = datetime+";"+""+rx_id+";"+rx_freq+";"+fmt+";"+to_mmsi+";"+cat+";"+from_mmsi+";"+tc1+";"+tc2+";"+freq+";"+pos+";"+eos+";"+ecc
    #print new_dsc_call
    
    #write_log("Adding new message from %s on %s" % (rx_freq, rx_id))
    #write_file(new_dsc_call+"\r\n")
    try:
        pysql.load_newlog(datetime, rx_id, rx_freq, fmt, cat, tc1, tc2, freq, pos, eos, ecc, raw_to_mmsi, raw_from_mmsi, to_type, from_type, raw_dsc_message, to_mid, from_mid, to_ctry, from_ctry, to_name, from_name)
    except:
        pysql.load_newlog(datetime, rx_id, rx_freq, fmt, cat, tc1, tc2, freq, pos, eos, ecc, raw_to_mmsi, raw_from_mmsi, to_type, from_type, raw_dsc_message, to_mid, from_mid, to_ctry, from_ctry, to_name, from_name)

    #pysql.load_yaddnet(datetime, rx_id, rx_freq, fmt, to_mmsi, cat, from_mmsi, tc1, tc2, freq, pos, eos, ecc)
    #pysql.load_fulllog(datetime, rx_id, rx_freq, fmt, to_mmsi, cat, from_mmsi, tc1, tc2, freq, pos, eos, ecc)
        
    return 

    
        
def write_file(text):
    filename = '/var/www/html/pages/php/test/dsc_raw.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    f.write(text+'\r\n')
    f.close()
        
def write_log(text):
    filename = '/var/www/html/pages/php/test/logfile.txt'
    f = open(filename, 'a+')
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    id = "UPLOAD"
    log = ";".join((timenow, id))
    entry = ";".join((log, text))
    #print entry
    f.write(entry+'\r\n')
    f.close()
    
 
    
#write_log("")
#write_log("Running YaDDNet Server Update.................")
#write_log("")
#pysql.load_logger("[UPLOAD]", "Running YaDDNet Server Update....")

