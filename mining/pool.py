# mining/pool.py - Sistema de Pool de Minería

import time
import threading
import hashlib
import sys
import os
from typing import Dict, List, Tuple
from datetime import datetime

# Agregar ruta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class PoolMiner:
    """Representa un minero en el pool"""
    
    def __init__(self, miner_id: str, address: str):
        self.miner_id = miner_id
        self.address = address
        self.shares = 0
        self.hashrate = 0
        self.connected_at = time.time()
        self.last_share_time = None
        self.total_shares = 0
        self.blocks_found = 0
        
    def add_share(self, difficulty: int = 1):
        """Agrega un share al minero"""
        self.shares += difficulty
        self.total_shares += difficulty
        self.last_share_time = time.time()
        
    def reset_shares(self):
        """Resetea shares para nueva ronda"""
        self.shares = 0
        
    def calculate_hashrate(self, window: int = 60):
        """Calcula hashrate basado en shares recientes"""
        if not self.last_share_time:
            return 0
        
        time_diff = time.time() - self.last_share_time
        if time_diff > window:
            return 0
        
        # Estimación simple: shares por segundo
        return self.shares / max(time_diff, 1)
    
    def to_dict(self):
        """Serializa minero a diccionario"""
        uptime = time.time() - self.connected_at
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        
        return {
            'miner_id': self.miner_id,
            'address': self.address,
            'shares': self.shares,
            'total_shares': self.total_shares,
            'hashrate': round(self.hashrate, 2),
            'blocks_found': self.blocks_found,
            'uptime': f"{hours}h {minutes}m",
            'last_share': datetime.fromtimestamp(
                self.last_share_time
            ).strftime('%Y-%m-%d %H:%M:%S') if self.last_share_time else None
        }


class MiningPool:
    """
    Pool de minería colaborativo
    
    Los mineros contribuyen con shares (pruebas de trabajo)
    Las recompensas se distribuyen proporcionalmente
    """
    
    def __init__(self, blockchain, pool_name: str = "ColCript Pool", 
                 pool_fee: float = 1.0):
        self.blockchain = blockchain
        self.pool_name = pool_name
        self.pool_fee = pool_fee  # % fee del pool
        self.miners: Dict[str, PoolMiner] = {}
        self.current_round_shares = 0
        self.total_blocks_mined = 0
        self.total_rewards_distributed = 0
        self.created_at = time.time()
        self.is_mining = False
        self.mining_thread = None
        
        # Estadísticas
        self.stats = {
            'blocks_found': 0,
            'total_shares': 0,
            'active_miners': 0,
            'pool_hashrate': 0
        }
    
    def add_miner(self, miner_id: str, address: str) -> Tuple[bool, str]:
        """Agrega un minero al pool"""
        if miner_id in self.miners:
            return False, "Miner already in pool"
        
        self.miners[miner_id] = PoolMiner(miner_id, address)
        return True, f"Miner {miner_id} joined the pool"
    
    def remove_miner(self, miner_id: str) -> Tuple[bool, str]:
        """Elimina un minero del pool"""
        if miner_id not in self.miners:
            return False, "Miner not found"
        
        del self.miners[miner_id]
        return True, f"Miner {miner_id} left the pool"
    
    def submit_share(self, miner_id: str, nonce: int, 
                     block_hash: str) -> Tuple[bool, str]:
        """
        Minero envía un share (proof of work)
        """
        if miner_id not in self.miners:
            return False, "Miner not registered"
        
        miner = self.miners[miner_id]
        
        # Validar que el hash tiene dificultad mínima (ej: al menos 1 cero)
        if not block_hash.startswith('0'):
            return False, "Invalid share: insufficient difficulty"
        
        # Contar cuántos ceros tiene (dificultad del share)
        difficulty = len(block_hash) - len(block_hash.lstrip('0'))
        
        # Agregar share al minero
        miner.add_share(difficulty)
        self.current_round_shares += difficulty
        self.stats['total_shares'] += difficulty
        
        # Si el hash cumple la dificultad del bloque real, encontramos bloque
        if self._is_valid_block_hash(block_hash):
            return True, "Block found!"
        
        return True, "Share accepted"
    
    def _is_valid_block_hash(self, block_hash: str) -> bool:
        """Verifica si el hash cumple la dificultad de la blockchain"""
        target = '0' * self.blockchain.difficulty
        return block_hash.startswith(target)
    
    def mine_block(self, timeout: int = 30) -> Tuple[bool, str, dict]:
        """
        Mina un bloque colaborativamente
        
        Returns:
            (success, message, distribution)
        """
        if len(self.miners) == 0:
            return False, "No miners in pool", {}
        
        print(f"\n⛏️  Mining block collaboratively...")
        print(f"   Pool: {self.pool_name}")
        print(f"   Miners: {len(self.miners)}")
        print(f"   Current shares: {self.current_round_shares}")
        
        # Resetear shares de esta ronda
        for miner in self.miners.values():
            miner.shares = 0
        self.current_round_shares = 0
        
        # Minar bloque (usar dirección del pool temporalmente)
        pool_address = "POOL_" + hashlib.sha256(
            self.pool_name.encode()
        ).hexdigest()[:20]
        
        start_time = time.time()
        block = self.blockchain.mine_pending_transactions(pool_address)
        mining_time = time.time() - start_time
        
        if not block:
            return False, "Mining failed", {}
        
        # Simular distribución de shares entre mineros
        # (En realidad, cada minero estaría enviando shares durante el minado)
        self._simulate_shares(mining_time)
        
        # Calcular recompensa total
        total_reward = self.blockchain.mining_reward
        total_fees = sum(tx.fee for tx in block.transactions if hasattr(tx, 'fee'))
        total_payout = total_reward + total_fees
        
        # Calcular fee del pool
        pool_fee_amount = total_payout * (self.pool_fee / 100)
        distributable = total_payout - pool_fee_amount
        
        # Distribuir recompensas proporcionalmente
        distribution = self._distribute_rewards(distributable)
        
        # Actualizar estadísticas
        self.total_blocks_mined += 1
        self.total_rewards_distributed += distributable
        self.stats['blocks_found'] += 1
        
        print(f"\n✅ Block mined! #{block.index}")
        print(f"   Hash: {block.hash[:20]}...")
        print(f"   Time: {mining_time:.2f} seconds")
        print(f"   Total reward: {total_payout} CLC")
        print(f"   Pool fee ({self.pool_fee}%): {pool_fee_amount} CLC")
        print(f"   Distributed: {distributable} CLC")
        print(f"\n💰 Distribution:")
        for miner_id, amount in distribution.items():
            print(f"   {miner_id}: {amount:.4f} CLC")
        
        return True, "Block mined successfully", distribution

    def _simulate_shares(self, mining_time: float):
        """
        Simula shares de mineros durante el tiempo de minado
        En producción, los mineros enviarían shares reales
        """
        if not self.miners:
            return
        
        # Asegurar mínimo de shares incluso en minados rápidos
        min_shares_per_miner = 100
        
        # Simular hashrate diferente para cada minero
        for i, miner in enumerate(self.miners.values()):
            # Hashrate simulado (varía por minero)
            base_hashrate = 1000 + (i * 500)
            
            # Calcular shares basado en tiempo Y mínimo garantizado
            time_based_shares = int(base_hashrate * mining_time / 10)
            shares = max(min_shares_per_miner, time_based_shares)
            
            miner.add_share(shares)
            self.current_round_shares += shares
            miner.hashrate = base_hashrate
            
            print(f"   {miner.miner_id}: {shares} shares ({base_hashrate} H/s)")
    
    def _distribute_rewards(self, amount: float) -> Dict[str, float]:
        """
        Distribuye recompensas proporcionalmente según shares
        
        Sistema PPLNS (Pay Per Last N Shares)
        """
        if self.current_round_shares == 0:
            return {}
        
        distribution = {}
        
        for miner_id, miner in self.miners.items():
            # Calcular proporción
            miner_proportion = miner.shares / self.current_round_shares
            miner_reward = amount * miner_proportion
            
            distribution[miner_id] = miner_reward
            
            # Actualizar estadísticas del minero
            miner.blocks_found += 1
        
        return distribution
    
    def get_stats(self) -> dict:
        """Obtiene estadísticas del pool"""
        # Calcular hashrate total del pool
        total_hashrate = sum(
            miner.calculate_hashrate() 
            for miner in self.miners.values()
        )
        
        # Contar mineros activos (con shares recientes)
        active_miners = sum(
            1 for miner in self.miners.values()
            if miner.last_share_time and 
            (time.time() - miner.last_share_time) < 300  # 5 minutos
        )
        
        uptime = time.time() - self.created_at
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        
        return {
            'pool_name': self.pool_name,
            'pool_fee': self.pool_fee,
            'total_miners': len(self.miners),
            'active_miners': active_miners,
            'pool_hashrate': round(total_hashrate, 2),
            'blocks_found': self.total_blocks_mined,
            'total_shares': self.stats['total_shares'],
            'rewards_distributed': self.total_rewards_distributed,
            'current_round_shares': self.current_round_shares,
            'uptime': f"{hours}h {minutes}m"
        }
    
    def get_miner_stats(self, miner_id: str) -> dict:
        """Obtiene estadísticas de un minero específico"""
        if miner_id not in self.miners:
            return None
        
        return self.miners[miner_id].to_dict()
    
    def get_all_miners(self) -> List[dict]:
        """Obtiene lista de todos los mineros"""
        return [miner.to_dict() for miner in self.miners.values()]
    
    def get_leaderboard(self, limit: int = 10) -> List[dict]:
        """Obtiene ranking de mineros por shares"""
        miners_list = self.get_all_miners()
        miners_list.sort(key=lambda x: x['total_shares'], reverse=True)
        return miners_list[:limit]


# Test
if __name__ == "__main__":
    print("\n⛏️  Probando Pool de Minería...\n")
    
    from blockchain.blockchain import Blockchain
    
    # Crear blockchain
    blockchain = Blockchain(auto_save=False)
    
    # Crear pool
    pool = MiningPool(blockchain, pool_name="ColCript Test Pool", pool_fee=2.0)
    
    # Agregar mineros
    pool.add_miner("miner1", "address1")
    pool.add_miner("miner2", "address2")
    pool.add_miner("miner3", "address3")
    
    print("Pool creado:")
    print(f"  Nombre: {pool.pool_name}")
    print(f"  Fee: {pool.pool_fee}%")
    print(f"  Mineros: {len(pool.miners)}")
    
    # Minar bloque
    success, msg, distribution = pool.mine_block()
    
    # Mostrar estadísticas
    print("\nEstadísticas del pool:")
    stats = pool.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nLeaderboard:")
    leaderboard = pool.get_leaderboard()
    for i, miner in enumerate(leaderboard, 1):
        print(f"  {i}. {miner['miner_id']}: {miner['total_shares']} shares")
    
    print("\n✅ Pool de Minería funcionando\n")
