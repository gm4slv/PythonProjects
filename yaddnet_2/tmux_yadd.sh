#!/bin/sh

/usr/bin/tmux new-session -d -s YaDDNet

/usr/bin/tmux new-window -t YaDDNet:2 -n 'yUDP' '/usr/bin/python /home/gm4slv/yaddnet/yadd_udp.py'
#/usr/bin/tmux new-window -t YaDDNet:3 -n 'dUDP' '/usr/bin/python /home/gm4slv/yaddnet/dscd_udp.py'
#/usr/bin/tmux new-window -t YaDDNet:6 -n 'dix' '/usr/bin/python /home/gm4slv/dix_udp.py'

