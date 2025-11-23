# blockchain/storage.py - Sistema de persistencia para ColCript

import os
import sys
import json
from datetime import datetime

# Obtener ruta absoluta del proyecto de forma dinámica
# POR QUÉ: Funciona en Termux, GitHub Actions, Windows, Mac, Linux
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from blockchain.block import Block
from blockchain.transaction import Transaction

class BlockchainStorage:
    def __init__(self, data_dir=None):
        """Inicializa el sistema de almacenamiento"""
        if data_dir is None:
            self.data_dir = os.path.join(project_root, 'data')
        else:
            self.data_dir = data_dir
        
        # Crear directorio si no existe
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_blockchain(self, blockchain, filename=None):
        """
        Guarda la blockchain en un archivo JSON
        """
        if filename is None:
            # Nombre por defecto con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"blockchain_{timestamp}.json"
        
        # Asegurar extensión .json
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join(self.data_dir, filename)
        
        # Serializar blockchain
        blockchain_data = {
            'version': '1.0',
            'difficulty': blockchain.difficulty,
            'mining_reward': blockchain.mining_reward,
            'timestamp': datetime.now().isoformat(),
            'blocks': []
        }
        
        # Serializar cada bloque
        for block in blockchain.chain:
            block_data = {
                'index': block.index,
                'timestamp': block.timestamp,
                'previous_hash': block.previous_hash,
                'miner_address': block.miner_address,
                'nonce': block.nonce,
                'hash': block.hash,
                'transactions': []
            }
            
            # Serializar transacciones del bloque
            for tx in block.transactions:
                tx_data = {
                    'sender': tx.sender,
                    'recipient': tx.recipient,
                    'amount': tx.amount,
                    'timestamp': tx.timestamp,
                    'signature': tx.signature
                }
                block_data['transactions'].append(tx_data)
            
            blockchain_data['blocks'].append(block_data)
        
        # Guardar en archivo
        with open(filepath, 'w') as f:
            json.dump(blockchain_data, f, indent=2)
        
        print(f"💾 Blockchain guardada: {filename}")
        return filepath
    
    def load_blockchain(self, filename):
        """
        Carga una blockchain desde un archivo JSON
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ Archivo no encontrado: {filename}")
            return None
        
        try:
            with open(filepath, 'r') as f:
                blockchain_data = json.load(f)
            
            print(f"📂 Cargando blockchain desde: {filename}")
            
            # Crear blockchain vacía (sin génesis automático)
            from blockchain.blockchain import Blockchain
            blockchain = Blockchain.__new__(Blockchain)
            blockchain.chain = []
            blockchain.pending_transactions = []
            blockchain.difficulty = blockchain_data['difficulty']
            blockchain.mining_reward = blockchain_data['mining_reward']
            
            # Reconstruir cada bloque
            for block_data in blockchain_data['blocks']:
                # Reconstruir transacciones
                transactions = []
                for tx_data in block_data['transactions']:
                    tx = Transaction.__new__(Transaction)
                    tx.sender = tx_data['sender']
                    tx.recipient = tx_data['recipient']
                    tx.amount = tx_data['amount']
                    tx.timestamp = tx_data['timestamp']
                    tx.signature = tx_data['signature']
    
                    # Manejar blockchains antiguas sin fee
                    if 'fee' in tx_data:
                        tx.fee = tx_data['fee']
                    else:
                        # Blockchains antiguas: asignar fee 0 a transacciones de minado,
                        # y fee por defecto a transacciones normales
                        if tx.sender == 'MINING':
                            tx.fee = 0
                        else:
                            import config
                            tx.fee = config.DEFAULT_TRANSACTION_FEE
                            print(f"⚠️  Transacción antigua sin fee, asignando {tx.fee} CLC")
    
                    transactions.append(tx)
                
                # Reconstruir bloque
                block = Block.__new__(Block)
                block.index = block_data['index']
                block.timestamp = block_data['timestamp']
                block.transactions = transactions
                block.previous_hash = block_data['previous_hash']
                block.miner_address = block_data['miner_address']
                block.nonce = block_data['nonce']
                block.hash = block_data['hash']
                
                blockchain.chain.append(block)
            
            print(f"✅ Blockchain cargada: {len(blockchain.chain)} bloques")
            
            # Verificar integridad
            if blockchain.is_chain_valid():
                print("✅ Blockchain válida")
                return blockchain
            else:
                print("❌ Blockchain corrupta - validación falló")
                return None
                
        except Exception as e:
            print(f"❌ Error al cargar blockchain: {e}")
            return None
    
    def list_blockchains(self):
        """
        Lista todas las blockchains guardadas
        """
        try:
            files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
            
            if not files:
                print("📁 No hay blockchains guardadas")
                return []
            
            blockchains = []
            
            print(f"\n📁 Blockchains guardadas ({len(files)}):\n")
            
            for i, filename in enumerate(sorted(files), 1):
                filepath = os.path.join(self.data_dir, filename)
                
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    blocks = len(data.get('blocks', []))
                    timestamp = data.get('timestamp', 'Desconocido')
                    
                    # Formatear timestamp
                    try:
                        dt = datetime.fromisoformat(timestamp)
                        timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        timestamp_str = timestamp
                    
                    info = {
                        'number': i,
                        'filename': filename,
                        'blocks': blocks,
                        'timestamp': timestamp_str
                    }
                    
                    blockchains.append(info)
                    
                    print(f"  {i}. {filename}")
                    print(f"     Bloques: {blocks}")
                    print(f"     Guardada: {timestamp_str}")
                    print()
                    
                except Exception as e:
                    print(f"  ⚠️  {filename} - Error al leer")
            
            return blockchains
            
        except Exception as e:
            print(f"❌ Error al listar blockchains: {e}")
            return []
    
    def delete_blockchain(self, filename):
        """
        Elimina una blockchain guardada
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ Archivo no encontrado: {filename}")
            return False
        
        try:
            os.remove(filepath)
            print(f"🗑️  Blockchain eliminada: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error al eliminar: {e}")
            return False

# Test
if __name__ == "__main__":
    print("\n💾 Probando sistema de almacenamiento...\n")
    
    from blockchain.blockchain import Blockchain
    from utils.crypto import generate_keypair
    
    # Crear blockchain de prueba
    print("1. Creando blockchain de prueba...")
    bc = Blockchain()
    
    # Crear wallet y minar
    priv, pub = generate_keypair()
    print(f"2. Minando bloque de prueba...")
    bc.mine_pending_transactions(pub)
    
    print(f"3. Blockchain tiene {len(bc.chain)} bloques")
    
    # Guardar
    storage = BlockchainStorage()
    print("\n4. Guardando blockchain...")
    storage.save_blockchain(bc, "test_blockchain.json")
    
    # Listar
    print("\n5. Listando blockchains guardadas:")
    storage.list_blockchains()
    
    # Cargar
    print("\n6. Cargando blockchain...")
    loaded_bc = storage.load_blockchain("test_blockchain.json")
    
    if loaded_bc:
        print(f"7. Blockchain cargada tiene {len(loaded_bc.chain)} bloques")
        print(f"8. Blockchain válida: {loaded_bc.is_chain_valid()}")
    
    print("\n✅ Sistema de almacenamiento funcionando\n")
