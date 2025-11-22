# utils/event_system.py - Sistema de Eventos y Notificaciones

import time
import requests
from typing import Dict, List, Callable, Optional
from datetime import datetime
import json
import os

class EventType:
    """Tipos de eventos del sistema"""
    TRANSACTION_CREATED = "transaction_created"
    TRANSACTION_CONFIRMED = "transaction_confirmed"
    BLOCK_MINED = "block_mined"
    BLOCK_ADDED = "block_added"
    WALLET_CREATED = "wallet_created"
    WALLET_LOADED = "wallet_loaded"
    FAUCET_CLAIMED = "faucet_claimed"
    CONTRACT_CREATED = "contract_created"
    CONTRACT_EXECUTED = "contract_executed"
    PEER_CONNECTED = "peer_connected"
    PEER_DISCONNECTED = "peer_disconnected"
    POOL_BLOCK_MINED = "pool_block_mined"
    POOL_MINER_JOINED = "pool_miner_joined"

class Event:
    """Representa un evento del sistema"""
    
    def __init__(self, event_type: str, data: dict):
        self.event_type = event_type
        self.data = data
        self.timestamp = time.time()
        self.id = f"{event_type}_{int(self.timestamp * 1000)}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.event_type,
            'data': self.data,
            'timestamp': self.timestamp,
            'datetime': datetime.fromtimestamp(self.timestamp).isoformat()
        }

class EventListener:
    """Listener de eventos"""
    
    def __init__(self, event_type: str, callback: Callable):
        self.event_type = event_type
        self.callback = callback
        self.id = f"listener_{int(time.time() * 1000000)}"

class WebhookListener:
    """Listener de webhook"""
    
    def __init__(self, event_type: str, url: str):
        self.event_type = event_type
        self.url = url
        self.id = f"webhook_{int(time.time() * 1000000)}"
        self.enabled = True
        self.last_triggered = None
        self.success_count = 0
        self.error_count = 0
    
    def trigger(self, event: Event) -> bool:
        """Dispara el webhook"""
        if not self.enabled:
            return False
        
        try:
            response = requests.post(
                self.url,
                json=event.to_dict(),
                timeout=5
            )
            
            self.last_triggered = time.time()
            
            if response.status_code == 200:
                self.success_count += 1
                return True
            else:
                self.error_count += 1
                return False
        except Exception as e:
            self.error_count += 1
            print(f"Webhook error: {e}")
            return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_type': self.event_type,
            'url': self.url,
            'enabled': self.enabled,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'last_triggered': datetime.fromtimestamp(
                self.last_triggered
            ).isoformat() if self.last_triggered else None
        }

class EventSystem:
    """
    Sistema central de eventos y notificaciones
    
    Permite:
    - Emitir eventos
    - Suscribirse a eventos (callbacks)
    - Registrar webhooks
    - Historial de eventos
    """
    
    def __init__(self):
        self.listeners: Dict[str, List[EventListener]] = {}
        self.webhooks: Dict[str, List[WebhookListener]] = {}
        self.event_history: List[Event] = []
        self.max_history = 100
        
        # Cargar webhooks persistentes
        self.load_webhooks()
    
    def emit(self, event_type: str, data: dict):
        """
        Emite un evento
        
        Args:
            event_type: Tipo de evento (EventType)
            data: Datos del evento
        """
        event = Event(event_type, data)
        
        # Agregar a historial
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
        
        # Notificar listeners
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                try:
                    listener.callback(event)
                except Exception as e:
                    print(f"Listener error: {e}")
        
        # Notificar webhooks
        if event_type in self.webhooks:
            for webhook in self.webhooks[event_type]:
                webhook.trigger(event)
        
        # Log
        print(f"📢 Event: {event_type} - {data}")
    
    def on(self, event_type: str, callback: Callable) -> str:
        """
        Suscribe un callback a un evento
        
        Args:
            event_type: Tipo de evento
            callback: Función a ejecutar
        
        Returns:
            ID del listener
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        
        listener = EventListener(event_type, callback)
        self.listeners[event_type].append(listener)
        
        return listener.id
    
    def off(self, listener_id: str):
        """Desuscribe un listener"""
        for event_type, listeners in self.listeners.items():
            self.listeners[event_type] = [
                l for l in listeners if l.id != listener_id
            ]
    
    def add_webhook(self, event_type: str, url: str) -> str:
        """
        Registra un webhook
        
        Args:
            event_type: Tipo de evento
            url: URL del webhook
        
        Returns:
            ID del webhook
        """
        if event_type not in self.webhooks:
            self.webhooks[event_type] = []
        
        webhook = WebhookListener(event_type, url)
        self.webhooks[event_type].append(webhook)
        
        # Guardar
        self.save_webhooks()
        
        return webhook.id
    
    def remove_webhook(self, webhook_id: str):
        """Elimina un webhook"""
        for event_type, webhooks in self.webhooks.items():
            self.webhooks[event_type] = [
                w for w in webhooks if w.id != webhook_id
            ]
        
        self.save_webhooks()
    
    def get_webhooks(self) -> List[dict]:
        """Obtiene todos los webhooks"""
        result = []
        for webhooks in self.webhooks.values():
            for webhook in webhooks:
                result.append(webhook.to_dict())
        return result
    
    def enable_webhook(self, webhook_id: str):
        """Habilita un webhook"""
        for webhooks in self.webhooks.values():
            for webhook in webhooks:
                if webhook.id == webhook_id:
                    webhook.enabled = True
        self.save_webhooks()
    
    def disable_webhook(self, webhook_id: str):
        """Deshabilita un webhook"""
        for webhooks in self.webhooks.values():
            for webhook in webhooks:
                if webhook.id == webhook_id:
                    webhook.enabled = False
        self.save_webhooks()
    
    def get_history(self, event_type: Optional[str] = None, 
                    limit: int = 50) -> List[dict]:
        """
        Obtiene historial de eventos
        
        Args:
            event_type: Filtrar por tipo (opcional)
            limit: Número máximo de eventos
        
        Returns:
            Lista de eventos
        """
        events = self.event_history
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        # Más recientes primero
        events = sorted(events, key=lambda e: e.timestamp, reverse=True)
        
        return [e.to_dict() for e in events[:limit]]
    
    def save_webhooks(self):
        """Guarda webhooks en archivo"""
        filepath = os.path.join('data', 'webhooks.json')
        os.makedirs('data', exist_ok=True)
        
        webhooks_data = []
        for webhooks in self.webhooks.values():
            for webhook in webhooks:
                webhooks_data.append({
                    'event_type': webhook.event_type,
                    'url': webhook.url,
                    'enabled': webhook.enabled
                })
        
        with open(filepath, 'w') as f:
            json.dump(webhooks_data, f, indent=2)
    
    def load_webhooks(self):
        """Carga webhooks desde archivo"""
        filepath = os.path.join('data', 'webhooks.json')
        
        if not os.path.exists(filepath):
            return
        
        try:
            with open(filepath, 'r') as f:
                webhooks_data = json.load(f)
            
            for data in webhooks_data:
                webhook = WebhookListener(data['event_type'], data['url'])
                webhook.enabled = data.get('enabled', True)
                
                if data['event_type'] not in self.webhooks:
                    self.webhooks[data['event_type']] = []
                
                self.webhooks[data['event_type']].append(webhook)
        except Exception as e:
            print(f"Error loading webhooks: {e}")

# Instancia global del sistema de eventos
event_system = EventSystem()

# Test
if __name__ == "__main__":
    print("\n🔔 Probando Sistema de Eventos...\n")
    
    # Test 1: Emitir evento simple
    print("1️⃣  Emitiendo evento simple...")
    event_system.emit(EventType.WALLET_CREATED, {
        'wallet': 'TestWallet',
        'address': 'abc123'
    })
    
    # Test 2: Suscribir callback
    print("\n2️⃣  Suscribiendo callback...")
    def on_transaction(event):
        print(f"   📨 Transaction recibida: {event.data}")
    
    listener_id = event_system.on(EventType.TRANSACTION_CREATED, on_transaction)
    print(f"   Listener ID: {listener_id}")
    
    # Test 3: Emitir evento con listener
    print("\n3️⃣  Emitiendo evento con listener...")
    event_system.emit(EventType.TRANSACTION_CREATED, {
        'from': 'Alice',
        'to': 'Bob',
        'amount': 10.5
    })
    
    # Test 4: Historial
    print("\n4️⃣  Historial de eventos...")
    history = event_system.get_history(limit=5)
    print(f"   Total eventos: {len(history)}")
    for event in history:
        print(f"   - {event['type']} @ {event['datetime']}")
    
    # Test 5: Webhooks
    print("\n5️⃣  Registrando webhook...")
    webhook_id = event_system.add_webhook(
        EventType.BLOCK_MINED,
        'http://localhost:9999/webhook'
    )
    print(f"   Webhook ID: {webhook_id}")
    
    webhooks = event_system.get_webhooks()
    print(f"   Total webhooks: {len(webhooks)}")
    
    print("\n✅ Sistema de Eventos funcionando\n")
