# wallet/faucet.py - Sistema de faucet (grifo) para ColCript

import os
import sys
import json
import time
from datetime import datetime, timedelta

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import config
from wallet.wallet import Wallet
from blockchain.transaction import Transaction

class Faucet:
    def __init__(self, blockchain):
        """
        Inicializa el sistema de faucet
        """
        self.blockchain = blockchain
        self.claims_file = os.path.join(project_root, 'data', 'faucet_claims.json')
        self.faucet_wallet_file = os.path.join(project_root, 'wallet', 'faucet_wallet.json')
        self.claims_history = self._load_claims()
        self.faucet_wallet = self._get_or_create_faucet_wallet()
    
    def _load_claims(self):
        """Carga el historial de reclamos"""
        if os.path.exists(self.claims_file):
            try:
                with open(self.claims_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_claims(self):
        """Guarda el historial de reclamos"""
        with open(self.claims_file, 'w') as f:
            json.dump(self.claims_history, f, indent=2)
    
    def _get_or_create_faucet_wallet(self):
        """Obtiene o crea la wallet del faucet"""
        if os.path.exists(self.faucet_wallet_file):
            return Wallet.load_from_file('faucet_wallet.json')
        else:
            faucet = Wallet(config.FAUCET_WALLET_NAME)
            faucet.save_to_file('faucet_wallet.json')
            return faucet
    
    def can_claim(self, wallet_address):
        """
        Verifica si una wallet puede reclamar del faucet
        """
        if not config.FAUCET_ENABLED:
            return False, "El faucet está deshabilitado"
        
        # Verificar balance actual
        balance = self.blockchain.get_balance(wallet_address)
        if balance >= config.FAUCET_MAX_BALANCE:
            return False, f"Tu balance ({balance} CLC) excede el máximo permitido ({config.FAUCET_MAX_BALANCE} CLC)"
        
        # Verificar último reclamo
        if wallet_address in self.claims_history:
            last_claim_timestamp = self.claims_history[wallet_address]['last_claim']
            last_claim_time = datetime.fromtimestamp(last_claim_timestamp)
            cooldown_end = last_claim_time + timedelta(hours=config.FAUCET_COOLDOWN_HOURS)
            
            if datetime.now() < cooldown_end:
                time_left = cooldown_end - datetime.now()
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                return False, f"Debes esperar {hours}h {minutes}m para reclamar nuevamente"
        
        # Verificar fondos del faucet
        faucet_balance = self.blockchain.get_balance(self.faucet_wallet.get_address())
        if faucet_balance < config.FAUCET_AMOUNT:
            return False, f"El faucet no tiene fondos suficientes (tiene {faucet_balance} CLC)"
        
        return True, "Puede reclamar"
    
    def claim(self, wallet_address):
        """
        Reclama CLC del faucet
        """
        can_claim, message = self.can_claim(wallet_address)
        
        if not can_claim:
            return False, message
        
        # Crear transacción desde el faucet
        try:
            transaction = Transaction(
                self.faucet_wallet.get_address(),
                wallet_address,
                config.FAUCET_AMOUNT,
                self.faucet_wallet.private_key,
                fee=0  # El faucet no cobra fee
            )
            
            if transaction.is_valid():
                self.blockchain.add_transaction(transaction)
                
                # Registrar reclamo
                self.claims_history[wallet_address] = {
                    'last_claim': time.time(),
                    'total_claimed': self.claims_history.get(wallet_address, {}).get('total_claimed', 0) + config.FAUCET_AMOUNT,
                    'claim_count': self.claims_history.get(wallet_address, {}).get('claim_count', 0) + 1
                }
                self._save_claims()
                
                return True, f"¡Reclamo exitoso! {config.FAUCET_AMOUNT} CLC agregados al pool de transacciones"
            else:
                return False, "Error al crear la transacción"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_faucet_info(self):
        """Obtiene información del faucet"""
        faucet_balance = self.blockchain.get_balance(self.faucet_wallet.get_address())
        total_claims = len(self.claims_history)
        total_distributed = sum(data.get('total_claimed', 0) for data in self.claims_history.values())
        
        return {
            'enabled': config.FAUCET_ENABLED,
            'amount_per_claim': config.FAUCET_AMOUNT,
            'cooldown_hours': config.FAUCET_COOLDOWN_HOURS,
            'max_balance_allowed': config.FAUCET_MAX_BALANCE,
            'faucet_balance': faucet_balance,
            'faucet_address': self.faucet_wallet.get_address(),
            'total_users': total_claims,
            'total_distributed': total_distributed
        }
    
    def get_claim_info(self, wallet_address):
        """Obtiene información de reclamos de una wallet"""
        if wallet_address not in self.claims_history:
            return {
                'has_claimed': False,
                'total_claimed': 0,
                'claim_count': 0,
                'last_claim': None,
                'can_claim_at': datetime.now()
            }
        
        data = self.claims_history[wallet_address]
        last_claim = datetime.fromtimestamp(data['last_claim'])
        can_claim_at = last_claim + timedelta(hours=config.FAUCET_COOLDOWN_HOURS)
        
        return {
            'has_claimed': True,
            'total_claimed': data['total_claimed'],
            'claim_count': data['claim_count'],
            'last_claim': last_claim,
            'can_claim_at': can_claim_at
        }
    
    def fund_faucet(self, amount, from_wallet):
        """
        Permite donar CLC al faucet
        """
        try:
            transaction = Transaction(
                from_wallet.get_address(),
                self.faucet_wallet.get_address(),
                amount,
                from_wallet.private_key
            )
            
            if transaction.is_valid():
                self.blockchain.add_transaction(transaction)
                return True, f"Donación de {amount} CLC enviada al faucet"
            else:
                return False, "Error al crear la transacción"
        except Exception as e:
            return False, f"Error: {str(e)}"

# Test
if __name__ == "__main__":
    print("\n🎁 Probando sistema de faucet...\n")
    
    from blockchain.storage import BlockchainStorage
    from utils.crypto import generate_keypair
    
    # Cargar blockchain
    storage = BlockchainStorage()
    print("1. Cargando blockchain...")
    bc = storage.load_blockchain("colcript_main.json")
    
    if not bc:
        print("❌ No se pudo cargar blockchain")
        sys.exit(1)
    
    print(f"✅ Blockchain cargada: {len(bc.chain)} bloques\n")
    
    # Crear faucet
    print("2. Inicializando faucet...")
    faucet = Faucet(bc)
    
    # Información del faucet
    print("\n3. Información del faucet:")
    info = faucet.get_faucet_info()
    print(f"   Habilitado: {info['enabled']}")
    print(f"   Cantidad por reclamo: {info['amount_per_claim']} CLC")
    print(f"   Cooldown: {info['cooldown_hours']} horas")
    print(f"   Balance del faucet: {info['faucet_balance']} CLC")
    print(f"   Usuarios que han reclamado: {info['total_users']}")
    print(f"   Total distribuido: {info['total_distributed']} CLC")
    
    # Crear wallet de prueba
    print("\n4. Creando wallet de prueba...")
    priv, pub = generate_keypair()
    print(f"   Dirección: {pub[:30]}...")
    
    # Verificar si puede reclamar
    print("\n5. Verificando elegibilidad...")
    can, msg = faucet.can_claim(pub)
    print(f"   Puede reclamar: {can}")
    print(f"   Mensaje: {msg}")
    
    print("\n✅ Sistema de faucet funcionando\n")
