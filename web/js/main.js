// main.js - Lógica principal de la interfaz

// ==================== STATE ====================

let currentWallet = null;
let updateInterval = null;

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🪙 ColCript Web UI iniciada');
    
    // Setup navigation
    setupNavigation();
    
    // Check API connection
    checkConnection();
    
    // Load dashboard
    loadDashboard();
    
    // Start auto-update
    startAutoUpdate();
});

// ==================== NAVIGATION ====================

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all links and pages
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            
            // Add active class to clicked link
            link.classList.add('active');
            
            // Show corresponding page
            const pageId = link.dataset.page;
            const page = document.getElementById(pageId);
            if (page) {
                page.classList.add('active');
                
                // Load page data
                loadPageData(pageId);
            }
        });
    });
}

function loadPageData(pageId) {
    switch(pageId) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'wallet':
            loadWalletPage();
            break;
        case 'mining':
            loadMiningPage();
            break;
        case 'explorer':
            loadExplorerPage();
            break;
        case 'faucet':
            loadFaucetPage();
            break;
        case 'contracts':
            loadContractsPage();
            break;
        case 'network':
            loadNetworkPage();
            break;
        case 'settings':
            loadSettingsPage();
            break;
    }
}

// ==================== CONNECTION ====================

async function checkConnection() {
    const statusEl = document.getElementById('connectionStatus');
    const statusDot = statusEl.querySelector('.status-dot');
    
    try {
        const info = await api.getInfo();
        
        if (info.success) {
            statusDot.classList.add('connected');
            statusEl.querySelector('span:last-child').textContent = 'Conectado';
        }
    } catch (error) {
        statusDot.classList.remove('connected');
        statusEl.querySelector('span:last-child').textContent = 'Desconectado';
        showToast('Error de conexión con la API', 'error');
    }
}

// ==================== DASHBOARD ====================

async function loadDashboard() {
    try {
        // Get dashboard data
        const dashboard = await api.getDashboard();
        const blockchainInfo = await api.getBlockchainInfo();
        const difficultyInfo = await api.getDifficultyInfo();
        
        if (dashboard.success) {
            const data = dashboard.data;
            
            // Update stats
            document.getElementById('circulating').textContent = 
                formatNumber(data.supply.circulating) + ' CLC';
            
            document.getElementById('totalBlocks').textContent = 
                data.network.total_blocks;
            
            document.getElementById('difficulty').textContent = 
                data.network.network_difficulty;
            
            // Difficulty status
            const diffStatus = document.getElementById('difficultyStatus');
            if (difficultyInfo.success) {
                const avgTime = difficultyInfo.data.current_avg_time;
                const targetTime = difficultyInfo.data.target_block_time;
                
                if (avgTime > 0) {
                    if (avgTime < targetTime * 0.5) {
                        diffStatus.textContent = '⚡ Muy rápido';
                    } else if (avgTime < targetTime * 0.75) {
                        diffStatus.textContent = '🔥 Rápido';
                    } else if (avgTime > targetTime * 2) {
                        diffStatus.textContent = '🐌 Muy lento';
                    } else if (avgTime > targetTime * 1.5) {
                        diffStatus.textContent = '🕐 Lento';
                    } else {
                        diffStatus.textContent = '✅ Óptimo';
                    }
                } else {
                    diffStatus.textContent = 'Calculando...';
                }
            }
            
            // Update wallet balance
            try {
                const balance = await api.getWalletBalance();
                if (balance.success) {
                    document.getElementById('myBalance').textContent = 
                        formatNumber(balance.data.balance) + ' CLC';
                    document.getElementById('walletStatus').textContent = 
                        balance.data.wallet;
                    currentWallet = balance.data;
                }
            } catch {
                document.getElementById('myBalance').textContent = '-- CLC';
                document.getElementById('walletStatus').textContent = 'Sin wallet';
                currentWallet = null;
            }
            
            // Update charts
            updateCharts();
        }
        
        // Load recent blocks
        loadRecentBlocks();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Error cargando dashboard', 'error');
    }
}

async function loadRecentBlocks() {
    const container = document.getElementById('recentBlocks');
    
    try {
        const blocks = await api.getBlocks(5);
        
        if (blocks.success && blocks.data.blocks.length > 0) {
            container.innerHTML = '';
            
            blocks.data.blocks.reverse().forEach(block => {
                const blockEl = document.createElement('div');
                blockEl.className = 'block-item';
                blockEl.innerHTML = `
                    <div class="block-number">#${block.index}</div>
                    <div class="block-info">
                        <div class="block-hash" onclick="copyToClipboard('${block.hash}')" style="cursor: pointer;" title="Click para copiar">
                            ${formatHash(block.hash)}
                        </div>
                        <div class="block-meta">
                            <span>⛏️ ${formatAddress(block.miner)}</span>
                            <span>📝 ${block.transactions} tx</span>
                            <span>🕐 ${formatTimeAgo(block.timestamp)}</span>
                        </div>
                    </div>
                    <button class="btn btn-secondary" onclick="viewBlock(${block.index})">
                        Ver
                    </button>
                `;
                container.appendChild(blockEl);
            });
        } else {
            container.innerHTML = '<p class="no-data">No hay bloques</p>';
        }
    } catch (error) {
        console.error('Error loading blocks:', error);
        container.innerHTML = '<p class="no-data">Error cargando bloques</p>';
    }
}

// ==================== WALLET PAGE ====================

async function loadWalletPage() {
    try {
        const balance = await api.getWalletBalance();
        
        if (balance.success) {
            const info = document.getElementById('walletInfo');
            info.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div>
                        <strong>Nombre:</strong> ${balance.data.wallet}
                    </div>
                    <div>
                        <strong>Balance:</strong> ${formatNumber(balance.data.balance)} CLC
                    </div>
                    <div>
                        <strong>Dirección:</strong><br>
                        <span style="font-family: monospace; font-size: 0.85rem; word-break: break-all; cursor: pointer;" 
                              onclick="copyToClipboard('${balance.data.address}')"
                              title="Click para copiar">
                            ${balance.data.address}
                        </span>
                    </div>
                </div>
            `;
            
            currentWallet = balance.data;
            
            // Load transaction history
            loadTransactionHistory();
        }
    } catch {
        document.getElementById('walletInfo').innerHTML = 
            '<p class="no-data">No hay wallet cargada</p>';
        currentWallet = null;
    }
}

async function loadTransactionHistory() {
    const container = document.getElementById('transactionHistory');
    
    try {
        const history = await api.getWalletHistory();
        
        if (history.success && history.data.transactions.length > 0) {
            const txs = history.data.transactions.slice(0, 10); // Últimas 10
            
            container.innerHTML = '<div style="display: flex; flex-direction: column; gap: 0.8rem;"></div>';
            const list = container.querySelector('div');
            
            txs.forEach(tx => {
                const txEl = document.createElement('div');
                txEl.style.cssText = 'padding: 1rem; background: var(--dark-light); border-radius: 8px; border: 1px solid var(--border);';
                
                let type = '';
                let typeColor = '';
                
                if (tx.sender === 'MINING') {
                    type = '⛏️ Minado';
                    typeColor = 'var(--success)';
                } else if (tx.sender === currentWallet.address) {
                    type = '📤 Enviado';
                    typeColor = 'var(--danger)';
                } else {
                    type = '📥 Recibido';
                    typeColor = 'var(--success)';
                }
                
                txEl.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="color: ${typeColor}; font-weight: bold;">${type}</span>
                        <span style="font-size: 0.85rem; color: var(--text-secondary);">
                            ${formatDate(tx.timestamp)}
                        </span>
                    </div>
                    <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">
                        ${formatNumber(tx.amount)} CLC
                    </div>
                    ${tx.fee > 0 ? `<div style="font-size: 0.85rem; color: var(--text-secondary);">Fee: ${tx.fee} CLC</div>` : ''}
                `;
                
                list.appendChild(txEl);
            });
        } else {
            container.innerHTML = '<p class="no-data">Sin transacciones</p>';
        }
    } catch (error) {
        console.error('Error loading history:', error);
        container.innerHTML = '<p class="no-data">Error cargando historial</p>';
    }
}

// ==================== MINING PAGE ====================

async function loadMiningPage() {
    try {
        // Update mining info
        const info = await api.getInfo();
        const pending = await api.getPendingTransactions();
        const difficulty = await api.getDifficultyInfo();
        
        if (info.success) {
            document.getElementById('miningReward').textContent = 
                info.data.mining_reward + ' CLC';
        }
        
        if (difficulty.success) {
            document.getElementById('miningDifficulty').textContent = 
                difficulty.data.current_difficulty;
        }
        
        if (pending.success) {
            document.getElementById('pendingTx').textContent = 
                pending.data.count;
        }
        
        // Load mining stats
        const stats = await api.getMiningStats();
        if (stats.success) {
            const data = stats.data;
            const container = document.getElementById('miningStatsContent');
            
            container.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>Mineros activos:</span>
                        <strong>${data.total_miners || 0}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Bloques minados:</span>
                        <strong>${data.total_blocks_mined || 0}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Tiempo promedio:</span>
                        <strong>${(data.avg_block_time || 0).toFixed(2)}s</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Hashrate estimado:</span>
                        <strong>${formatNumber(data.estimated_hashrate || 0)} H/s</strong>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading mining page:', error);
    }
}

// ==================== EXPLORER PAGE ====================

async function loadExplorerPage() {
    loadAllBlocks();
}

async function loadAllBlocks() {
    const container = document.getElementById('allBlocks');
    container.innerHTML = '<p class="loading">Cargando bloques...</p>';
    
    try {
        const blockchain = await api.getBlockchain();
        
        if (blockchain.success && blockchain.data.chain.length > 0) {
            container.innerHTML = '<div style="display: flex; flex-direction: column; gap: 1rem;"></div>';
            const list = container.querySelector('div');
            
            // Mostrar en orden inverso (más reciente primero)
            blockchain.data.chain.reverse().forEach(block => {
                const blockEl = document.createElement('div');
                blockEl.className = 'block-item';
                blockEl.style.cursor = 'pointer';
                blockEl.onclick = () => viewBlock(block.index);
                
                blockEl.innerHTML = `
                    <div class="block-number">#${block.index}</div>
                    <div class="block-info">
                        <div class="block-hash">${formatHash(block.hash)}</div>
                        <div class="block-meta">
                            <span>⛏️ ${formatAddress(block.miner)}</span>
                            <span>📝 ${block.transactions_count} tx</span>
                            <span>🎲 Nonce: ${block.nonce}</span>
                            <span>🕐 ${formatTimeAgo(block.timestamp)}</span>
                        </div>
                    </div>
                `;
                
                list.appendChild(blockEl);
            });
        } else {
            container.innerHTML = '<p class="no-data">No hay bloques</p>';
        }
    } catch (error) {
        console.error('Error loading blocks:', error);
        container.innerHTML = '<p class="no-data">Error cargando bloques</p>';
    }
}

async function searchBlock() {
    const blockNumber = document.getElementById('blockNumber').value;
    
    if (!blockNumber) {
        showToast('Ingresa un número de bloque', 'warning');
        return;
    }
    
    await viewBlock(parseInt(blockNumber));
}

async function viewBlock(blockNumber) {
    const container = document.getElementById('blockDetails');
    const content = document.getElementById('blockDetailsContent');
    
    container.style.display = 'block';
    content.innerHTML = '<p class="loading">Cargando bloque...</p>';
    
    // Switch to explorer page if not there
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelector('[data-page="explorer"]').classList.add('active');
    document.getElementById('explorer').classList.add('active');
    
    try {
        const block = await api.getBlock(blockNumber);
        
        if (block.success) {
            const b = block.data.block;
            const txs = block.data.transactions;
            
            content.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div><strong>Índice:</strong> #${b.index}</div>
                    <div><strong>Hash:</strong><br>
                        <span style="font-family: monospace; font-size: 0.85rem; word-break: break-all; cursor: pointer;"
                              onclick="copyToClipboard('${b.hash}')" title="Click para copiar">
                            ${b.hash}
                        </span>
                    </div>
                    <div><strong>Hash Anterior:</strong><br>
                        <span style="font-family: monospace; font-size: 0.85rem; word-break: break-all;">
                            ${b.previous_hash}
                        </span>
                    </div>
                    <div><strong>Minero:</strong><br>
                        <span style="font-family: monospace; font-size: 0.85rem; word-break: break-all;">
                            ${b.miner}
                        </span>
                    </div>
                    <div><strong>Timestamp:</strong> ${formatDate(b.timestamp)}</div>
                    <div><strong>Nonce:</strong> ${formatNumber(b.nonce)}</div>
                    <div><strong>Dificultad:</strong> ${b.difficulty}</div>
                    <div><strong>Transacciones:</strong> ${b.transactions_count}</div>
                    <div><strong>Monto Total:</strong> ${formatNumber(b.total_amount)} CLC</div>
                    
                    <hr style="border-color: var(--border);">
                    
                    <h4>📝 Transacciones:</h4>
                    ${txs.map(tx => `
                        <div style="padding: 1rem; background: var(--dark-light); border-radius: 8px; margin-top: 0.5rem;">
                            <div><strong>De:</strong> ${tx.sender === 'MINING' ? '⛏️ MINING REWARD' : formatAddress(tx.sender)}</div>
                            <div><strong>Para:</strong> ${formatAddress(tx.recipient)}</div>
                            <div><strong>Cantidad:</strong> ${formatNumber(tx.amount)} CLC</div>
                            ${tx.fee > 0 ? `<div><strong>Fee:</strong> ${tx.fee} CLC</div>` : ''}
                        </div>
                    `).join('')}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading block:', error);
        content.innerHTML = '<p class="no-data">Error cargando bloque</p>';
    }
}

// ==================== FAUCET PAGE ====================

async function loadFaucetPage() {
    const container = document.getElementById('faucetInfo');
    
    try {
        const info = await api.getFaucetInfo();
        
        if (info.success) {
            const data = info.data;
            
            container.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 1rem; text-align: left;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>Cantidad por reclamo:</span>
                        <strong>${data.amount_per_claim} CLC</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Cooldown:</span>
                        <strong>${data.cooldown_hours} horas</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Balance del faucet:</span>
                        <strong>${formatNumber(data.faucet_balance)} CLC</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Total distribuido:</span>
                        <strong>${formatNumber(data.total_distributed)} CLC</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Usuarios:</span>
                        <strong>${data.total_users}</strong>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading faucet info:', error);
        container.innerHTML = '<p class="no-data">Error cargando información</p>';
    }
}

// ==================== SETTINGS PAGE ====================

async function loadSettingsPage() {
    const container = document.getElementById('difficultyInfo');
    
    try {
        const info = await api.getDifficultyInfo();
        
        if (info.success) {
            const data = info.data;
            
            container.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>Dificultad actual:</span>
                        <strong>${data.current_difficulty}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Tiempo promedio:</span>
                        <strong>${data.current_avg_time.toFixed(2)}s</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Tiempo objetivo:</span>
                        <strong>${data.target_block_time}s</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Intervalo de ajuste:</span>
                        <strong>Cada ${data.adjustment_interval} bloques</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Próximo ajuste en:</span>
                        <strong>${data.blocks_until_adjustment} bloques</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Ajuste automático:</span>
                        <strong>${data.adjustment_enabled ? '✅ Habilitado' : '❌ Deshabilitado'}</strong>
                    </div>
                </div>
            `;
            
            // Update toggle
            document.getElementById('autoAdjustToggle').checked = data.adjustment_enabled;
            
            // Update manual difficulty
            document.getElementById('manualDifficulty').value = data.current_difficulty;
        }
    } catch (error) {
        console.error('Error loading difficulty info:', error);
        container.innerHTML = '<p class="no-data">Error cargando información</p>';
    }
}

// ==================== ACTIONS ====================

async function createWallet() {
    const name = document.getElementById('walletName').value.trim();
    
    if (!name) {
        showToast('Ingresa un nombre para la wallet', 'warning');
        return;
    }
    
    try {
        const result = await api.createWallet(name);
        
        if (result.success) {
            showToast('Wallet creada exitosamente', 'success');
            loadWalletPage();
        }
    } catch (error) {
        showToast('Error creando wallet: ' + error.message, 'error');
    }
}

async function loadWallet() {
    const filename = document.getElementById('walletName').value.trim();
    
    if (!filename) {
        showToast('Ingresa el nombre del archivo', 'warning');
        return;
    }
    
    // Add .json if not present
    const file = filename.endsWith('.json') ? filename : filename + '.json';
    
    try {
        const result = await api.loadWallet(file);
        
        if (result.success) {
            showToast('Wallet cargada exitosamente', 'success');
            loadWalletPage();
        }
    } catch (error) {
        showToast('Error cargando wallet: ' + error.message, 'error');
    }
}

async function sendTransaction() {
    if (!currentWallet) {
        showToast('Primero debes cargar una wallet', 'warning');
        return;
    }
    
    const recipient = document.getElementById('sendTo').value.trim();
    const amount = parseFloat(document.getElementById('sendAmount').value);
    const fee = parseFloat(document.getElementById('sendFee').value);
    
    if (!recipient || !amount || !fee) {
        showToast('Completa todos los campos', 'warning');
        return;
    }
    
    if (amount <= 0) {
        showToast('La cantidad debe ser mayor a 0', 'warning');
        return;
    }
    
    try {
        const result = await api.sendTransaction(recipient, amount, fee);
        
        if (result.success) {
            showToast('Transacción enviada. Mina un bloque para confirmarla.', 'success');
            
            // Clear form
            document.getElementById('sendTo').value = '';
            document.getElementById('sendAmount').value = '';
            document.getElementById('sendFee').value = '0.5';
            
            // Reload wallet info
            setTimeout(() => loadWalletPage(), 1000);
        }
    } catch (error) {
        showToast('Error enviando transacción: ' + error.message, 'error');
    }
}

async function mineBlock() {
    if (!currentWallet) {
        showToast('Primero debes cargar una wallet', 'warning');
        return;
    }
    
    const btn = document.getElementById('mineBtn');
    const status = document.getElementById('miningStatus');
    
    btn.disabled = true;
    btn.textContent = '⛏️ Minando...';
    status.className = 'mining-status active';
    status.textContent = '⛏️ Minando bloque... Esto puede tomar unos segundos.';
    
    try {
        const result = await api.mineBlock();
        
        if (result.success) {
            status.className = 'mining-status active success';
            status.innerHTML = `
                ✅ ¡Bloque minado exitosamente!<br>
                Hash: ${formatHash(result.data.block.hash)}<br>
                Nonce: ${formatNumber(result.data.block.nonce)}<br>
                Tiempo: ${result.data.mining_time}s<br>
                Recompensa: ${result.data.reward} CLC
            `;
            
            showToast('¡Bloque minado exitosamente!', 'success');
            
            // Reload data
            setTimeout(() => {
                loadDashboard();
                loadMiningPage();
            }, 2000);
        }
    } catch (error) {
        status.className = 'mining-status active error';
        status.textContent = '❌ Error: ' + error.message;
        showToast('Error minando bloque: ' + error.message, 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = '⛏️ Minar Bloque';
    }
}

async function claimFaucet() {
    if (!currentWallet) {
        showToast('Primero debes cargar una wallet', 'warning');
        return;
    }
    
    try {
        const result = await api.claimFaucet();
        
        if (result.success) {
            showToast('¡Reclamo exitoso! Mina un bloque para confirmar.', 'success');
            loadFaucetPage();
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

async function setDifficulty() {
    const difficulty = parseInt(document.getElementById('manualDifficulty').value);
    
    if (difficulty < 2 || difficulty > 8) {
        showToast('La dificultad debe estar entre 2 y 8', 'warning');
        return;
    }
    
    try {
        const result = await api.setDifficulty(difficulty);
        
        if (result.success) {
            showToast('Dificultad actualizada', 'success');
            loadSettingsPage();
            loadDashboard();
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

async function toggleAutoAdjust() {
    const enabled = document.getElementById('autoAdjustToggle').checked;
    
    try {
        const result = await api.toggleAutoAdjustment(enabled);
        
        if (result.success) {
            showToast(enabled ? 'Ajuste automático habilitado' : 'Ajuste automático deshabilitado', 'success');
            loadSettingsPage();
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

// ==================== AUTO UPDATE ====================

function startAutoUpdate() {
    // Update every 30 seconds
    updateInterval = setInterval(() => {
        const activePage = document.querySelector('.page.active');
        if (activePage && activePage.id === 'dashboard') {
            loadDashboard();
        }
    }, 30000);
}

// ==================== TOAST NOTIFICATIONS ====================

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    
    toast.textContent = message;
    toast.className = `toast ${type}`;
    
    // Show toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Hide toast after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 5000);
}

// ==================== CONTRACTS PAGE ====================

async function loadContractsPage() {
    loadContractsList();
}

async function loadContractsList() {
    const container = document.getElementById('contractsList');
    container.innerHTML = '<p class="loading">Cargando contratos...</p>';
    
    try {
        const response = await api.request('/contracts/list');
        
        if (response.success && response.data.contracts.length > 0) {
            container.innerHTML = '<div style="display: flex; flex-direction: column; gap: 1rem;"></div>';
            const list = container.querySelector('div');
            
            response.data.contracts.forEach(contract => {
                const contractEl = document.createElement('div');
                contractEl.className = 'contract-item';
                contractEl.style.cssText = 'padding: 1rem; background: var(--dark-light); border: 1px solid var(--border); border-radius: 8px;';
                
                const status = contract.executed ? '✅ Ejecutado' : '⏳ Pendiente';
                const statusColor = contract.executed ? 'var(--success)' : 'var(--warning)';
                
                let typeIcon = '📜';
                if (contract.contract_type === 'timelock') typeIcon = '⏰';
                if (contract.contract_type === 'multisig') typeIcon = '✍️';
                if (contract.contract_type === 'escrow') typeIcon = '🤝';
                
                contractEl.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <span style="font-size: 1.5rem;">${typeIcon}</span>
                            <strong>${contract.contract_id}</strong>
                        </div>
                        <span style="color: ${statusColor}; font-weight: bold;">${status}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: var(--text-secondary); display: flex; flex-direction: column; gap: 0.3rem;">
                        <div>Tipo: ${contract.contract_type}</div>
                        ${contract.info.unlock_block ? `<div>Desbloqueo: Bloque ${contract.info.unlock_block}</div>` : ''}
                        ${contract.info.amount ? `<div>Cantidad: ${formatNumber(contract.info.amount)} CLC</div>` : ''}
                        ${contract.info.required_sigs ? `<div>Firmas: ${contract.info.current_sigs}/${contract.info.required_sigs}</div>` : ''}
                        ${contract.info.status && contract.contract_type === 'escrow' ? `<div>Estado: ${contract.info.status}</div>` : ''}
                    </div>
                    <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                        <button class="btn btn-secondary" onclick="viewContract('${contract.contract_id}')">Ver Detalles</button>
                        ${!contract.executed ? `<button class="btn btn-primary" onclick="executeContract('${contract.contract_id}')">Ejecutar</button>` : ''}
                    </div>
                `;
                
                list.appendChild(contractEl);
            });
        } else {
            container.innerHTML = '<p class="no-data">No hay contratos creados</p>';
        }
    } catch (error) {
        console.error('Error loading contracts:', error);
        container.innerHTML = '<p class="no-data">Error cargando contratos</p>';
    }
}

function showContractForm() {
    const type = document.getElementById('contractType').value;
    
    // Ocultar todos los formularios
    document.getElementById('timelockForm').style.display = 'none';
    document.getElementById('multisigForm').style.display = 'none';
    document.getElementById('escrowForm').style.display = 'none';
    
    // Mostrar el formulario seleccionado
    if (type === 'timelock') {
        document.getElementById('timelockForm').style.display = 'block';
    } else if (type === 'multisig') {
        document.getElementById('multisigForm').style.display = 'block';
    } else if (type === 'escrow') {
        document.getElementById('escrowForm').style.display = 'block';
    }
}

async function createTimelockContract() {
    if (!currentWallet) {
        showToast('Primero debes cargar una wallet', 'warning');
        return;
    }
    
    const unlockBlock = parseInt(document.getElementById('unlockBlock').value);
    const amount = parseFloat(document.getElementById('contractAmount').value);
    const recipient = document.getElementById('contractRecipient').value.trim();
    
    if (!unlockBlock || !amount || !recipient) {
        showToast('Completa todos los campos', 'warning');
        return;
    }
    
    try {
        const response = await api.request('/contracts/timelock/create', {
            method: 'POST',
            body: JSON.stringify({
                creator: currentWallet.address,
                unlock_block: unlockBlock,
                amount: amount,
                recipient: recipient
            })
        });
        
        if (response.success) {
            showToast('Contrato Timelock creado exitosamente', 'success');
            
            // Limpiar formulario
            document.getElementById('unlockBlock').value = '';
            document.getElementById('contractAmount').value = '';
            document.getElementById('contractRecipient').value = '';
            
            // Recargar lista
            loadContractsList();
        }
    } catch (error) {
        showToast('Error creando contrato: ' + error.message, 'error');
    }
}

async function createMultisigContract() {
    if (!currentWallet) {
        showToast('Primero debes cargar una wallet', 'warning');
        return;
    }
    
    const requiredSigs = parseInt(document.getElementById('requiredSigs').value);
    const signersText = document.getElementById('signers').value.trim();
    const amount = parseFloat(document.getElementById('multisigAmount').value);
    const recipient = document.getElementById('multisigRecipient').value.trim();
    
    if (!requiredSigs || !signersText || !amount || !recipient) {
        showToast('Completa todos los campos', 'warning');
        return;
    }
    
    const signers = signersText.split('\n').map(s => s.trim()).filter(s => s);
    
    if (signers.length < requiredSigs) {
        showToast('El número de firmantes debe ser >= firmas requeridas', 'warning');
        return;
    }
    
    try {
        const response = await api.request('/contracts/multisig/create', {
            method: 'POST',
            body: JSON.stringify({
                creator: currentWallet.address,
                required_sigs: requiredSigs,
                signers: signers,
                amount: amount,
                recipient: recipient
            })
        });
        
        if (response.success) {
            showToast('Contrato Multisig creado exitosamente', 'success');
            
            // Limpiar formulario
            document.getElementById('requiredSigs').value = '';
            document.getElementById('signers').value = '';
            document.getElementById('multisigAmount').value = '';
            document.getElementById('multisigRecipient').value = '';
            
            // Recargar lista
            loadContractsList();
        }
    } catch (error) {
        showToast('Error creando contrato: ' + error.message, 'error');
    }
}

async function createEscrowContract() {
    if (!currentWallet) {
        showToast('Primero debes cargar una wallet', 'warning');
        return;
    }
    
    const buyer = document.getElementById('buyer').value.trim();
    const seller = document.getElementById('seller').value.trim();
    const arbiter = document.getElementById('arbiter').value.trim();
    const amount = parseFloat(document.getElementById('escrowAmount').value);
    
    if (!buyer || !seller || !arbiter || !amount) {
        showToast('Completa todos los campos', 'warning');
        return;
    }
    
    try {
        const response = await api.request('/contracts/escrow/create', {
            method: 'POST',
            body: JSON.stringify({
                creator: currentWallet.address,
                buyer: buyer,
                seller: seller,
                arbiter: arbiter,
                amount: amount
            })
        });
        
        if (response.success) {
            showToast('Contrato Escrow creado exitosamente', 'success');
            
            // Limpiar formulario
            document.getElementById('buyer').value = '';
            document.getElementById('seller').value = '';
            document.getElementById('arbiter').value = '';
            document.getElementById('escrowAmount').value = '';
            
            // Recargar lista
            loadContractsList();
        }
    } catch (error) {
        showToast('Error creando contrato: ' + error.message, 'error');
    }
}

async function viewContract(contractId) {
    try {
        const response = await api.request(`/contracts/${contractId}`);
        
        if (response.success) {
            const contract = response.data;
            
            alert(`Contrato ${contractId}
            
Tipo: ${contract.contract_type}
Estado: ${contract.executed ? 'Ejecutado' : 'Pendiente'}
Creador: ${formatAddress(contract.creator)}
${contract.execution_result ? `
Gas usado: ${contract.execution_result.gas_used}
Operaciones: ${contract.execution_result.operations.join(', ')}` : ''}`);
        }
    } catch (error) {
        showToast('Error cargando contrato: ' + error.message, 'error');
    }
}

async function executeContract(contractId) {
    const confirm = window.confirm(`¿Ejecutar contrato ${contractId}?`);
    
    if (!confirm) return;
    
    try {
        const response = await api.request(`/contracts/${contractId}/execute`, {
            method: 'POST'
        });
        
        if (response.success) {
            showToast('Contrato ejecutado exitosamente', 'success');
            loadContractsList();
        }
    } catch (error) {
        showToast('Error ejecutando contrato: ' + error.message, 'error');
    }
}


// ==================== NETWORK PAGE ====================

async function loadNetworkPage() {
    await loadNodeInfo();
    await loadPeersList();
    await loadNetworkStats();
}

async function loadNodeInfo() {
    const container = document.getElementById('nodeInfo');
    container.innerHTML = '<p class="loading">Cargando información del nodo...</p>';
    
    try {
        const response = await api.request('/network/info');
        
        if (response.success) {
            const info = response.data;
            
            container.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px;">
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Node ID</div>
                        <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">${info.node_id}</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px;">
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Host</div>
                        <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">${info.host}:${info.port}</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px;">
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Peers</div>
                        <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem; color: var(--primary);">${info.peers_count}</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px;">
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Uptime</div>
                        <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">${info.uptime}</div>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading node info:', error);
        container.innerHTML = '<p class="no-data">Error cargando información del nodo</p>';
    }
}

async function loadPeersList() {
    const container = document.getElementById('peersList');
    container.innerHTML = '<p class="loading">Cargando peers...</p>';
    
    try {
        const response = await api.request('/network/peers');
        
        if (response.success) {
            if (response.data.count === 0) {
                container.innerHTML = '<p class="no-data">No hay peers conectados</p>';
            } else {
                container.innerHTML = '<div style="display: flex; flex-direction: column; gap: 0.5rem;"></div>';
                const list = container.querySelector('div');
                
                response.data.peers.forEach(peer => {
                    const peerEl = document.createElement('div');
                    peerEl.style.cssText = 'padding: 1rem; background: var(--dark); border: 1px solid var(--border); border-radius: 8px; display: flex; justify-content: space-between; align-items: center;';
                    
                    peerEl.innerHTML = `
                        <div>
                            <strong>🌐 ${peer}</strong>
                        </div>
                        <button class="btn btn-secondary" onclick="removePeer('${peer}')" style="padding: 0.5rem 1rem;">
                            ❌ Eliminar
                        </button>
                    `;
                    
                    list.appendChild(peerEl);
                });
            }
        }
    } catch (error) {
        console.error('Error loading peers:', error);
        container.innerHTML = '<p class="no-data">Error cargando peers</p>';
    }
}

async function loadNetworkStats() {
    const container = document.getElementById('networkStats');
    container.innerHTML = '<p class="loading">Cargando estadísticas...</p>';
    
    try {
        const response = await api.request('/network/info');
        
        if (response.success) {
            const info = response.data;
            
            container.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--success);">📥 ${info.blocks_received}</div>
                        <div style="color: var(--text-secondary); margin-top: 0.5rem;">Bloques Recibidos</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--primary);">📤 ${info.blocks_sent}</div>
                        <div style="color: var(--text-secondary); margin-top: 0.5rem;">Bloques Enviados</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--success);">💼 ${info.transactions_received}</div>
                        <div style="color: var(--text-secondary); margin-top: 0.5rem;">Transacciones Recibidas</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--primary);">💸 ${info.transactions_sent}</div>
                        <div style="color: var(--text-secondary); margin-top: 0.5rem;">Transacciones Enviadas</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--warning);">📊 ${info.blockchain_height}</div>
                        <div style="color: var(--text-secondary); margin-top: 0.5rem;">Altura Blockchain</div>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading network stats:', error);
        container.innerHTML = '<p class="no-data">Error cargando estadísticas</p>';
    }
}

function showAddPeerModal() {
    document.getElementById('addPeerModal').style.display = 'flex';
}

function closeAddPeerModal() {
    document.getElementById('addPeerModal').style.display = 'none';
    document.getElementById('peerHost').value = '';
    document.getElementById('peerPort').value = '';
}

async function addPeer() {
    const host = document.getElementById('peerHost').value.trim();
    const port = document.getElementById('peerPort').value.trim();
    
    if (!host || !port) {
        showToast('Completa todos los campos', 'warning');
        return;
    }
    
    try {
        const response = await api.request('/network/peer/add', {
            method: 'POST',
            body: JSON.stringify({ host, port: parseInt(port) })
        });
        
        if (response.success) {
            showToast('Peer agregado exitosamente', 'success');
            closeAddPeerModal();
            loadNetworkPage();
        }
    } catch (error) {
        showToast('Error agregando peer: ' + error.message, 'error');
    }
}

async function removePeer(peerStr) {
    const [host, port] = peerStr.split(':');
    
    const confirm = window.confirm(`¿Eliminar peer ${peerStr}?`);
    if (!confirm) return;
    
    try {
        const response = await api.request('/network/peer/remove', {
            method: 'POST',
            body: JSON.stringify({ host, port: parseInt(port) })
        });
        
        if (response.success) {
            showToast('Peer eliminado exitosamente', 'success');
            loadNetworkPage();
        }
    } catch (error) {
        showToast('Error eliminando peer: ' + error.message, 'error');
    }
}

async function syncNetwork() {
    showToast('Sincronizando con la red...', 'info');
    
    try {
        const response = await api.request('/network/sync', {
            method: 'POST'
        });
        
        if (response.success) {
            showToast('Red sincronizada exitosamente', 'success');
            loadNetworkPage();
        }
    } catch (error) {
        showToast('Error sincronizando: ' + error.message, 'error');
    }
}

// ==================== POOL PAGE ====================

async function loadPoolPage() {
    await loadPoolInfo();
    await loadPoolMiners();
    await loadPoolLeaderboard();
}

async function loadPoolInfo() {
    const container = document.getElementById('poolInfo');
    container.innerHTML = '<p class="loading">Loading pool info...</p>';
    
    try {
        const response = await api.request('/pool/info');
        
        if (response.success) {
            const info = response.data;
            
            container.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--primary);">⛏️</div>
                        <div style="font-size: 1.5rem; font-weight: bold; margin-top: 0.5rem;">${info.pool_name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Pool Name</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--warning);">💰</div>
                        <div style="font-size: 1.5rem; font-weight: bold; margin-top: 0.5rem;">${info.pool_fee}%</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Pool Fee</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--success);">👷</div>
                        <div style="font-size: 1.5rem; font-weight: bold; margin-top: 0.5rem;">${info.total_miners}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Total Miners</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; color: var(--primary);">✅</div>
                        <div style="font-size: 1.5rem; font-weight: bold; margin-top: 0.5rem;">${info.active_miners}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Active Miners</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem;">📦</div>
                        <div style="font-size: 1.5rem; font-weight: bold; margin-top: 0.5rem;">${info.blocks_found}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">Blocks Found</div>
                    </div>
                    <div style="padding: 1rem; background: var(--dark); border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem;">💎</div>
                        <div style="font-size: 1.5rem; font-weight: bold; margin-top: 0.5rem;">${formatNumber(info.rewards_distributed)}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">CLC Distributed</div>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading pool info:', error);
        container.innerHTML = '<p class="no-data">Error loading pool info</p>';
    }
}

async function loadPoolMiners() {
    const container = document.getElementById('poolMinersList');
    container.innerHTML = '<p class="loading">Loading miners...</p>';
    
    try {
        const response = await api.request('/pool/miners');
        
        if (response.success && response.data.count > 0) {
            container.innerHTML = '<div style="display: flex; flex-direction: column; gap: 0.5rem;"></div>';
            const list = container.querySelector('div');
            
            response.data.miners.forEach(miner => {
                const minerEl = document.createElement('div');
                minerEl.style.cssText = 'padding: 1rem; background: var(--dark); border: 1px solid var(--border); border-radius: 8px;';
                
                minerEl.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>⛏️ ${miner.miner_id}</strong>
                            <div style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.3rem;">
                                Address: ${formatAddress(miner.address)}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.2rem; font-weight: bold; color: var(--primary);">${miner.shares}</div>
                            <div style="font-size: 0.8rem; color: var(--text-secondary);">shares</div>
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem; font-size: 0.85rem; color: var(--text-secondary); display: flex; gap: 1rem;">
                        <span>📊 ${miner.hashrate} H/s</span>
                        <span>🎯 ${miner.total_shares} total</span>
                        <span>⏱️ ${miner.uptime}</span>
                    </div>
                `;
                
                list.appendChild(minerEl);
            });
        } else {
            container.innerHTML = '<p class="no-data">No miners in pool</p>';
        }
    } catch (error) {
        console.error('Error loading miners:', error);
        container.innerHTML = '<p class="no-data">Error loading miners</p>';
    }
}

async function loadPoolLeaderboard() {
    const container = document.getElementById('poolLeaderboard');
    container.innerHTML = '<p class="loading">Loading leaderboard...</p>';
    
    try {
        const response = await api.request('/pool/leaderboard?limit=10');
        
        if (response.success && response.data.count > 0) {
            container.innerHTML = '<div style="display: flex; flex-direction: column; gap: 0.5rem;"></div>';
            const list = container.querySelector('div');
            
            response.data.leaderboard.forEach((miner, index) => {
                const position = index + 1;
                let medal = '';
                if (position === 1) medal = '🥇';
                else if (position === 2) medal = '🥈';
                else if (position === 3) medal = '🥉';
                else medal = `${position}.`;
                
                const minerEl = document.createElement('div');
                minerEl.style.cssText = 'padding: 0.75rem 1rem; background: var(--dark); border-radius: 8px; display: flex; justify-content: space-between; align-items: center;';
                
                minerEl.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="font-size: 1.5rem; min-width: 2rem;">${medal}</span>
                        <div>
                            <strong>${miner.miner_id}</strong>
                            <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                ${miner.blocks_found} blocks found
                            </div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.2rem; font-weight: bold; color: var(--primary);">
                            ${miner.total_shares}
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">shares</div>
                    </div>
                `;
                
                list.appendChild(minerEl);
            });
        } else {
            container.innerHTML = '<p class="no-data">No leaderboard data yet</p>';
        }
    } catch (error) {
        console.error('Error loading leaderboard:', error);
        container.innerHTML = '<p class="no-data">Error loading leaderboard</p>';
    }
}

async function joinPool() {
    const minerIdInput = document.getElementById('minerIdInput');
    const minerId = minerIdInput.value.trim();
    
    if (!minerId) {
        showToast('Enter a miner ID', 'warning');
        return;
    }
    
    if (!currentWallet) {
        showToast('Load a wallet first', 'warning');
        return;
    }
    
    try {
        const response = await api.request('/pool/join', {
            method: 'POST',
            body: JSON.stringify({
                miner_id: minerId,
                address: currentWallet.address
            })
        });
        
        if (response.success) {
            showToast(`Joined ${response.data.pool_name}!`, 'success');
            minerIdInput.value = '';
            loadPoolPage();
        }
    } catch (error) {
        showToast('Error joining pool: ' + error.message, 'error');
    }
}

async function leavePool() {
    const minerIdInput = document.getElementById('minerIdInput');
    const minerId = minerIdInput.value.trim();
    
    if (!minerId) {
        showToast('Enter your miner ID', 'warning');
        return;
    }
    
    const confirm = window.confirm(`Leave pool as ${minerId}?`);
    if (!confirm) return;
    
    try {
        const response = await api.request('/pool/leave', {
            method: 'POST',
            body: JSON.stringify({
                miner_id: minerId
            })
        });
        
        if (response.success) {
            showToast('Left the pool', 'success');
            minerIdInput.value = '';
            loadPoolPage();
        }
    } catch (error) {
        showToast('Error leaving pool: ' + error.message, 'error');
    }
}

async function poolMine() {
    const statusDiv = document.getElementById('poolMiningStatus');
    
    statusDiv.innerHTML = '<p class="loading">⛏️ Mining block collaboratively...</p>';
    
    try {
        const response = await api.request('/pool/mine', {
            method: 'POST'
        });
        
        if (response.success) {
            const data = response.data;
            
            let distributionHTML = '<div style="margin-top: 1rem;"><strong>💰 Distribution:</strong><ul style="margin-top: 0.5rem;">';
            for (const [minerId, amount] of Object.entries(data.distribution)) {
                distributionHTML += `<li>${minerId}: ${formatNumber(amount)} CLC</li>`;
            }
            distributionHTML += '</ul></div>';
            
            statusDiv.innerHTML = `
                <div style="padding: 1rem; background: var(--success-bg); border: 1px solid var(--success); border-radius: 8px;">
                    <strong>✅ Block #${data.block_index} mined!</strong>
                    ${distributionHTML}
                </div>
            `;
            
            showToast('Block mined successfully!', 'success');
            
            // Recargar datos
            setTimeout(() => {
                loadPoolPage();
                statusDiv.innerHTML = '<p>Pool is ready to mine</p>';
            }, 3000);
        }
    } catch (error) {
        statusDiv.innerHTML = '<p>Pool is ready to mine</p>';
        showToast('Error mining: ' + error.message, 'error');
    }
}

// ==================== EXPORT FUNCTIONS ====================

window.createWallet = createWallet;
window.loadWallet = loadWallet;
window.sendTransaction = sendTransaction;
window.mineBlock = mineBlock;
window.searchBlock = searchBlock;
window.viewBlock = viewBlock;
window.claimFaucet = claimFaucet;
window.setDifficulty = setDifficulty;
window.toggleAutoAdjust = toggleAutoAdjust;
window.showToast = showToast;
