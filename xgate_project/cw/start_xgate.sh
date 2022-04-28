#!/bin/sh

session="xGate"

tmux start-server

tmux new-session -d -s $session 

tmux rename-window "xgated"

tmux selectp -t 0
tmux send-keys "python ./xgate_dtmf.py" C-m



tmux selectp -t 0
tmux splitw -h -p 50
tmux send-keys "python ./watchdog.py" C-m

tmux selectp -t 1
tmux splitw -v -p 40
#tmux send-keys "python ./status.py" C-m





#tmux selectp -t 0
#tmux splitw -v -p 30
#tmux send-keys "python ~/PythonProjects/sandbox/parrot.py" C-m

tmux selectp -t 2 
#tmux attach-session -t $session
