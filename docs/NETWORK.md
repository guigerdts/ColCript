# 🌐 Guía de Red P2P - ColCript

Documentación completa del sistema de red descentralizada Peer-to-Peer de ColCript.

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura de Red](#arquitectura-de-red)
3. [Nodos](#nodos)
4. [Protocolo de Comunicación](#protocolo-de-comunicación)
5. [Sincronización](#sincronización)
6. [Consenso](#consenso)
7. [Configuración de Red](#configuración-de-red)
8. [Casos de Uso](#casos-de-uso)
9. [Resolución de Problemas](#resolución-de-problemas)

---

## 📖 Introducción

La red P2P de ColCript permite que múltiples nodos se conecten y sincronicen entre sí, creando una blockchain verdaderamente descentralizada.

### Características

- **Descentralizada**: No hay servidor central
- **Resistente a fallos**: Si un nodo cae, la red continúa
- **Propagación rápida**: Transacciones y bloques se propagan automáticamente
- **Sincronización automática**: Nuevos nodos se sincronizan con la red
- **Descubrimiento de peers**: Encuentra nodos automáticamente

---

## 🏗️ Arquitectura de Red

### Topología

ColCript usa una topología de red **mesh descentralizada**:
Nodo A
    /   |   \
   /    |    \
Nodo B  |   Nodo C
   \    |    /
    \   |   /
     Nodo D
      /   \
     /     \
 Nodo E   Nodo F
**Características:**
- Cada nodo puede conectarse con múltiples peers
- No hay jerarquía entre nodos
- Información se propaga en todas direcciones
- Redundancia natural

---

### Componentes
┌─────────────────────────────────────┐
│         Nodo ColCript               │
├─────────────────────────────────────┤
│  ┌──────────────────────────────┐  │
│  │   API REST (Puerto 5000)     │  │
│  │  - Endpoints HTTP            │  │
│  │  - JSON responses            │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │   P2P Node (Puerto 6000)     │  │
│  │  - Gestión de peers          │  │
│  │  - Sincronización            │  │
│  │  - Propagación               │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │      Blockchain              │  │
│  │  - Cadena de bloques         │  │
│  │  - Validación                │  │
│  │  - Persistencia              │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
---

## 🔌 Nodos

### Estructura de un Nodo

(python)
class Node:
    node_id: str              # ID único (hash de host:port:timestamp)
    host: str                 # Dirección IP
    port: int                 # Puerto (default: 6000)
    peers: Set[Tuple]         # Set de (host, port)
    blockchain: Blockchain    # Referencia a blockchain local
    
    # Estadísticas
    blocks_received: int
    blocks_sent: int
    transactions_received: int
    transactions_sent: int
    connected_at: float       # Timestamp de inicio
Tipos de Nodos
1. Nodo Completo (Full Node)
Almacena la blockchain completa y valida todas las transacciones.
# Iniciar nodo completo
node = Node(
    host='192.168.1.100',
    port=6000,
    blockchain=blockchain
)
node.start()
Características:
✅ Almacena toda la blockchain
✅ Valida todas las transacciones
✅ Puede minar bloques
✅ Puede propagar transacciones y bloques
❌ Requiere más almacenamiento
❌ Requiere más ancho de banda
2. Nodo Semilla (Seed Node)
Nodo bien conocido que ayuda a otros nodos a descubrir la red.
# Lista de nodos semilla
SEED_NODES = [
    ('seed1.colcript.com', 6000),
    ('seed2.colcript.com', 6000),
    ('192.168.1.100', 6000)
]

# Descubrir peers
discovered = node.discover_peers(SEED_NODES)
Características:
✅ Siempre en línea
✅ Dirección estática conocida
✅ Ayuda a descubrir otros nodos
✅ Mantiene lista de peers activos
Ciclo de Vida de un Nodo
1. Inicialización
   ↓
2. Cargar blockchain local
   ↓
3. Iniciar servidor P2P
   ↓
4. Conectar con seed nodes
   ↓
5. Descubrir peers
   ↓
6. Sincronizar blockchain
   ↓
7. Escuchar nuevas transacciones/bloques
   ↓
8. Propagar información a peers
   ↓
9. (Ciclo continuo)
📡 Protocolo de Comunicación
Endpoints de Red
La comunicación entre nodos se realiza mediante HTTP REST:
Endpoint
Método
Propósito
/api/info
GET
Información básica del nodo
/api/blockchain
GET
Obtener blockchain completa
/api/blockchain/info
GET
Info resumida (altura, etc.)
/api/network/peers
GET
Lista de peers conectados
/api/network/transaction
POST
Recibir nueva transacción
/api/network/block
POST
Recibir nuevo bloque
Mensajes de Red
1. Ping/Pong (Health Check)
# Nodo A verifica si Nodo B está vivo
curl http://nodeB:5000/api/info

# Respuesta de Nodo B
{
  "success": true,
  "data": {
    "nombre": "ColCript",
    "bloques": 42,
    "version": "1.0.0"
  }
}
2. Solicitud de Blockchain
# Nodo A solicita blockchain de Nodo B
curl http://nodeB:5000/api/blockchain/info

# Respuesta
{
  "success": true,
  "data": {
    "bloques": 50,
    "ultimo_bloque": {...}
  }
}

# Si B tiene más bloques, A descarga
curl http://nodeB:5000/api/blockchain
3. Propagación de Transacción
# Nodo A propaga transacción a Nodo B
curl -X POST http://nodeB:5000/api/network/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "address1",
    "recipient": "address2",
    "amount": 10.5,
    "fee": 0.5,
    "timestamp": 1700000000,
    "signature": "signature..."
  }'

# Nodo B responde
{
  "success": true,
  "message": "Transaction received and added to pool"
}

# Nodo B propaga a sus otros peers
4. Propagación de Bloque
# Nodo A mina bloque y lo propaga
curl -X POST http://nodeB:5000/api/network/block \
  -H "Content-Type: application/json" \
  -d '{
    "index": 43,
    "timestamp": 1700000100,
    "transactions": [...],
    "previous_hash": "0000abc...",
    "nonce": 12345,
    "hash": "0000def...",
    "miner_address": "miner..."
  }'

# Nodo B valida y agrega
{
  "success": true,
  "message": "Block received",
  "data": {
    "block_received": true,
    "block_index": 43
  }
}
🔄 Sincronización
Algoritmo de Sincronización
def sync_with_peer(peer_host, peer_port):
    """
    Sincroniza blockchain con un peer
    """
    # 1. Obtener info del peer
    response = requests.get(f"http://{peer_host}:{peer_port}/api/blockchain/info")
    peer_info = response.json()
    
    peer_height = peer_info['data']['bloques']
    local_height = len(blockchain.chain)
    
    print(f"Local: {local_height} bloques")
    print(f"Peer: {peer_height} bloques")
    
    # 2. Determinar si necesitamos sincronizar
    if peer_height > local_height:
        print("Peer tiene más bloques, descargando...")
        
        # 3. Descargar blockchain del peer
        response = requests.get(f"http://{peer_host}:{peer_port}/api/blockchain")
        peer_chain = response.json()['data']['chain']
        
        # 4. Validar cadena del peer
        if validate_chain(peer_chain):
            print("Cadena válida, reemplazando...")
            blockchain.chain = peer_chain
            blockchain.save()
            print("✅ Sincronización completada")
        else:
            print("❌ Cadena inválida, rechazada")
    
    elif peer_height < local_height:
        print("Tenemos más bloques, peer debería sincronizar con nosotros")
    
    else:
        print("Ambos están sincronizados")
Flujo de Sincronización
Nodo A (5 bloques) conecta con Nodo B (10 bloques)
    ↓
A: "¿Cuántos bloques tienes?"
B: "Tengo 10 bloques"
    ↓
A: "Yo solo tengo 5, envíame tu cadena"
B: [envía blockchain completa]
    ↓
A: [valida blockchain recibida]
    ↓
¿Cadena válida?
    ↓ SÍ
A: [reemplaza su cadena con la de B]
A: "Ahora tengo 10 bloques"
    ↓
✅ Sincronizados
Sincronización Inicial
Cuando un nodo nuevo se une a la red:
def initial_sync(node, seed_nodes):
    """
    Sincronización inicial con la red
    """
    print("🔄 Iniciando sincronización con la red...")
    
    # 1. Conectar con seed nodes
    for seed_host, seed_port in seed_nodes:
        success, msg = node.add_peer(seed_host, seed_port)
        if success:
            print(f"✅ Conectado con {seed_host}:{seed_port}")
    
    # 2. Descubrir más peers
    discovered = node.discover_peers(seed_nodes)
    print(f"📡 Descubiertos {discovered} peers")
    
    # 3. Sincronizar con todos los peers
    node.sync_with_network()
    
    # 4. Verificar estado
    height = len(node.blockchain.chain)
    print(f"✅ Sincronización completada: {height} bloques")
⚖️ Consenso
Regla: Cadena Más Larga Gana
ColCript usa el consenso de cadena más larga (similar a Bitcoin):
def resolve_conflicts(node):
    """
    Resuelve conflictos usando la cadena más larga
    """
    max_length = len(node.blockchain.chain)
    new_chain = None
    
    # Verificar todos los peers
    for peer_host, peer_port in node.peers:
        response = requests.get(
            f"http://{peer_host}:{peer_port}/api/blockchain"
        )
        
        if response.status_code == 200:
            peer_data = response.json()
            peer_chain = peer_data['data']['chain']
            peer_length = len(peer_chain)
            
            # Si encontramos cadena más larga y válida
            if peer_length > max_length and validate_chain(peer_chain):
                max_length = peer_length
                new_chain = peer_chain
    
    # Reemplazar si encontramos mejor cadena
    if new_chain:
        node.blockchain.chain = new_chain
        node.blockchain.save()
        return True, f"Chain replaced with length {max_length}"
    
    return False, "Our chain is authoritative"
Escenario: Fork en la Red
Situación inicial:
Todos los nodos tienen: [B0, B1, B2, B3]

Dos mineros minan simultáneamente:
    Nodo A: [B0, B1, B2, B3, B4a]
    Nodo B: [B0, B1, B2, B3, B4b]

Fork temporal:
    Grupo 1: [B0, B1, B2, B3, B4a]
    Grupo 2: [B0, B1, B2, B3, B4b]

Nodo A mina B5:
    Nodo A: [B0, B1, B2, B3, B4a, B5]  (5 bloques)
    Grupo 1: [B0, B1, B2, B3, B4a]     (4 bloques)
    Grupo 2: [B0, B1, B2, B3, B4b]     (4 bloques)

Sincronización:
    Todos adoptan: [B0, B1, B2, B3, B4a, B5]
    (Cadena más larga gana)

B4b es descartado (bloque huérfano)
Prevención de Double Spending
def validate_transaction_in_network(tx):
    """
    Valida que una transacción no sea doble gasto
    """
    # 1. Verificar en blockchain
    if tx_exists_in_chain(tx, blockchain):
        return False, "Transaction already in blockchain"
    
    # 2. Verificar en pool de pendientes
    if tx_exists_in_pool(tx, blockchain.pending_transactions):
        return False, "Transaction already in mempool"
    
    # 3. Verificar balance
    balance = blockchain.get_balance(tx.sender)
    total_needed = tx.amount + tx.fee
    
    if balance < total_needed:
        return False, "Insufficient balance"
    
    # 4. Verificar firma
    if not tx.is_valid():
        return False, "Invalid signature"
    
    return True, "Transaction valid"
⚙️ Configuración de Red
Configurar un Nodo
1. CLI
python colcript.py

# Menú Principal
Opción 19: Red P2P

# Submenú Red P2P
Opción 1: Información del nodo
Opción 3: Agregar peer
    Host: 192.168.1.100
    Puerto: 5000
2. API
# Iniciar servidor (inicia nodo automáticamente)
python api/server.py

# El nodo P2P se inicia en puerto 6000
# La API REST en puerto 5000
3. Programáticamente
from blockchain.blockchain import Blockchain
from network.node import Node

# Crear blockchain
blockchain = Blockchain()

# Crear y iniciar nodo
node = Node(
    host='192.168.1.100',
    port=6000,
    blockchain=blockchain
)
node.start()

print(f"Nodo iniciado: {node.node_id}")
print(f"Host: {node.host}:{node.port}")
Conectar Nodos
Método 1: Agregar Peer Manualmente
# Desde Nodo A, agregar Nodo B
curl -X POST http://localhost:5000/api/network/peer/add \
  -H "Content-Type: application/json" \
  -d '{
    "host": "192.168.1.100",
    "port": 5000
  }'
Método 2: Descubrimiento Automático
# Descubrir peers a través de seed nodes
curl -X POST http://localhost:5000/api/network/discover \
  -H "Content-Type: application/json" \
  -d '{
    "seed_nodes": [
      "192.168.1.100:5000",
      "192.168.1.101:5000"
    ]
  }'
Configurar Red Local
Ejemplo: 3 Nodos en Red Local
Nodo 1 (192.168.1.100):
# Terminal 1
cd ~/ColCript
python api/server.py
# Servidor en 192.168.1.100:5000
# Nodo P2P en 192.168.1.100:6000
Nodo 2 (192.168.1.101):
# Terminal 2 (otra máquina o puerto diferente)
cd ~/ColCript
# Editar config.json para usar puerto 5001
python api/server.py
# Servidor en 192.168.1.101:5001
# Nodo P2P en 192.168.1.101:6001

# Conectar con Nodo 1
curl -X POST http://localhost:5001/api/network/peer/add \
  -d '{"host": "192.168.1.100", "port": 5000}'
Nodo 3 (192.168.1.102):
# Terminal 3
cd ~/ColCript
# Puerto 5002
python api/server.py

# Conectar con Nodo 1 (descubre Nodo 2 automáticamente)
curl -X POST http://localhost:5002/api/network/peer/add \
  -d '{"host": "192.168.1.100", "port": 5000}'
🎯 Casos de Uso
Caso 1: Red de Desarrollo Local
# Nodo 1 (minero)
cd ~/ColCript
python api/server.py

# Nodo 2 (explorador)
# En otra terminal o máquina
cd ~/ColCript
PORT=5001 python api/server.py

# Conectar nodos
curl -X POST http://localhost:5001/api/network/peer/add \
  -d '{"host": "localhost", "port": 5000}'

# Minar en Nodo 1
curl -X POST http://localhost:5000/api/mine \
  -d '{"miner_address": "miner1"}'

# Ver en Nodo 2 (se sincroniza automáticamente)
curl http://localhost:5001/api/blockchain/info
Caso 2: Red Entre Múltiples Usuarios
Configuración:
Alice: 192.168.1.10:5000
Bob: 192.168.1.20:5000
Charlie: 192.168.1.30:5000
Alice crea transacción:
# Alice envía CLC a Bob
curl -X POST http://192.168.1.10:5000/api/transaction \
  -d '{
    "sender": "alice_address",
    "recipient": "bob_address",
    "amount": 10.0,
    "fee": 0.5,
    "private_key": "alice_key"
  }'

# Transacción se propaga automáticamente a Bob y Charlie
Charlie mina el bloque:
curl -X POST http://192.168.1.30:5000/api/mine \
  -d '{"miner_address": "charlie_address"}'

# Bloque se propaga a Alice y Bob
Bob verifica balance:
curl http://192.168.1.20:5000/api/wallet/balance/bob_address
# Balance actualizado: +10 CLC
Caso 3: Nodo Público en Internet
Configurar firewall:
# Abrir puertos
sudo ufw allow 5000/tcp  # API REST
sudo ufw allow 6000/tcp  # P2P
Configurar IP pública:
# En network/node.py
node = Node(
    host='0.0.0.0',  # Escuchar en todas las interfaces
    port=6000,
    blockchain=blockchain
)
Usar servicio de DNS dinámico:
- Registrar dominio: minnodo.ddns.net
- Configurar para apuntar a IP pública
- Compartir: minnodo.ddns.net:5000
🐛 Resolución de Problemas
Problema 1: Nodo No Se Conecta
Síntomas:
curl -X POST http://localhost:5000/api/network/peer/add \
  -d '{"host": "192.168.1.100", "port": 5000}'

# Respuesta:
{
  "success": false,
  "message": "Peer is not responding"
}
Soluciones:
Verificar que el peer esté en línea:
curl http://192.168.1.100:5000/api/info
Verificar firewall:
# Linux
sudo ufw status
sudo ufw allow 5000/tcp

# Verificar conectividad
telnet 192.168.1.100 5000
Verificar IP correcta:
# En la máquina del peer
ip addr show
# o
ifconfig
Problema 2: Sincronización Lenta
Síntomas:
Descarga de blockchain muy lenta
Timeout en requests
Soluciones:
Aumentar timeout:
response = requests.get(
    url,
    timeout=30  # Aumentar a 30 segundos
)
Sincronizar en lotes:
# En lugar de toda la cadena, descargar por rangos
for start in range(0, total_blocks, 100):
    end = min(start + 100, total_blocks)
    blocks = download_blocks_range(start, end)
    validate_and_add(blocks)
Usar compresión:
import gzip

# Comprimir blockchain antes de enviar
compressed = gzip.compress(json.dumps(chain).encode())
Problema 3: Fork No Se Resuelve
Síntomas:
Diferentes nodos tienen diferentes cadenas
Consenso no converge
Soluciones:
Forzar sincronización:
curl -X POST http://localhost:5000/api/network/sync
Verificar validez de cadenas:
curl -X POST http://localhost:5000/api/blockchain/validate
Reset y resincronizar:
# Backup de wallet
# Eliminar blockchain local
# Descargar desde peer confiable
Problema 4: Doble Gasto
Síntomas:
Misma transacción aparece múltiples veces
Balance negativo
Prevención:
def add_transaction(tx):
    # 1. Verificar que no existe en blockchain
    for block in blockchain.chain:
        for block_tx in block.transactions:
            if tx.signature == block_tx.signature:
                return False, "Transaction already in chain"
    
    # 2. Verificar que no está en pool
    for pending_tx in blockchain.pending_transactions:
        if tx.signature == pending_tx.signature:
            return False, "Transaction already pending"
    
    # 3. Agregar al pool
    blockchain.pending_transactions.append(tx)
    return True, "Transaction added"
Problema 5: Nodo Desincronizado
Síntomas:
curl http://localhost:5000/api/blockchain/info
# Local: 42 bloques

curl http://peer:5000/api/blockchain/info
# Peer: 50 bloques
Solución:
# Forzar sincronización completa
curl -X POST http://localhost:5000/api/network/sync

# Verificar
curl http://localhost:5000/api/blockchain/info
# Local: 50 bloques ✅
📊 Monitoreo de Red
Script de Monitoreo
#!/bin/bash
# monitor_network.sh

while true; do
    clear
    echo "=== ESTADO DE LA RED ==="
    echo ""
    
    # Info del nodo
    echo "Nodo Local:"
    curl -s http://localhost:5000/api/network/info | jq '.data'
    
    echo ""
    echo "Peers:"
    curl -s http://localhost:5000/api/network/peers | jq '.data.peers[]'
    
    echo ""
    echo "Blockchain:"
    curl -s http://localhost:5000/api/blockchain/info | jq '.data'
    
    sleep 5
done
Uso:
chmod +x monitor_network.sh
./monitor_network.sh
Dashboard de Red
# network_dashboard.py
import requests
import time
from rich.console import Console
from rich.table import Table

console = Console()

def show_network_status():
    while True:
        console.clear()
        
        # Tabla de nodos
        table = Table(title="Red ColCript")
        table.add_column("Nodo", style="cyan")
        table.add_column("Bloques", style="magenta")
        table.add_column("Peers", style="green")
        table.add_column("Estado", style="yellow")
        
        nodes = [
            ("localhost:5000", "Local"),
            ("192.168.1.100:5000", "Peer 1"),
            ("192.168.1.101:5000", "Peer 2")
        ]
        
        for node_url, node_name in nodes:
            try:
                response = requests.get(
                    f"http://{node_url}/api/blockchain/info",
                    timeout=2
                )
                data = response.json()['data']
                
                table.add_row(
                    node_name,
                    str(data['bloques']),
                    str(len(data.get('peers', []))),
                    "✅ Online"
                )
            except:
                table.add_row(
                    node_name,
                    "-",
                    "-",
                    "❌ Offline"
                )
        
        console.print(table)
        time.sleep(5)

if __name__ == "__main__":
    show_network_status()
📚 Referencias
Bitcoin P2P Network
Ethereum DevP2P
Libp2p Specification
Gossip Protocol
🔗 Recursos Adicionales
API Reference - Endpoints de red
Architecture - Diseño del sistema P2P
Installation Guide - Configurar múltiples nodos
¡Tu nodo está listo para unirse a la red ColCript! 🌐
