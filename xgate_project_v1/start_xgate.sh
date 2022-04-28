#!/bin/sh

session="xGate"

dir="/home/gm4slv/bin/cw_sidetone"
tmux start-server

tmux new-session -d -s $session 

tmux rename-window "xgated"

tmux selectp -t 0
tmux send-keys "cd $dir" C-m
tmux send-keys "python ./xgate_dtmf.py" C-m



tmux selectp -t 0
tmux splitw -h -p 50
tmux send-keys "cd $dir" C-m
tmux send-keys "python ./watchdog.py" C-m

tmux selectp -t 1
tmux splitw -v -p 60
tmux send-keys "cd $dir" C-m
tmux send-keys "python ./test.py" C-m



tmux selectp -t 0 -P 'fg=colour107'
tmux selectp -t 1 -P 'fg=colour100'


#tmux selectp -t 0
#tmux splitw -v -p 30
#tmux send-keys "python ~/PythonProjects/sandbox/parrot.py" C-m

tmux selectp -t 2 
#tmux attach-session -t $session
