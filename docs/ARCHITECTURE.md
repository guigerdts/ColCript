# 🏗️ Arquitectura de ColCript

Este documento describe la arquitectura técnica completa de ColCript, incluyendo el diseño de componentes, flujos de datos y decisiones de implementación.

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Componentes Principales](#componentes-principales)
3. [Flujos de Datos](#flujos-de-datos)
4. [Decisiones de Diseño](#decisiones-de-diseño)
5. [Seguridad](#seguridad)
6. [Rendimiento](#rendimiento)

---

## 🎯 Visión General

ColCript es una criptomoneda completa implementada en Python que combina:
- Blockchain Proof of Work (PoW)
- Sistema de transacciones firmadas digitalmente
- Smart Contracts con script engine
- Red P2P descentralizada
- Interfaces múltiples (CLI, API, Web)

### Principios de Diseño

1. **Simplicidad**: Código legible y mantenible
2. **Modularidad**: Componentes independientes y reutilizables
3. **Extensibilidad**: Fácil agregar nuevas características
4. **Seguridad**: Validaciones en cada capa
5. **Educativo**: Implementación clara de conceptos blockchain

---

## 🧩 Componentes Principales

### 1. Core Blockchain (`blockchain/`)

#### 1.1 Blockchain (`blockchain.py`)

**Responsabilidades:**
- Mantener la cadena de bloques
- Validar nuevos bloques
- Gestionar pool de transacciones pendientes
- Calcular dificultad y hashrate
- Auto-guardado y persistencia

**Estructura de datos:**
(python)
class Blockchain:
    chain: List[Block]                    # Cadena de bloques
    pending_transactions: List[Transaction]  # Pool de transacciones
    difficulty: int                       # Dificultad actual
    block_time: int                       # Tiempo objetivo por bloque
    mining_reward: float                  # Recompensa de minería
Flujo de validación:
Nuevo Bloque
    ↓
¿Hash válido? → NO → Rechazar
    ↓ SÍ
¿Índice correcto? → NO → Rechazar
    ↓ SÍ
¿Hash previo válido? → NO → Rechazar
    ↓ SÍ
¿Transacciones válidas? → NO → Rechazar
    ↓ SÍ
Agregar a cadena
1.2 Block (block.py)
Estructura:
class Block:
    index: int              # Posición en la cadena
    timestamp: float        # Unix timestamp
    transactions: List      # Lista de transacciones
    previous_hash: str      # Hash del bloque anterior
    nonce: int             # Número de prueba de trabajo
    hash: str              # Hash del bloque
    miner_address: str     # Dirección del minero
Cálculo de hash:
def calculate_hash(self):
    block_string = json.dumps({
        "index": self.index,
        "timestamp": self.timestamp,
        "transactions": [tx.to_dict() for tx in self.transactions],
        "previous_hash": self.previous_hash,
        "nonce": self.nonce,
        "miner_address": self.miner_address
    }, sort_keys=True)
    
    return hashlib.sha256(block_string.encode()).hexdigest()
1.3 Transaction (transaction.py)
Estructura:
class Transaction:
    sender: str         # Dirección pública del remitente
    recipient: str      # Dirección pública del destinatario
    amount: float       # Cantidad de CLC
    fee: float         # Fee de transacción
    timestamp: float    # Unix timestamp
    signature: str      # Firma digital ECDSA
Flujo de validación:
Transacción
    ↓
¿Cantidad > 0? → NO → Inválida
    ↓ SÍ
¿Fee >= 0? → NO → Inválida
    ↓ SÍ
¿Firma válida? → NO → Inválida
    ↓ SÍ
¿Balance suficiente? → NO → Rechazar
    ↓ SÍ
Agregar al pool
1.4 Wallet (wallet.py)
Generación de claves:
# 1. Generar clave privada (ECDSA secp256k1)
private_key = SigningKey.generate(curve=SECP256k1)

# 2. Derivar clave pública
public_key = private_key.get_verifying_key()

# 3. Crear dirección (hash de clave pública)
address = hashlib.sha256(
    public_key.to_string()
).hexdigest()
Firma de transacciones:
def sign_transaction(self, transaction):
    # Crear mensaje a firmar
    tx_string = json.dumps({
        'sender': transaction.sender,
        'recipient': transaction.recipient,
        'amount': transaction.amount,
        'timestamp': transaction.timestamp
    }, sort_keys=True)
    
    # Firmar con clave privada
    signature = self.private_key.sign(
        tx_string.encode()
    )
    
    return signature.hex()
1.5 Difficulty Adjustment (difficulty.py)
Algoritmo de ajuste:
def adjust_difficulty():
    if blocks_since_adjustment < ADJUSTMENT_INTERVAL:
        return current_difficulty
    
    # Calcular tiempo promedio
    time_taken = latest_block.timestamp - adjustment_block.timestamp
    expected_time = ADJUSTMENT_INTERVAL * TARGET_BLOCK_TIME
    
    # Ajustar dificultad
    if time_taken < expected_time / 2:
        new_difficulty = current_difficulty + 1
    elif time_taken > expected_time * 2:
        new_difficulty = max(1, current_difficulty - 1)
    else:
        new_difficulty = current_difficulty
    
    return new_difficulty
Parámetros:
TARGET_BLOCK_TIME: 10 segundos
ADJUSTMENT_INTERVAL: 10 bloques
MIN_DIFFICULTY: 1
MAX_DIFFICULTY: 20
2. Smart Contracts (contracts/)
2.1 Script Engine (opcodes.py)
Arquitectura Stack-Based:
Stack: [5, 3]
Opcode: OP_ADD
    ↓
Pop: 3, 5
    ↓
Execute: 5 + 3 = 8
    ↓
Push: 8
    ↓
Stack: [8]
Categorías de Opcodes:
Stack Operations (6 opcodes)
OP_DUP, OP_DROP, OP_SWAP, etc.
Arithmetic (7 opcodes)
OP_ADD, OP_SUB, OP_MUL, OP_DIV, etc.
Comparison (8 opcodes)
OP_EQUAL, OP_LESSTHAN, OP_GREATERTHAN, etc.
Logic (4 opcodes)
OP_AND, OP_OR, OP_NOT, OP_XOR
Crypto (4 opcodes)
OP_SHA256, OP_HASH160, OP_CHECKSIG, etc.
Flow Control (5 opcodes)
OP_IF, OP_ELSE, OP_ENDIF, OP_VERIFY, OP_RETURN
Time (2 opcodes)
OP_CHECKLOCKTIMEVERIFY, OP_CHECKSEQUENCEVERIFY
Ejemplo de ejecución:
# Script: [10, OP_DUP, OP_ADD]
# Estado inicial: stack = []

# 1. PUSH 10
stack = [10]

# 2. OP_DUP
stack = [10, 10]

# 3. OP_ADD
a = stack.pop()  # 10
b = stack.pop()  # 10
stack.append(a + b)  # 20
stack = [20]

# Resultado: 20
2.2 Tipos de Contratos (smart_contract.py)
1. Timelock Contract
script = [
    unlock_block,              # Push altura de desbloqueo
    OP_CHECKLOCKTIMEVERIFY,    # Verificar >= altura actual
    1                          # Push true
]
2. Multisig Contract
script = [
    required_sigs,             # Firmas requeridas
    total_signers,             # Total de firmantes
    OP_LESSTHANOREQUAL,        # required <= total
    1                          # Push true
]
3. Escrow Contract
script = [
    arbiter_decision,          # Decisión del árbitro
    OP_VERIFY                  # Verificar == true
]
Sistema de Gas:
Cada operación consume 1 gas
Gas limit: 10,000
Previene loops infinitos
3. Red P2P (network/)
3.1 Node (node.py)
Arquitectura de Nodos:
Nodo A (127.0.0.1:6000)
           /        \
          /          \
    Nodo B          Nodo C
  (IP1:5000)      (IP2:5000)
         \          /
          \        /
           Nodo D
Componentes:
class Node:
    node_id: str            # ID único del nodo
    host: str              # IP del nodo
    port: int              # Puerto
    peers: Set[Tuple]      # Set de (host, port)
    blockchain: Blockchain  # Referencia a blockchain
Flujo de Sincronización:
Nodo A conecta con Nodo B
    ↓
A solicita info de B
    ↓
B tiene más bloques?
    ↓ SÍ
A descarga blockchain de B
    ↓
A valida cadena recibida
    ↓
Cadena válida y más larga?
    ↓ SÍ
A reemplaza su cadena
Protocolo de Comunicación:
Descubrimiento:
GET /api/network/peers → Lista de peers
Sincronización:
GET /api/blockchain/info → Altura de cadena
GET /api/blockchain → Cadena completa
Propagación:
POST /api/network/transaction → Nueva transacción
POST /api/network/block → Nuevo bloque
4. API REST (api/)
4.1 Servidor Flask (server.py)
Arquitectura de Endpoints:
Cliente → Request → Flask → init_blockchain()
                              ↓
                         Blockchain
                              ↓
                         Response ← JSON
Estructura de Respuesta:
{
  "success": true,
  "message": "Success message",
  "data": {
    // Datos específicos
  }
}
Categorías de Endpoints:
Info (2 endpoints)
GET /api/info
GET /api/docs
Blockchain (8 endpoints)
GET /api/blockchain
GET /api/blockchain/info
GET /api/block/:index
POST /api/blockchain/validate
etc.
Transactions (6 endpoints)
POST /api/transaction
GET /api/transactions/pending
GET /api/transactions/history/:address
etc.
Wallets (4 endpoints)
POST /api/wallet/create
GET /api/wallet/balance/:address
etc.
Mining (3 endpoints)
POST /api/mine
GET /api/hashrate
etc.
Faucet (1 endpoint)
POST /api/faucet/claim
Difficulty (4 endpoints)
GET /api/difficulty/info
POST /api/difficulty/set
etc.
Contracts (9 endpoints)
GET /api/contracts/list
POST /api/contracts/timelock/create
etc.
Network (9 endpoints)
GET /api/network/info
POST /api/network/peer/add
etc.
CORS y Seguridad:
# CORS habilitado para desarrollo
CORS(app, resources={
    r"/api/*": {"origins": "*"}
})

# En producción, limitar orígenes:
# CORS(app, resources={
#     r"/api/*": {"origins": ["https://tu-dominio.com"]}
# })
5. Interfaz Web (web/)
5.1 Arquitectura Frontend
Estructura de páginas:
index.html (SPA - Single Page Application)
    ↓
Navigation → Páginas
    ├── Dashboard
    ├── Wallet
    ├── Mining
    ├── Explorer
    ├── Faucet
    ├── Contracts
    ├── Network
    └── Settings
Flujo de comunicación:
Interfaz Web → JavaScript (main.js)
                    ↓
                Fetch API
                    ↓
              API REST (Flask)
                    ↓
               Blockchain
                    ↓
           Response JSON
                    ↓
         Update UI (DOM)
Gestión de Estado:
// Estado global
let currentWallet = null;
let currentPage = 'dashboard';

// Persistencia local (NO localStorage)
// Estado se mantiene solo durante la sesión
🔄 Flujos de Datos
Flujo 1: Crear y Minar Transacción
1. Usuario crea transacción
   ↓
2. Wallet firma transacción
   ↓
3. Blockchain valida y agrega al pool
   ↓
4. Minero selecciona transacciones del pool
   ↓
5. Minero crea bloque candidato
   ↓
6. Minero ejecuta PoW (encuentra nonce válido)
   ↓
7. Blockchain valida nuevo bloque
   ↓
8. Bloque se agrega a la cadena
   ↓
9. Transacciones se marcan como confirmadas
   ↓
10. Blockchain se guarda en disco
Flujo 2: Sincronización P2P
1. Nodo A se conecta a Nodo B
   ↓
2. A solicita altura de cadena de B
   ↓
3. B responde con su altura
   ↓
4. A compara con su altura local
   ↓
5. Si B > A: A descarga cadena de B
   ↓
6. A valida cadena recibida
   ↓
7. Si válida: A reemplaza su cadena
   ↓
8. A notifica a sus peers
   ↓
9. Proceso se repite en red
Flujo 3: Ejecución de Smart Contract
1. Usuario crea contrato
   ↓
2. Contrato se guarda con script
   ↓
3. Usuario ejecuta contrato
   ↓
4. Script Engine inicializa stack vacío
   ↓
5. Para cada instrucción:
   a. Validar gas disponible
   b. Ejecutar opcode
   c. Actualizar stack
   d. Incrementar gas usado
   ↓
6. Stack final debe tener value truthy
   ↓
7. Marcar contrato como ejecutado
   ↓
8. Guardar resultado
🎯 Decisiones de Diseño
1. ¿Por qué Python?
Ventajas:
Sintaxis clara y legible
Excelente para propósitos educativos
Librería ecdsa para criptografía
Flask para API REST rápida
Fácil mantenimiento
Desventajas:
Rendimiento menor que Go/Rust
GIL limita concurrencia
No ideal para producción alta escala
2. ¿Por qué PoW en lugar de PoS?
Razones:
Más simple de implementar
Concepto original de Bitcoin
Fácil de entender
Educativo
3. ¿Por qué JSON en lugar de base de datos?
Razones:
Simplicidad
Sin dependencias externas
Fácil inspección manual
Portabilidad
Suficiente para propósito educativo
Limitación:
No escala para millones de bloques
En producción usar PostgreSQL/LevelDB
4. ¿Por qué Stack-Based Script Engine?
Razones:
Compatible con Bitcoin Script
Determinístico
Sin estado compartido
Fácil de razonar
🔒 Seguridad
Validaciones Implementadas
Blockchain:
Hash válido con dificultad
Índice secuencial
Hash previo correcto
Timestamp razonable
Transacciones:
Firma digital válida
Balance suficiente
Montos positivos
No doble gasto
Smart Contracts:
Gas limit
Validación de stack
Prevención de loops infinitos
Verificación de permisos
Red P2P:
Validación de peers
Cadena más larga gana
No aceptar bloques inválidos
Vectores de Ataque Mitigados
51% Attack: Requiere mayoría de poder computacional
Double Spending: Validación de balance antes de transacción
Replay Attack: Timestamps únicos
Sybil Attack: Consenso por PoW, no por número de nodos
⚡ Rendimiento
Benchmarks Aproximados
Minería:
Dificultad 1: ~1,000 hashes/seg
Dificultad 4: ~10 segundos/bloque
Dificultad 10: ~5 minutos/bloque
Transacciones:
Validación: ~1ms por transacción
Firma: ~2ms por transacción
1000 tx/bloque: ~3 segundos validación
API:
GET requests: ~10-50ms
POST requests: ~50-200ms
Minería: Variable (según dificultad)
Optimizaciones Futuras
Minería paralela con multiprocessing
Índices para búsqueda rápida de transacciones
Cache de balances calculados
Pruned blockchain (eliminar datos antiguos)
SPV (Simple Payment Verification)
📚 Referencias
Bitcoin Whitepaper
Ethereum Yellow Paper
Mastering Bitcoin
ECDSA Specification
Próximo: API Reference
