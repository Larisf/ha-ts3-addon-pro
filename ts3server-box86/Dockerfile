FROM arm64v8/debian:bookworm-slim

# Installiere Abhängigkeiten
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
    && rm -rf /var/lib/apt/lists/*

# Installiere Python-Pakete
RUN pip3 install Flask ts3

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

# TeamSpeak Server vorbereiten
WORKDIR /app
RUN wget -O ts3server.tar.bz2 https://files.teamspeak-services.com/releases/server/3.13.7/teamspeak3-server_linux_amd64-3.13.7.tar.bz2 && \
    tar xvf ts3server.tar.bz2 --strip-components=1 && \
    rm ts3server.tar.bz2 && \
    touch .ts3server_license_accepted

# Füge diese Zeilen hinzu
COPY password_watcher.sh /
RUN chmod +x /password_watcher.sh

# Ändere den ENTRYPOINT
ENTRYPOINT ["/bin/bash", "-c", "/password_watcher.sh & /entrypoint.sh"]
# Kopiere Dateien
COPY entrypoint.sh /
COPY api.py /app/
COPY ts3-panel.js /app/
COPY ts3-panel.css /app/
RUN chmod +x /entrypoint.sh
