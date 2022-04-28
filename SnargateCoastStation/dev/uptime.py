# test uptime
import time
import datetime


def get_uptime(start_time):

    #start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))


  

    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))





    start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')



    ends = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    

    diff = ends - start

   
    weeks, days  = divmod(diff.days, 7)
    minutes, secs = divmod(diff.seconds, 60)
    
    hours, mins = divmod(minutes, 60)


    uptime = "Server Up %d weeks %d days %d:%d " % (weeks, days, hours, mins)
    
    return uptime



uptime = get_uptime("2015-05-02 14:00:00")
print uptime

