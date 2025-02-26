from flask import Flask, request, send_file, render_template_string, redirect, url_for, flash
import os
import datetime
import tarfile
import telnetlib

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Für Flash-Messages

# TS3 Query Server Einstellungen
TS3_SERVER_HOST = "localhost"  # Falls TS3 im gleichen Container läuft, bleibt das so
TS3_SERVER_PORT = 10011
TS3_SERVER_USER = "serveradmin"
TS3_SERVER_PASSWORD = ""
TS3_VIRTUAL_SERVER_ID = 1

# HTML-Template für die GUI
HTML_TEMPLATE = '''
<!doctype html>
<html lang="de">
  <head>
    <meta charset="utf-8">
    <title>TS3 Server Verwaltung</title>
    <style>
      body { font-family: Arial, sans-serif; text-align: center; background: #f8f9fa; padding: 20px; }
      h1, h2 { color: #343a40; }
      button { background-color: #28a745; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 5px; font-size: 16px; }
      button:hover { background-color: #218838; }
      ul { list-style-type: none; padding: 0; display: inline-block; text-align: left; }
      li { background: #ffffff; margin: 5px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
      .container { max-width: 600px; margin: auto; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
    </style>
  </head>
  <body>
    <div class="container">
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
      <h2>Aktuell verbundene Nutzer</h2>
      <ul>
        {% for user in users %}
          <li>{{ user }}</li>
        {% endfor %}
      </ul>
      {% with messages = get_flashed_messages() %}
        {% if messages %}
          <ul>
            {% for message in messages %}
              <li>{{ message }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}
    </div>
  </body>
</html>
'''

@app.route('/')
def index():
    users = []  # Platzhalter für TS3-Benutzer
    return render_template_string(HTML_TEMPLATE, users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
