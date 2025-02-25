#!/bin/bash

# TS3-Server mit bash starten
bash ./ts3server_minimal_runscript.sh &
TS3_PID=$!

# Flask-Server korrekt starten
python3 -m waitress --port=8099 --call app:create_app &
FLASK_PID=$!

# Backup-Script nur starten, wenn vorhanden
if [ -f "/app/scripts/backup.sh" ]; then
  /app/scripts/backup.sh &
  BACKUP_PID=$!
fi

wait $TS3_PID $FLASK_PID ${BACKUP_PID:-}
