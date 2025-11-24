#!/usr/bin/env python3

# wallet/advanced.py - Funcionalidades avanzadas de wallet para ColCript

import os
import sys
import json
import csv
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import requests

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class AdvancedWallet:
    def __init__(self, wallet_address: str, node_url: str = "http://localhost:5000"):
        self.address = wallet_address
        self.node_url = node_url
        self.contacts_file = Path(f"wallet/wallet_{wallet_address[:10]}_contacts.json")
        self.labels_file = Path(f"wallet/wallet_{wallet_address[:10]}_labels.json")
        
        # Cargar contactos y etiquetas
        self.contacts = self._load_contacts()
        self.labels = self._load_labels()
    
    def _load_contacts(self) -> Dict:
        """Cargar libro de contactos"""
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_contacts(self):
        """Guardar contactos"""
        with open(self.contacts_file, 'w') as f:
            json.dump(self.contacts, f, indent=2)
    
    def _load_labels(self) -> Dict:
        """Cargar etiquetas de direcciones"""
        if self.labels_file.exists():
            with open(self.labels_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_labels(self):
        """Guardar etiquetas"""
        with open(self.labels_file, 'w') as f:
            json.dump(self.labels, f, indent=2)
    
    # === CONTACTOS ===
    
    def add_contact(self, name: str, address: str, notes: str = ""):
        """Agregar contacto al libro de direcciones"""
        self.contacts[name] = {
            "address": address,
            "notes": notes,
            "created": datetime.now().isoformat()
        }
        self._save_contacts()
        return True
    
    def remove_contact(self, name: str):
        """Eliminar contacto"""
        if name in self.contacts:
            del self.contacts[name]
            self._save_contacts()
            return True
        return False
    
    def get_contact(self, name: str) -> Optional[Dict]:
        """Obtener contacto por nombre"""
        return self.contacts.get(name)
    
    def list_contacts(self) -> Dict:
        """Listar todos los contactos"""
        return self.contacts
    
    def find_contact_by_address(self, address: str) -> Optional[str]:
        """Buscar nombre de contacto por dirección"""
        for name, info in self.contacts.items():
            if info["address"] == address:
                return name
        return None
    
    # === ETIQUETAS ===
    
    def add_label(self, address: str, label: str):
        """Agregar etiqueta a una dirección"""
        self.labels[address] = label
        self._save_labels()
        return True
    
    def remove_label(self, address: str):
        """Eliminar etiqueta de una dirección"""
        if address in self.labels:
            del self.labels[address]
            self._save_labels()
            return True
        return False
    
    def get_label(self, address: str) -> Optional[str]:
        """Obtener etiqueta de una dirección"""
        # Primero buscar en etiquetas
        if address in self.labels:
            return self.labels[address]
        # Luego buscar en contactos
        contact_name = self.find_contact_by_address(address)
        if contact_name:
            return f"Contact: {contact_name}"
        return None
    
    # === HISTORIAL ===
    
    def get_transaction_history(self, limit: int = 100) -> List[Dict]:
        """Obtener historial completo de transacciones"""
        try:
            # Obtener todas las transacciones de la blockchain
            chain_response = requests.get(f"{self.node_url}/api/chain", timeout=5)
            if chain_response.status_code != 200:
                return []
            
            chain_data = chain_response.json()
            blocks = chain_data.get("data", {}).get("chain", [])
            
            transactions = []
            
            for block in blocks:
                block_time = block.get("timestamp", "")
                block_index = block.get("index", 0)
                
                for tx in block.get("transactions", []):
                    tx_hash = tx.get("hash", "")
                    sender = tx.get("sender", "")
                    recipient = tx.get("recipient", "")
                    amount = tx.get("amount", 0)
                    fee = tx.get("fee", 0)
                    tx_type = tx.get("type", "transfer")
                    
                    # Solo incluir transacciones relacionadas con esta wallet
                    if sender == self.address or recipient == self.address:
                        direction = "sent" if sender == self.address else "received"
                        other_party = recipient if direction == "sent" else sender
                        
                        transactions.append({
                            "hash": tx_hash,
                            "block": block_index,
                            "timestamp": block_time,
                            "direction": direction,
                            "amount": amount,
                            "fee": fee if direction == "sent" else 0,
                            "type": tx_type,
                            "from": sender,
                            "to": recipient,
                            "other_party": other_party,
                            "other_party_label": self.get_label(other_party)
                        })
            
            # Ordenar por tiempo (más reciente primero)
            transactions.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return transactions[:limit]
            
        except Exception as e:
            print(f"❌ Error obteniendo historial: {e}")
            return []
    
    def get_transaction_stats(self) -> Dict:
        """Obtener estadísticas de transacciones"""
        history = self.get_transaction_history(limit=10000)
        
        total_sent = sum(tx["amount"] for tx in history if tx["direction"] == "sent")
        total_received = sum(tx["amount"] for tx in history if tx["direction"] == "received")
        total_fees = sum(tx["fee"] for tx in history)
        
        sent_count = len([tx for tx in history if tx["direction"] == "sent"])
        received_count = len([tx for tx in history if tx["direction"] == "received"])
        
        return {
            "total_transactions": len(history),
            "sent_count": sent_count,
            "received_count": received_count,
            "total_sent": total_sent,
            "total_received": total_received,
            "total_fees": total_fees,
            "net_flow": total_received - total_sent - total_fees
        }
    
    # === EXPORTAR ===
    
    def export_to_json(self, filename: str = None) -> str:
        """Exportar historial a JSON"""
        if not filename:
            filename = f"wallet_{self.address[:10]}_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        history = self.get_transaction_history(limit=10000)
        stats = self.get_transaction_stats()
        
        export_data = {
            "wallet_address": self.address,
            "export_date": datetime.now().isoformat(),
            "statistics": stats,
            "transactions": history,
            "contacts": self.contacts,
            "labels": self.labels
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename
    
    def export_to_csv(self, filename: str = None) -> str:
        """Exportar historial a CSV"""
        if not filename:
            filename = f"wallet_{self.address[:10]}_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        history = self.get_transaction_history(limit=10000)
        
        with open(filename, 'w', newline='') as f:
            if not history:
                return filename
            
            fieldnames = ['timestamp', 'block', 'hash', 'direction', 'amount', 
                         'fee', 'type', 'from', 'to', 'other_party_label']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for tx in history:
                writer.writerow({
                    'timestamp': tx['timestamp'],
                    'block': tx['block'],
                    'hash': tx['hash'],
                    'direction': tx['direction'],
                    'amount': tx['amount'],
                    'fee': tx['fee'],
                    'type': tx['type'],
                    'from': tx['from'],
                    'to': tx['to'],
                    'other_party_label': tx.get('other_party_label', '')
                })
        
        return filename

# === FUNCIONES DE UTILIDAD ===

def format_transaction(tx: Dict) -> str:
    """Formatear transacción para mostrar"""
    direction_symbol = "📤" if tx["direction"] == "sent" else "📥"
    amount_str = f"-{tx['amount']}" if tx["direction"] == "sent" else f"+{tx['amount']}"
    
    other_label = tx.get("other_party_label", "")
    other_display = f" ({other_label})" if other_label else ""
    
    return f"{direction_symbol} {amount_str} CLC - {tx['type']} - Block #{tx['block']}{other_display}"

def print_transaction_history(wallet_address: str, limit: int = 20):
    """Imprimir historial de transacciones bonito"""
    wallet = AdvancedWallet(wallet_address)
    history = wallet.get_transaction_history(limit=limit)
    
    print(f"\n{'='*80}")
    print(f"📊 HISTORIAL DE TRANSACCIONES - {wallet_address[:20]}...")
    print(f"{'='*80}\n")
    
    if not history:
        print("❌ No hay transacciones")
        return
    
    for i, tx in enumerate(history, 1):
        print(f"{i}. {format_transaction(tx)}")
        print(f"   Hash: {tx['hash'][:32]}...")
        print(f"   Fecha: {tx['timestamp']}")
        if tx['direction'] == 'sent':
            print(f"   Fee: {tx['fee']} CLC")
        print()
    
    # Mostrar estadísticas
    stats = wallet.get_transaction_stats()
    print(f"\n{'='*80}")
    print("📈 ESTADÍSTICAS")
    print(f"{'='*80}")
    print(f"Total Transacciones: {stats['total_transactions']}")
    print(f"Enviadas: {stats['sent_count']} ({stats['total_sent']} CLC)")
    print(f"Recibidas: {stats['received_count']} ({stats['total_received']} CLC)")
    print(f"Fees pagados: {stats['total_fees']} CLC")
    print(f"Balance neto: {stats['net_flow']:+.2f} CLC")
    print()

if __name__ == "__main__":
    print("🎯 ColCript Advanced Wallet Module")
    print("   Úsalo desde: python -m wallet.advanced")
