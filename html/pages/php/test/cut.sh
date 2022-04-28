#!/bin/bash


while read F  ; do
        echo $F
	sed -i '/CUT HERE/,$d' $F
	cat skel.php >> $F

done <filelist.txt

