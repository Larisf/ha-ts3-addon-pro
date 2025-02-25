FROM arm64v8/debian:bookworm-slim

# Systemdependencies
RUN apt-get update && apt-get install -y \
    wget curl git cmake build-essential \
    libsdl2-dev libx11-dev python3 python3-pip \
    sqlite3 libsqlite3-dev && apt-get clean

# Box64 kompilieren
RUN git clone https://github.com/ptitSeb/box64.git && \
    cd box64 && mkdir build && cd build && \
    cmake .. -DARM_DYNAREC=ON && \
    make -j$(nproc) && make install && cd / && rm -rf box64

# TS3 Server installieren
WORKDIR /app
RUN wget -O ts3.tar.bz2 $(curl -s 'https://files.teamspeak-services.com/releases/server/3.13.7/teamspeak3-server_linux_amd64-3.13.7.tar.bz2') && \
    tar xvf ts3.tar.bz2 --strip-components=1 && \
    rm ts3.tar.bz2 && \
    touch .ts3server_license_accepted

# Webinterface
COPY www /www
RUN pip3 install flask waitress

# Startscript
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
