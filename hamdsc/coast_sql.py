# coast_sqlite3
import sqlite3
import time

 
def load_resolve(mmsi, name, call):
    db = sqlite3.connect("resolve.db")
    cur = db.cursor()
    
    cur.execute("INSERT INTO resolve ( mmsi, name, call) VALUES (?,?,?)", ( mmsi, name, call))
    db.commit()
    db.close()
    
def get_resolve(to_mmsi):
    print "In resolve with %s" % to_mmsi
    db = sqlite3.connect("resolve.db")
    with db:
        cur = db.cursor()
        
        cur.execute('''SELECT * FROM resolve WHERE mmsi=?''', (to_mmsi,))
        results = cur.fetchone()
        print "From resolve DB", results
    db.close()        
    return results
   
def dump_resolve():
    db = sqlite3.connect("resolve.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM resolve order by mmsi")
        results = cur.fetchall()
        
    db.close()        
    return results

def load_admin(message):
    db = sqlite3.connect("admin.db")
    cur = db.cursor()
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    cur.execute("INSERT INTO admin (datetime, message) VALUES (?,?)", (datetime, message))
    db.commit()
    db.close()

def clear_admin_7day_table():

    
    db = sqlite3.connect("admin.db") 
    # create a table
    cur = db.cursor() 
    
    cur.execute("delete from admin where datetime < datetime('now', '-7 days')")

    db.commit()

    # disconnect from server
    db.close()
 
def clear_admin_login_table():

    
    db = sqlite3.connect("admin.db") 
    # create a table
    cur = db.cursor() 
    
    cur.execute("delete from admin where message like 'Admin; User%' or message like 'Admin; Connect%' or message like 'Admin; Log%' or message like 'Admin; Client%'")

    db.commit()

    # disconnect from server
    db.close()

    
def get_admin():
    db = sqlite3.connect("admin.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM (SELECT * FROM admin where datetime > datetime('now', '-8 hour') ORDER BY 1 DESC LIMIT 100) sub ORDER BY 1 ASC")
        results = cur.fetchall()
        
        
    db.close()        
    return results

def dump_admin():
    db = sqlite3.connect("admin.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM admin ORDER BY 1 ASC")
        results = cur.fetchall()
        
        
    db.close()        
    return results

def load_checklog(time, freq, tr, mmsi, name, call, tc1, eos, id):
    db = sqlite3.connect("check.db", timeout=5)
    cur = db.cursor()
    
    cur.execute("INSERT INTO checklog (datetime, freq, tr, mmsi, name, call, tc1, eos, id) VALUES (?,?,?,?,?,?,?,?,?)", (time, freq, tr, mmsi, name, call, tc1, eos, id))
    db.commit()
    db.close()  

def get_checklog():
    db = sqlite3.connect("check.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM (SELECT * FROM checklog  ORDER BY 1 DESC LIMIT 50) sub ORDER BY 1 ASC")
        results = cur.fetchall()
        
        
    db.close()       
    return results    

def dump_checklog():
    db = sqlite3.connect("check.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM checklog  ORDER BY 1 ASC")
        results = cur.fetchall()
        
        print "in dump() ", results
    db.close()       
    return results    
    
    

def load_rxtx(time, freq, tr, mmsi, name, call, tc1, eos, id):
    db = sqlite3.connect("rxtx.db", timeout=5)
    cur = db.cursor()
    
    cur.execute("INSERT INTO rxtx (datetime, freq, tr, mmsi, name, call, tc1, eos, id) VALUES (?,?,?,?,?,?,?,?,?)", (time, freq, tr, mmsi, name, call, tc1, eos, id))
    db.commit()
    db.close()  
    
def get_rxtx():
    db = sqlite3.connect("rxtx.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM (SELECT * FROM rxtx  ORDER BY 1 DESC LIMIT 50) sub ORDER BY 1 ASC")
        results = cur.fetchall()
        
        
    db.close()       
    return results    

def dump_rxtx():
    db = sqlite3.connect("rxtx.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM rxtx  ORDER BY 1 ASC")
        results = cur.fetchall()
        
        
    db.close()       
    return results    
    
    
def load_rx(time, freq, rx, mmsi, name, call, tc1, eos):
    db = sqlite3.connect("calls.db")
    cur = db.cursor()
    
    cur.execute("INSERT INTO rx (datetime, freq, rx, mmsi, name, call, tc1, eos) VALUES (?,?,?,?,?,?,?,?)", (time, freq, rx, mmsi, name, call, tc1, eos))
    db.commit()
    db.close()

def get_rx():
    db = sqlite3.connect("calls.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM (SELECT * FROM rx  ORDER BY 1 DESC LIMIT 50) sub ORDER BY 1 ASC")
        results = cur.fetchall()
        
        
    db.close()       
    return results

def dump_rx():
    db = sqlite3.connect("calls.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM rx ORDER BY 1 ASC")
        results = cur.fetchall()
        
        
    db.close()       
    return results

    
def load_tx(time, freq, mmsi, name, call, tc1, eos):
    db = sqlite3.connect("calls.db", timeout=5)
    cur = db.cursor()
    
    cur.execute("INSERT INTO tx (datetime, freq, mmsi, name, call, tc1, eos) VALUES (?,?,?,?,?,?,?)", (time, freq, mmsi, name, call, tc1, eos))
    db.commit()
    db.close()
    
def get_tx():
    db = sqlite3.connect("calls.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM (SELECT * FROM tx  ORDER BY 1 DESC LIMIT 50) sub ORDER BY 1 ASC")
        results = cur.fetchall()
        
    db.close()    
            
    return results
    
def dump_tx():
    db = sqlite3.connect("calls.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM tx ORDER BY 1 ASC")
        results = cur.fetchall()
        
    db.close()    
            
    return results
    
def get_last_rx():

    db = sqlite3.connect("calls.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT datetime, freq, mmsi, name, call, tc1, eos  FROM rx ORDER BY 1 DESC LIMIT 1")
        results = cur.fetchall()
        
    db.close()    
            
    return results
    
def get_last_tx():

    db = sqlite3.connect("calls.db")
    with db:
        cur = db.cursor()
        
        cur.execute("SELECT * FROM tx ORDER BY 1 DESC LIMIT 1")
        results = cur.fetchall()
        
    db.close()    
            
    return results

