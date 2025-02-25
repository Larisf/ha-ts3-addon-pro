from flask import Flask, send_from_directory, jsonify
import sqlite3
import os

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return send_from_directory('www', 'index.html')
    
    @app.route('/clients')
    def get_clients():
        try:
            conn = sqlite3.connect('/app/ts3server.sqlitedb')
            c = conn.cursor()
            c.execute("SELECT name,client_id FROM clients")
            clients = [{"name": row[0], "id": row[1]} for row in c.fetchall()]
            return jsonify(clients)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app
