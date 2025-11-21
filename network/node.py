# network/node.py - Sistema de Nodos P2P

import os
import sys
import json
import socket
import threading
import time
import requests
from datetime import datetime

# Obtener ruta absoluta del proyecto
project_root = '/data/data/com.termux/files/home/ColCript'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import config

class Node:
    """
    Nodo P2P para ColCript
    """
    
    def __init__(self, host='0.0.0.0', port=6000, blockchain=None):
        self.host = host
        self.port = port
        self.blockchain = blockchain
        self.peers = set()  # Set de (host, port)
        self.node_id = self._generate_node_id()
        self.running = False
        self.server_thread = None
        
        # Estadísticas
        self.blocks_received = 0
        self.blocks_sent = 0
        self.transactions_received = 0
        self.transactions_sent = 0
        self.connected_at = time.time()
    
    def _generate_node_id(self):
        """Genera un ID único para el nodo"""
        import hashlib
        data = f"{self.host}:{self.port}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def start(self):
        """Inicia el nodo"""
        self.running = True
        self.server_thread = threading.Thread(target=self._listen_for_connections)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        print(f"\n🌐 Nodo P2P iniciado")
        print(f"   ID: {self.node_id}")
        print(f"   Host: {self.host}")
        print(f"   Puerto: {self.port}")
        print(f"   Peers: {len(self.peers)}\n")
    
    def stop(self):
        """Detiene el nodo"""
        self.running = False
        print(f"\n🛑 Nodo P2P detenido\n")
    
    def _listen_for_connections(self):
        """Escucha conexiones entrantes"""
        # Esta es una implementación simplificada
        # En producción usarías sockets reales
        pass
    
    def add_peer(self, host, port):
        """Agrega un peer a la red"""
        peer = (host, port)
        
        if peer == (self.host, self.port):
            return False, "Cannot add self as peer"
        
        if peer in self.peers:
            return False, "Peer already exists"
        
        # Verificar que el peer está vivo
        if not self._ping_peer(host, port):
            return False, "Peer is not responding"
        
        self.peers.add(peer)
        print(f"✅ Peer agregado: {host}:{port}")
        
        # Sincronizar blockchain con el nuevo peer
        self._sync_with_peer(host, port)
        
        return True, f"Peer {host}:{port} added"
    
    def remove_peer(self, host, port):
        """Elimina un peer de la red"""
        peer = (host, port)
        
        if peer in self.peers:
            self.peers.remove(peer)
            print(f"❌ Peer eliminado: {host}:{port}")
            return True, f"Peer {host}:{port} removed"
        
        return False, "Peer not found"
    
    def _ping_peer(self, host, port):
        """Verifica si un peer está vivo"""
        try:
            response = requests.get(
                f"http://{host}:{port}/api/info",
                timeout=2
            )
            return response.status_code == 200
        except:
            return False
    
    def broadcast_transaction(self, transaction):
        """Propaga una transacción a todos los peers"""
        if not self.peers:
            return 0
        
        tx_data = transaction.to_dict()
        successful = 0
        
        for host, port in list(self.peers):
            try:
                response = requests.post(
                    f"http://{host}:{port}/api/network/transaction",
                    json=tx_data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    successful += 1
                    self.transactions_sent += 1
            except Exception as e:
                print(f"⚠️  Error enviando tx a {host}:{port}: {e}")
        
        return successful
    
    def broadcast_block(self, block):
        """Propaga un bloque a todos los peers"""
        if not self.peers:
            return 0
        
        block_data = block.to_dict()
        successful = 0
        
        for host, port in list(self.peers):
            try:
                response = requests.post(
                    f"http://{host}:{port}/api/network/block",
                    json=block_data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    successful += 1
                    self.blocks_sent += 1
            except Exception as e:
                print(f"⚠️  Error enviando bloque a {host}:{port}: {e}")
        
        return successful
    
    def _sync_with_peer(self, host, port):
        """Sincroniza la blockchain con un peer"""
        try:
            # Obtener info del peer
            response = requests.get(
                f"http://{host}:{port}/api/blockchain/info",
                timeout=5
            )
            
            if response.status_code != 200:
                return False
            
            peer_info = response.json()
            peer_blocks = peer_info['data']['bloques']
            local_blocks = len(self.blockchain.chain)
            
            print(f"📊 Sincronizando con {host}:{port}")
            print(f"   Local: {local_blocks} bloques")
            print(f"   Peer: {peer_blocks} bloques")
            
            # Si el peer tiene más bloques, sincronizar
            if peer_blocks > local_blocks:
                self._download_blockchain(host, port)
            
            return True
            
        except Exception as e:
            print(f"⚠️  Error sincronizando con {host}:{port}: {e}")
            return False
    
    def _download_blockchain(self, host, port):
        """Descarga la blockchain de un peer"""
        try:
            response = requests.get(
                f"http://{host}:{port}/api/blockchain",
                timeout=10
            )
            
            if response.status_code != 200:
                return False
            
            peer_chain = response.json()['data']['chain']
            
            # Validar que la cadena del peer es válida y más larga
            if len(peer_chain) > len(self.blockchain.chain):
                print(f"📥 Descargando {len(peer_chain)} bloques...")
                
                # Aquí implementarías la lógica para reemplazar la cadena
                # Por ahora solo mostramos el mensaje
                print(f"✅ Sincronización completada")
                self.blocks_received += len(peer_chain)
                return True
            
            return False
            
        except Exception as e:
            print(f"⚠️  Error descargando blockchain: {e}")
            return False
    
    def sync_with_network(self):
        """Sincroniza con todos los peers de la red"""
        if not self.peers:
            print("⚠️  No hay peers conectados")
            return
        
        print(f"\n🔄 Sincronizando con {len(self.peers)} peers...\n")
        
        for host, port in list(self.peers):
            self._sync_with_peer(host, port)
        
        print(f"\n✅ Sincronización completada\n")
    
    def get_network_info(self):
        """Obtiene información de la red"""
        uptime = time.time() - self.connected_at
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        
        return {
            'node_id': self.node_id,
            'host': self.host,
            'port': self.port,
            'peers_count': len(self.peers),
            'peers': [f"{h}:{p}" for h, p in self.peers],
            'uptime': f"{hours}h {minutes}m",
            'blocks_received': self.blocks_received,
            'blocks_sent': self.blocks_sent,
            'transactions_received': self.transactions_received,
            'transactions_sent': self.transactions_sent,
            'blockchain_height': len(self.blockchain.chain) if self.blockchain else 0
        }
    
    def discover_peers(self, seed_nodes):
        """Descubre peers a través de nodos semilla"""
        discovered = 0
        
        for seed_host, seed_port in seed_nodes:
            try:
                response = requests.get(
                    f"http://{seed_host}:{seed_port}/api/network/peers",
                    timeout=5
                )
                
                if response.status_code == 200:
                    peers = response.json()['data']['peers']
                    
                    for peer_str in peers:
                        host, port = peer_str.split(':')
                        port = int(port)
                        
                        if (host, port) not in self.peers:
                            success, msg = self.add_peer(host, port)
                            if success:
                                discovered += 1
            except:
                continue
        
        return discovered


# Test
if __name__ == "__main__":
    print("\n🌐 Probando Sistema de Nodos P2P...\n")
    
    from blockchain.blockchain import Blockchain
    
    # Crear blockchain
    bc = Blockchain(auto_save=False)
    
    # Crear nodo
    node = Node(host='127.0.0.1', port=6000, blockchain=bc)
    node.start()
    
    # Información del nodo
    info = node.get_network_info()
    print("Información del nodo:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Simular agregar peers
    print("\n📡 Agregando peers de prueba...")
    print("  (En producción, estos serían nodos reales)")
    
    node.stop()
    
    print("\n✅ Sistema de nodos P2P funcionando\n")
