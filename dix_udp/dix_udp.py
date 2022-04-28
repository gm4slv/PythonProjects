#######
# a udp receiver to handle APRS packets from DiXPRS running at MB7UZE
# April 2016 GM4SLV
# 
# 
import socket
import time
import pysql

# listen on LAN interface
UDP_IP = "192.168.21.20"
# and port
UDP_PORT = 5050

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def write_file(text):
    filename = r'/var/www/html/pages/mb7uze.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    #timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    f.write(text+"\n")
    #print timenow + "> " +text
    f.close()


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 31 < ord(c) < 127)
    return ''.join(stripped)


def tail(n):
    filename = r'/var/www/html/pages/mb7uze.txt'
    tailfile = r'/var/www/html/pages/mb7uze.txt'
    fin = open(filename, 'r')
    list = fin.readlines()
    fin.close()
    tail_list = list[-n:]
    fout = open(tailfile, "w")
    fout.writelines(tail_list)
    fout.close()


def get_3rdpcall( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def get_last_digi(path):
    if len(path) > 0:
        path_list = path.split(",")
    else:
        return ""
    #print path_list

    for i in reversed(path_list):
        #print i[0:4]
        if i[-1] == "*" and i[0:4] != "WIDE":
            #print "Found a digi ", i
            return i[:-1]

        else:
            last_digi = ""

    return last_digi

def make_packet_list(packet):
    p3call = ""
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    dixpacket = timenow + "|" + packet 
    #print dixpacket
    dixpacket_list = dixpacket.split('|')
    #print dixpacket_list
    datetime = dixpacket_list[0]
    source = dixpacket_list[2]
    tx_rx = dixpacket_list[3]
    if tx_rx == "R0":
        tx_rx = "RX"
    elif tx_rx == "T0":
        tx_rx = "TX"
    aprspacket = dixpacket_list[4]
    aprspacket_list = aprspacket.split(">")
    callsign = aprspacket_list[0]
    pathdata = ">".join(aprspacket_list[1:])
    pathdata_list = pathdata.split(":")
    path = pathdata_list[0]
    dest_path_list = path.split(",")
    dest = dest_path_list[0]
    path = ",".join(dest_path_list[1:])
    ldigi = get_last_digi(path)
    payload = ":".join(pathdata_list[1:])
    protocol = payload[0]
    #print protocol
    if protocol == "!":
        ptype = "Posit"
    elif protocol == "=":
        ptype = "Posit"
    elif protocol == "/":
        ptype = "Posit"
    elif protocol == "@":
        ptype = "Posit"
    elif protocol == ";":
        ptype = "Object"
    elif protocol == ">":
        ptype = "Status"
    elif protocol == ":":
        msg_list = payload.split(":")
    #    print msg_list
        if msg_list[2][0:3] == "ack":
            ptype = "Ack"
        else:
            ptype = "Message"
    elif protocol == "'" or protocol == "`":
        ptype = "Mic-E"
    elif protocol == "}":
        ptype = "3rd Party"
        p3call = get_3rdpcall(payload,"}",">")
    elif protocol == "T":
        ptype = "Telemetry"
    elif protocol == "<":
        ptype = "I-Gate"
    elif protocol == "$":
        ptype = "Posit"
    else:
        ptype = "Unk"
    #filedata = '{:<20} {:<7} {:<7} {:<10} {:<8} {:<40} {:<50}' .format(datetime, source, tx_rx, callsign, dest, path, payload)
    #filedata = '{:<19}  {:<6} {:<10} {:<7} {:<40} {:<10} {:<}' .format(datetime, tx_rx, callsign, dest, path, ptype, payload)
    #write_file(filedata)
    #print "%s \t %s \t %s \t %s \t %s \t %s " % (datetime, source, tx_rx, callsign, path, payload)
    return datetime, tx_rx, callsign, dest, path, ptype, payload, p3call, ldigi

while True:
    data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
    #print data
    #write_file(data)
    stripped = strip_non_ascii(data)
    datetime, tx_rx, callsign, dest, path, ptype, payload, p3call, ldigi  = make_packet_list(stripped)
    pysql.load_igate(datetime, tx_rx, callsign, dest, path, ptype, payload, p3call, ldigi)
    #write_file(make_packet_list(stripped))
    #tail(40)
