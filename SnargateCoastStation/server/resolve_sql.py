import MySQLdb
import time

from special_dict import *
specials_list = [ "219015591", "237673000","237673100", "219055000" ]

def write_resolve_log(text):
    filename = 'reslog.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    id = "RESOLVER"
    log = ";".join((timenow, id))
    entry = ";".join((log, text))
    f.write(entry+'\r\n')
    f.close()


def check_mmsi(mmsi):

    # lookup specials first....
    if mmsi in specials_list:
       print "looking for special"
       special_ship = special_dict[mmsi] 
       print "special_ship ", special_ship
       name = special_ship.split(",")[0]
       call = special_ship.split(",")[1]
       vtype = "n/a"
       ship = (name, call, vtype)
       print "special found ", ship
       return ship

    db = MySQLdb.connect(host="yadd", user="root", db="yadd")

    cur = db.cursor()

    sql = "SELECT shipname, callsign, vesseltype from resolve2 where mmsi = %s" % mmsi

    cur.execute(sql)
    ship = cur.fetchone()
    db.close()
    print "Resolver says ", ship
    if ship:
        write_resolve_log("Found in YaDDNEt database : %s : %s" % (mmsi, ship))
        return ship
    else:
        write_resolve_log("Not found in YaDDNEt database %s" % mmsi)
        return ["unk", "unk", "n/a"]



