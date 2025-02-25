FROM arm64v8/debian:bookworm-slim

# 1. Systemdependencies
RUN apt-get update && apt-get install -y \
    wget curl git cmake build-essential bash \
    libsdl2-dev libx11-dev python3 python3-pip \
    sqlite3 libsqlite3-dev && apt-get clean

# 2. Box64 kompilieren
RUN git clone https://github.com/ptitSeb/box64.git && \
    cd box64 && mkdir build && cd build && \
    cmake .. -DARM_DYNAREC=ON && \
    make -j$(nproc) && make install && cd / && rm -rf box64

# 3. TS3 Server installieren
WORKDIR /app
RUN wget -O ts3server.tar.bz2 https://files.teamspeak-services.com/releases/server/3.13.7/teamspeak3-server_linux_amd64-3.13.7.tar.bz2 && \
    tar xvf ts3server.tar.bz2 --strip-components=1 && \
    rm ts3server.tar.bz2 && \
    touch .ts3server_license_accepted

# 4. Skripte kopieren
COPY scripts/backup.sh /app/scripts/
COPY www /www
COPY entrypoint.sh /

# 5. Python Abhängigkeiten
RUN pip3 install flask==2.3.3 waitress==2.1.2

# 6. Berechtigungen
RUN chmod +x /entrypoint.sh /app/scripts/*.sh

ENTRYPOINT ["/entrypoint.sh"]
