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

    def to_dict(self):
        """
        Exporta wallet a diccionario para guardar en JSON
        
        POR QUÉ: Permite guardar y cargar wallets desde archivos
        Los tests necesitan este método para verificar serialización
        
        Returns:
            dict con name, private_key, public_key
        """
        return {
            'name': self.name,
            'private_key': self.private_key,
            'public_key': self.public_key
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crea wallet desde diccionario
        
        POR QUÉ: Permite cargar wallets guardadas desde diccionarios
        Complementa to_dict() para serialización completa
        
        Args:
            data: diccionario con name, private_key, public_key
        
        Returns:
            Wallet object reconstruido
        """
        wallet = Wallet.__new__(Wallet)  # Crear sin llamar __init__
        wallet.name = data.get('name', 'Wallet')
        wallet.private_key = data['private_key']
        wallet.public_key = data['public_key']
        return wallet

    def __repr__(self):
        return f"Wallet('{self.name}', {self.public_key[:10]}...)"

# Test
if __name__ == "__main__":
    print("\n💼 Probando sistema de Wallet...\n")

    # Crear wallet
    my_wallet = Wallet("Mi Wallet ColCript")

    # Test to_dict (NUEVO)
    print("\n📋 Test to_dict()...")
    wallet_dict = my_wallet.to_dict()
    print(f"   Exportado: {list(wallet_dict.keys())}")

    # Test from_dict (NUEVO)
    print("\n📥 Test from_dict()...")
    restored_wallet = Wallet.from_dict(wallet_dict)
    print(f"   Dirección original: {my_wallet.get_address()[:30]}...")
    print(f"   Dirección restaurada: {restored_wallet.get_address()[:30]}...")
    print(f"   ¿Son iguales? {my_wallet.get_address() == restored_wallet.get_address()}")

    # Guardar wallet
    print("\n💾 Test save_to_file()...")
    my_wallet.save_to_file()

    # Cargar wallet
    print("\n📂 Test load_from_file()...")
    loaded_wallet = Wallet.load_from_file("Mi_Wallet_ColCript.json")

    # Verificar que son iguales
    print(f"\n🔍 Verificación final:")
    print(f"   Direcciones coinciden: {my_wallet.get_address() == loaded_wallet.get_address()}")

    print("\n✅ Sistema de Wallet funcionando correctamente\n")
