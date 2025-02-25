#!/bin/bash

# Migriere SQLite → MySQL
echo "Migriere Daten von SQLite zu MySQL..."

SQLITE_DB="/config/ts3server.sqlitedb"
MYSQL_CONF="/app/ts3db_mysql.ini"

# Lese MySQL-Zugangsdaten
HOST=$(grep 'host=' ${MYSQL_CONF} | cut -d= -f2)
USER=$(grep 'username=' ${MYSQL_CONF} | cut -d= -f2)
PASS=$(grep 'password=' ${MYSQL_CONF} | cut -d= -f2)
DB=$(grep 'database=' ${MYSQL_CONF} | cut -d= -f2)

# Exportiere Daten
sqlite3 ${SQLITE_DB} .dump | \
mysql -h ${HOST} -u ${USER} -p${PASS} ${DB}

echo "Migration abgeschlossen!"
