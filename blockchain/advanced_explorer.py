# blockchain/advanced_explorer.py - Explorer avanzado para ColCript

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from blockchain.blockchain import Blockchain
from blockchain.block import Block

class AdvancedExplorer:
    """Explorer avanzado con búsquedas y estadísticas"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
    
    # === BÚSQUEDA AVANZADA ===
    
    def search_transaction(self, tx_hash: str) -> Optional[Dict]:
        """
        Buscar transacción por hash
        
        POR QUÉ: Encontrar transacciones específicas
        """
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if hasattr(tx, 'hash') and tx.hash == tx_hash:
                    return {
                        'transaction': tx.to_dict(),
                        'block': block.index,
                        'block_hash': block.hash,
                        'timestamp': block.timestamp,
                        'confirmations': len(self.blockchain.chain) - block.index
                    }
        return None
    
    def search_address_transactions(self, address: str, limit: int = 100) -> List[Dict]:
        """
        Buscar todas las transacciones de una dirección
        
        POR QUÉ: Ver historial completo de una wallet
        """
        transactions = []
        
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.sender == address or tx.recipient == address:
                    direction = "sent" if tx.sender == address else "received"
                    
                    transactions.append({
                        'hash': tx.hash if hasattr(tx, 'hash') else '',
                        'block': block.index,
                        'timestamp': block.timestamp,
                        'direction': direction,
                        'amount': tx.amount,
                        'fee': tx.fee if hasattr(tx, 'fee') else 0,
                        'from': tx.sender,
                        'to': tx.recipient,
                        'confirmations': len(self.blockchain.chain) - block.index
                    })
        
        # Ordenar por más reciente primero
        transactions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return transactions[:limit]

    def search_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Buscar bloques en rango de fechas
        
        POR QUÉ: Análisis histórico por período
        """
        results = []
        
        for block in self.blockchain.chain:
            try:
                # Manejar timestamp como string o float
                if isinstance(block.timestamp, float):
                    block_date = datetime.fromtimestamp(block.timestamp)
                else:
                    block_date = datetime.fromisoformat(block.timestamp.replace('Z', '+00:00'))
                
                start = datetime.fromisoformat(start_date)
                end = datetime.fromisoformat(end_date)
                
                if start <= block_date <= end:
                    results.append({
                        'index': block.index,
                        'hash': block.hash,
                        'timestamp': block.timestamp,
                        'transactions': len(block.transactions),
                        'miner': block.miner_address
                    })
            except Exception as e:
                # Saltar bloques con timestamps inválidos
                continue    

        return results
    
    # === ESTADÍSTICAS AVANZADAS ===
    
    def get_top_holders(self, limit: int = 10) -> List[Dict]:
        """
        Obtener top holders por balance
        
        POR QUÉ: Ver distribución de riqueza
        """
        balances = defaultdict(float)
        
        # Calcular balances de todas las direcciones
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.sender != "0":  # Ignorar mining rewards
                    balances[tx.sender] -= tx.amount
                    if hasattr(tx, 'fee'):
                        balances[tx.sender] -= tx.fee
                
                balances[tx.recipient] += tx.amount
        
        # Ordenar por balance
        sorted_holders = sorted(balances.items(), key=lambda x: x[1], reverse=True)
        
        # Calcular supply total
        total_supply = sum(balances.values())
        
        results = []
        for address, balance in sorted_holders[:limit]:
            percentage = (balance / total_supply * 100) if total_supply > 0 else 0
            results.append({
                'rank': len(results) + 1,
                'address': address,
                'balance': balance,
                'percentage': round(percentage, 2)
            })
        
        return results
    
    def get_miner_ranking(self, limit: int = 10) -> List[Dict]:
        """
        Ranking de mineros por bloques minados
        
        POR QUÉ: Ver quiénes están minando más
        """
        miner_stats = defaultdict(lambda: {'blocks': 0, 'rewards': 0})
        
        for block in self.blockchain.chain[1:]:  # Skip genesis
            miner = block.miner_address
            miner_stats[miner]['blocks'] += 1
            miner_stats[miner]['rewards'] += self.blockchain.mining_reward
        
        # Ordenar por bloques minados
        sorted_miners = sorted(
            miner_stats.items(),
            key=lambda x: x[1]['blocks'],
            reverse=True
        )
        
        results = []
        for address, stats in sorted_miners[:limit]:
            results.append({
                'rank': len(results) + 1,
                'address': address,
                'blocks_mined': stats['blocks'],
                'total_rewards': stats['rewards'],
                'percentage': round(stats['blocks'] / (len(self.blockchain.chain) - 1) * 100, 2)
            })
        
        return results
    
    def get_network_activity(self, days: int = 7) -> Dict:
        """
        Actividad de red en últimos N días
        
        POR QUÉ: Ver tendencias de uso
        """
        now = datetime.now()
        start_date = now - timedelta(days=days)
        
        activity = {
            'transactions_per_day': defaultdict(int),
            'blocks_per_day': defaultdict(int),
            'volume_per_day': defaultdict(float)
        }
        
        for block in self.blockchain.chain:
            try:
                block_date = datetime.fromisoformat(block.timestamp.replace('Z', '+00:00'))
                
                if block_date >= start_date:
                    day_key = block_date.strftime('%Y-%m-%d')
                    
                    activity['blocks_per_day'][day_key] += 1
                    activity['transactions_per_day'][day_key] += len(block.transactions)
                    
                    for tx in block.transactions:
                        activity['volume_per_day'][day_key] += tx.amount
            except:
                continue
        
        return {
            'period_days': days,
            'transactions_per_day': dict(activity['transactions_per_day']),
            'blocks_per_day': dict(activity['blocks_per_day']),
            'volume_per_day': dict(activity['volume_per_day'])
        }
    
    def get_realtime_stats(self) -> Dict:
        """
        Estadísticas en tiempo real
        
        POR QUÉ: Dashboard de estado actual
        """
        recent_blocks = self.blockchain.chain[-10:] if len(self.blockchain.chain) > 10 else self.blockchain.chain
        
        # Calcular tiempo promedio entre bloques
        block_times = []
        for i in range(1, len(recent_blocks)):
            try:
                prev_time = datetime.fromisoformat(recent_blocks[i-1].timestamp.replace('Z', '+00:00'))
                curr_time = datetime.fromisoformat(recent_blocks[i].timestamp.replace('Z', '+00:00'))
                diff = (curr_time - prev_time).total_seconds()
                block_times.append(diff)
            except:
                continue
        
        avg_block_time = sum(block_times) / len(block_times) if block_times else 0
        
        # Última actividad
        last_block = self.blockchain.chain[-1]
        try:
            last_activity = datetime.fromisoformat(last_block.timestamp.replace('Z', '+00:00'))
            seconds_ago = (datetime.now() - last_activity).total_seconds()
        except:
            seconds_ago = 0
        
        return {
            'chain_height': len(self.blockchain.chain),
            'pending_transactions': len(self.blockchain.pending_transactions),
            'current_difficulty': self.blockchain.difficulty,
            'average_block_time': round(avg_block_time, 2),
            'last_activity_seconds_ago': round(seconds_ago, 2),
            'last_block': {
                'index': last_block.index,
                'hash': last_block.hash,
                'transactions': len(last_block.transactions),
                'miner': last_block.miner_address
            }
        }
    
    def get_difficulty_history(self, limit: int = 100) -> List[Dict]:
        """
        Historial de dificultad
        
        POR QUÉ: Ver cambios de dificultad en el tiempo
        """
        history = []
        
        for block in self.blockchain.chain[-limit:]:
            history.append({
                'block': block.index,
                'timestamp': block.timestamp,
                'difficulty': getattr(block, 'difficulty', self.blockchain.difficulty),
                'hash': block.hash[:16] + '...'
            })
        
        return history

if __name__ == "__main__":
    print("🔍 ColCript Advanced Explorer Module")
    print("   Use from: from blockchain.advanced_explorer import AdvancedExplorer")
