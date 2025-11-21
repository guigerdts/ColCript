# wallet/wallet.py - Sistema de billetera para ColCript

import os
import sys
import json

# Obtener ruta absoluta del proyecto
project_root = '/data/data/com.termux/files/home/ColCript'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.crypto import generate_keypair
from blockchain.transaction import Transaction

class Wallet:
    def __init__(self, name=None):
        """Crea una nueva wallet"""
        self.name = name or "Wallet"
        self.private_key, self.public_key = generate_keypair()
        print(f"✅ Wallet '{self.name}' creada")
        print(f"   Dirección: {self.public_key[:30]}...")
    
    def get_address(self):
        """Obtiene la dirección pública de la wallet"""
        return self.public_key
    
    def get_balance(self, blockchain):
        """Obtiene el balance de la wallet en una blockchain"""
        return blockchain.get_balance(self.public_key)
    
    def send_coins(self, recipient_address, amount, fee=None):
        """
        Crea una transacción para enviar monedas
        fee: comisión opcional (si no se especifica, usa el default)
        """
        transaction = Transaction(
            self.public_key,
            recipient_address,
            amount,
            self.private_key,
            fee
        )
        
        if transaction.is_valid():
            fee_display = transaction.fee if transaction.fee else 0
            print(f"✅ Transacción creada: {amount} CLC -> {recipient_address[:20]}...")
            return transaction
        else:
            print("❌ Error al crear la transacción")
            return None
    
    def save_to_file(self, filename=None):
        """Guarda la wallet en un archivo"""
        if filename is None:
            filename = f"{self.name.replace(' ', '_')}.json"
        
        wallet_data = {
            'name': self.name,
            'private_key': self.private_key,
            'public_key': self.public_key
        }
        
        filepath = os.path.join(project_root, 'wallet', filename)
        
        with open(filepath, 'w') as f:
            json.dump(wallet_data, f, indent=4)
        
        print(f"💾 Wallet guardada en: {filename}")
        return filepath
    
    @staticmethod
    def load_from_file(filename):
        """Carga una wallet desde un archivo"""
        filepath = os.path.join(project_root, 'wallet', filename)
        
        try:
            with open(filepath, 'r') as f:
                wallet_data = json.load(f)
            
            wallet = Wallet.__new__(Wallet)
            wallet.name = wallet_data['name']
            wallet.private_key = wallet_data['private_key']
            wallet.public_key = wallet_data['public_key']
            
            print(f"✅ Wallet '{wallet.name}' cargada desde archivo")
            print(f"   Dirección: {wallet.public_key[:30]}...")
            return wallet
        except FileNotFoundError:
            print(f"❌ Archivo {filename} no encontrado")
            return None
    
    def __repr__(self):
        return f"Wallet('{self.name}', {self.public_key[:10]}...)"

# Test
if __name__ == "__main__":
    print("\n💼 Probando sistema de Wallet...\n")
    
    # Crear wallet
    my_wallet = Wallet("Mi Wallet ColCript")
    
    # Guardar wallet
    my_wallet.save_to_file()
    
    # Cargar wallet
    print("\n📂 Cargando wallet desde archivo...")
    loaded_wallet = Wallet.load_from_file("Mi_Wallet_ColCript.json")
    
    # Verificar que son iguales
    print(f"\n🔍 Verificación:")
    print(f"   Direcciones coinciden: {my_wallet.get_address() == loaded_wallet.get_address()}")
    
    print("\n✅ Sistema de Wallet funcionando correctamente\n")
