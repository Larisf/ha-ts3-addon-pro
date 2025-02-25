from flask import Flask, send_from_directory, request
import sqlite3, os, subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('www', 'index.html')

@app.route('/backup', methods=['POST'])
def create_backup():
    subprocess.run(["/app/scripts/backup.sh"])
    return {"status": "success"}

@app.route('/upload-license', methods=['POST'])
def upload_license():
    file = request.files['license']
    file.save('/app/.ts3server_license_accepted')
    return {"status": "success"}

@app.route('/clients')
def get_clients():
    conn = sqlite3.connect('/app/ts3server.sqlitedb')
    c = conn.cursor()
    c.execute("SELECT * FROM clients")
    return {"clients": c.fetchall()}

if __name__ == "__main__":
    app.run()
