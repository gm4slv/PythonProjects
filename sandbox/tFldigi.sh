#!/bin/sh

session="Shack"

tmux start-server

tmux new-session -d -s $session 

tmux rename-window "tFldigi"

tmux selectp -t 0
tmux send-keys "python ./rx.py" C-m



tmux selectp -t 0
tmux splitw -v -p 50
tmux send-keys "python ./tx.py" C-m

tmux selectp -t 1
tmux splitw -v -p 40
tmux send-keys "python ./status.py" C-m





#tmux selectp -t 0
#tmux splitw -v -p 30
#tmux send-keys "python ~/PythonProjects/sandbox/parrot.py" C-m

tmux new-window -t $session:1 -n "Help"
#tmux selectw -t $session:1
tmux send-keys "python ./help.py" C-m

tmux selectw -t $session:0
tmux selectp -t 0 -P 'fg=colour107'
tmux selectp -t 2 -P 'fg=colour100'
#tmux selectp -t 3 -P 'fg=colour130'
#tmux selectp -t 1 -P 'fg=colour95'
tmux selectp -t 1 
tmux attach-session -t $session
