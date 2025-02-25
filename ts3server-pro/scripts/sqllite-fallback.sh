#!/bin/bash

# Prüfe ob SQLite-Datenbank existiert
if [ ! -f "/config/ts3server.sqlitedb" ]; then
  echo "Erstelle neue SQLite-Datenbank..."
  cp /app/ts3server.sqlitedb /config/
fi

# Setze symbolischen Link
ln -sf /config/ts3server.sqlitedb /app/ts3server.sqlitedb
