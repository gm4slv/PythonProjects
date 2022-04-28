
#!/bin/bash

DATE=`date +%Y-%m-%d_%H%M%S`
YESTERDAY=`date +%Y-%m-%d -d 'yesterday'`

mysqldump -u root yadd > /home/gm4slv/backup/newyadd_$DATE.sql
rsync -av /home/gm4slv/backup/* 192.168.21.5::Backup/

rm -f /home/gm4slv/backup/newyadd_$YESTERDAY*.sql


