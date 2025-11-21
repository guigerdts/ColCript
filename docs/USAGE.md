# 📖 Guía de Uso - ColCript

Guía completa para usar todas las funcionalidades de ColCript.

---

## 📋 Tabla de Contenidos

1. [Inicio Rápido](#inicio-rápido)
2. [Interfaz CLI](#interfaz-cli)
3. [API REST](#api-rest)
4. [Interfaz Web](#interfaz-web)
5. [Gestión de Wallets](#gestión-de-wallets)
6. [Transacciones](#transacciones)
7. [Minería](#minería)
8. [Smart Contracts](#smart-contracts)
9. [Red P2P](#red-p2p)
10. [Casos de Uso Comunes](#casos-de-uso-comunes)

---

## 🚀 Inicio Rápido

### Primer Uso (5 minutos)

bash
# 1. Iniciar ColCript CLI
cd ~/ColCript
python colcript.py

# 2. Crear blockchain
Opción: 1
Auto-guardado: S
Nombre: mi_blockchain.json

# 3. Crear wallet
Opción: 4
Nombre: MiWallet

# 4. Obtener CLC gratis
Opción: 10
Dirección: [tu_dirección]

# 5. Minar algunos bloques
Opción: 12 (hacer 3 veces)

# 6. Ver balance
Opción: 6
# Deberías tener ~155 CLC (50*3 recompensa + 5 faucet)

# 7. Enviar CLC
Opción: 11
Destinatario: [otra_dirección]
Cantidad: 10
¡Felicidades! Has completado tu primera transacción en ColCript. 🎉
💻 Interfaz CLI
Menú Principal
📋 MENÚ PRINCIPAL:
  1. Crear nueva blockchain       11. Enviar ColCript
  2. Cargar blockchain existente  12. Minar bloque
  3. Listar blockchains guardadas 13. Ver blockchain
  4. Crear nueva wallet           14. Ver información
  5. Cargar wallet existente      15. Guardar wallet
  6. Ver balance                  16. Guardar blockchain manualmente
  7. Ver historial de transacciones  17. Ajuste de dificultad
  8. Explorador de bloques        18. Smart Contracts
  9. Estadísticas y métricas      19. Red P2P
 10. Faucet (CLC gratis)           0. Salir
1. Gestión de Blockchain
Crear Nueva Blockchain
python colcript.py

Opción: 1
¿Activar auto-guardado? (S/n): S
Nombre del archivo: mi_blockchain.json
Resultado:
Se crea bloque génesis
Blockchain lista para usar
Auto-guardado activado
Cargar Blockchain Existente
Opción: 2
Número de blockchain a cargar: [seleccionar]
Notas:
Valida integridad al cargar
Muestra error si está corrupta
Activa auto-guardado si estaba configurado
Listar Blockchains
Opción: 3
Muestra:
Nombre del archivo
Número de bloques
Fecha de última modificación
2. Gestión de Wallets
Crear Wallet
Opción: 4
Nombre de la wallet: MiWallet
Guarda:
Clave pública
Clave privada (¡importante!)
Dirección
⚠️ IMPORTANTE: Anota tu clave privada. No se puede recuperar.
Cargar Wallet
Opción: 5
Nombre del archivo: MiWallet.json
Ver Balance
Opción: 6
Muestra:
Balance disponible
Transacciones pendientes (enviadas/recibidas)
Balance total
Ver Historial
Opción: 7
Muestra:
Todas las transacciones
Tipo (enviada/recibida/recompensa)
Cantidad, fee, bloque
Timestamp
3. Faucet
Opción: 10
Dirección: [tu_dirección]
Reglas:
5 CLC gratis
Cooldown: 24 horas
Una vez por dirección
4. Transacciones
Enviar CLC
Opción: 11

Destinatario: abc123def456...
Cantidad: 10.5
Fee (sugerido 0.5): 0.5
Proceso:
Validación de balance
Firma con clave privada
Agregado al pool
Esperando minería
5. Minería
Minar Bloque
Opción: 12
Proceso:
Selecciona transacciones del pool
Crea bloque candidato
Ejecuta Proof of Work
Agrega bloque a la cadena
Recibe recompensa + fees
Recompensa:
Base: 50 CLC
Fees de transacciones
Se guarda automáticamente
6. Explorador
Ver Blockchain
Opción: 13
Muestra todos los bloques con:
Índice, hash, timestamp
Número de transacciones
Minero, nonce
Explorador Interactivo
Opción: 8

Opciones:
  1. Buscar bloque por índice
  2. Buscar bloque por hash
  3. Buscar transacción
  4. Ver bloque más reciente
  5. Ver detalles de transacción
7. Estadísticas
Opción: 9
Muestra:
Total de bloques
Transacciones totales
Dificultad actual
Hashrate estimado
Supply total
Top wallets
8. Ajuste de Dificultad
Opción: 17

Submenú:
  1. Ver información de dificultad
  2. Configurar dificultad manual
  3. Habilitar/deshabilitar auto-ajuste
  4. Configurar parámetros de ajuste
Ejemplo:
Opción: 2 (Configurar manual)
Nueva dificultad (1-20): 5
✅ Dificultad establecida en 5
⚠️  Auto-ajuste deshabilitado
9. Smart Contracts
Opción: 18

Submenú:
  1. Crear Timelock
  2. Crear Multisig
  3. Crear Escrow
  4. Listar contratos
  5. Ver contrato
  6. Ejecutar contrato
  7. Firmar contrato (Multisig)
  8. Decidir Escrow
Ver guía completa: CONTRACTS.md
10. Red P2P
Opción: 19

Submenú:
  1. Información del nodo
  2. Listar peers
  3. Agregar peer
  4. Eliminar peer
  5. Sincronizar con red
  6. Descubrir peers
  7. Detener nodo
Ver guía completa: NETWORK.md
🌐 API REST
Iniciar Servidor
cd ~/ColCript
python api/server.py
Servidor disponible en:
API: http://localhost:5000
Interfaz Web: http://localhost:5000
Documentación: http://localhost:5000/api/docs
Ejemplos de Uso con cURL
Información General
curl http://localhost:5000/api/info
Ver Blockchain
curl http://localhost:5000/api/blockchain
Crear Wallet
curl -X POST http://localhost:5000/api/wallet/create \
  -H "Content-Type: application/json" \
  -d '{"name": "ApiWallet"}'
Ver Balance
curl http://localhost:5000/api/wallet/balance/[dirección]
Crear Transacción
curl -X POST http://localhost:5000/api/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "dirección_origen",
    "recipient": "dirección_destino",
    "amount": 10.5,
    "fee": 0.5,
    "private_key": "clave_privada"
  }'
Minar Bloque
curl -X POST http://localhost:5000/api/mine \
  -H "Content-Type: application/json" \
  -d '{"miner_address": "tu_dirección"}'
Usar Faucet
curl -X POST http://localhost:5000/api/faucet/claim \
  -H "Content-Type: application/json" \
  -d '{"address": "tu_dirección"}'
Ejemplos con Python
import requests

BASE_URL = "http://localhost:5000/api"

# Obtener info
response = requests.get(f"{BASE_URL}/info")
print(response.json())

# Crear wallet
response = requests.post(
    f"{BASE_URL}/wallet/create",
    json={"name": "PythonWallet"}
)
wallet = response.json()['data']
print(f"Dirección: {wallet['address']}")

# Obtener CLC del faucet
response = requests.post(
    f"{BASE_URL}/faucet/claim",
    json={"address": wallet['address']}
)
print(response.json()['message'])

# Ver balance
response = requests.get(
    f"{BASE_URL}/wallet/balance/{wallet['address']}"
)
balance = response.json()['data']['balance']
print(f"Balance: {balance} CLC")
Ejemplos con JavaScript
const BASE_URL = 'http://localhost:5000/api';

// Obtener info
fetch(`${BASE_URL}/info`)
  .then(res => res.json())
  .then(data => console.log(data));

// Crear wallet
fetch(`${BASE_URL}/wallet/create`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({name: 'JsWallet'})
})
  .then(res => res.json())
  .then(data => {
    console.log('Dirección:', data.data.address);
  });

// Usar faucet
fetch(`${BASE_URL}/faucet/claim`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({address: 'tu_dirección'})
})
  .then(res => res.json())
  .then(data => console.log(data.message));
Ver documentación completa: API.md
🖥️ Interfaz Web
Acceder
Iniciar servidor:
python api/server.py
Abrir navegador:
http://localhost:5000
Páginas Disponibles
1. Dashboard (📊)
Funcionalidades:
Resumen general
Gráfica de bloques minados
Transacciones recientes
Balance de wallet
Estadísticas de red
2. Wallet (💼)
Funcionalidades:
Crear nueva wallet
Cargar wallet existente
Ver balance
Historial de transacciones
Copiar dirección
Uso:
Click en "💼 Wallet"
"Crear Nueva Wallet"
Guardar clave privada
Ver dirección y balance
3. Minería (⛏️)
Funcionalidades:
Iniciar minería
Ver progreso en tiempo real
Historial de bloques minados
Estadísticas de minería
Uso:
Cargar wallet
Click en "⛏️ Minería"
"Minar Bloque"
Esperar (10-30 segundos según dificultad)
Ver recompensa
4. Explorador (🔍)
Funcionalidades:
Ver todos los bloques
Buscar por índice o hash
Ver transacciones de cada bloque
Detalles completos
Uso:
Click en "🔍 Explorador"
Ver lista de bloques
Click en un bloque para detalles
Ver transacciones incluidas
5. Faucet (🎁)
Funcionalidades:
Reclamar 5 CLC gratis
Ver cooldown restante
Historial de claims
Uso:
Click en "🎁 Faucet"
Ingresar tu dirección
"Reclamar CLC"
Esperar 24h para siguiente claim
6. Contratos (📜)
Funcionalidades:
Crear contratos (Timelock, Multisig, Escrow)
Ver contratos activos
Ejecutar contratos
Firmar contratos Multisig
Uso Timelock:
Click en "📜 Contratos"
Seleccionar "Timelock"
Ingresar:
Bloque de desbloqueo: 100
Cantidad: 50 CLC
Destinatario: dirección
"Crear Timelock"
Esperar hasta bloque 100
"Ejecutar" contrato
7. Red P2P (🌐)
Funcionalidades:
Ver información del nodo
Agregar/eliminar peers
Sincronizar con red
Estadísticas de red
Uso:
Click en "🌐 Red P2P"
Ver info del nodo local
"Agregar Peer"
Ingresar IP y puerto
"Sincronizar Red"
8. Ajustes (⚙️)
Funcionalidades:
Configurar dificultad
Habilitar/deshabilitar auto-ajuste
Configurar parámetros de minería
Ver configuración actual
👛 Gestión de Wallets
Crear Wallet
CLI:
python colcript.py
Opción: 4
Nombre: MiWallet
API:
curl -X POST http://localhost:5000/api/wallet/create \
  -d '{"name": "MiWallet"}'
Python:
from blockchain.wallet import Wallet

wallet = Wallet(name="MiWallet")
wallet.save()

print(f"Dirección: {wallet.get_address()}")
print(f"Clave privada: {wallet.get_private_key()}")
Importar Wallet
Python:
from blockchain.wallet import Wallet

# Importar con clave privada
wallet = Wallet.from_private_key(
    private_key="clave_privada_hex",
    name="WalletImportada"
)
wallet.save()
Backup de Wallet
# Copiar archivo de wallet
cp ~/ColCript/data/wallets/MiWallet.json ~/backup/

# O exportar solo clave privada
# (guardar en lugar seguro)
Múltiples Wallets
# Crear múltiples wallets
wallet1 = Wallet(name="Personal")
wallet2 = Wallet(name="Trabajo")
wallet3 = Wallet(name="Ahorros")

# Guardar todas
wallet1.save()
wallet2.save()
wallet3.save()

# Usar según necesidad
blockchain.create_transaction(
    sender=wallet1,
    recipient=wallet2.get_address(),
    amount=10.0
)
💸 Transacciones
Crear Transacción
from blockchain.transaction import Transaction
from blockchain.wallet import Wallet

# Cargar wallet
sender_wallet = Wallet.load("MiWallet.json")

# Crear transacción
tx = Transaction(
    sender=sender_wallet.get_address(),
    recipient="dirección_destinatario",
    amount=10.5,
    fee=0.5
)

# Firmar
sender_wallet.sign_transaction(tx)

# Agregar a blockchain
blockchain.add_transaction(tx)
Verificar Estado
# Ver transacciones pendientes
curl http://localhost:5000/api/transactions/pending

# Ver si fue incluida en bloque
curl http://localhost:5000/api/transactions/history/[dirección]
Calcular Fee Óptimo
def calculate_optimal_fee(blockchain):
    """
    Calcula fee óptimo basado en congestión de red
    """
    pending = len(blockchain.pending_transactions)
    
    if pending < 10:
        return 0.1  # Red libre
    elif pending < 50:
        return 0.5  # Normal
    elif pending < 100:
        return 1.0  # Congestionada
    else:
        return 2.0  # Muy congestionada

# Uso
optimal_fee = calculate_optimal_fee(blockchain)
print(f"Fee recomendado: {optimal_fee} CLC")
⛏️ Minería
Minería Básica
from blockchain.blockchain import Blockchain
from blockchain.wallet import Wallet

blockchain = Blockchain()
wallet = Wallet.load("MinerWallet.json")

# Minar bloque
block = blockchain.mine_pending_transactions(
    miner_address=wallet.get_address()
)

print(f"✅ Bloque minado: {block.hash}")
print(f"💎 Recompensa: {blockchain.mining_reward} CLC")
Minería Continua
import time

def continuous_mining(blockchain, wallet, num_blocks=None):
    """
    Mina bloques continuamente
    """
    blocks_mined = 0
    
    while num_blocks is None or blocks_mined < num_blocks:
        print(f"\n⛏️  Minando bloque {len(blockchain.chain)}...")
        
        block = blockchain.mine_pending_transactions(
            wallet.get_address()
        )
        
        if block:
            blocks_mined += 1
            print(f"✅ Bloque minado: {block.hash[:20]}...")
            print(f"💎 Recompensa: {blockchain.mining_reward} CLC")
            
            # Pausa entre bloques
            time.sleep(1)

# Minar 10 bloques
continuous_mining(blockchain, wallet, num_blocks=10)
Pool de Minería (Simulado)
class MiningPool:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.miners = {}
        self.shares = {}
    
    def add_miner(self, miner_address):
        """Agrega minero al pool"""
        self.miners[miner_address] = True
        self.shares[miner_address] = 0
    
    def mine_block(self):
        """Mina bloque y distribuye recompensa"""
        # Minar
        block = self.blockchain.mine_pending_transactions("pool_address")
        
        if block:
            # Distribuir recompensa proporcionalmente
            total_shares = sum(self.shares.values())
            reward = self.blockchain.mining_reward
            
            for miner, shares in self.shares.items():
                miner_reward = (shares / total_shares) * reward
                print(f"{miner}: {miner_reward} CLC")
            
            # Reset shares
            self.shares = {m: 0 for m in self.miners}

# Uso
pool = MiningPool(blockchain)
pool.add_miner("miner1")
pool.add_miner("miner2")

# Simular contribuciones
pool.shares["miner1"] = 60  # 60% de trabajo
pool.shares["miner2"] = 40  # 40% de trabajo

pool.mine_block()
📜 Smart Contracts
Ver guía completa: CONTRACTS.md
Ejemplo Rápido: Timelock
from contracts.smart_contract import ContractManager

manager = ContractManager(blockchain)

# Crear contrato
contract = manager.create_timelock(
    creator=wallet.get_address(),
    unlock_block=100,
    amount=50.0,
    recipient="beneficiary_address"
)

print(f"Contrato creado: {contract.contract_id}")

# Esperar hasta bloque 100...
# (minar bloques)

# Ejecutar contrato
context = {'block_height': len(blockchain.chain)}
success, msg = manager.execute_contract(contract.contract_id, context)

if success:
    print("✅ Contrato ejecutado!")
else:
    print(f"❌ {msg}")
🌐 Red P2P
Ver guía completa: NETWORK.md
Ejemplo Rápido: Conectar Nodos
from network.node import Node

# Nodo 1
node1 = Node(host='192.168.1.100', port=6000, blockchain=blockchain1)
node1.start()

# Nodo 2
node2 = Node(host='192.168.1.101', port=6000, blockchain=blockchain2)
node2.start()

# Conectar nodos
node2.add_peer('192.168.1.100', 6000)

# Sincronizar
node2.sync_with_network()

print(f"Nodo 1: {len(blockchain1.chain)} bloques")
print(f"Nodo 2: {len(blockchain2.chain)} bloques")
🎯 Casos de Uso Comunes
Caso 1: Sistema de Pagos Simple
# 1. Crear wallets para usuarios
alice = Wallet(name="Alice")
bob = Wallet(name="Bob")

# 2. Alice recibe fondos del faucet
faucet_tx = blockchain.faucet_claim(alice.get_address())

# 3. Minar para confirmar
blockchain.mine_pending_transactions(alice.get_address())

# 4. Alice paga a Bob
tx = Transaction(
    sender=alice.get_address(),
    recipient=bob.get_address(),
    amount=3.0,
    fee=0.1
)
alice.sign_transaction(tx)
blockchain.add_transaction(tx)

# 5. Minar para confirmar
blockchain.mine_pending_transactions(bob.get_address())

# 6. Verificar balances
print(f"Alice: {blockchain.get_balance(alice.get_address())} CLC")
print(f"Bob: {blockchain.get_balance(bob.get_address())} CLC")
Caso 2: Ahorro Programado
from contracts.smart_contract import ContractManager

# 1. Crear contrato de ahorro a 6 meses
# (aprox 15,552,000 bloques si 10 seg/bloque = ~180 días)
current_block = len(blockchain.chain)
unlock_block = current_block + 15_552_000

savings = manager.create_timelock(
    creator=wallet.get_address(),
    unlock_block=unlock_block,
    amount=1000.0,
    recipient=wallet.get_address()
)

print(f"Ahorro bloqueado hasta bloque {unlock_block}")

# 2. Después de 6 meses...
context = {'block_height': len(blockchain.chain)}
success, msg = manager.execute_contract(savings.contract_id, context)

if success:
    print("✅ Ahorro liberado!")
Caso 3: Crowdfunding
class CrowdfundingContract:
    def __init__(self, goal, deadline_block):
        self.goal = goal
        self.deadline_block = deadline_block
        self.contributions = {}
        self.total_raised = 0
    
    def contribute(self, contributor, amount):
        """Agregar contribución"""
        if contributor in self.contributions:
            self.contributions[contributor] += amount
        else:
            self.contributions[contributor] = amount
        
        self.total_raised += amount
        return True, f"Contributed {amount} CLC"
    
    def finalize(self, current_block):
        """Finalizar campaña"""
        if current_block < self.deadline_block:
            return False, "Campaign not ended yet"
        
        if self.total_raised >= self.goal:
            return True, f"✅ Goal reached! {self.total_raised} CLC"
        else:
            # Devolver fondos
            return False, f"❌ Goal not reached. Refunding..."

# Uso
campaign = CrowdfundingContract(goal=1000.0, deadline_block=200)

# Contribuciones
campaign.contribute("user1", 300)
campaign.contribute("user2", 500)
campaign.contribute("user3", 300)

# Finalizar
success, msg = campaign.finalize(len(blockchain.chain))
print(msg)
Caso 4: Votación Descentralizada
class VotingContract:
    def __init__(self, options, voting_period_blocks):
        self.options = options
        self.votes = {option: 0 for option in options}
        self.voters = set()
        self.start_block = len(blockchain.chain)
        self.end_block = self.start_block + voting_period_blocks
    
    def vote(self, voter_address, option):
        """Emitir voto"""
        if voter_address in self.voters:
            return False, "Already voted"
        
        if option not in self.options:
            return False, "Invalid option"
        
        current_block = len(blockchain.chain)
        if current_block > self.end_block:
            return False, "Voting period ended"
        
        self.votes[option] += 1
        self.voters.add(voter_address)
        return True, f"Voted for {option}"
    
    def get_results(self):
        """Obtener resultados"""
        winner = max(self.votes, key=self.votes.get)
        return {
            'winner': winner,
            'votes': self.votes,
            'total_voters': len(self.voters)
        }

# Uso
voting = VotingContract(
    options=["Opción A", "Opción B", "Opción C"],
    voting_period_blocks=100
)

# Votar
voting.vote("voter1", "Opción A")
voting.vote("voter2", "Opción A")
voting.vote("voter3", "Opción B")

# Resultados
results = voting.get_results()
print(f"Ganador: {results['winner']}")
print(f"Votos: {results['votes']}")
🔧 Tips y Trucos
1. Verificar Blockchain
# CLI
python colcript.py
Opción: 14 (Ver información)

# API
curl -X POST http://localhost:5000/api/blockchain/validate
2. Backup Automático
# Script de backup diario
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR=~/ColCript-Backups

mkdir -p $BACKUP_DIR

cp -r ~/ColCript/data $BACKUP_DIR/data-$DATE

echo "✅ Backup completado: $BACKUP_DIR/data-$DATE"
# Programar con cron
crontab -e

# Agregar línea:
0 2 * * * /path/to/backup.sh
3. Monitoreo de Performance
import time
import psutil

def monitor_mining():
    """Monitorea performance de minería"""
    start_time = time.time()
    start_cpu = psutil.cpu_percent()
    
    # Minar bloque
    block = blockchain.mine_pending_transactions(wallet.get_address())
    
    end_time = time.time()
    end_cpu = psutil.cpu_percent()
    
    print(f"Tiempo: {end_time - start_time:.2f} segundos")
    print(f"CPU: {end_cpu}%")
    print(f"Hash rate: {block.nonce / (end_time - start_time):.2f} H/s")
4. Limpieza de Datos
# Eliminar blockchains de prueba
rm ~/ColCript/data/blockchains/test_*.json

# Eliminar wallets antiguas
rm ~/ColCript/data/wallets/old_*.json

# Limpiar logs
rm ~/ColCript/logs/*.log
📚 Recursos Adicionales
Documentación Completa
Arquitectura
API Reference
Smart Contracts
Red P2P
Instalación
Ejemplos de Código
Ver /examples en el repositorio
Comunidad
GitHub Issues
Discord/Telegram (si aplica)
🆘 Obtener Ayuda
Problemas Comunes
Problema: Balance no se actualiza
Solución: Esperar a que se mine el bloque con la transacción
Problema: Transacción rechazada
Solución: Verificar balance suficiente (amount + fee)
Problema: Blockchain corrupta
Solución: Restaurar desde backup o resincronizar
Soporte
Consultar documentación
Buscar en GitHub Issues
Crear nuevo issue con:
Descripción del problema
Pasos para reproducir
Logs de error
Versión de ColCript
¡Disfruta usando ColCript! 🚀💎
