# python MySQL Test file

import MySQLdb
import time

#datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))

    
def load_igate(datetime, txrx, callsign, dest, path, ptype, payload, p3call, ldigi):

    #load_logger("[UPLOAD]", "PySQL Loading MAIN database")
    db = MySQLdb.connect(host="localhost", user="root", db="mb7uze") 
    
    cur = db.cursor()
    
    sql = "INSERT INTO igate (dt, txrx, callsign, dest, path, ptype, payload, p3call, ldigi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    data = (datetime, txrx, callsign, dest, path, ptype, payload, p3call, ldigi)
    
    cur.execute(sql, data)
    db.commit()
    db.close()

    
    
