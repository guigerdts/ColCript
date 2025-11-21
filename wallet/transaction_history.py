# wallet/transaction_history.py - Sistema de historial de transacciones

import os
import sys
from datetime import datetime
import json

# Obtener ruta absoluta del proyecto
project_root = '/data/data/com.termux/files/home/ColCript'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class TransactionHistory:
    def __init__(self, blockchain, wallet_address):
        """
        Inicializa el analizador de historial
        """
        self.blockchain = blockchain
        self.wallet_address = wallet_address
        self.transactions = []
        self._analyze_transactions()
    
    def _analyze_transactions(self):
        """
        Analiza toda la blockchain y extrae transacciones relevantes
        """
        self.transactions = []
        
        for block in self.blockchain.chain:
            for tx in block.transactions:
                # Verificar si la wallet está involucrada
                if tx.sender == self.wallet_address or tx.recipient == self.wallet_address:
                    tx_info = {
                        'block': block.index,
                        'timestamp': tx.timestamp,
                        'sender': tx.sender,
                        'recipient': tx.recipient,
                        'amount': tx.amount,
                        'signature': tx.signature,
                        'block_hash': block.hash,
                        'type': self._get_transaction_type(tx)
                    }
                    self.transactions.append(tx_info)
    
    def _get_transaction_type(self, tx):
        """
        Determina el tipo de transacción
        """
        if tx.sender == 'MINING' and tx.recipient == self.wallet_address:
            return 'MINADO'
        elif tx.sender == self.wallet_address:
            return 'ENVIADO'
        elif tx.recipient == self.wallet_address:
            return 'RECIBIDO'
        else:
            return 'DESCONOCIDO'
    
    def get_all_transactions(self):
        """
        Obtiene todas las transacciones
        """
        return self.transactions
    
    def get_sent_transactions(self):
        """
        Obtiene solo las transacciones enviadas
        """
        return [tx for tx in self.transactions if tx['type'] == 'ENVIADO']
    
    def get_received_transactions(self):
        """
        Obtiene solo las transacciones recibidas (no minado)
        """
        return [tx for tx in self.transactions if tx['type'] == 'RECIBIDO']
    
    def get_mining_rewards(self):
        """
        Obtiene solo las recompensas de minado
        """
        return [tx for tx in self.transactions if tx['type'] == 'MINADO']
    
    def get_transaction_count(self):
        """
        Obtiene conteo de transacciones por tipo
        """
        return {
            'total': len(self.transactions),
            'enviadas': len(self.get_sent_transactions()),
            'recibidas': len(self.get_received_transactions()),
            'minado': len(self.get_mining_rewards())
        }
    
    def get_total_sent(self):
        """
        Calcula el total enviado
        """
        return sum(tx['amount'] for tx in self.get_sent_transactions())
    
    def get_total_received(self):
        """
        Calcula el total recibido (incluyendo minado)
        """
        received = sum(tx['amount'] for tx in self.get_received_transactions())
        mined = sum(tx['amount'] for tx in self.get_mining_rewards())
        return received + mined
    
    def get_summary(self):
        """
        Genera un resumen del historial
        """
        counts = self.get_transaction_count()
        
        return {
            'wallet_address': self.wallet_address[:30] + '...',
            'transacciones_totales': counts['total'],
            'enviadas': counts['enviadas'],
            'recibidas': counts['recibidas'],
            'recompensas_minado': counts['minado'],
            'total_enviado': self.get_total_sent(),
            'total_recibido': self.get_total_received(),
            'balance_neto': self.get_total_received() - self.get_total_sent()
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
    
    def print_transaction(self, tx, index=None):
        """
        Imprime una transacción de forma legible
        """
        prefix = f"{index}. " if index else ""
        
        print(f"\n{prefix}{'='*60}")
        
        # Tipo de transacción con emoji
        type_emoji = {
            'ENVIADO': '📤',
            'RECIBIDO': '📥',
            'MINADO': '⛏️'
        }
        emoji = type_emoji.get(tx['type'], '❓')
        
        print(f"{emoji} Tipo: {tx['type']}")
        print(f"📅 Fecha: {self.format_timestamp(tx['timestamp'])}")
        print(f"💰 Cantidad: {tx['amount']} CLC")
        
        if tx['type'] == 'ENVIADO':
            print(f"📍 Para: {tx['recipient'][:40]}...")
        elif tx['type'] == 'RECIBIDO':
            print(f"📍 De: {tx['sender'][:40]}...")
        
        print(f"🧱 Bloque: #{tx['block']}")
        print(f"🔗 Hash del bloque: {tx['block_hash'][:40]}...")
        
        if tx['signature']:
            print(f"✍️  Firmada: Sí")
        
        print('='*60)
    
    def print_all_transactions(self):
        """
        Imprime todas las transacciones
        """
        if not self.transactions:
            print("\n📭 No hay transacciones en el historial\n")
            return
        
        print(f"\n📜 HISTORIAL COMPLETO ({len(self.transactions)} transacciones)")
        
        for i, tx in enumerate(self.transactions, 1):
            self.print_transaction(tx, i)
    
    def print_summary(self):
        """
        Imprime el resumen del historial
        """
        summary = self.get_summary()
        
        print(f"\n📊 RESUMEN DE TRANSACCIONES")
        print("="*60)
        print(f"📍 Wallet: {summary['wallet_address']}")
        print(f"\n📈 Estadísticas:")
        print(f"   Total de transacciones: {summary['transacciones_totales']}")
        print(f"   📤 Enviadas: {summary['enviadas']}")
        print(f"   📥 Recibidas: {summary['recibidas']}")
        print(f"   ⛏️  Recompensas de minado: {summary['recompensas_minado']}")
        print(f"\n💰 Balances:")
        print(f"   Total recibido: {summary['total_recibido']} CLC")
        print(f"   Total enviado: {summary['total_enviado']} CLC")
        print(f"   Balance neto: {summary['balance_neto']} CLC")
        print("="*60 + "\n")
    
    def export_to_json(self, filename=None):
        """
        Exporta el historial a un archivo JSON
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"historial_{timestamp}.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join(project_root, 'data', filename)
        
        export_data = {
            'wallet_address': self.wallet_address,
            'export_date': datetime.now().isoformat(),
            'summary': self.get_summary(),
            'transactions': self.transactions
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"💾 Historial exportado: {filename}\n")
        return filepath

# Test
if __name__ == "__main__":
    print("\n📜 Probando sistema de historial...\n")
    
    from blockchain.blockchain import Blockchain
    from blockchain.storage import BlockchainStorage
    from utils.crypto import generate_keypair
    
    # Cargar o crear blockchain
    storage = BlockchainStorage()
    
    print("1. Intentando cargar blockchain existente...")
    bc = storage.load_blockchain("colcript_main.json")
    
    if not bc:
        print("2. Creando nueva blockchain de prueba...")
        bc = Blockchain(auto_save=False)
        
        # Crear wallet y hacer transacciones
        priv, pub = generate_keypair()
        print("3. Minando bloques...")
        bc.mine_pending_transactions(pub)
        bc.mine_pending_transactions(pub)
    else:
        # Usar una dirección de la blockchain cargada
        if len(bc.chain) > 1:
            pub = bc.chain[1].miner_address
            print(f"2. Usando wallet de blockchain existente")
        else:
            print("❌ Blockchain sin transacciones")
            sys.exit(1)
    
    print(f"\n4. Analizando historial de: {pub[:30]}...\n")
    
    # Crear historial
    history = TransactionHistory(bc, pub)
    
    # Mostrar resumen
    history.print_summary()
    
    # Mostrar todas las transacciones
    history.print_all_transactions()
    
    # Exportar
    print("\n5. Exportando historial...")
    history.export_to_json("test_historial.json")
    
    print("✅ Sistema de historial funcionando\n")
