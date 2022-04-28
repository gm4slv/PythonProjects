#!/bin/bash

heartbeat_file="/home/gm4slv/heartbeat.txt"

current=`date +%s`
last_modified=`stat -c "%Y" $heartbeat_file`

crash=`date +%Y%m%d@%H%M%S`

echo $current
echo $last_modified


if [ $(($current-$last_modified)) -gt 60 ]; then
	kill -9 $(pidof -x xgate_m710_split.py);
	kill -9 $(pidof tmux);
	cp "$heartbeat_file" "crashed_at_$crash.txt"
	/home/gm4slv/bin/check_xgate.sh;
else
     echo "new";
fi
