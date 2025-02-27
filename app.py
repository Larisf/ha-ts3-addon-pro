#!/usr/bin/env python3
import io
import tarfile
import os
import subprocess
from flask import Flask, request, send_from_directory, render_template_string, send_file

app = Flask(__name__)
CONFIG_DIR = "/config"
BACKUP_DIR = "/backup"
os.makedirs(BACKUP_DIR, exist_ok=True)  # Sicherstellen, dass das Backup-Verzeichnis existiert

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>TeamSpeak 3 Server</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <style>
        :root {
            --bg-color: #f8f9fa;
            --text-color: #212529;
            --card-bg: #ffffff;
            --btn-primary: #007bff;
            --btn-secondary: #6c757d;
        }
        [data-theme="dark"] {
            --bg-color: #212529;
            --text-color: #f8f9fa;
            --card-bg: #343a40;
            --btn-primary: #0d6efd;
            --btn-secondary: #adb5bd;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: Arial, sans-serif;
            transition: background 0.3s, color 0.3s;
        }
        .container {
            max-width: 600px;
            margin-top: 50px;
        }
        .card {
            border-radius: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            background-color: var(--card-bg);
            transition: background 0.3s;
        }
        .btn-primary {
            background-color: var(--btn-primary);
            border: none;
        }
        .btn-primary:hover {
            background-color: #0056b3;
        }
        .btn-secondary {
            background-color: var(--btn-secondary);
            border: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card p-4">
            <h2 class="text-center">TeamSpeak 3 Server Verwaltung</h2>

            <button onclick="toggleTheme()" class="btn btn-secondary mb-3">🌙/☀️ Dark Mode</button>

            <h4 class="mt-4">Lizenz hochladen</h4>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <input type="file" name="license" accept=".dat" class="form-control">
                </div>
                <button type="submit" class="btn btn-primary w-100">Upload LICENSEKEY.DAT</button>
            </form>

            <hr>

            <h4 class="mt-4">Backup erstellen</h4>
            <form action="/backup" method="post">
                <button type="submit" class="btn btn-secondary w-100">Backup erstellen</button>
            </form>
        </div>
    </div>

    <script>
        function toggleTheme() {
            const currentTheme = document.body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }

        (function () {
            const savedTheme = localStorage.getItem('theme') || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
            document.body.setAttribute('data-theme', savedTheme);
        })();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload():
    if 'license' not in request.files:
        return "Fehlende Datei", 400
    file = request.files['license']
    if file.filename == '':
        return "Keine Datei ausgewählt", 400
    filepath = os.path.join(CONFIG_DIR, 'LICENSEKEY.DAT')
    file.save(filepath)
    return "Lizenz erfolgreich hochgeladen"

@app.route("/backup", methods=["POST"])
def backup():
    
    try:
        # Erstelle ein in-memory tar.gz-Archiv
        backup_io = io.BytesIO()
        with tarfile.open(fileobj=backup_io, mode="w:gz") as tar:
            tar.add(CONFIG_DIR, arcname=os.path.basename(CONFIG_DIR))

        # Setze den Zeiger zurück, damit die Datei vom Anfang gelesen werden kann
        backup_io.seek(0)

        # Datei an den Browser senden, damit sie heruntergeladen wird
        return send_file(backup_io, as_attachment=True, download_name="backup.tar.gz", mimetype="application/gzip")

    except Exception as e:
        return f"Fehler beim Erstellen des Backups: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
