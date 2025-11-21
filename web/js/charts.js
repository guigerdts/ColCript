// charts.js - Gráficas con Chart.js

let supplyChart = null;
let walletsChart = null;

// ==================== SUPPLY CHART ====================

function createSupplyChart(circulating, total) {
    const ctx = document.getElementById('supplyChart');
    if (!ctx) return;

    // Destruir gráfica anterior si existe
    if (supplyChart) {
        supplyChart.destroy();
    }

    const remaining = total - circulating;

    supplyChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['En Circulación', 'Por Minar'],
            datasets: [{
                data: [circulating, remaining],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(51, 65, 85, 0.5)'
                ],
                borderColor: [
                    'rgba(59, 130, 246, 1)',
                    'rgba(51, 65, 85, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#e2e8f0',
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = formatNumber(context.parsed);
                            const percentage = ((context.parsed / total) * 100).toFixed(2);
                            return `${label}: ${value} CLC (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// ==================== WALLETS CHART ====================

function createWalletsChart(wallets) {
    const ctx = document.getElementById('walletsChart');
    if (!ctx) return;

    // Destruir gráfica anterior si existe
    if (walletsChart) {
        walletsChart.destroy();
    }

    // Tomar top 5 wallets
    const topWallets = wallets.slice(0, 5);
    
    const labels = topWallets.map((w, i) => `Wallet ${i + 1}`);
    const data = topWallets.map(w => w[1]);
    
    walletsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Balance (CLC)',
                data: data,
                backgroundColor: 'rgba(139, 92, 246, 0.8)',
                borderColor: 'rgba(139, 92, 246, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Balance: ${formatNumber(context.parsed.y)} CLC`;
                        },
                        afterLabel: function(context) {
                            const address = topWallets[context.dataIndex][0];
                            return `Dirección: ${formatAddress(address)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#94a3b8',
                        callback: function(value) {
                            return formatNumber(value) + ' CLC';
                        }
                    },
                    grid: {
                        color: 'rgba(51, 65, 85, 0.3)'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: 'rgba(51, 65, 85, 0.3)'
                    }
                }
            }
        }
    });
}

// ==================== UPDATE CHARTS ====================

async function updateCharts() {
    try {
        const dashboard = await api.getDashboard();
        
        if (dashboard.success) {
            const data = dashboard.data;
            
            // Supply chart
            createSupplyChart(
                data.supply.circulating,
                data.supply.total
            );
            
            // Wallets chart
            if (data.wallets.top_wallets && data.wallets.top_wallets.length > 0) {
                createWalletsChart(data.wallets.top_wallets);
            }
        }
    } catch (error) {
        console.error('Error updating charts:', error);
    }
}

// ==================== EXPORT ====================

window.createSupplyChart = createSupplyChart;
window.createWalletsChart = createWalletsChart;
window.updateCharts = updateCharts;
