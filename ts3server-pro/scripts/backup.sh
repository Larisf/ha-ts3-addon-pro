#!/bin/bash
while true; do
    sleep 86400 # 24h
    tar -czvf "/backup/ts3-$(date +%Y-%m-%d).tar.gz" \
        /app/ts3server.sqlitedb \
        /app/.ts3server_license_accepted
done
