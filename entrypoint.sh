#!/bin/bash
cd /app
echo "TeamSpeak 3 Server startet..."

# Lizenzdatei kopieren, falls vorhanden
if [ -n "$LICENSE_KEY" ]; then
  echo "$LICENSE_KEY" > LICENSEKEY.DAT
fi

exec box64 ./ts3server_minimal_runscript.sh