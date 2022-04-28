#!/bin/bash


source /home/gm4slv/.bashrc

pidof python xgate_dtmf.py >/dev/null


if [[ $? -ne 0 ]] ; then
	echo "Restarting xgate : $(date)" >> /home/gm4slv/xgate.log
	#tmux new-session -d -s xgate 
	#tmux new-window -n 'xgate' 'python /home/gm4slv/bin/cw/xgate_dtmf.py'
	#tmux new-window -n 'watch' 'python /home/gm4slv/bin/cw/watchdog.py'
	/home/gm4slv/bin/cw/start_xgate.sh
fi

