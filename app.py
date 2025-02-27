#!/usr/bin/env python3
from flask import Flask, request, send_from_directory, render_template_string
import os
import subprocess

app = Flask(__name__)
CONFIG_DIR = '/config'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>TeamSpeak 3 Server</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 600px;
            margin-top: 50px;
        }
        .card {
            border-radius: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        .btn-primary {
            background-color: #007bff;
            border: none;
        }
        .btn-primary:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card p-4">
            <h2 class="text-center">TeamSpeak 3 Server Verwaltung</h2>
            
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

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
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

@app.route('/backup', methods=['POST'])
def backup():
    backup_file = os.path.join(CONFIG_DIR, 'backup.tar.gz')
    subprocess.run(['tar', 'czf', backup_file, CONFIG_DIR])
    return send_from_directory(CONFIG_DIR, 'backup.tar.gz', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
