#!/bin/bash

# Starte TS3 Server
box64 ./ts3server_minimal_runscript.sh &

# Starte Webinterface
python3 -m waitress --port=8099 --call "flask:create_app" &

# Backups
/app/scripts/backup.sh &

wait
