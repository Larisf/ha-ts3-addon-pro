#!/bin/bash
echo "Starte Supervisor..."
exec supervisord -c /app/supervisord.conf
