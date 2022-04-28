#! /usr/bin/env python

## a text-terminal version of the WatchCheck app
## to track error, daily error rate of timepieces.

#
import time
import datetime
import json



def get_delta():

    print time.strftime("Current Time = %H:%M")
    
    h = time.strftime("%H")
    w = raw_input("Watch time %s:" % (h))
    print w
    
    date = time.strftime("%Y/%m/%d")
    s = date + " " + h +":"+ w +":00"
    
    raw_input("Press enter when seconds = 0 ")
    
    watchtime = time.mktime(datetime.datetime.strptime(s, "%Y/%m/%d %H:%M:%S").timetuple())
    record_time = time.strftime("%Y/%m/%d %H:%M:%S")
    timenow = time.time()
    delta = watchtime - timenow
    
    return record_time,delta


def watch_stat():

    try:
        saved_error = open('error_list.json')
        error_list = json.load(saved_error)
    except:
        error_list = []

    if len(error_list) > 1:
        first_record = error_list[0]
        latest_record = error_list[-1]
        previous_record = error_list[-2]

        first_time = first_record[0]

        first_delta = first_record[1]

        latest_time = latest_record[0] 
        latest_delta = latest_record[1]

        previous_time = previous_record[0]
        previous_delta = previous_record[1]

        FMT = '%Y/%m/%d %H:%M:%S'
    
        t_latest = datetime.datetime.strptime(latest_time, FMT)
        t_previous = datetime.datetime.strptime(previous_time, FMT)
        t_first = datetime.datetime.strptime(first_time, FMT)

        tdelta = t_latest - t_previous
        full_delta = t_latest - t_first

        elapsed_time = tdelta.total_seconds()

        full_time = full_delta.total_seconds()

        print "First record time ", first_time
        print "First record delta ", first_delta
        print ""

        print "Previous record time ", previous_time
        print "Previous record delta ", previous_delta
        print ""

        print "Latest record time " , latest_time
        print "Latest record delta ", latest_delta
        print ""
    
        print "Overall elapsed time ", full_delta
        print "Latest elapsed time ", tdelta
        print ""

        # Current Error rate
        time_error = latest_delta - previous_delta
        error_rate = time_error / elapsed_time
        daily_rate = error_rate * (60*60*24)
        ppm_daily = error_rate * 1000000

        # Overall Error rate
        total_error = latest_delta - first_delta
        average_error_rate = total_error / full_time

        average_rate = average_error_rate * (60*60*24)
        ppm_overall = average_error_rate * 1000000


        print "Latest delta change ", time_error

        print "Latest elapsed time %d seconds " % (elapsed_time)

        print ""
        print "Daily PPM : %0.3f" % ppm_daily
        print "Daily rate error: %0.1f s/d " % (daily_rate)

        print ""
        print "Total Time %d seconds" % (full_time)
        print "Total error ", total_error
        print "Total PPM : %0.3f" % ppm_overall
        print "Total rate error: %0.1f s/d" % (average_rate)
        print ""
        print "========================================================"
        print " Delta : %0.1f s | Rate : %0.1f s/d | Average : %0.1f s/d" % (latest_delta, daily_rate, average_rate)
        print "========================================================"
        print ""
    else:
        print "No rate yet"


def new_record():
    
    try:
        saved_error = open('error_list.json')
        error_list = json.load(saved_error)
    except:
        error_list = []

    s,delta = get_delta()

    print ""
    print "%s \n\nDelta %0.1f seconds" % (s, delta)
    last_data=[s,delta]
    error_list.append(last_data)
    #print error_list

    with open('error_list.json', 'wb') as outfile:
        json.dump(error_list, outfile)

    return

def delete_last():
    try:
        saved_error = open('error_list.json')
        error_list = json.load(saved_error)
    except:
        error_list = []
    error_list.pop()
    
    with open('error_list.json', 'wb') as outfile:
        json.dump(error_list, outfile)
    
    return


def menu():
    print "N : New Record\nD : Delete Last\nS : Stats\nQ : Quit"
    choice = raw_input("Command > : ").upper()
    if choice == "N":
        print "New"
        new_record()
        watch_stat()
        menu()
    elif choice == "S":
        print "Stat"
        watch_stat()
        menu()
    elif choice == "D":
        delete_last()
        watch_stat()
        menu()
    elif choice == "Q":
        return
    else:
        print "?"
        menu()


menu()

