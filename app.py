from flask import Flask, request, send_file, render_template_string, redirect, url_for, flash
import os
import datetime
import tarfile

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Für Flash-Messages

# HTML-Template für die GUI
HTML_TEMPLATE = '''
<!doctype html>
<html lang="de">
  <head>
    <meta charset="utf-8">
    <title>TS3 Server Verwaltung</title>
  </head>
  <body>
    <h1>TS3 Server Verwaltung</h1>
    <h2>Backup erstellen</h2>
    <form action="/backup" method="post">
      <button type="submit">Backup erstellen</button>
    </form>
    <h2>LICENSEKEY hochladen</h2>
    <form action="/upload-license" method="post" enctype="multipart/form-data">
      <input type="file" name="licensefile" accept=".dat">
      <button type="submit">Hochladen</button>
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
  </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/backup', methods=['POST'])
def backup():
    backup_filename = f"ts3_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
    backup_path = os.path.join('/app', backup_filename)
    # Erstelle ein Backup des /app Verzeichnisses (die gerade erstellte Backup-Datei wird ausgeschlossen)
    with tarfile.open(backup_path, "w:gz") as tar:
        def exclude_backup(tarinfo):
            if tarinfo.name.startswith(backup_filename):
                return None
            return tarinfo
        tar.add('/app', arcname='.', filter=exclude_backup)
    return send_file(backup_path, as_attachment=True)

@app.route('/upload-license', methods=['POST'])
def upload_license():
    if 'licensefile' not in request.files:
        flash("Keine Datei hochgeladen.")
        return redirect(url_for('index'))
    file = request.files['licensefile']
    if file.filename == '':
        flash("Keine Datei ausgewählt.")
        return redirect(url_for('index'))
    if file and file.filename.endswith('.dat'):
        # Speichere die LICENSEKEY.dat im persistenten Config-Verzeichnis
        license_path = '/config/LICENSEKEY.dat'
        file.save(license_path)
        flash("LICENSEKEY.dat erfolgreich hochgeladen. Bitte Container neu starten, damit die Lizenz aktiviert wird.")
    else:
        flash("Ungültige Datei. Bitte eine .dat Datei hochladen.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Starte die Flask-App auf Port 5000 und binde an alle Interfaces
    app.run(host='0.0.0.0', port=5000)
