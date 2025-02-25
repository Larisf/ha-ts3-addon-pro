#!/bin/bash

while true; do
  sleep $(($BACKUP_INTERVAL * 3600))
  
  BACKUP_NAME="ts3_backup_$(date +%Y-%m-%d_%H-%M).tar.gz"
  tar -czvf "/backup/$BACKUP_NAME" \
    /config/ts3server \
    /license/ts3server.ini \
    /app/ts3db_mysql.ini
  
  echo "Backup erstellt: $BACKUP_NAME"
done
