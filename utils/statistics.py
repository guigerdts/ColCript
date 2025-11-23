# utils/statistics.py - Sistema de estadísticas para ColCript

import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import config

class BlockchainStatistics:
    def __init__(self, blockchain):
        """
        Inicializa el analizador de estadísticas
        """
        self.blockchain = blockchain
        self._cache = {}
    
    def get_total_supply(self):
        """Retorna el supply total configurado"""
        return config.TOTAL_SUPPLY
    
    def get_circulating_supply(self):
        """Calcula CLC en circulación (minados hasta ahora)"""
        if 'circulating_supply' in self._cache:
            return self._cache['circulating_supply']
        
        total = 0
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.sender == 'MINING':
                    total += tx.amount
        
        self._cache['circulating_supply'] = total
        return total
    
    def get_supply_percentage(self):
        """Porcentaje del supply total que está en circulación"""
        circulating = self.get_circulating_supply()
        total = self.get_total_supply()
        return (circulating / total) * 100
    
    def get_all_addresses(self):
        """Obtiene todas las direcciones únicas en la blockchain"""
        addresses = set()
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.sender != 'MINING' and tx.sender != 'GENESIS':
                    addresses.add(tx.sender)
                if tx.recipient != 'GENESIS':
                    addresses.add(tx.recipient)
        return addresses
    
    def get_wallet_balances(self):
        """Calcula el balance de todas las wallets"""
        if 'wallet_balances' in self._cache:
            return self._cache['wallet_balances']
        
        balances = defaultdict(float)
        
        for block in self.blockchain.chain:
            for tx in block.transactions:
                # Recipient recibe
                if tx.recipient != 'GENESIS':
                    balances[tx.recipient] += tx.amount
                
                # Sender paga (si no es MINING)
                if tx.sender != 'MINING' and tx.sender != 'GENESIS':
                    balances[tx.sender] -= tx.amount
                    # También paga el fee
                    if hasattr(tx, 'fee'):
                        balances[tx.sender] -= tx.fee
        
        self._cache['wallet_balances'] = dict(balances)
        return dict(balances)
    
    def get_top_wallets(self, limit=10):
        """Obtiene las wallets con más CLC"""
        balances = self.get_wallet_balances()
        sorted_wallets = sorted(balances.items(), key=lambda x: x[1], reverse=True)
        return sorted_wallets[:limit]
    
    def get_wealth_distribution(self):
        """Analiza la distribución de riqueza"""
        balances = self.get_wallet_balances()
        total_wallets = len(balances)
        
        if total_wallets == 0:
            return {
                'gini_coefficient': 0,
                'top_1_percent': 0,
                'top_10_percent': 0,
                'median_balance': 0
            }
        
        sorted_balances = sorted(balances.values(), reverse=True)
        circulating = self.get_circulating_supply()
        
        # Top 1% y 10%
        top_1_count = max(1, total_wallets // 100)
        top_10_count = max(1, total_wallets // 10)
        
        top_1_wealth = sum(sorted_balances[:top_1_count])
        top_10_wealth = sum(sorted_balances[:top_10_count])
        
        top_1_percent = (top_1_wealth / circulating * 100) if circulating > 0 else 0
        top_10_percent = (top_10_wealth / circulating * 100) if circulating > 0 else 0
        
        # Mediana
        median_idx = total_wallets // 2
        median_balance = sorted_balances[median_idx] if sorted_balances else 0
        
        return {
            'top_1_percent': top_1_percent,
            'top_10_percent': top_10_percent,
            'median_balance': median_balance,
            'total_wallets': total_wallets
        }
    
    def get_mining_stats(self):
        """Estadísticas de minería"""
        miners = defaultdict(int)
        total_blocks = 0
        total_mining_time = 0
        total_nonces = 0
        
        for block in self.blockchain.chain:
            if block.index == 0:  # Skip génesis
                continue
            
            total_blocks += 1
            miners[block.miner_address] += 1
            total_nonces += block.nonce
            
            # Estimar tiempo (si hay timestamps)
            if hasattr(block, 'timestamp') and block.index > 0:
                prev_block = self.blockchain.chain[block.index - 1]
                if hasattr(prev_block, 'timestamp'):
                    time_diff = block.timestamp - prev_block.timestamp
                    total_mining_time += time_diff
        
        avg_block_time = total_mining_time / total_blocks if total_blocks > 0 else 0
        avg_nonce = total_nonces / total_blocks if total_blocks > 0 else 0
        
        # Top minero
        top_miner = max(miners.items(), key=lambda x: x[1]) if miners else (None, 0)
        
        return {
            'total_miners': len(miners),
            'total_blocks_mined': total_blocks,
            'avg_block_time': avg_block_time,
            'avg_nonce': avg_nonce,
            'estimated_hashrate': avg_nonce / avg_block_time if avg_block_time > 0 else 0,
            'top_miner': top_miner[0],
            'top_miner_blocks': top_miner[1]
        }
    
    def get_transaction_stats(self):
        """Estadísticas de transacciones"""
        total_tx = 0
        total_volume = 0
        total_fees = 0
        tx_by_type = defaultdict(int)
        
        for block in self.blockchain.chain:
            for tx in block.transactions:
                total_tx += 1
                total_volume += tx.amount
                
                if hasattr(tx, 'fee'):
                    total_fees += tx.fee
                
                if tx.sender == 'MINING':
                    tx_by_type['mining_rewards'] += 1
                else:
                    tx_by_type['transfers'] += 1
        
        return {
            'total_transactions': total_tx,
            'total_volume': total_volume,
            'total_fees_paid': total_fees,
            'mining_rewards': tx_by_type['mining_rewards'],
            'transfers': tx_by_type['transfers'],
            'avg_tx_per_block': total_tx / len(self.blockchain.chain) if self.blockchain.chain else 0
        }
    
    def get_network_health(self):
        """Indicadores de salud de la red"""
        is_valid = self.blockchain.is_chain_valid()
        
        # Calcular descentralización (basado en distribución de minería)
        mining_stats = self.get_mining_stats()
        total_blocks = mining_stats['total_blocks_mined']
        top_miner_blocks = mining_stats['top_miner_blocks']
        
        centralization = (top_miner_blocks / total_blocks * 100) if total_blocks > 0 else 0
        decentralization_score = 100 - centralization
        
        return {
            'blockchain_valid': is_valid,
            'total_blocks': len(self.blockchain.chain),
            'decentralization_score': decentralization_score,
            'network_difficulty': self.blockchain.difficulty,
            'block_reward': self.blockchain.mining_reward
        }
    
    def get_complete_dashboard(self):
        """Genera dashboard completo con todas las estadísticas"""
        return {
            'supply': {
                'total': self.get_total_supply(),
                'circulating': self.get_circulating_supply(),
                'percentage': self.get_supply_percentage()
            },
            'wallets': {
                'total_wallets': len(self.get_all_addresses()),
                'top_wallets': self.get_top_wallets(5),
                'distribution': self.get_wealth_distribution()
            },
            'mining': self.get_mining_stats(),
            'transactions': self.get_transaction_stats(),
            'network': self.get_network_health()
        }

# Test
if __name__ == "__main__":
    print("\n📊 Probando sistema de estadísticas...\n")
    
    from blockchain.storage import BlockchainStorage
    
    # Cargar blockchain
    storage = BlockchainStorage()
    print("1. Cargando blockchain...")
    bc = storage.load_blockchain("colcript_main.json")
    
    if not bc:
        print("❌ No se pudo cargar blockchain")
        sys.exit(1)
    
    print(f"✅ Blockchain cargada: {len(bc.chain)} bloques\n")
    
    # Crear analizador
    stats = BlockchainStatistics(bc)
    
    # Obtener dashboard
    print("2. Generando estadísticas...\n")
    dashboard = stats.get_complete_dashboard()
    
    print("="*60)
    print("📊 DASHBOARD DE COLCRIPT")
    print("="*60)
    
    print(f"\n💰 SUPPLY:")
    print(f"   Total: {dashboard['supply']['total']:,} CLC")
    print(f"   En circulación: {dashboard['supply']['circulating']:,} CLC")
    print(f"   Porcentaje: {dashboard['supply']['percentage']:.4f}%")
    
    print(f"\n💼 WALLETS:")
    print(f"   Total de wallets: {dashboard['wallets']['total_wallets']}")
    print(f"   Top 5 wallets:")
    for i, (addr, balance) in enumerate(dashboard['wallets']['top_wallets'], 1):
        print(f"      {i}. {addr[:30]}... : {balance} CLC")
    
    print(f"\n⛏️  MINERÍA:")
    mining = dashboard['mining']
    print(f"   Total de mineros: {mining['total_miners']}")
    print(f"   Bloques minados: {mining['total_blocks_mined']}")
    print(f"   Tiempo promedio: {mining['avg_block_time']:.2f}s")
    
    print(f"\n💸 TRANSACCIONES:")
    tx = dashboard['transactions']
    print(f"   Total: {tx['total_transactions']}")
    print(f"   Volumen: {tx['total_volume']} CLC")
    print(f"   Fees pagados: {tx['total_fees_paid']} CLC")
    
    print(f"\n🌐 RED:")
    net = dashboard['network']
    print(f"   Blockchain válida: {net['blockchain_valid']}")
    print(f"   Bloques totales: {net['total_blocks']}")
    print(f"   Score descentralización: {net['decentralization_score']:.1f}%")
    
    print("\n" + "="*60)
    print("✅ Sistema de estadísticas funcionando\n")
