# blockchain/transaction.py - Sistema de transacciones de ColCript

import time
import os
import sys

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.crypto import hash_data, sign_data, verify_signature

class Transaction:
    def __init__(self, sender, recipient, amount, private_key=None, fee=None):
        """
        Crea una nueva transacción
        sender: dirección pública del remitente (o 'MINING' para recompensas)
        recipient: dirección pública del destinatario
        amount: cantidad de CLC a enviar
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None

        # Configurar fee
        if sender == 'MINING':
            self.fee = 0  # Transacciones de recompensa no tienen fee
        else:
            if fee is None:
                import config
                self.fee = config.DEFAULT_TRANSACTION_FEE
            else:
                self.fee = fee
        
        # Si hay clave privada, firmar la transacción
        if private_key and sender != 'MINING':
            self.sign_transaction(private_key)
    
    def to_dict(self):
        """Convierte la transacción a diccionario"""
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature,
            'fee': self.fee
        }
    
    def sign_transaction(self, private_key):
        """Firma la transacción con la clave privada del remitente"""
        if self.sender == 'MINING':
            return  # Las recompensas de minado no se firman
        
        transaction_data = {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'fee': self.fee
        }
        
        self.signature = sign_data(private_key, transaction_data)
    
    def is_valid(self):
        """Verifica si la transacción es válida"""
        # Las recompensas de minado son válidas por defecto
        if self.sender == 'MINING':
            return True
        
        # Verificar que tenga firma
        if not self.signature:
            print("❌ Transacción sin firma")
            return False
        
        # Verificar la firma
        transaction_data = {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'fee': self.fee
        }
        
        is_valid = verify_signature(self.sender, self.signature, transaction_data)
        
        if not is_valid:
            print("❌ Firma inválida")
        
        return is_valid
    
    def get_hash(self):
        """Obtiene el hash de la transacción"""
        return hash_data(self.to_dict())
    
    def __repr__(self):
        fee_str = f" (fee: {self.fee} CLC)" if self.fee > 0 else ""
        return f"Transaction({self.sender[:10]}... -> {self.recipient[:10]}...: {self.amount} CLC{fee_str})"

# Test
if __name__ == "__main__":
    print("💰 Probando sistema de transacciones...")
    
    # Importar funciones de generación de claves
    from utils.crypto import generate_keypair
    
    # Crear dos wallets de prueba
    priv1, pub1 = generate_keypair()
    priv2, pub2 = generate_keypair()
    
    print(f"✅ Wallet 1: {pub1[:20]}...")
    print(f"✅ Wallet 2: {pub2[:20]}...")
    
    # Crear transacción de recompensa (minado)
    mining_tx = Transaction('MINING', pub1, 50)
    print(f"\n✅ Transacción de minado creada: {mining_tx}")
    print(f"   Válida: {mining_tx.is_valid()}")
    
    # Crear transacción normal
    normal_tx = Transaction(pub1, pub2, 10, priv1)
    print(f"\n✅ Transacción normal creada: {normal_tx}")
    print(f"   Válida: {normal_tx.is_valid()}")
    print(f"   Hash: {normal_tx.get_hash()[:20]}...")
