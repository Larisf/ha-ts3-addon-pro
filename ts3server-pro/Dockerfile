FROM arm64v8/node:20-bookworm-slim

# Installiere alle Abhängigkeiten
RUN apt-get update && apt-get install -y \
    wget curl jq tar git cmake build-essential \
    libsdl2-dev libx11-dev python3 python3-pip \
    mysql-client libmysqlclient-dev && \
    pip3 install ts3py mysql-connector-python && \
    rm -rf /var/lib/apt/lists/*

# Box64 kompilieren
RUN git clone https://github.com/ptitSeb/box64.git && \
    cd box64 && mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo && \
    make -j$(nproc) && make install

# Konfiguration
WORKDIR /app
COPY . .

# Installiere Node-Module
RUN npm install express ws body-parcer multer mysql2

# Berechtigungen setzen
RUN chmod +x /app/scripts/*.sh && \
    chmod +x /app/entrypoint.sh

EXPOSE 8099
ENTRYPOINT ["/app/entrypoint.sh"]
