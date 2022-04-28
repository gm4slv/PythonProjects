#!/bin/sh

session="xGate"

dir="/home/gm4slv/bin/xgate_m710"
tmux start-server

tmux new-session -d -s $session 

tmux rename-window "xgated"

tmux selectp -t 0
tmux send-keys "cd $dir" C-m
tmux send-keys " ./xgate_m710_split.py" C-m
#tmux send-keys "python ./xgate_m710_simplex.py" C-m
#tmux send-keys "python ./xgate_m710.py" C-m



tmux selectp -t 0
tmux splitw -h -p 50
tmux send-keys "cd $dir" C-m
#tmux send-keys "python ./watchdog.py" C-m

tmux selectp -t 0
tmux splitw -v -p 50
tmux send-keys "cd $dir" C-m
tmux send-keys "python ./test.py" C-m



tmux selectp -t 0 -P 'fg=colour107'
tmux selectp -t 1 -P 'fg=colour100'

#tmux selectp -t 0
#tmux splitw -v -p 50


#tmux selectp -t 3 
#tmux attach-session -t $session
