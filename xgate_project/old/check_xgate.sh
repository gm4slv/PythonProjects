#!/bin/bash

source /home/gm4slv/.bashrc

pidof python xgate_dtmf.py >/dev/null


if [[ $? -ne 0 ]] ; then
	echo "Restarting xgate : $(date)" >> /home/gm4slv/xgate.log
	tmux new-session -d -s xgate 'python /home/gm4slv/bin/xgate_dtmf.py'
fi

