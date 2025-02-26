#!/bin/bash

# Passwort aus Logs extrahieren
extract_password() {
  grep -oP 'password= \K\S+' /app/logs/ts3server_* | head -1
}

# Beim ersten Start
if [ ! -f /app/.password_set ]; then
  echo "Generiere Admin-Passwort beim ersten Start..."
  TS3_ADMIN_PASSWORD=$(extract_password)
  export TS3_ADMIN_PASSWORD
  touch /app/.password_set
fi

# Starte API und Server

# Starte API-Server mit dem virtuellen Environment
/opt/venv/bin/python3 /app/api.py &

# Starte TS3-Server
cd /app
exec box64 ./ts3server_minimal_runscript.sh
