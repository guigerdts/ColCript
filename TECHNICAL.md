# 📕 Documentación Técnica de ColCript

Documentación técnica completa para desarrolladores y usuarios avanzados.

---

## 📖 Tabla de Contenidos

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Componentes Core](#componentes-core)
3. [Criptografía](#criptografía)
4. [Proof of Work](#proof-of-work)
5. [Sistema de Transacciones](#sistema-de-transacciones)
6. [Persistencia](#persistencia)
7. [API Interna](#api-interna)
8. [Seguridad](#seguridad)
9. [Optimizaciones](#optimizaciones)
10. [Extensibilidad](#extensibilidad)

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Componentes
┌─────────────────────────────────────────────────────────┐
│                    ColCript CLI                         │
│                   (colcript.py)                         │
└────────────────────┬────────────────────────────────────┘
│
┌────────────┼────────────┐
│            │            │
▼            ▼            ▼
┌───────────┐ ┌──────────┐ ┌──────────┐
│ Blockchain│ │  Wallet  │ │  Utils   │
│  Module   │ │  Module  │ │  Module  │
└───────────┘ └──────────┘ └──────────┘
│             │             │
├─Block       ├─Wallet      ├─Crypto
├─Transaction├─Faucet      ├─Statistics
├─Blockchain ├─History     └─Charts
├─Storage    │
└─Explorer   │
### Flujo de Datos
Usuario → CLI → Blockchain → Storage → JSON
↓
Transaction
↓
Block
↓
Validation
---

## 🔧 Componentes Core

### 1. Block (Bloque)

**Archivo:** `blockchain/block.py`

**Propiedades:**
```python
{
    index: int              # Número del bloque
    timestamp: float        # Timestamp Unix
    transactions: list      # Lista de Transaction
    previous_hash: str      # Hash del bloque anterior
    miner_address: str      # Dirección del minero
    nonce: int             # Nonce para PoW
    hash: str              # Hash del bloque
}
Métodos principales:
calculate_hash() → Calcula SHA-256 del bloque
mine_block(difficulty) → Ejecuta Proof of Work
has_valid_transactions() → Valida todas las transacciones
to_dict() → Serializa a diccionario
Algoritmo de Minado:
def mine_block(self, difficulty):
    target = '0' * difficulty
    while self.hash[:difficulty] != target:
        self.nonce += 1
        self.hash = self.calculate_hash()
2. Transaction (Transacción)
Archivo: blockchain/transaction.py
Propiedades:
{
    sender: str            # Dirección pública del remitente
    recipient: str         # Dirección pública del destinatario
    amount: float          # Cantidad de CLC
    timestamp: float       # Timestamp Unix
    signature: str         # Firma ECDSA (hex)
    fee: float            # Comisión de transacción
}
Métodos principales:
sign_transaction(private_key) → Firma con ECDSA
is_valid() → Verifica firma y formato
get_hash() → Hash SHA-256 de la transacción
to_dict() → Serializa a diccionario
Proceso de Firma:
1. Serializar datos de transacción (sin firma)
2. Generar hash SHA-256
3. Firmar hash con clave privada ECDSA
4. Convertir firma a hexadecimal
5. Almacenar firma en la transacción
3. Blockchain (Cadena)
Archivo: blockchain/blockchain.py
Propiedades:
{
    chain: list                    # Lista de bloques
    pending_transactions: list     # Pool de transacciones
    difficulty: int                # Dificultad PoW
    mining_reward: float           # Recompensa por bloque
    auto_save: bool               # Auto-guardado
    storage: BlockchainStorage    # Sistema de persistencia
}
Métodos principales:
create_genesis_block() → Crea bloque inicial
add_transaction(tx) → Agrega transacción al pool
mine_pending_transactions(miner) → Mina nuevo bloque
get_balance(address) → Calcula balance de una wallet
is_chain_valid() → Valida integridad de la cadena
Validación de Cadena:
def is_chain_valid(self):
    for i in range(1, len(self.chain)):
        current = self.chain[i]
        previous = self.chain[i-1]
        
        # Validar hash del bloque
        if current.hash != current.calculate_hash():
            return False
        
        # Validar enlace con bloque anterior
        if current.previous_hash != previous.hash:
            return False
        
        # Validar transacciones
        if not current.has_valid_transactions():
            return False
        
        # Validar proof of work
        if current.hash[:difficulty] != '0' * difficulty:
            return False
    
    return True
🔐 Criptografía
ECDSA (Elliptic Curve Digital Signature Algorithm)
Archivo: utils/crypto.py
Curva utilizada: SECP256k1 (misma que Bitcoin)
Generación de Claves:
def generate_keypair():
    # Generar clave privada aleatoria
    private_key = SigningKey.generate(curve=SECP256k1)
    
    # Derivar clave pública
    public_key = private_key.get_verifying_key()
    
    # Convertir a hexadecimal
    private_hex = binascii.hexlify(private_key.to_string())
    public_hex = binascii.hexlify(public_key.to_string())
    
    return (private_hex, public_hex)
Longitud de Claves:
Clave privada: 256 bits (64 caracteres hex)
Clave pública: 512 bits (128 caracteres hex)
Firma Digital:
def sign_data(private_key_hex, data):
    # Reconstruir clave privada
    private_key = SigningKey.from_string(
        binascii.unhexlify(private_key_hex),
        curve=SECP256k1
    )
    
    # Serializar datos
    data_str = json.dumps(data, sort_keys=True)
    
    # Firmar
    signature = private_key.sign(data_str.encode())
    
    return binascii.hexlify(signature).decode()
Verificación:
def verify_signature(public_key_hex, signature_hex, data):
    public_key = VerifyingKey.from_string(
        binascii.unhexlify(public_key_hex),
        curve=SECP256k1
    )
    
    signature = binascii.unhexlify(signature_hex)
    data_str = json.dumps(data, sort_keys=True)
    
    return public_key.verify(signature, data_str.encode())
SHA-256 Hashing
Uso:
Hash de bloques
Hash de transacciones
Proof of Work
Implementación:
def hash_data(data):
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()
Propiedades:
Determinista
Unidireccional
Avalanche effect
Resistente a colisiones
⚙️ Proof of Work
Algoritmo
Objetivo: Encontrar un nonce tal que el hash del bloque comience con N ceros.
Dificultad: Configurada en config.py → MINING_DIFFICULTY = 4
Complejidad:
Dificultad 1: ~16 intentos (promedio)
Dificultad 2: ~256 intentos
Dificultad 3: ~4,096 intentos
Dificultad 4: ~65,536 intentos
Dificultad 5: ~1,048,576 intentos
Proceso:
1. Inicializar nonce = 0
2. Calcular hash del bloque
3. Si hash comienza con N ceros → Éxito
4. Sino, incrementar nonce y repetir paso 2
Código:
def mine_block(self, difficulty):
    target = '0' * difficulty
    
    while self.hash[:difficulty] != target:
        self.nonce += 1
        self.hash = self.calculate_hash()
    
    return self.hash
Tiempo de Minado (en dispositivo moderno):
Dificultad 3: ~0.05s
Dificultad 4: ~0.5-2s
Dificultad 5: ~10-30s
💸 Sistema de Transacciones
Ciclo de Vida
1. Creación
   ↓
2. Firma Digital
   ↓
3. Pool de Pendientes (Mempool)
   ↓
4. Minado (Inclusión en Bloque)
   ↓
5. Confirmación
   ↓
6. Inmutable
Pool de Transacciones (Mempool)
Propiedades:
Lista temporal de transacciones no confirmadas
Ordenadas por fee (mayor primero)
Límite: 100 transacciones (configurable)
Priorización:
if config.PRIORITIZE_BY_FEE:
    self.pending_transactions.sort(
        key=lambda tx: tx.fee, 
        reverse=True
    )
Sistema de Fees
Configuración:
MIN_TRANSACTION_FEE = 0.1 CLC
DEFAULT_TRANSACTION_FEE = 0.5 CLC
MAX_TRANSACTION_FEE = 10 CLC
Distribución:
Usuario paga: Cantidad + Fee
Minero recibe: Recompensa Base + Sum(Fees del bloque)
Ejemplo:
Bloque con 3 transacciones:
- TX1: 10 CLC + 0.5 fee
- TX2: 5 CLC + 1.0 fee
- TX3: 20 CLC + 0.5 fee

Minero recibe: 50 (base) + 2.0 (fees) = 52 CLC
💾 Persistencia
BlockchainStorage
Archivo: blockchain/storage.py
Formato: JSON
Estructura del Archivo:
{
  "version": "1.0",
  "difficulty": 4,
  "mining_reward": 50,
  "timestamp": "2025-11-17T18:08:11",
  "blocks": [
    {
      "index": 0,
      "timestamp": 1763347827.217,
      "previous_hash": "0",
      "miner_address": "GENESIS",
      "nonce": 4325,
      "hash": "000014b4669b...",
      "transactions": [...]
    }
  ]
}
Métodos:
save_blockchain(blockchain, filename) → Guarda a JSON
load_blockchain(filename) → Carga desde JSON
list_blockchains() → Lista archivos disponibles
Auto-guardado:
# Activado por defecto
if self.auto_save:
    self.storage.save_blockchain(self, self.save_filename)
Compatibilidad:
Detecta blockchains antiguas sin fees
Asigna fees por defecto automáticamente
Migración transparente
🔌 API Interna
Blockchain API
# Crear blockchain
bc = Blockchain(auto_save=True, save_filename="mi_blockchain.json")

# Agregar transacción
tx = Transaction(sender, recipient, amount, private_key, fee)
bc.add_transaction(tx)

# Minar
bc.mine_pending_transactions(miner_address)

# Consultar balance
balance = bc.get_balance(address)

# Validar
is_valid = bc.is_chain_valid()
Wallet API
# Crear wallet
wallet = Wallet("Mi Wallet")

# Guardar
wallet.save_to_file("mi_wallet.json")

# Cargar
wallet = Wallet.load_from_file("mi_wallet.json")

# Obtener dirección
address = wallet.get_address()

# Enviar CLC
tx = wallet.send_coins(recipient, amount, fee)

# Ver balance
balance = wallet.get_balance(blockchain)
Faucet API
# Crear faucet
faucet = Faucet(blockchain)

# Verificar elegibilidad
can_claim, message = faucet.can_claim(address)

# Reclamar
success, message = faucet.claim(address)

# Información
info = faucet.get_faucet_info()

# Donar
success, msg = faucet.fund_faucet(amount, wallet)
Statistics API
# Crear analizador
stats = BlockchainStatistics(blockchain)

# Supply
circulating = stats.get_circulating_supply()
percentage = stats.get_supply_percentage()

# Top wallets
top = stats.get_top_wallets(10)

# Distribución
dist = stats.get_wealth_distribution()

# Dashboard completo
dashboard = stats.get_complete_dashboard()
🛡️ Seguridad
Validación de Transacciones
Verificaciones:
✅ Firma digital válida
✅ Sender ≠ Recipient
✅ Amount > 0
✅ Fee válido
✅ Balance suficiente (al minar)
Validación de Bloques
Verificaciones:
✅ Hash correcto
✅ Proof of Work válido
✅ Enlace con bloque anterior correcto
✅ Todas las transacciones válidas
✅ Timestamp razonable
Validación de Cadena
Verificaciones:
✅ Bloque génesis correcto
✅ Todos los bloques válidos
✅ Cadena enlazada correctamente
✅ Sin bloques duplicados
Protección de Claves Privadas
Almacenamiento:
Las claves privadas se guardan en archivos JSON
Usuario responsable de la seguridad del archivo
Recomendación: Encriptar archivos de wallet
Buenas prácticas:
# Proteger archivos de wallet
chmod 600 wallet/*.json

# Backup seguro
cp wallet/*.json ~/backup_seguro/

# No compartir claves privadas
# No subir wallets a repositorios públicos
⚡ Optimizaciones
Caché de Estadísticas
class BlockchainStatistics:
    def __init__(self, blockchain):
        self._cache = {}  # Caché para cálculos costosos
Beneficio: Evita recalcular estadísticas en cada consulta.
Priorización de Transacciones
# Ordenar por fee descendente
pending_transactions.sort(key=lambda tx: tx.fee, reverse=True)
Beneficio: Mayor throughput económico.
Validación Lazy
# Solo validar cuando es necesario
if not self._validated:
    self._validate()
🔧 Extensibilidad
Agregar Nuevos Tipos de Transacciones
class SmartContractTransaction(Transaction):
    def __init__(self, sender, contract_code, *args):
        super().__init__(sender, "CONTRACT", 0, *args)
        self.contract_code = contract_code
    
    def execute(self, blockchain):
        # Lógica del smart contract
        pass
Agregar Algoritmos de Consenso
class ProofOfStake:
    def validate_block(self, block, validators):
        # Implementar PoS
        pass
Extender el Explorador
class AdvancedExplorer(BlockExplorer):
    def get_transaction_graph(self):
        # Grafo de transacciones
        pass
    
    def analyze_patterns(self):
        # Análisis de patrones
        pass
📊 Métricas de Performance
Tiempos de Operación (Promedio)
Operación
Tiempo
Generar keypair
~5ms
Firmar transacción
~2ms
Verificar firma
~3ms
Calcular hash
~0.1ms
Minar bloque (diff 4)
~1s
Validar bloque
~10ms
Guardar blockchain
~50ms
Cargar blockchain
~100ms
Consumo de Memoria
Componente
Memoria
Bloque vacío
~1 KB
Transacción
~500 bytes
Blockchain (100 bloques)
~100 KB
Wallet
~200 bytes
🧪 Testing
Pruebas Unitarias
Cada módulo incluye pruebas en su bloque if __name__ == "__main__":
# Test de criptografía
python utils/crypto.py

# Test de transacciones
python blockchain/transaction.py

# Test de bloques
python blockchain/block.py

# Test de blockchain
python blockchain/blockchain.py
Pruebas de Integración
# Test completo del flujo
def test_complete_flow():
    bc = Blockchain()
    alice = Wallet("Alice")
    bob = Wallet("Bob")
    
    bc.mine_pending_transactions(alice.get_address())
    tx = alice.send_coins(bob.get_address(), 10)
    bc.add_transaction(tx)
    bc.mine_pending_transactions(bob.get_address())
    
    assert bc.get_balance(bob.get_address()) == 60  # 10 + 50
    assert bc.is_chain_valid()
📈 Roadmap Técnico
Mejoras Planificadas
Merkle Trees
Optimizar verificación de transacciones
Reducir tamaño de bloques
Segregated Witness (SegWit)
Separar firmas de transacciones
Mayor capacidad por bloque
Lightning Network
Canales de pago off-chain
Transacciones instantáneas
Sharding
Dividir blockchain en fragmentos
Mayor escalabilidad
Smart Contracts
Contratos autoejecutables
Turing completo
📚 Referencias
Papers y Documentación
Bitcoin Whitepaper: Satoshi Nakamoto, 2008
ECDSA: SEC 2: Recommended Elliptic Curve Parameters
SHA-256: FIPS 180-4
Librerías Utilizadas
cryptography: https://cryptography.io
ecdsa: https://github.com/tlsfuzzer/python-ecdsa
hashlib: Python Standard Library
📞 Contacto Técnico
Para cuestiones técnicas avanzadas:
📧 Email: dev@colcript.com
💬 GitHub: Issues Técnicos
📖 Wiki: Documentación Extendida
ColCript - Blockchain educativa de código abierto 🪙
