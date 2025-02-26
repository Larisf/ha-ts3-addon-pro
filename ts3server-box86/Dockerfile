FROM arm64v8/debian:bookworm-slim

# Installiere Basis-Abhängigkeiten
RUN apt-get update && apt-get install -y \
    wget \
    curl \
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
    inotify-tools \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Python Virtual Environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Python-Abhängigkeiten
RUN pip install --no-cache-dir --upgrade pip && \
    pip install \
    Flask==2.0.3 \
    werkzeug==2.0.3

RUN git clone https://github.com/benediktschmitt/py-ts3.git && \
    cd py-ts3 && \
    pip install .


# Box64 kompilieren
RUN git clone https://github.com/ptitSeb/box64.git && \
    cd box64 && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DARM_DYNAREC=ON -GNinja && \
    ninja && \
    ninja install && \
    cd / && \
    rm -rf box64

# TeamSpeak Server installieren
WORKDIR /app
RUN wget -O ts3server.tar.bz2 https://files.teamspeak-services.com/releases/server/3.13.7/teamspeak3-server_linux_amd64-3.13.7.tar.bz2 && \
    tar xvf ts3server.tar.bz2 --strip-components=1 && \
    rm ts3server.tar.bz2 && \
    touch .ts3server_license_accepted

# Copy Files
COPY entrypoint.sh /entrypoint.sh
COPY api.py /app/
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
