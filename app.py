from flask import Flask, request, send_from_directory
import os
import subprocess

app = Flask(__name__, static_folder='web')

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/backup', methods=['POST'])
def backup():
    subprocess.run(['tar', 'czvf', '/backup/ts3_backup.tar.gz', '.'])
    return "Backup erstellt!"

@app.route('/upload_license', methods=['POST'])
def upload_license():
    if 'license' not in request.files:
        return "Keine Datei hochgeladen"
    file = request.files['license']
    if file.filename == '':
        return "Keine Datei ausgewählt"
    if file:
        file.save(os.path.join('/app', 'LICENSEKEY.DAT'))
        return "Lizenz hochgeladen!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)