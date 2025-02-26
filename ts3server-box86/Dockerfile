FROM arm64v8/debian:bookworm-slim

# Installiere Basis-Abhängigkeiten
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
    python3-venv \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*


# Erstelle virtuelles Python-Environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installiere Python-Pakete im virtuellen Environment
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install \
    Flask==2.0.3 \
    python-ts3==4.1.0 \
    Werkzeug==2.0.3

# Box64 kompilieren
RUN git clone https://github.com/ptitSeb/box64.git && \
    cd box64 && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DARM_DYNAREC=ON && \
    make -j$(nproc) && \
    make install && \
    cd / && \
    rm -rf box64

# TeamSpeak Server installieren
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
