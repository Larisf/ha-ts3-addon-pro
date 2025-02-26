class TS3Panel extends HTMLElement {
  setConfig(config) {
    this.config = config;
    this.innerHTML = `
      <ha-card header="TeamSpeak 3 Management">
        <div class="card-content">
          <div id="clients-list" style="margin-bottom: 16px;"></div>
          <div class="actions">
            <mwc-button raised @click=${() => this.refresh()}>
              <ha-icon icon="mdi:refresh"></ha-icon>
              Aktualisieren
            </mwc-button>
          </div>
        </div>
      </ha-card>
    `;
    this.refresh();
  }

  async refresh() {
    const list = this.querySelector('#clients-list');
    list.innerHTML = '<div style="text-align: center;">Lade Daten...</div>';
    
    try {
      const response = await fetch('/api/ts3/clients');
      const clients = await response.json();
      this.renderClients(clients);
    } catch (error) {
      list.innerHTML = `<div class="error">Fehler: ${error.message}</div>`;
    }
  }

  renderClients(clients) {
    const list = this.querySelector('#clients-list');
    list.innerHTML = clients.map(client => `
      <div class="client">
        <ha-icon icon="mdi:account-voice"></ha-icon>
        <div class="client-info">
          <div class="name">${client.name}</div>
          <div class="channel">Channel ID: ${client.channel}</div>
        </div>
        <mwc-icon-button 
          icon="mdi:exit-to-app" 
          @click=${() => this.kickClient(client.id)}>
        </mwc-icon-button>
      </div>
    `).join('');
  }

  async kickClient(clientId) {
    if (confirm('Möchten Sie diesen Benutzer wirklich kicken?')) {
      try {
        await fetch(`/api/ts3/kick/${clientId}`, {method: 'POST'});
        this.refresh();
      } catch (error) {
        alert(`Fehler: ${error.message}`);
      }
    }
  }
}

customElements.define('ts3-panel', TS3Panel);
