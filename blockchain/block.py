# blockchain/block.py - Sistema de bloques de ColCript

import time
import os
import sys

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.crypto import hash_data
from blockchain.transaction import Transaction

class Block:
    def __init__(self, index, transactions, previous_hash, miner_address):
        """
        Crea un nuevo bloque
        index: número del bloque en la cadena
        transactions: lista de transacciones
        previous_hash: hash del bloque anterior
        miner_address: dirección del minero que creó el bloque
        """
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.miner_address = miner_address
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calcula el hash del bloque"""
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'miner_address': self.miner_address,
            'nonce': self.nonce
        }
        return hash_data(block_data)
    
    def mine_block(self, difficulty):
        """
        Mina el bloque (Proof of Work)
        Encuentra un nonce que haga que el hash comience con N ceros
        """
        target = '0' * difficulty
        
        print(f"⛏️  Minando bloque {self.index}...")
        start_time = time.time()
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
            # Mostrar progreso cada 10000 intentos
            if self.nonce % 10000 == 0:
                print(f"   Intentos: {self.nonce}, Hash: {self.hash[:10]}...")
        
        elapsed_time = time.time() - start_time
        print(f"✅ Bloque minado! Nonce: {self.nonce}")
        print(f"   Hash: {self.hash}")
        print(f"   Tiempo: {elapsed_time:.2f} segundos")
    
    def has_valid_transactions(self):
        """Verifica que todas las transacciones del bloque sean válidas"""
        for tx in self.transactions:
            if not tx.is_valid():
                return False
        return True
    
    def to_dict(self):
        """Convierte el bloque a diccionario"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'miner_address': self.miner_address,
            'nonce': self.nonce,
            'hash': self.hash
        }
    
    def __repr__(self):
        return f"Block #{self.index} [{len(self.transactions)} txs] - Hash: {self.hash[:10]}..."

# Test
if __name__ == "__main__":
    print("⛓️  Probando sistema de bloques...")
    
    from utils.crypto import generate_keypair
    
    # Crear wallet de minero
    miner_priv, miner_pub = generate_keypair()
    print(f"✅ Minero: {miner_pub[:20]}...")
    
    # Crear transacción de recompensa
    reward_tx = Transaction('MINING', miner_pub, 50)
    print(f"✅ Transacción de recompensa creada")
    
    # Crear bloque génesis (primer bloque)
    genesis_block = Block(0, [reward_tx], "0", miner_pub)
    print(f"\n✅ Bloque génesis creado: {genesis_block}")
    
    # Minar el bloque
    genesis_block.mine_block(difficulty=2)
    
    print(f"\n✅ Transacciones válidas: {genesis_block.has_valid_transactions()}")
