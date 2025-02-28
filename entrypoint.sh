#!/bin/bash
cd /app
echo "TeamSpeak 3 Server startet..."
exec box64 ./ts3server_minimal_runscript.sh

exec python3 /app/app.py
