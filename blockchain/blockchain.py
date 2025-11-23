# blockchain/blockchain.py - Blockchain de ColCript

import os
import sys
import json

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from blockchain.block import Block
from blockchain.transaction import Transaction
from blockchain.difficulty import DifficultyAdjustment
import config
from blockchain.storage import BlockchainStorage

class Blockchain:
    def __init__(self, auto_save=True, save_filename="colcript_main.json"):
        """Inicializa la blockchain"""
        self.chain = []
        self.pending_transactions = []
        self.difficulty = config.MINING_DIFFICULTY
        self.mining_reward = config.MINING_REWARD
        self.auto_save = auto_save
        self.save_filename = save_filename
        self.storage = BlockchainStorage()
    
        # Crear bloque génesis
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Crea el primer bloque de la cadena"""
        genesis_tx = Transaction('MINING', 'GENESIS', 0)
        genesis_block = Block(0, [genesis_tx], "0", "GENESIS")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print(f"✅ Bloque génesis creado: {genesis_block.hash[:20]}...")
    
    def get_latest_block(self):
        """Obtiene el último bloque de la cadena"""
        return self.chain[-1]

    def add_transaction(self, transaction):
        """Añade una transacción a las pendientes"""
        if not transaction.is_valid():
            print("❌ Transacción inválida, no se puede añadir")
            return False
    
        self.pending_transactions.append(transaction)
    
        # Ordenar por fee si está habilitado
        if config.PRIORITIZE_BY_FEE:
            self.pending_transactions.sort(key=lambda tx: tx.fee, reverse=True)
    
        print(f"✅ Transacción añadida al pool (fee: {transaction.fee} CLC)")
        return True
    
    def mine_pending_transactions(self, miner_address):
        """
        Mina las transacciones pendientes y añade el bloque a la cadena
        """
        # Ajustar dificultad si es necesario
        if config.DIFFICULTY_ADJUSTMENT_ENABLED:
            adjusted, old_diff, new_diff, reason = DifficultyAdjustment.adjust_if_needed(self)
            if adjusted:
                print(f"\n🔧 AJUSTE DE DIFICULTAD: {old_diff} → {new_diff}")
                print(f"   Razón: {reason}\n") 

        # Calcular fees totales de las transacciones pendientes
        total_fees = sum(tx.fee for tx in self.pending_transactions if hasattr(tx, 'fee'))
    
        # Crear transacción de recompensa para el minero (recompensa base + fees)
        total_reward = self.mining_reward + total_fees
        reward_tx = Transaction('MINING', miner_address, total_reward)
        self.pending_transactions.append(reward_tx)

        
        # Crear nuevo bloque
        block = Block(
            len(self.chain),
            self.pending_transactions,
            self.get_latest_block().hash,
            miner_address
        )
        
        # Minar el bloque
        block.mine_block(self.difficulty)
        
        # Añadir a la cadena
        self.chain.append(block)
        
        # Limpiar transacciones pendientes
        self.pending_transactions = []
        

        # Auto-guardar blockchain
        if self.auto_save:
            self.storage.save_blockchain(self, self.save_filename)

        # Mostrar información de fees
        if total_fees > 0:
            print(f"💰 Fees recolectados: {total_fees} CLC")
            print(f"💎 Recompensa total: {total_reward} CLC (base: {self.mining_reward} + fees: {total_fees})")
        else:
            print(f"💎 Recompensa: {self.mining_reward} CLC (sin fees)")

        print(f"✅ Bloque #{block.index} añadido a la cadena")
        return block

    def get_balance(self, address):
        """Calcula el balance de una dirección"""
        balance = 0
    
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                    # El remitente también paga el fee
                    if hasattr(tx, 'fee') and tx.sender != 'MINING':
                        balance -= tx.fee
                if tx.recipient == address:
                    balance += tx.amount
    
        return balance

    def is_chain_valid(self):
        """Verifica que la blockchain sea válida"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verificar que el hash del bloque sea correcto
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Hash inválido en bloque #{i}")
                return False
            
            # Verificar que el bloque apunte al anterior
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Cadena rota en bloque #{i}")
                return False
            
            # Verificar que las transacciones sean válidas
            if not current_block.has_valid_transactions():
                print(f"❌ Transacciones inválidas en bloque #{i}")
                return False
            
            # Verificar proof of work
            if current_block.hash[:self.difficulty] != '0' * self.difficulty:
                print(f"❌ Proof of work inválido en bloque #{i}")
                return False
        
        return True
    
    def get_chain_info(self):
        """Obtiene información de la blockchain"""
        return {
            'nombre': config.COIN_NAME,
            'simbolo': config.COIN_SYMBOL,
            'bloques': len(self.chain),
            'transacciones_pendientes': len(self.pending_transactions),
            'dificultad': self.difficulty,
            'ultimo_bloque': self.get_latest_block().hash
        }
    
    def __repr__(self):
        return f"Blockchain({config.COIN_NAME}): {len(self.chain)} bloques"

# Test
if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f"🚀 INICIANDO BLOCKCHAIN {config.COIN_NAME} ({config.COIN_SYMBOL})")
    print(f"{'='*50}\n")
    
    from utils.crypto import generate_keypair
    
    # Crear blockchain
    colcript = Blockchain()
    print(f"\n📊 {colcript}")
    
    # Crear wallets
    print("\n💼 Creando wallets...")
    alice_priv, alice_pub = generate_keypair()
    bob_priv, bob_pub = generate_keypair()
    print(f"   Alice: {alice_pub[:20]}...")
    print(f"   Bob: {bob_pub[:20]}...")
    
    # Minar bloque inicial para Alice
    print(f"\n⛏️  Alice mina el primer bloque...")
    colcript.mine_pending_transactions(alice_pub)
    print(f"   Balance de Alice: {colcript.get_balance(alice_pub)} CLC")
    
    # Alice envía CLC a Bob
    print(f"\n💸 Alice envía 20 CLC a Bob...")
    tx1 = Transaction(alice_pub, bob_pub, 20, alice_priv)
    colcript.add_transaction(tx1)
    
    # Bob mina el bloque
    print(f"\n⛏️  Bob mina el bloque con la transacción...")
    colcript.mine_pending_transactions(bob_pub)
    print(f"   Balance de Alice: {colcript.get_balance(alice_pub)} CLC")
    print(f"   Balance de Bob: {colcript.get_balance(bob_pub)} CLC")
    
    # Verificar blockchain
    print(f"\n🔍 Verificando integridad de la blockchain...")
    is_valid = colcript.is_chain_valid()
    print(f"   Blockchain válida: {is_valid}")
    
    # Información final
    print(f"\n📊 Información de la blockchain:")
    info = colcript.get_chain_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    print(f"\n{'='*50}")
    print(f"✅ BLOCKCHAIN {config.COIN_NAME} FUNCIONANDO CORRECTAMENTE")
    print(f"{'='*50}\n")
