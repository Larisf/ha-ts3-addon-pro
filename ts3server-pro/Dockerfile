FROM arm64v8/debian:bookworm-slim

# Systemdependencies
RUN apt-get update && apt-get install -y \
    wget curl git cmake build-essential \
    libsdl2-dev libx11-dev python3 python3-pip python3-venv \
    sqlite3 libsqlite3-dev && apt-get clean

# Box64 kompilieren
RUN git clone https://github.com/ptitSeb/box64.git && \
    cd box64 && mkdir build && cd build && \
    cmake .. -DARM_DYNAREC=ON && \
    make -j$(nproc) && make install && cd / && rm -rf box64

# TS3 Server installieren
WORKDIR /app
RUN wget -O ts3.tar.bz2 $(curl -s 'https://www.teamspeak.com/versions/server.json' | jq -r '.linux.x86.mirrors[0]') && \
    tar xvf ts3.tar.bz2 --strip-components=1 && \
    rm ts3.tar.bz2 && \
    touch .ts3server_license_accepted

# Webinterface mit virtuellem Environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY www /www
RUN pip install --no-warn-script-location flask waitress

# Startscript
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
