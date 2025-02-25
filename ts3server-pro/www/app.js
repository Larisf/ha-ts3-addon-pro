document.addEventListener('DOMContentLoaded', () => {
    const clientList = document.getElementById('client-list');
    const refreshBtn = document.getElementById('refresh');

    async function updateClients() {
        try {
            const response = await fetch('/clients');
            const clients = await response.json();
            
            clientList.innerHTML = clients.map(client => `
                <div class="client-card">
                    <h3>${client.name}</h3>
                    <sl-badge>ID: ${client.id}</sl-badge>
                </div>
            `).join('');
        } catch (error) {
            console.error('Fehler:', error);
        }
    }

    refreshBtn.addEventListener('click', updateClients);
    setInterval(updateClients, 10000); // Auto-Update alle 10 Sekunden
    updateClients();
});
