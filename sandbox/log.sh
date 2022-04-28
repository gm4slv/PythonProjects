#!/bin/bash

EXECDIR=/home/gm4slv/PythonProjects/sandbox
LOG=gm4slv_fldigi.txt
TAIL=gm4slv_tail.txt
DIR=/var/www/html/pages/



scp -q $EXECDIR/$LOG gm4slv@shack:$DIR
scp -q $EXECDIR/$TAIL gm4slv@shack:$DIR
