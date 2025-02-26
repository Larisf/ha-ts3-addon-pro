from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/clients')
def get_clients():
    try:
        output = subprocess.check_output([
            '/app/ts3server_linux_amd64/ts3server_startscript.sh',
            'status'
        ])
        return jsonify({"status": "running", "clients": extract_clients(output)})
    except:
        return jsonify({"status": "error"})

def extract_clients(output):
    # Hier die Logik zur Extraktion der Client-Liste
    return [{"name": "Testuser", "id": 1}]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
