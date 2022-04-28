#!/bin/bash

PLOTDIR=/home/gm4slv/mysql_test
DIR=/home/gm4slv/yaddnet
graph=$PLOTDIR/graph.dat
graphtail=$PLOTDIR/graph.dat.tail
TIME=`date "+%d/%m/%y %H:%M:%S"`
WWW=/var/www/html/pages/php/test/tmp

rate=`mysql --skip-column-names -u root yadd < $DIR/hourly_stat`
rate2=`mysql --skip-column-names -u root yadd < $DIR/hourly_stat_2`
rate4=`mysql --skip-column-names -u root yadd < $DIR/hourly_stat_4`
rate6=`mysql --skip-column-names -u root yadd < $DIR/hourly_stat_6`
rate8=`mysql --skip-column-names -u root yadd < $DIR/hourly_stat_8`
rate12=`mysql --skip-column-names -u root yadd < $DIR/hourly_stat_12`
rate16=`mysql --skip-column-names -u root yadd < $DIR/hourly_stat_16`
ratec=`mysql --skip-column-names -u root yadd < $DIR/hourly_stat_coast`
rates=`mysql --skip-column-names -u root yadd < $DIR/hourly_stat_ship`
stamp="$TIME $rate $rate2 $rate4 $rate6 $rate8 $rate12 $rate16 $ratec $rates"
echo $stamp >> $graph

gnuplot $DIR/yadd_rate.gplt
gnuplot $DIR/yadd_stn_rate.gplt
cp $PLOTDIR/yadd_hour_60.png $WWW
cp $PLOTDIR/yadd_hour_stn_60.png $WWW

tail -n 3000 $graph > $graphtail
cp $graphtail $graph
