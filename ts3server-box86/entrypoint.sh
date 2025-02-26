#!/bin/bash

# Starte API-Server
python3 /app/api.py &

# Starte TS3-Server
cd /app
exec box64 ./ts3server_minimal_runscript.sh
