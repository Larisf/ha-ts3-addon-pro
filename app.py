from flask import Flask, request, send_from_directory, render_template_string
import os, subprocess

app = Flask(__name__)
CONFIG_DIR = '/config'

@app.route('/')
def index():
    # Einfaches HTML-Template – hier kannst du natürlich weiter CSS/JS einbinden
    return render_template_string('''
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <title>Teamspeak Server GUI</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 2em; }
          form { margin-bottom: 1em; }
          input[type="submit"] { padding: 0.5em 1em; }
        </style>
      </head>
      <body>
        <h1>Teamspeak Server GUI</h1>
        <h2>Lizenz hochladen</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
          <input type="file" name="license" accept=".dat">
          <input type="submit" value="Upload LICENSEKEY.DAT">
        </form>
        <h2>Backup erstellen</h2>
        <form action="/backup" method="post">
          <input type="submit" value="Backup erstellen">
        </form>
      </body>
    </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    if 'license' not in request.files:
        return "Datei fehlt", 400
    file = request.files['license']
    if file.filename == '':
        return "Keine Datei ausgewählt", 400
    filepath = os.path.join(CONFIG_DIR, 'LICENSEKEY.DAT')
    file.save(filepath)
    return "Lizenz erfolgreich hochgeladen"

@app.route('/backup', methods=['POST'])
def backup():
    backup_file = os.path.join(CONFIG_DIR, 'backup.tar.gz')
    # Erstelle ein tar.gz-Archiv des Konfigurationsverzeichnisses
    subprocess.run(['tar', 'czf', backup_file, CONFIG_DIR])
    return send_from_directory(CONFIG_DIR, 'backup.tar.gz', as_attachment=True)

if __name__ == '__main__':
    # Wichtige Einstellung: Damit der Flask-Server über Ingress erreichbar ist
    app.run(host='0.0.0.0', port=5000)
