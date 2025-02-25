#!/bin/bash

# Konfiguration generieren
CONFIG_FILE="/app/ts3server.ini"

# MySQL nur wenn Konfiguration existiert
if [ -n "${MYSQL_HOST}" ]; then
  echo "🔌 MySQL-Konfiguration erkannt"
  cat <<EOF > ${CONFIG_FILE}
machine_id=
default_voice_port=9987
voice_ip=0.0.0.0
licensepath=/license
filetransfer_port=30033
filetransfer_ip=0.0.0.0
query_port=10011
query_ip=0.0.0.0
dbplugin=ts3db_mysql
dbpluginparameter=ts3db_mysql.ini
dbsqlpath=sql/
dbsqlcreatepath=create_mysql
dbconnections=10
EOF

  cat <<EOF > /app/ts3db_mysql.ini
[config]
host=${MYSQL_HOST}
port=3306
username=${MYSQL_USER}
password=${MYSQL_PASSWORD}
database=${MYSQL_DATABASE}
socket=
EOF

else
  echo "💡 Verwende SQLite-Datenbank"
  cat <<EOF > ${CONFIG_FILE}
machine_id=
default_voice_port=9987
voice_ip=0.0.0.0
licensepath=/license
filetransfer_port=30033
filetransfer_ip=0.0.0.0
query_port=10011
query_ip=0.0.0.0
dbsqlpath=sql/
dbsqlcreatepath=create_sqlite
dbconnections=10
EOF
fi

# Dienste starten
echo "🚀 Starte TeamSpeak Server..."
box64 ./ts3server_minimal_runscript.sh &
sleep 5

echo "🌐 Starte Web Interface..."
node /app/websocket_server.js &

echo "💾 Aktiviere Backups..."
/app/scripts/backup.sh &

wait
