#!/bin/sh

# Starte API
/opt/venv/bin/python3 /app/api.py &

# Warte auf Passwort-Generierung
while [ ! -f /app/.ts3server_license_accepted ]; do
  sleep 1
done

# Starte TS3 Server
exec box64 /app/ts3server_minimal_runscript.sh \
    serveradmin_password={{ options.query_password }} \
    query_port=10011 \
    filetransfer_port=30033 \
    voice_port=9987/udp
