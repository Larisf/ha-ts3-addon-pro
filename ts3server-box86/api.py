from flask import Flask, jsonify
from ts3.query import TS3QueryConnection
import os

app = Flask(__name__)
PASSWORD = os.environ.get('SERVERADMIN_PASSWORD', '')

@app.route('/clients')
def get_clients():
    try:
        with TS3QueryConnection("127.0.0.1", 10011) as ts3:
            ts3.login("serveradmin", PASSWORD)
            clients = ts3.clientlist()
            return jsonify([{
                "id": client["clid"],
                "name": client["client_nickname"],
                "channel": client["cid"]
            } for client in clients])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/kick/<int:client_id>', methods=['POST'])
def kick_client(client_id):
    try:
        with TS3QueryConnection("127.0.0.1", 10011) as ts3:
            ts3.login("serveradmin", PASSWORD)
            ts3.clientkick(clid=client_id, reasonid=5)
            return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
