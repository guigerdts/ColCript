# blockchain/block_explorer.py - Explorador de bloques para ColCript

import os
import sys
from datetime import datetime
import json

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import config

class BlockExplorer:
    def __init__(self, blockchain):
        """
        Inicializa el explorador de bloques
        """
        self.blockchain = blockchain
    
    def get_block_by_number(self, block_number):
        """
        Obtiene un bloque por su número
        """
        if 0 <= block_number < len(self.blockchain.chain):
            return self.blockchain.chain[block_number]
        return None
    
    def get_block_by_hash(self, block_hash):
        """
        Busca un bloque por su hash
        """
        for block in self.blockchain.chain:
            if block.hash == block_hash or block.hash.startswith(block_hash):
                return block
        return None
    
    def search_blocks_by_miner(self, miner_address):
        """
        Busca todos los bloques minados por una dirección
        """
        blocks = []
        for block in self.blockchain.chain:
            if block.miner_address == miner_address or block.miner_address.startswith(miner_address):
                blocks.append(block)
        return blocks
    
    def get_block_stats(self, block):
        """
        Calcula estadísticas de un bloque
        """
        return {
            'index': block.index,
            'timestamp': block.timestamp,
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'miner': block.miner_address,
            'nonce': block.nonce,
            'transactions_count': len(block.transactions),
            'total_amount': sum(tx.amount for tx in block.transactions),
            'difficulty': self.blockchain.difficulty,
            'size_bytes': len(str(block.to_dict()))
        }
    
    def verify_block(self, block):
        """
        Verifica la integridad de un bloque específico
        """
        issues = []
        
        # Verificar hash
        calculated_hash = block.calculate_hash()
        if block.hash != calculated_hash:
            issues.append("Hash no coincide con el calculado")
        
        # Verificar proof of work
        if block.hash[:self.blockchain.difficulty] != '0' * self.blockchain.difficulty:
            issues.append("Proof of work inválido")
        
        # Verificar transacciones
        for i, tx in enumerate(block.transactions):
            if not tx.is_valid():
                issues.append(f"Transacción #{i} inválida")
        
        # Verificar enlace con bloque anterior (si no es génesis)
        if block.index > 0:
            prev_block = self.get_block_by_number(block.index - 1)
            if prev_block and block.previous_hash != prev_block.hash:
                issues.append("Hash del bloque anterior no coincide")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def format_timestamp(self, timestamp):
        """
        Formatea el timestamp a formato legible
        """
        try:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "Fecha desconocida"
    
    def print_block_summary(self, block):
        """
        Imprime un resumen de un bloque
        """
        print(f"\n{'='*70}")
        print(f"🧱 BLOQUE #{block.index}")
        print(f"{'='*70}")
        print(f"🔗 Hash: {block.hash}")
        print(f"⬅️  Hash anterior: {block.previous_hash}")
        print(f"⛏️  Minero: {block.miner_address[:50]}...")
        print(f"📅 Fecha: {self.format_timestamp(block.timestamp)}")
        print(f"🎲 Nonce: {block.nonce}")
        print(f"📦 Transacciones: {len(block.transactions)}")
        print(f"💰 Total transferido: {sum(tx.amount for tx in block.transactions)} {config.COIN_SYMBOL}")
        print(f"{'='*70}\n")
    
    def print_block_detailed(self, block):
        """
        Imprime información detallada de un bloque
        """
        stats = self.get_block_stats(block)
        verification = self.verify_block(block)
        
        print(f"\n{'='*70}")
        print(f"🔍 DETALLES COMPLETOS DEL BLOQUE #{block.index}")
        print(f"{'='*70}")
        
        print(f"\n📊 INFORMACIÓN GENERAL:")
        print(f"   🔗 Hash: {block.hash}")
        print(f"   ⬅️  Hash anterior: {block.previous_hash}")
        print(f"   ⛏️  Minero: {block.miner_address}")
        print(f"   📅 Fecha/Hora: {self.format_timestamp(block.timestamp)}")
        print(f"   🎲 Nonce: {block.nonce:,}")
        print(f"   ⚙️  Dificultad: {stats['difficulty']} ceros")
        print(f"   📏 Tamaño: {stats['size_bytes']:,} bytes")
        
        print(f"\n💰 INFORMACIÓN FINANCIERA:")
        print(f"   📦 Transacciones: {stats['transactions_count']}")
        print(f"   💵 Total transferido: {stats['total_amount']} {config.COIN_SYMBOL}")
        
        print(f"\n✅ VERIFICACIÓN:")
        if verification['valid']:
            print(f"   ✅ Bloque válido")
        else:
            print(f"   ❌ Bloque con problemas:")
            for issue in verification['issues']:
                print(f"      • {issue}")
        
        print(f"\n📋 TRANSACCIONES ({len(block.transactions)}):")
        print(f"{'='*70}")
        
        for i, tx in enumerate(block.transactions, 1):
            print(f"\n   Transacción #{i}:")
            print(f"   De: {tx.sender[:40]}...")
            print(f"   Para: {tx.recipient[:40]}...")
            print(f"   Cantidad: {tx.amount} {config.COIN_SYMBOL}")
            print(f"   Fecha: {self.format_timestamp(tx.timestamp)}")
            if tx.signature:
                print(f"   Firmada: ✅ Sí")
            print(f"   {'-'*66}")
        
        print(f"\n{'='*70}\n")
    
    def get_blockchain_stats(self):
        """
        Obtiene estadísticas generales de la blockchain
        """
        total_transactions = sum(len(block.transactions) for block in self.blockchain.chain)
        total_volume = sum(
            sum(tx.amount for tx in block.transactions)
            for block in self.blockchain.chain
        )
        
        # Calcular mineros únicos
        miners = set()
        miner_blocks = {}
        for block in self.blockchain.chain:
            if block.miner_address != 'GENESIS':
                miners.add(block.miner_address)
                miner_blocks[block.miner_address] = miner_blocks.get(block.miner_address, 0) + 1
        
        # Top minero
        top_miner = None
        top_miner_blocks = 0
        if miner_blocks:
            top_miner = max(miner_blocks, key=miner_blocks.get)
            top_miner_blocks = miner_blocks[top_miner]
        
        return {
            'total_blocks': len(self.blockchain.chain),
            'total_transactions': total_transactions,
            'total_volume': total_volume,
            'unique_miners': len(miners),
            'top_miner': top_miner,
            'top_miner_blocks': top_miner_blocks,
            'difficulty': self.blockchain.difficulty,
            'mining_reward': self.blockchain.mining_reward
        }
    
    def print_blockchain_stats(self):
        """
        Imprime estadísticas generales de la blockchain
        """
        stats = self.get_blockchain_stats()
        
        print(f"\n{'='*70}")
        print(f"📊 ESTADÍSTICAS DE LA BLOCKCHAIN")
        print(f"{'='*70}")
        
        print(f"\n🧱 BLOQUES:")
        print(f"   Total de bloques: {stats['total_blocks']}")
        print(f"   Bloques minados: {stats['total_blocks'] - 1}")  # Sin contar génesis
        
        print(f"\n💰 TRANSACCIONES:")
        print(f"   Total de transacciones: {stats['total_transactions']}")
        print(f"   Volumen total: {stats['total_volume']} {config.COIN_SYMBOL}")
        
        print(f"\n⛏️  MINERÍA:")
        print(f"   Mineros únicos: {stats['unique_miners']}")
        print(f"   Dificultad actual: {stats['difficulty']}")
        print(f"   Recompensa por bloque: {stats['mining_reward']} {config.COIN_SYMBOL}")
        
        if stats['top_miner']:
            print(f"\n🏆 TOP MINERO:")
            print(f"   Dirección: {stats['top_miner'][:50]}...")
            print(f"   Bloques minados: {stats['top_miner_blocks']}")
        
        print(f"\n{'='*70}\n")
    
    def export_block(self, block, filename=None):
        """
        Exporta la información de un bloque a JSON
        """
        if filename is None:
            filename = f"block_{block.index}.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join(project_root, 'data', filename)
        
        block_data = {
            'block_info': self.get_block_stats(block),
            'verification': self.verify_block(block),
            'full_block': block.to_dict()
        }
        
        with open(filepath, 'w') as f:
            json.dump(block_data, f, indent=2)
        
        print(f"💾 Bloque exportado: {filename}\n")
        return filepath

# Test
if __name__ == "__main__":
    print("\n🔍 Probando explorador de bloques...\n")
    
    from blockchain.storage import BlockchainStorage
    
    # Cargar blockchain
    storage = BlockchainStorage()
    print("1. Cargando blockchain...")
    bc = storage.load_blockchain("colcript_main.json")
    
    if not bc:
        print("❌ No se pudo cargar blockchain")
        sys.exit(1)
    
    print(f"✅ Blockchain cargada: {len(bc.chain)} bloques\n")
    
    # Crear explorador
    explorer = BlockExplorer(bc)
    
    # Estadísticas generales
    print("2. Estadísticas de la blockchain:")
    explorer.print_blockchain_stats()
    
    # Ver bloque específico
    print("3. Detalles del bloque #1:")
    block1 = explorer.get_block_by_number(1)
    if block1:
        explorer.print_block_detailed(block1)
    
    # Buscar bloques por minero
    if len(bc.chain) > 1:
        miner = bc.chain[1].miner_address
        print(f"4. Bloques minados por {miner[:30]}...")
        blocks = explorer.search_blocks_by_miner(miner)
        print(f"   Encontrados: {len(blocks)} bloques\n")
    
    # Exportar bloque
    print("5. Exportando bloque #0...")
    block0 = explorer.get_block_by_number(0)
    if block0:
        explorer.export_block(block0, "test_block_export.json")
    
    print("✅ Explorador de bloques funcionando\n")
