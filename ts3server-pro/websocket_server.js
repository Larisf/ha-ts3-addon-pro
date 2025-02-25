const express = require('express');
const WebSocket = require('ws');
const multer = require('multer');
const mysql = require('mysql2/promise');
const fs = require('fs');
const { exec } = require('child_process');

const app = express();
const upload = multer({ dest: '/license' });
const wss = new WebSocket.Server({ port: 8099 });

// MySQL Verbindung
let mysqlPool;
if (process.env.MYSQL_HOST) {
  mysqlPool = mysql.createPool({
    host: process.env.MYSQL_HOST,
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database: process.env.MYSQL_DATABASE
  });
}

// Backup Endpoint
app.post('/backup', async (req, res) => {
  const backupName = `backup_${Date.now()}.tar.gz`;
  exec(`tar -czf /backup/${backupName} /config/ts3server`, (error) => {
    if (error) return res.status(500).send(error);
    res.json({ status: 'success', file: backupName });
  });
});

// License Upload
app.post('/upload-license', upload.single('license'), (req, res) => {
  fs.renameSync(req.file.path, `/license/ts3server.ini`);
  res.json({ status: 'success' });
});

// WebSocket Handler
wss.on('connection', (ws) => {
  ws.on('message', async (message) => {
    const { action, data } = JSON.parse(message);
    
    try {
      switch(action) {
        case 'get_clients':
          const [clients] = await mysqlPool.query('SELECT * FROM clients');
          ws.send(JSON.stringify(clients));
          break;
        case 'run_query':
          const [result] = await mysqlPool.query(data.query);
          ws.send(JSON.stringify(result));
          break;
      }
    } catch (error) {
      console.error(error);
    }
  });
});

app.use(express.static('/www'));
app.listen(3000);
