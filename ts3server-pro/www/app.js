// Backup Funktionen
document.getElementById('create-backup').addEventListener('click', () => {
  fetch('/backup', { method: 'POST' })
    .then(response => response.json())
    .then(data => showNotification(`Backup erstellt: ${data.file}`));
});

// Lizenz Upload
function uploadLicense() {
  const file = document.getElementById('license-upload').files[0];
  const formData = new FormData();
  formData.append('license', file);

  fetch('/upload-license', {
    method: 'POST',
    body: formData
  }).then(() => showNotification('Lizenz erfolgreich aktualisiert'));
}

// SQL Abfragen
function runQuery() {
  const query = document.getElementById('sql-query').value;
  ws.send(JSON.stringify({
    action: 'run_query',
    data: { query }
  }));
}

// WebSocket Handler
ws.onmessage = (event) => {
  const result = JSON.parse(event.data);
  document.getElementById('query-result').innerHTML = 
    `<pre>${JSON.stringify(result, null, 2)}</pre>`;
};
