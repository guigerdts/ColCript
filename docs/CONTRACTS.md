📝 Paso 6.4: Crear CONTRACTS.md
nano docs/CONTRACTS.md
Copia todo este contenido:
# 📜 Guía de Smart Contracts - ColCript

Documentación completa del sistema de Smart Contracts de ColCript, incluyendo el Script Engine, tipos de contratos y ejemplos de uso.

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Script Engine](#script-engine)
3. [Tipos de Contratos](#tipos-de-contratos)
4. [Creación de Contratos](#creación-de-contratos)
5. [Ejecución de Contratos](#ejecución-de-contratos)
6. [Sistema de Gas](#sistema-de-gas)
7. [Ejemplos Avanzados](#ejemplos-avanzados)
8. [Mejores Prácticas](#mejores-prácticas)

---

## 📖 Introducción

Los Smart Contracts en ColCript son programas autoejecutables almacenados en la blockchain que se ejecutan cuando se cumplen condiciones predefinidas.

### Características

- **Stack-Based**: Arquitectura basada en pila (similar a Bitcoin Script)
- **Determinístico**: Mismos inputs = mismos outputs
- **Verificable**: Código visible y auditable
- **Seguro**: Sistema de gas previene loops infinitos
- **Persistente**: Se guardan en la blockchain

---

## ⚙️ Script Engine

### Arquitectura Stack-Based

El Script Engine de ColCript usa una arquitectura basada en pila:
Stack
     ┌───┐
     │ 3 │  ← Top
     ├───┤
     │ 5 │
     └───┘
Operación: OP_ADD
Stack
     ┌───┐
     │ 8 │  ← Resultado (5+3)
     └───┘
### Flujo de Ejecución
Script: [10, 5, OP_ADD, OP_DUP, OP_MUL]
Inicializar stack vacío: []
Ejecutar cada instrucción:
PUSH 10    → Stack: [10]
PUSH 5     → Stack: [10, 5]
OP_ADD     → Stack: [15]      (10+5)
OP_DUP     → Stack: [15, 15]  (duplicar)
OP_MUL     → Stack: [225]     (15*15)
Resultado final: 225
---

## 🔢 Opcodes Disponibles

### 1. Stack Operations (Operaciones de Pila)

| Opcode | Descripción | Ejemplo |
|--------|-------------|---------|
| **OP_DUP** | Duplica el elemento del top | `[5] → [5, 5]` |
| **OP_DROP** | Elimina el elemento del top | `[5, 3] → [5]` |
| **OP_SWAP** | Intercambia los 2 elementos del top | `[5, 3] → [3, 5]` |
| **OP_OVER** | Copia el segundo elemento al top | `[5, 3] → [5, 3, 5]` |
| **OP_PICK** | Copia el n-ésimo elemento al top | `[a, b, c], n=2 → [a, b, c, a]` |
| **OP_ROLL** | Mueve el n-ésimo elemento al top | `[a, b, c], n=2 → [b, c, a]` |

**Ejemplo:**
(python)
script = [10, OpCode.OP_DUP]
# Resultado: Stack = [10, 10]
2. Arithmetic Operations (Operaciones Aritméticas)
Opcode
Descripción
Ejemplo
OP_ADD
Suma los 2 últimos elementos
[5, 3] → [8]
OP_SUB
Resta los 2 últimos elementos
[5, 3] → [2]
OP_MUL
Multiplica los 2 últimos elementos
[5, 3] → [15]
OP_DIV
Divide los 2 últimos elementos
[10, 2] → [5]
OP_MOD
Módulo de los 2 últimos elementos
[10, 3] → [1]
OP_INC
Incrementa el último elemento en 1
[5] → [6]
OP_DEC
Decrementa el último elemento en 1
[5] → [4]
Ejemplo:
script = [10, 5, OpCode.OP_ADD, 2, OpCode.OP_MUL]
# 10 + 5 = 15
# 15 * 2 = 30
# Resultado: Stack = [30]
3. Comparison Operations (Operaciones de Comparación)
Opcode
Descripción
Ejemplo
OP_EQUAL
Verifica igualdad
[5, 5] → [1] (true)
OP_NOTEQUAL
Verifica desigualdad
[5, 3] → [1] (true)
OP_LESSTHAN
Verifica menor que
[3, 5] → [1] (true)
OP_GREATERTHAN
Verifica mayor que
[5, 3] → [1] (true)
OP_LESSTHANOREQUAL
Verifica menor o igual
[3, 5] → [1] (true)
OP_GREATERTHANOREQUAL
Verifica mayor o igual
[5, 5] → [1] (true)
OP_MIN
Retorna el mínimo
[5, 3] → [3]
OP_MAX
Retorna el máximo
[5, 3] → [5]
Ejemplo:
script = [10, 5, OpCode.OP_GREATERTHAN]
# 10 > 5 = true
# Resultado: Stack = [1]
4. Logic Operations (Operaciones Lógicas)
Opcode
Descripción
Ejemplo
OP_NOT
Negación lógica
[1] → [0], [0] → [1]
OP_AND
AND lógico
[1, 1] → [1], [1, 0] → [0]
OP_OR
OR lógico
[1, 0] → [1], [0, 0] → [0]
OP_XOR
XOR lógico
[1, 0] → [1], [1, 1] → [0]
Ejemplo:
script = [1, 1, OpCode.OP_AND, 0, OpCode.OP_OR]
# 1 AND 1 = 1
# 1 OR 0 = 1
# Resultado: Stack = [1]
5. Crypto Operations (Operaciones Criptográficas)
Opcode
Descripción
Ejemplo
OP_SHA256
Hash SHA-256 del elemento
["hello"] → ["2cf24dba..."]
OP_HASH160
RIPEMD160(SHA256(x))
["data"] → ["hash160..."]
OP_CHECKSIG
Verifica firma digital
[pubkey, sig, msg] → [1/0]
OP_CHECKMULTISIG
Verifica multifirma
[pubkeys, sigs, msg] → [1/0]
Ejemplo:
script = ["hello", OpCode.OP_SHA256]
# Resultado: Stack = ["2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"]
6. Flow Control (Control de Flujo)
Opcode
Descripción
Uso
OP_IF
Inicia bloque condicional
if (stack.pop())
OP_ELSE
Bloque alternativo
else
OP_ENDIF
Finaliza bloque condicional
endif
OP_VERIFY
Verifica que top == true
Falla si false
OP_RETURN
Termina con fallo
Aborta ejecución
Ejemplo:
script = [
    10, 5, OpCode.OP_GREATERTHAN,  # 10 > 5 = true
    OpCode.OP_IF,
        100,
    OpCode.OP_ELSE,
        200,
    OpCode.OP_ENDIF
]
# Resultado: Stack = [100]
7. Time Operations (Operaciones de Tiempo)
Opcode
Descripción
Uso
OP_CHECKLOCKTIMEVERIFY
Verifica altura de bloque
block_height >= locktime
OP_CHECKSEQUENCEVERIFY
Verifica secuencia relativa
sequence >= required
Ejemplo:
script = [100, OpCode.OP_CHECKLOCKTIMEVERIFY, 1]
# Verifica: block_height >= 100
# Si true, continúa; si false, falla
📑 Tipos de Contratos
1. Timelock Contract (⏰ Contrato de Tiempo)
Desbloquea fondos cuando se alcanza una altura de bloque específica.
Estructura
class TimelockContract:
    unlock_block: int      # Bloque de desbloqueo
    amount: float          # Cantidad de CLC
    recipient: str         # Dirección destinataria
Script
script = [
    unlock_block,              # Push altura de desbloqueo
    OpCode.OP_CHECKLOCKTIMEVERIFY,  # Verificar >= altura actual
    1                          # Push true
]
Ejemplo de Uso
CLI:
python colcript.py
# Opción 18 → Smart Contracts
# Opción 1 → Crear Timelock
# Unlock block: 100
# Cantidad: 50
# Destinatario: abc123...
API:
curl -X POST http://localhost:5000/api/contracts/timelock/create \
  -H "Content-Type: application/json" \
  -d '{
    "creator": "creator_address",
    "unlock_block": 100,
    "amount": 50.0,
    "recipient": "recipient_address"
  }'
Python:
from contracts.smart_contract import ContractManager

manager = ContractManager(blockchain)

contract = manager.create_timelock(
    creator="creator_address",
    unlock_block=100,
    amount=50.0,
    recipient="recipient_address"
)

print(f"Contract created: {contract.contract_id}")
Casos de Uso
Ahorro programado: Bloquear fondos hasta fecha futura
Herencia: Desbloquear fondos después de tiempo específico
Vesting: Liberar tokens gradualmente
Crowdfunding: Retornar fondos si no se alcanza objetivo
2. Multisig Contract (✍️ Contrato Multi-Firma)
Requiere múltiples firmas para liberar fondos.
Estructura
class MultisigContract:
    required_sigs: int     # Firmas requeridas
    signers: List[str]     # Lista de direcciones autorizadas
    amount: float          # Cantidad de CLC
    recipient: str         # Dirección destinataria
    signatures: List[str]  # Firmas actuales
Script
script = [
    required_sigs,              # Firmas requeridas
    len(signers),               # Total de firmantes
    OpCode.OP_LESSTHANOREQUAL,  # required <= total
    1                           # Push true
]
Ejemplo de Uso
CLI:
python colcript.py
# Opción 18 → Smart Contracts
# Opción 2 → Crear Multisig
# Firmas requeridas: 2
# Número de firmantes: 3
# Firmante 1: address1...
# Firmante 2: address2...
# Firmante 3: address3...
# Cantidad: 100
# Destinatario: recipient...
API:
# Crear contrato
curl -X POST http://localhost:5000/api/contracts/multisig/create \
  -H "Content-Type: application/json" \
  -d '{
    "creator": "creator_address",
    "required_sigs": 2,
    "signers": ["addr1", "addr2", "addr3"],
    "amount": 100.0,
    "recipient": "recipient_address"
  }'

# Respuesta: {"contract_id": "MS-1"}

# Firmar (firmante 1)
curl -X POST http://localhost:5000/api/contracts/multisig/MS-1/sign \
  -H "Content-Type: application/json" \
  -d '{"signer": "addr1"}'

# Firmar (firmante 2)
curl -X POST http://localhost:5000/api/contracts/multisig/MS-1/sign \
  -H "Content-Type: application/json" \
  -d '{"signer": "addr2"}'

# Ejecutar (ya tiene 2 de 3 firmas)
curl -X POST http://localhost:5000/api/contracts/multisig/MS-1/execute
Python:
manager = ContractManager(blockchain)

# Crear contrato
contract = manager.create_multisig(
    creator="creator_address",
    required_sigs=2,
    signers=["addr1", "addr2", "addr3"],
    amount=100.0,
    recipient="recipient_address"
)

# Firmar
contract.add_signature("addr1")
contract.add_signature("addr2")

# Ejecutar
context = {'block_height': len(blockchain.chain)}
success, msg = contract.execute(blockchain, context)
Casos de Uso
Cuentas conjuntas: Requiere aprobación de múltiples partes
Tesorería de organización: 3 de 5 directores deben aprobar
Seguridad adicional: Wallet personal + wallet empresa
Gestión de fondos: Múltiples administradores
3. Escrow Contract (🤝 Contrato de Custodia)
Un árbitro decide si liberar fondos al vendedor o devolverlos al comprador.
Estructura
class EscrowContract:
    buyer: str         # Dirección del comprador
    seller: str        # Dirección del vendedor
    arbiter: str       # Dirección del árbitro
    amount: float      # Cantidad de CLC
    status: str        # 'pending', 'approved', 'rejected'
    decision: bool     # True = aprobar, False = rechazar
Script
script = [
    arbiter_decision,    # True o False
    OpCode.OP_VERIFY     # Verificar == true
]
Ejemplo de Uso
CLI:
python colcript.py
# Opción 18 → Smart Contracts
# Opción 3 → Crear Escrow
# Comprador: buyer_address...
# Vendedor: seller_address...
# Árbitro: arbiter_address...
# Cantidad: 200

# Luego el árbitro decide:
# Opción 8 → Decidir Escrow
# ID: ES-1
# ¿Aprobar? S/n: S
API:
# Crear contrato
curl -X POST http://localhost:5000/api/contracts/escrow/create \
  -H "Content-Type: application/json" \
  -d '{
    "creator": "buyer_address",
    "buyer": "buyer_address",
    "seller": "seller_address",
    "arbiter": "arbiter_address",
    "amount": 200.0
  }'

# Árbitro decide (aprobar)
curl -X POST http://localhost:5000/api/contracts/escrow/ES-1/decide \
  -H "Content-Type: application/json" \
  -d '{
    "arbiter": "arbiter_address",
    "approve": true
  }'

# Ejecutar contrato
curl -X POST http://localhost:5000/api/contracts/escrow/ES-1/execute
Python:
manager = ContractManager(blockchain)

# Crear contrato
contract = manager.create_escrow(
    creator="buyer_address",
    buyer="buyer_address",
    seller="seller_address",
    arbiter="arbiter_address",
    amount=200.0
)

# Árbitro decide
success, msg = contract.make_decision(
    arbiter="arbiter_address",
    approve=True
)

# Ejecutar
context = {'block_height': len(blockchain.chain)}
success, msg = contract.execute(blockchain, context)
Casos de Uso
Comercio P2P: Protección para comprador y vendedor
Freelance: Pago cuando se entrega trabajo
Inmobiliaria: Depósito en custodia
E-commerce: Garantía de entrega
🔧 Creación de Contratos
Paso a Paso
1. Definir Parámetros
# Timelock
unlock_block = 100
amount = 50.0
recipient = "recipient_address"

# Multisig
required_sigs = 2
signers = ["addr1", "addr2", "addr3"]
amount = 100.0
recipient = "recipient_address"

# Escrow
buyer = "buyer_address"
seller = "seller_address"
arbiter = "arbiter_address"
amount = 200.0
2. Crear Script
from contracts.opcodes import OpCode

# Timelock script
timelock_script = [
    unlock_block,
    OpCode.OP_CHECKLOCKTIMEVERIFY,
    1
]

# Multisig script
multisig_script = [
    required_sigs,
    len(signers),
    OpCode.OP_LESSTHANOREQUAL,
    1
]

# Escrow script
escrow_script = [
    arbiter_decision,
    OpCode.OP_VERIFY
]
3. Instanciar Contrato
from contracts.smart_contract import (
    TimelockContract,
    MultisigContract,
    EscrowContract
)

# Timelock
contract = TimelockContract(
    contract_id="TL-1",
    creator=creator_address,
    unlock_block=unlock_block,
    amount=amount,
    recipient=recipient
)

# Multisig
contract = MultisigContract(
    contract_id="MS-1",
    creator=creator_address,
    required_sigs=required_sigs,
    signers=signers,
    amount=amount,
    recipient=recipient
)

# Escrow
contract = EscrowContract(
    contract_id="ES-1",
    creator=creator_address,
    buyer=buyer,
    seller=seller,
    arbiter=arbiter,
    amount=amount
)
4. Guardar Contrato
# Agregar a ContractManager
manager.contracts[contract.contract_id] = contract

# Guardar en disco
manager.save_contracts()
▶️ Ejecución de Contratos
Flujo de Ejecución
1. Verificar que contrato no esté ejecutado
   ↓
2. Preparar contexto (altura de bloque, etc.)
   ↓
3. Inicializar Script Engine
   ↓
4. Ejecutar cada instrucción del script
   ↓
5. Verificar stack final (debe ser truthy)
   ↓
6. Marcar contrato como ejecutado
   ↓
7. Guardar resultado
Código de Ejecución
def execute_contract(contract_id, context=None):
    # 1. Obtener contrato
    contract = manager.get_contract(contract_id)
    
    if not contract:
        return False, "Contract not found"
    
    if contract.executed:
        return False, "Contract already executed"
    
    # 2. Preparar contexto
    if context is None:
        context = {
            'block_height': len(blockchain.chain)
        }
    
    # 3. Ejecutar
    success, msg = contract.execute(blockchain, context)
    
    # 4. Guardar
    if success:
        manager.save_contracts()
    
    return success, msg
Verificar Condiciones
Timelock:
def can_execute_timelock(contract):
    current_height = len(blockchain.chain)
    return current_height >= contract.data['unlock_block']
Multisig:
def can_execute_multisig(contract):
    current_sigs = len(contract.data['signatures'])
    required_sigs = contract.data['required_sigs']
    return current_sigs >= required_sigs
Escrow:
def can_execute_escrow(contract):
    return contract.data['status'] == 'approved'
⛽ Sistema de Gas
¿Qué es Gas?
Gas es una unidad que mide el costo computacional de ejecutar operaciones en el Script Engine. Previene:
Loops infinitos
Ataques de denegación de servicio
Scripts maliciosos
Consumo de Gas
Cada operación consume 1 gas:
script = [10, 5, OpCode.OP_ADD, OpCode.OP_DUP]

Gas usado:
- PUSH 10:  1 gas
- PUSH 5:   1 gas
- OP_ADD:   1 gas
- OP_DUP:   1 gas
Total:      4 gas
Gas Limit
Gas Limit: 10,000 operaciones
Si se excede → Ejecución abortada
Se puede ajustar según necesidades
class ScriptEngine:
    def __init__(self):
        self.gas_used = 0
        self.gas_limit = 10000
    
    def _execute_instruction(self, instruction):
        if self.gas_used >= self.gas_limit:
            raise Exception("Gas limit exceeded")
        
        # ... ejecutar instrucción ...
        
        self.gas_used += 1
Optimización de Gas
Mal (más gas):
script = [
    10, OpCode.OP_DUP, OpCode.OP_DUP, OpCode.OP_DUP,
    OpCode.OP_ADD, OpCode.OP_ADD, OpCode.OP_ADD
]
# Gas: 7
Bien (menos gas):
script = [10, 4, OpCode.OP_MUL]
# Gas: 3
🔬 Ejemplos Avanzados
### Ejemplo 1: Ahorro con Interés Compuesto

Combina Timelock con cálculo de intereses.

(python)
from contracts.opcodes import OpCode

# Parámetros
principal = 1000      # Capital inicial
rate = 5              # 5% anual
years = 2             # 2 años
unlock_block = 1000   # Bloque futuro

# Script: calcular interés compuesto
# Fórmula: A = P * (1 + r)^t
# Simplificado: A = P * 1.05 * 1.05
script = [
    principal,           # 1000
    105,                 # 105%
    OpCode.OP_MUL,       # 1000 * 105 = 105000
    100,                 # /100
    OpCode.OP_DIV,       # 105000 / 100 = 1050
    105,                 # 105%
    OpCode.OP_MUL,       # 1050 * 105 = 110250
    100,                 # /100
    OpCode.OP_DIV,       # 110250 / 100 = 1102.5
    unlock_block,        # Push unlock block
    OpCode.OP_CHECKLOCKTIMEVERIFY,  # Verificar tiempo
    1                    # Push true
]

# Crear contrato personalizado
contract = SmartContract(
    contract_id="SAVINGS-1",
    contract_type="savings",
    creator=creator_address,
    script=script,
    data={
        'principal': principal,
        'final_amount': 1102.5,
        'unlock_block': unlock_block
    }
)
Ejemplo 2: Votación Multi-Firma
Requiere mayoría de votos para aprobar.
# Parámetros
total_voters = 5
required_votes = 3     # Mayoría: 3 de 5

# Script: verificar mayoría
script = [
    current_votes,              # Votos actuales
    required_votes,             # Votos requeridos
    OpCode.OP_GREATERTHANOREQUAL,  # current >= required
    OpCode.OP_VERIFY            # Verificar = true
]

# Crear contrato de votación
contract = MultisigContract(
    contract_id="VOTE-1",
    creator=creator_address,
    required_sigs=required_votes,
    signers=[
        "voter1_address",
        "voter2_address",
        "voter3_address",
        "voter4_address",
        "voter5_address"
    ],
    amount=0,  # No transfiere fondos
    recipient=proposal_address
)

# Votar
contract.add_signature("voter1_address")
contract.add_signature("voter2_address")
contract.add_signature("voter3_address")

# Ejecutar (se aprueba con 3 votos)
success, msg = contract.execute(blockchain)
Ejemplo 3: Subasta Descentralizada
Contrato de subasta con timelock y multisig.
class AuctionContract(SmartContract):
    def __init__(self, contract_id, creator, item, 
                 min_bid, end_block):
        self.item = item
        self.min_bid = min_bid
        self.end_block = end_block
        self.highest_bid = 0
        self.highest_bidder = None
        self.bids = []
        
        # Script: verificar fin de subasta
        script = [
            end_block,
            OpCode.OP_CHECKLOCKTIMEVERIFY,
            1
        ]
        
        super().__init__(
            contract_id=contract_id,
            contract_type="auction",
            creator=creator,
            script=script,
            data={
                'item': item,
                'min_bid': min_bid,
                'end_block': end_block,
                'highest_bid': 0,
                'highest_bidder': None
            }
        )
    
    def place_bid(self, bidder, amount):
        """Coloca una oferta"""
        if amount <= self.highest_bid:
            return False, "Bid too low"
        
        if amount < self.min_bid:
            return False, "Below minimum bid"
        
        # Actualizar oferta más alta
        self.highest_bid = amount
        self.highest_bidder = bidder
        self.bids.append({
            'bidder': bidder,
            'amount': amount,
            'timestamp': time.time()
        })
        
        return True, f"Bid placed: {amount} CLC"
    
    def finalize(self, blockchain):
        """Finaliza la subasta"""
        context = {'block_height': len(blockchain.chain)}
        
        # Verificar que terminó
        if context['block_height'] < self.end_block:
            return False, "Auction not ended yet"
        
        # Ejecutar contrato
        success, msg = self.execute(blockchain, context)
        
        if success and self.highest_bidder:
            return True, f"Winner: {self.highest_bidder} with {self.highest_bid} CLC"
        
        return False, "No bids received"

# Uso
auction = AuctionContract(
    contract_id="AUC-1",
    creator=seller_address,
    item="Obra de Arte Digital",
    min_bid=100.0,
    end_block=500
)

# Ofertas
auction.place_bid("bidder1", 150.0)
auction.place_bid("bidder2", 200.0)
auction.place_bid("bidder3", 250.0)

# Finalizar cuando llegue al bloque 500
auction.finalize(blockchain)
Ejemplo 4: Contrato de Herencia
Fondos se liberan si no hay actividad por cierto tiempo.
class InheritanceContract(SmartContract):
    def __init__(self, contract_id, owner, heir, 
                 amount, inactivity_blocks):
        self.owner = owner
        self.heir = heir
        self.amount = amount
        self.inactivity_blocks = inactivity_blocks
        self.last_activity_block = None
        
        script = [
            inactivity_blocks,
            OpCode.OP_CHECKLOCKTIMEVERIFY,
            1
        ]
        
        super().__init__(
            contract_id=contract_id,
            contract_type="inheritance",
            creator=owner,
            script=script,
            data={
                'owner': owner,
                'heir': heir,
                'amount': amount,
                'inactivity_blocks': inactivity_blocks,
                'last_activity_block': 0
            }
        )
    
    def check_in(self, blockchain):
        """Owner demuestra estar activo"""
        self.last_activity_block = len(blockchain.chain)
        self.data['last_activity_block'] = self.last_activity_block
        return True, "Check-in registered"
    
    def claim(self, blockchain):
        """Heir reclama fondos"""
        current_block = len(blockchain.chain)
        blocks_passed = current_block - self.last_activity_block
        
        if blocks_passed < self.inactivity_blocks:
            return False, f"Only {blocks_passed} blocks passed, need {self.inactivity_blocks}"
        
        # Ejecutar contrato
        context = {'block_height': current_block}
        return self.execute(blockchain, context)

# Uso
inheritance = InheritanceContract(
    contract_id="INH-1",
    owner=owner_address,
    heir=heir_address,
    amount=10000.0,
    inactivity_blocks=1000  # ~2.7 horas si 10 seg/bloque
)

# Owner hace check-in regularmente
inheritance.check_in(blockchain)

# Si owner no hace check-in por 1000 bloques,
# heir puede reclamar
inheritance.claim(blockchain)
Ejemplo 5: Préstamo P2P con Colateral
class LoanContract(SmartContract):
    def __init__(self, contract_id, lender, borrower, 
                 loan_amount, collateral, interest_rate, 
                 repayment_blocks):
        self.lender = lender
        self.borrower = borrower
        self.loan_amount = loan_amount
        self.collateral = collateral
        self.interest_rate = interest_rate
        self.repayment_blocks = repayment_blocks
        self.repaid = False
        
        # Total a repagar: principal + interés
        total_repayment = loan_amount * (1 + interest_rate / 100)
        
        script = [
            repayment_blocks,
            OpCode.OP_CHECKLOCKTIMEVERIFY,
            1
        ]
        
        super().__init__(
            contract_id=contract_id,
            contract_type="loan",
            creator=lender,
            script=script,
            data={
                'lender': lender,
                'borrower': borrower,
                'loan_amount': loan_amount,
                'collateral': collateral,
                'interest_rate': interest_rate,
                'total_repayment': total_repayment,
                'repayment_blocks': repayment_blocks,
                'repaid': False
            }
        )
    
    def repay(self, amount):
        """Borrower repaga el préstamo"""
        if amount < self.data['total_repayment']:
            return False, "Insufficient repayment amount"
        
        self.repaid = True
        self.data['repaid'] = True
        return True, "Loan repaid, collateral released"
    
    def claim_collateral(self, blockchain):
        """Lender reclama colateral si no se repaga"""
        context = {'block_height': len(blockchain.chain)}
        
        if context['block_height'] < self.repayment_blocks:
            return False, "Repayment period not ended"
        
        if self.repaid:
            return False, "Loan already repaid"
        
        # Ejecutar y transferir colateral al lender
        return self.execute(blockchain, context)

# Uso
loan = LoanContract(
    contract_id="LOAN-1",
    lender=lender_address,
    borrower=borrower_address,
    loan_amount=1000.0,
    collateral=1500.0,  # 150% colateral
    interest_rate=10,    # 10%
    repayment_blocks=500
)

# Borrower repaga
loan.repay(1100.0)  # 1000 + 10% = 1100

# O si no repaga, lender reclama colateral
# loan.claim_collateral(blockchain)
✅ Mejores Prácticas
1. Seguridad
✅ HACER:
# Validar inputs
def create_timelock(unlock_block, amount, recipient):
    if unlock_block <= 0:
        raise ValueError("Invalid unlock_block")
    if amount <= 0:
        raise ValueError("Invalid amount")
    if not recipient:
        raise ValueError("Recipient required")
    # ... crear contrato

# Verificar permisos
def make_decision(arbiter, approve):
    if arbiter != self.data['arbiter']:
        return False, "Only arbiter can decide"
    # ... continuar

# Prevenir re-entrada
if self.executed:
    return False, "Contract already executed"
❌ NO HACER:
# NO validar inputs
def create_timelock(unlock_block, amount, recipient):
    # Directo sin validación
    contract = TimelockContract(...)

# NO verificar permisos
def make_decision(arbiter, approve):
    # Cualquiera puede decidir
    self.data['decision'] = approve

# NO prevenir doble ejecución
def execute(self):
    # Se puede ejecutar múltiples veces
    self.script_engine.execute(self.script)
2. Optimización de Gas
✅ HACER:
# Usar operaciones eficientes
script = [10, 5, OpCode.OP_MUL]  # 3 gas

# Combinar operaciones
script = [
    amount,
    rate,
    OpCode.OP_MUL,
    100,
    OpCode.OP_DIV
]  # 5 gas
❌ NO HACER:
# Operaciones redundantes
script = [
    10, OpCode.OP_DUP, OpCode.OP_DUP,
    OpCode.OP_ADD, OpCode.OP_ADD
]  # 5 gas (innecesario)

# Bucles implícitos
script = [
    value, OpCode.OP_DUP, OpCode.OP_DUP, OpCode.OP_DUP,
    # ... muchas operaciones repetitivas
]  # Alto consumo de gas
3. Testing
✅ HACER:
# Test unitario de contrato
def test_timelock_contract():
    contract = TimelockContract(
        contract_id="TL-TEST",
        creator="creator",
        unlock_block=10,
        amount=50.0,
        recipient="recipient"
    )
    
    # Test: no se puede ejecutar antes de tiempo
    blockchain = Blockchain()
    context = {'block_height': 5}
    success, msg = contract.execute(blockchain, context)
    assert not success
    
    # Test: se puede ejecutar después de tiempo
    context = {'block_height': 15}
    success, msg = contract.execute(blockchain, context)
    assert success

# Test de gas
def test_gas_consumption():
    engine = ScriptEngine()
    script = [10, 5, OpCode.OP_ADD]
    
    success, msg = engine.execute(script)
    assert engine.gas_used == 3
❌ NO HACER:
# NO probar en producción
contract = create_contract_for_production()
# Esperando que funcione sin testing

# NO ignorar edge cases
def test_basic():
    # Solo prueba caso feliz
    contract.execute(blockchain)
    # No prueba: valores negativos, overflow, etc.
4. Documentación
✅ HACER:
class CustomContract(SmartContract):
    """
    Contrato personalizado para X propósito.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
    
    Ejemplo:
        >>> contract = CustomContract(...)
        >>> contract.execute(blockchain)
    """
    
    def custom_function(self, arg):
        """
        Descripción de la función.
        
        Args:
            arg: Descripción del argumento
        
        Returns:
            tuple: (success, message)
        """
        # ... implementación
❌ NO HACER:
class CustomContract(SmartContract):
    # Sin documentación
    
    def custom_function(self, arg):
        # Sin comentarios sobre qué hace
        x = arg * 2
        return x > 10
5. Manejo de Errores
✅ HACER:
def execute_contract(contract_id):
    try:
        contract = manager.get_contract(contract_id)
        
        if not contract:
            return False, "Contract not found"
        
        if contract.executed:
            return False, "Already executed"
        
        success, msg = contract.execute(blockchain)
        
        if success:
            manager.save_contracts()
        
        return success, msg
        
    except Exception as e:
        logging.error(f"Error executing contract: {e}")
        return False, f"Execution failed: {str(e)}"
❌ NO HACER:
def execute_contract(contract_id):
    # Sin manejo de errores
    contract = manager.contracts[contract_id]
    contract.execute(blockchain)
    # Puede fallar sin información útil
🐛 Debugging
Verificar Ejecución
# Activar modo debug en Script Engine
class ScriptEngine:
    def __init__(self, debug=False):
        self.debug = debug
        # ...
    
    def _execute_instruction(self, instruction):
        if self.debug:
            print(f"Executing: {instruction}")
            print(f"Stack before: {self.stack}")
        
        # ... ejecutar
        
        if self.debug:
            print(f"Stack after: {self.stack}")
            print(f"Gas used: {self.gas_used}")

# Usar
engine = ScriptEngine(debug=True)
engine.execute(script)
Logs de Contratos
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def execute_contract(contract_id):
    logging.info(f"Executing contract {contract_id}")
    
    contract = manager.get_contract(contract_id)
    logging.debug(f"Contract type: {contract.contract_type}")
    logging.debug(f"Contract data: {contract.data}")
    
    success, msg = contract.execute(blockchain)
    
    if success:
        logging.info(f"Contract executed successfully")
    else:
        logging.error(f"Contract execution failed: {msg}")
    
    return success, msg
📚 Referencias
Bitcoin Script
Ethereum Smart Contracts
Solidity Documentation
Stack-Based Virtual Machines
🔗 Recursos Adicionales
API Reference - Endpoints de contratos
Network Guide - Propagación de contratos en red
Architecture - Diseño técnico del sistema
¡Empieza a crear tus propios Smart Contracts en ColCript! 🚀
