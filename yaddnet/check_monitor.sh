#!/bin/bash

#ps auxw | grep w2w_monitor | grep -v grep > /dev/null

#if [ $? != 0 ]
#then
#echo "Not running"
#cp /var/www/html/pages/php/test/down.html /var/www/html/pages/php/test/snargate_status.html
pkill -f w2w_monitor.py
sleep 5
/home/gm4slv/yaddnet/monitor.sh
#fi

