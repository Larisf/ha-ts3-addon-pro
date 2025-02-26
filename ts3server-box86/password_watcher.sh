#!/bin/bash

# Überwache die Log-Dateien
tail -F /app/logs/ts3server_*.log | while read line
do
  if [[ $line == *"password="* ]] && [ -z "$TS3_ADMIN_PASSWORD" ]; then
    export TS3_ADMIN_PASSWORD=$(echo "$line" | grep -oP 'password= \K\S+')
    sed -i "s/your_password/${TS3_ADMIN_PASSWORD}/" /app/api.py
    break
  fi
done
