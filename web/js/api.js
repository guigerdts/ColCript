// api.js - Cliente para la API de ColCript

const API_BASE = 'http://localhost:5000/api';

// ==================== API CLIENT ====================

class ColCriptAPI {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    // Método auxiliar para hacer requests
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Error en la petición');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // ==================== INFO ====================
    
    async getInfo() {
        return this.request('/info');
    }

    // ==================== BLOCKCHAIN ====================
    
    async getBlockchain() {
        return this.request('/blockchain');
    }

    async getBlockchainInfo() {
        return this.request('/blockchain/info');
    }

    async validateBlockchain() {
        return this.request('/blockchain/validate');
    }

    async listBlockchains() {
        return this.request('/blockchain/list');
    }

    async createBlockchain(filename = 'web_blockchain.json') {
        return this.request('/blockchain/create', {
            method: 'POST',
            body: JSON.stringify({ filename })
        });
    }

    async loadBlockchain(filename) {
        return this.request('/blockchain/load', {
            method: 'POST',
            body: JSON.stringify({ filename })
        });
    }

    // ==================== WALLET ====================
    
    async createWallet(name) {
        return this.request('/wallet/create', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
    }

    async loadWallet(filename) {
        return this.request('/wallet/load', {
            method: 'POST',
            body: JSON.stringify({ filename })
        });
    }

    async getWalletBalance() {
        return this.request('/wallet/balance');
    }

    async getWalletAddress() {
        return this.request('/wallet/address');
    }

    async getWalletHistory() {
        return this.request('/wallet/history');
    }

    // ==================== TRANSACTIONS ====================
    
    async sendTransaction(recipient, amount, fee = 0.5) {
        return this.request('/transaction/send', {
            method: 'POST',
            body: JSON.stringify({ recipient, amount, fee })
        });
    }

    async getPendingTransactions() {
        return this.request('/transaction/pending');
    }

    // ==================== MINING ====================
    
    async mineBlock() {
        return this.request('/mining/mine', {
            method: 'POST'
        });
    }

    async getMiningStats() {
        return this.request('/mining/stats');
    }

    // ==================== EXPLORER ====================
    
    async getBlock(number) {
        return this.request(`/explorer/block/${number}`);
    }

    async getBlocks(limit = 10) {
        return this.request(`/explorer/blocks?limit=${limit}`);
    }

    async search(query) {
        return this.request(`/explorer/search?q=${query}`);
    }

    // ==================== STATISTICS ====================
    
    async getDashboard() {
        return this.request('/statistics/dashboard');
    }

    async getSupply() {
        return this.request('/statistics/supply');
    }

    async getTopWallets(limit = 10) {
        return this.request(`/statistics/wallets?limit=${limit}`);
    }

    // ==================== FAUCET ====================
    
    async getFaucetInfo() {
        return this.request('/faucet/info');
    }

    async claimFaucet() {
        return this.request('/faucet/claim', {
            method: 'POST'
        });
    }

    // ==================== DIFFICULTY ====================
    
    async getDifficultyInfo() {
        return this.request('/difficulty/info');
    }

    async setDifficulty(difficulty) {
        return this.request('/difficulty/set', {
            method: 'POST',
            body: JSON.stringify({ difficulty })
        });
    }

    async toggleAutoAdjustment(enabled) {
        return this.request('/difficulty/toggle', {
            method: 'POST',
            body: JSON.stringify({ enabled })
        });
    }

    async configureDifficulty(targetTime, interval) {
        return this.request('/difficulty/config', {
            method: 'POST',
            body: JSON.stringify({ 
                target_time: targetTime, 
                interval: interval 
            })
        });
    }
}

// Instancia global de la API
const api = new ColCriptAPI(API_BASE);

// Agregar métodos Advanced después de crear la instancia
api.getWalletContacts = async function(address) {
    return this.request(`/wallet/advanced/contacts?address=${address}`);
}.bind(api);

api.addWalletContact = async function(address, name, contactAddress, notes = '') {
    return this.request('/wallet/advanced/contacts', {
        method: 'POST',
        body: JSON.stringify({ address, name, contact_address: contactAddress, notes })
    });
}.bind(api);

api.removeWalletContact = async function(address, name) {
    return this.request('/wallet/advanced/contacts', {
        method: 'DELETE',
        body: JSON.stringify({ address, name })
    });
}.bind(api);

api.getWalletLabels = async function(address) {
    return this.request(`/wallet/advanced/labels?address=${address}`);
}.bind(api);

api.addWalletLabel = async function(address, labelAddress, label) {
    return this.request('/wallet/advanced/labels', {
        method: 'POST',
        body: JSON.stringify({ address, label_address: labelAddress, label })
    });
}.bind(api);

api.removeWalletLabel = async function(address, labelAddress) {
    return this.request('/wallet/advanced/labels', {
        method: 'DELETE',
        body: JSON.stringify({ address, label_address: labelAddress })
    });
}.bind(api);

api.getWalletAdvancedHistory = async function(address, limit = 20) {
    return this.request(`/wallet/advanced/history/${address}?limit=${limit}`);
}.bind(api);

api.getWalletAdvancedStats = async function(address) {
    return this.request(`/wallet/advanced/stats/${address}`);
}.bind(api);

api.searchTransaction = async function(txHash) {
    return this.request(`/explorer/advanced/search/transaction/${txHash}`);
}.bind(api);

api.searchAddressTransactions = async function(address, limit = 100) {
    return this.request(`/explorer/advanced/search/address/${address}?limit=${limit}`);
}.bind(api);

api.getTopHolders = async function(limit = 10) {
    return this.request(`/explorer/advanced/top-holders?limit=${limit}`);
}.bind(api);

api.getMinerRanking = async function(limit = 10) {
    return this.request(`/explorer/advanced/miner-ranking?limit=${limit}`);
}.bind(api);

api.getNetworkActivity = async function(days = 7) {
    return this.request(`/explorer/advanced/network-activity?days=${days}`);
}.bind(api);

api.getRealtimeStats = async function() {
    return this.request('/explorer/advanced/realtime');
}.bind(api);

api.getDifficultyHistory = async function(limit = 100) {
    return this.request(`/explorer/advanced/difficulty-history?limit=${limit}`);
}.bind(api);

api.searchByDateRange = async function(startDate, endDate) {
    return this.request(`/explorer/advanced/search/date-range?start=${startDate}&end=${endDate}`);
}.bind(api);

// ==================== HELPER FUNCTIONS ====================

// Formatear dirección (mostrar solo inicio y final)
function formatAddress(address) {
    if (!address) return '--';
    if (address.length <= 20) return address;
    return `${address.substring(0, 10)}...${address.substring(address.length - 10)}`;
}

// Formatear hash
function formatHash(hash) {
    if (!hash) return '--';
    if (hash.length <= 20) return hash;
    return `${hash.substring(0, 16)}...`;
}

// Formatear fecha
function formatDate(timestamp) {
    if (!timestamp) return '--';
    const date = new Date(timestamp * 1000);
    return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Formatear número con separadores de miles
function formatNumber(num) {
    if (num === undefined || num === null) return '--';
    return num.toLocaleString('es-ES', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });
}

// Formatear tiempo relativo
function formatTimeAgo(timestamp) {
    if (!timestamp) return '--';
    const now = Date.now() / 1000;
    const diff = now - timestamp;
    
    if (diff < 60) return 'hace un momento';
    if (diff < 3600) return `hace ${Math.floor(diff / 60)} min`;
    if (diff < 86400) return `hace ${Math.floor(diff / 3600)} h`;
    return `hace ${Math.floor(diff / 86400)} días`;
}

// Copiar al portapapeles
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copiado al portapapeles', 'success');
    } catch (err) {
        console.error('Error al copiar:', err);
        showToast('Error al copiar', 'error');
    }
}

// ==================== EXPORT ====================

// Hacer disponible globalmente
window.api = api;
window.formatAddress = formatAddress;
window.formatHash = formatHash;
window.formatDate = formatDate;
window.formatNumber = formatNumber;
window.formatTimeAgo = formatTimeAgo;
window.copyToClipboard = copyToClipboard;
