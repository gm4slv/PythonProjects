#!/bin/bash

EXECDIR=/home/gm4slv/PythonProjects/tFldigi
LOG=parrot_log.txt
DIR=/var/www/html/pages/


scp -q $EXECDIR/$LOG gm4slv@shack:$DIR
