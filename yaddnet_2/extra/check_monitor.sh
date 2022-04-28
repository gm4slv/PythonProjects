#!/bin/bash

ps auxw | grep w2w | grep -v SCREEN | grep -v grep > /dev/null

if [ $? != 0 ]
then
echo "Not running"
cp /var/www/html/pages/php/test/down.html /var/www/html/pages/php/test/snargate_status.html
/home/gm4slv/monitor.sh
fi

