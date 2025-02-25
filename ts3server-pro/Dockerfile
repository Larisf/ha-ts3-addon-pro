#FROM arm64v8/node:20-bookworm-slim
# Explizite ARMv7/ARMv8 Architektur angeben
FROM --platform=linux/arm/v7 python:3.11-slim-bookworm

# 1. Korrigierte Paketquellen für ARM64
RUN echo "deb http://deb.debian.org/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list

# 2. Basis-Pakete installieren
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    apt-transport-https \
    gnupg \
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
    python3-dev \
    libssl-dev \
    libffi-dev \
    gcc \
    g++ \
    && apt-get clean

# 3. MariaDB Repository hinzufügen
RUN apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc' && \
    echo "deb [arch=arm64] https://mirror.rackspace.com/mariadb/repo/10.11/debian bookworm main" > /etc/apt/sources.list.d/mariadb.list

# 4. Datenbank-Pakete installieren
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sqlite3 \
    libsqlite3-dev \
    mariadb-client \
    libmariadb-dev && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/include/mariadb /usr/include/mysql && \
    ln -s /usr/lib/aarch64-linux-gnu/libmariadb.so /usr/lib/aarch64-linux-gnu/libmysqlclient.so

# 5. Box64 kompilieren
RUN git clone https://github.com/ptitSeb/box64.git && \
    cd box64 && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DARM_DYNAREC=ON && \
    make -j$(nproc) && \
    make install && \
    cd / && \
    rm -rf box64

# 6. Python Abhängigkeiten
RUN pip3 install --no-cache-dir \
    ts3py \
    pymysql \
    cryptography

# 7. Anwendungsverzeichnis erstellen
WORKDIR /app
COPY . .

# 8. Node.js Abhängigkeiten
RUN npm install --production \
    express \
    ws \
    body-parser \
    multer \
    mysql2

# 9. Berechtigungen setzen
RUN chmod +x /app/scripts/*.sh && \
    chmod +x /app/entrypoint.sh

# 10. Ports und Umgebungsvariablen
EXPOSE 8099 9987/udp 10011 30033
ENV NODE_ENV=production

# Startscript
ENTRYPOINT ["/app/entrypoint.sh"]
