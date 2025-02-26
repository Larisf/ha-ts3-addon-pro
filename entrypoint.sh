#!/bin/bash
cd /app

# Prüfe, ob eine LICENSEKEY.dat im persistenten Config-Verzeichnis vorhanden ist und kopiere sie in das App-Verzeichnis
if [ -f /config/LICENSEKEY.dat ]; then
    cp /config/LICENSEKEY.dat /app/
fi

# Starte den TS3 Server im Hintergrund
echo "TeamSpeak 3 Server startet..."
bash ./ts3server_minimal_runscript.sh &

# Starte das Web-GUI (Flask App)
echo "Starte Web-GUI..."
python3 /app/app.py
