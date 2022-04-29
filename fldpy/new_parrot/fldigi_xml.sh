#!/bin/sh

session="Shack"

tmux start-server

tmux new-session -d -s $session 

tmux rename-window "fldigi"

tmux selectp -t 0
tmux send-keys "python2 ./rx_buf.py" C-m



tmux selectp -t 0
tmux splitw -h -p 50
tmux send-keys "python2 ./parrot_flmsg.py" C-m

tmux selectp -t 1 
tmux attach-session -t $session
