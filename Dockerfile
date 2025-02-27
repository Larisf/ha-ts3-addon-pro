FROM arm64v8/debian:bookworm-slim

# Installiere Abhängigkeiten inklusive Python, pip und Supervisor
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    jq \
    tar \
    git \
    cmake \
    build-essential \
    libsdl2-dev \
    libx11-dev \
    python3 \
    python3-pip \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Installiere benötigte Python-Pakete mit dem Flag, um systemweite Installation zu erlauben
RUN pip3 install --break-system-packages flask

# Installiere Box64
RUN git clone https://github.com/ptitSeb/box64.git && \
    cd box64 && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo && \
    make -j$(nproc) && \
    make install && \
    cd / && \
    rm -rf box64

# Hole die neueste TS3 Server Version und bereite den Server vor
WORKDIR /app
RUN wget -O ts3server.tar.bz2 https://files.teamspeak-services.com/releases/server/3.13.7/teamspeak3-server_linux_amd64-3.13.7.tar.bz2 && \
    tar xvf ts3server.tar.bz2 --strip-components=1 && \
    rm ts3server.tar.bz2 && \
    touch .ts3server_license_accepted

# Kopiere das Flask-App-Skript und die Supervisor-Konfiguration (falls benötigt)
COPY app.py /app/app.py
COPY supervisord.conf /app/supervisord.conf

# Kopiere das angepasste entrypoint-Skript
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Starte über Supervisor
ENTRYPOINT ["/entrypoint.sh"]
