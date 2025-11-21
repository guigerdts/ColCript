# 📡 API Reference - ColCript

Documentación completa de todos los endpoints de la API REST de ColCript.

---

## 📋 Tabla de Contenidos

1. [Información General](#información-general)
2. [Endpoints de Información](#endpoints-de-información)
3. [Endpoints de Blockchain](#endpoints-de-blockchain)
4. [Endpoints de Transacciones](#endpoints-de-transacciones)
5. [Endpoints de Wallets](#endpoints-de-wallets)
6. [Endpoints de Minería](#endpoints-de-minería)
7. [Endpoints de Faucet](#endpoints-de-faucet)
8. [Endpoints de Dificultad](#endpoints-de-dificultad)
9. [Endpoints de Smart Contracts](#endpoints-de-smart-contracts)
10. [Endpoints de Red P2P](#endpoints-de-red-p2p)
11. [Códigos de Error](#códigos-de-error)

---

## 📊 Información General

### Base URL
http://localhost:5000/api
### Formato de Respuesta

Todas las respuestas siguen este formato estándar:

**Respuesta Exitosa:**
(json)
{
  "success": true,
  "message": "Success message",
  "data": {
    // Datos específicos del endpoint
  }
}
Respuesta de Error:
{
  "success": false,
  "message": "Error description",
  "data": null
}
Headers Recomendados
Content-Type: application/json
Accept: application/json
1️⃣ Endpoints de Información
GET /api/info
Obtiene información general de la blockchain.
Request:
curl http://localhost:5000/api/info
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "nombre": "ColCript",
    "simbolo": "CLC",
    "version": "1.0.0",
    "bloques": 42,
    "transacciones_pendientes": 3,
    "dificultad": 4,
    "mining_reward": 50,
    "total_supply": 2100,
    "hashrate": "1250 H/s"
  }
}
GET /api/docs
Obtiene documentación de todos los endpoints disponibles.
Request:
curl http://localhost:5000/api/docs
Response:
{
  "success": true,
  "message": "API Documentation",
  "data": {
    "version": "1.0.0",
    "endpoints": {
      "GET /api/info": "Información general",
      "GET /api/blockchain": "Ver blockchain completa",
      // ... más endpoints
    }
  }
}
2️⃣ Endpoints de Blockchain
GET /api/blockchain
Obtiene la blockchain completa.
Query Parameters:
limit (opcional): Número máximo de bloques a retornar
offset (opcional): Offset para paginación
Request:
curl http://localhost:5000/api/blockchain?limit=10&offset=0
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "chain": [
      {
        "index": 0,
        "timestamp": 1700000000.123,
        "transactions": [],
        "previous_hash": "0",
        "nonce": 12345,
        "hash": "0000abc...",
        "miner_address": "genesis"
      },
      // ... más bloques
    ],
    "length": 42,
    "total_blocks": 42
  }
}
GET /api/blockchain/info
Obtiene información resumida de la blockchain.
Request:
curl http://localhost:5000/api/blockchain/info
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "bloques": 42,
    "ultimo_bloque": {
      "index": 41,
      "hash": "0000def...",
      "timestamp": 1700000500.456
    },
    "dificultad": 4,
    "transacciones_pendientes": 3,
    "hashrate": "1250 H/s"
  }
}
GET /api/block/:index
Obtiene un bloque específico por su índice.
Parameters:
index: Índice del bloque (número entero)
Request:
curl http://localhost:5000/api/block/5
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "block": {
      "index": 5,
      "timestamp": 1700000250.789,
      "transactions": [
        {
          "sender": "address1...",
          "recipient": "address2...",
          "amount": 10.5,
          "fee": 0.5,
          "timestamp": 1700000240.123,
          "signature": "signature..."
        }
      ],
      "previous_hash": "0000ghi...",
      "nonce": 54321,
      "hash": "0000jkl...",
      "miner_address": "minerAddress..."
    }
  }
}
GET /api/block/latest
Obtiene el último bloque de la cadena.
Request:
curl http://localhost:5000/api/block/latest
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "block": {
      "index": 41,
      "timestamp": 1700000500.456,
      // ... resto del bloque
    }
  }
}
GET /api/block/hash/:hash
Busca un bloque por su hash.
Parameters:
hash: Hash del bloque
Request:
curl http://localhost:5000/api/block/hash/0000abc123...
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "block": {
      "index": 10,
      "hash": "0000abc123...",
      // ... resto del bloque
    }
  }
}
POST /api/blockchain/validate
Valida la integridad de toda la blockchain.
Request:
curl -X POST http://localhost:5000/api/blockchain/validate
Response:
{
  "success": true,
  "message": "Blockchain is valid",
  "data": {
    "valid": true,
    "blocks_validated": 42,
    "errors": []
  }
}
POST /api/blockchain/export
Exporta la blockchain a un archivo JSON.
Request Body:
{
  "filename": "my_blockchain_export.json"
}
Request:
curl -X POST http://localhost:5000/api/blockchain/export \
  -H "Content-Type: application/json" \
  -d '{"filename": "export.json"}'
Response:
{
  "success": true,
  "message": "Blockchain exported successfully",
  "data": {
    "filename": "export.json",
    "blocks": 42,
    "size_bytes": 125000
  }
}
3️⃣ Endpoints de Transacciones
POST /api/transaction
Crea una nueva transacción.
Request Body:
{
  "sender": "sender_address",
  "recipient": "recipient_address",
  "amount": 10.5,
  "fee": 0.5,
  "private_key": "private_key_hex"
}
Request:
curl -X POST http://localhost:5000/api/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "abc123...",
    "recipient": "def456...",
    "amount": 10.5,
    "fee": 0.5,
    "private_key": "0123456789abcdef..."
  }'
Response:
{
  "success": true,
  "message": "Transaction created successfully",
  "data": {
    "transaction": {
      "sender": "abc123...",
      "recipient": "def456...",
      "amount": 10.5,
      "fee": 0.5,
      "timestamp": 1700000600.123,
      "signature": "signature..."
    },
    "pending_count": 4
  }
}
GET /api/transactions/pending
Lista todas las transacciones pendientes.
Request:
curl http://localhost:5000/api/transactions/pending
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "count": 3,
    "transactions": [
      {
        "sender": "address1...",
        "recipient": "address2...",
        "amount": 5.0,
        "fee": 0.2,
        "timestamp": 1700000550.123
      },
      // ... más transacciones
    ]
  }
}
GET /api/transactions/history/:address
Obtiene el historial de transacciones de una dirección.
Parameters:
address: Dirección de wallet
Request:
curl http://localhost:5000/api/transactions/history/abc123...
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "address": "abc123...",
    "total_transactions": 15,
    "sent": 8,
    "received": 7,
    "transactions": [
      {
        "type": "sent",
        "recipient": "def456...",
        "amount": 10.5,
        "fee": 0.5,
        "block": 25,
        "timestamp": 1700000300.456
      },
      {
        "type": "received",
        "sender": "ghi789...",
        "amount": 20.0,
        "block": 30,
        "timestamp": 1700000400.789
      },
      // ... más transacciones
    ]
  }
}
GET /api/transaction/verify
Verifica si una transacción es válida.
Query Parameters:
sender: Dirección del remitente
recipient: Dirección del destinatario
amount: Cantidad
signature: Firma de la transacción
Request:
curl "http://localhost:5000/api/transaction/verify?sender=abc...&recipient=def...&amount=10&signature=sig..."
Response:
{
  "success": true,
  "message": "Transaction is valid",
  "data": {
    "valid": true,
    "signature_valid": true,
    "balance_sufficient": true
  }
}
4️⃣ Endpoints de Wallets
POST /api/wallet/create
Crea una nueva wallet.
Request Body:
{
  "name": "Mi Wallet"
}
Request:
curl -X POST http://localhost:5000/api/wallet/create \
  -H "Content-Type: application/json" \
  -d '{"name": "Mi Wallet"}'
Response:
{
  "success": true,
  "message": "Wallet created successfully",
  "data": {
    "name": "Mi Wallet",
    "address": "abc123def456...",
    "private_key": "0123456789abcdef...",
    "public_key": "04abcdef..."
  }
}
⚠️ IMPORTANTE: Guarda la clave privada de forma segura. No se puede recuperar.
GET /api/wallet/balance/:address
Obtiene el balance de una wallet.
Parameters:
address: Dirección de la wallet
Request:
curl http://localhost:5000/api/wallet/balance/abc123...
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "address": "abc123...",
    "balance": 125.5,
    "pending_sent": 10.5,
    "pending_received": 5.0,
    "available": 120.0
  }
}
POST /api/wallet/import
Importa una wallet existente.
Request Body:
{
  "name": "Wallet Importada",
  "private_key": "0123456789abcdef..."
}
Request:
curl -X POST http://localhost:5000/api/wallet/import \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Imported",
    "private_key": "0123456789abcdef..."
  }'
Response:
{
  "success": true,
  "message": "Wallet imported successfully",
  "data": {
    "name": "Imported",
    "address": "abc123...",
    "balance": 50.0
  }
}
5️⃣ Endpoints de Minería
POST /api/mine
Mina un nuevo bloque.
Request Body:
{
  "miner_address": "miner_address"
}
Request:
curl -X POST http://localhost:5000/api/mine \
  -H "Content-Type: application/json" \
  -d '{"miner_address": "abc123..."}'
Response:
{
  "success": true,
  "message": "Block mined successfully",
  "data": {
    "block": {
      "index": 43,
      "hash": "0000mno...",
      "nonce": 98765,
      "transactions_count": 3,
      "mining_time": 8.45
    },
    "reward": 50.0,
    "fees": 1.5,
    "total_earned": 51.5
  }
}
GET /api/hashrate
Obtiene el hashrate actual de la red.
Request:
curl http://localhost:5000/api/hashrate
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "hashrate": "1250 H/s",
    "hashrate_numeric": 1250,
    "difficulty": 4,
    "average_block_time": 10.2
  }
}
GET /api/mining/stats
Obtiene estadísticas de minería.
Request:
curl http://localhost:5000/api/mining/stats
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "total_blocks_mined": 42,
    "total_rewards": 2100.0,
    "average_mining_time": 10.5,
    "last_block_time": 9.8,
    "difficulty": 4,
    "next_difficulty_adjustment": 8
  }
}
6️⃣ Endpoints de Faucet
POST /api/faucet/claim
Reclama CLC gratis del faucet.
Request Body:
{
  "address": "recipient_address"
}
Request:
curl -X POST http://localhost:5000/api/faucet/claim \
  -H "Content-Type: application/json" \
  -d '{"address": "abc123..."}'
Response:
{
  "success": true,
  "message": "Faucet claim successful",
  "data": {
    "address": "abc123...",
    "amount": 5.0,
    "next_claim_time": 1700086400.0,
    "cooldown_hours": 24
  }
}
Error (cooldown activo):
{
  "success": false,
  "message": "You must wait 18.5 hours before claiming again",
  "data": {
    "time_remaining": 66600,
    "next_claim_time": 1700086400.0
  }
}
7️⃣ Endpoints de Dificultad
GET /api/difficulty/info
Obtiene información sobre la dificultad actual.
Request:
curl http://localhost:5000/api/difficulty/info
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "current_difficulty": 4,
    "auto_adjust_enabled": true,
    "target_block_time": 10,
    "adjustment_interval": 10,
    "blocks_until_adjustment": 7,
    "average_block_time": 10.2,
    "last_adjustment_block": 40
  }
}
POST /api/difficulty/set
Establece la dificultad manualmente (desactiva auto-ajuste).
Request Body:
{
  "difficulty": 5
}
Request:
curl -X POST http://localhost:5000/api/difficulty/set \
  -H "Content-Type: application/json" \
  -d '{"difficulty": 5}'
Response:
{
  "success": true,
  "message": "Difficulty set to 5",
  "data": {
    "difficulty": 5,
    "auto_adjust_enabled": false
  }
}
POST /api/difficulty/toggle
Activa/desactiva el ajuste automático de dificultad.
Request Body:
{
  "enabled": true
}
Request:
curl -X POST http://localhost:5000/api/difficulty/toggle \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
Response:
{
  "success": true,
  "message": "Auto-adjust enabled",
  "data": {
    "auto_adjust_enabled": true,
    "current_difficulty": 4
  }
}
POST /api/difficulty/config
Configura parámetros de ajuste de dificultad.
Request Body:
{
  "target_time": 10,
  "interval": 10
}
Request:
curl -X POST http://localhost:5000/api/difficulty/config \
  -H "Content-Type: application/json" \
  -d '{"target_time": 10, "interval": 10}'
Response:
{
  "success": true,
  "message": "Difficulty config updated",
  "data": {
    "target_block_time": 10,
    "adjustment_interval": 10
  }
}
8️⃣ Endpoints de Smart Contracts
GET /api/contracts/list
Lista todos los contratos.
Query Parameters:
status (opcional): "pending" o "executed"
Request:
curl http://localhost:5000/api/contracts/list?status=pending
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "count": 5,
    "contracts": [
      {
        "contract_id": "TL-1",
        "contract_type": "timelock",
        "creator": "address...",
        "executed": false,
        "info": {
          "type": "Timelock",
          "unlock_block": 100,
          "amount": 50.0,
          "recipient": "address..."
        }
      },
      // ... más contratos
    ]
  }
}
GET /api/contracts/:id
Obtiene detalles de un contrato específico.
Parameters:
id: ID del contrato (ej: "TL-1")
Request:
curl http://localhost:5000/api/contracts/TL-1
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "contract_id": "TL-1",
    "contract_type": "timelock",
    "creator": "address...",
    "created_at": 1700000000.123,
    "executed": false,
    "execution_block": null,
    "execution_result": null,
    "info": {
      "type": "Timelock",
      "unlock_block": 100,
      "amount": 50.0,
      "recipient": "address...",
      "status": "Pending"
    },
    "data": {
      "unlock_block": 100,
      "amount": 50.0,
      "recipient": "address..."
    }
  }
}
POST /api/contracts/timelock/create
Crea un contrato Timelock.
Request Body:
{
  "creator": "creator_address",
  "unlock_block": 100,
  "amount": 50.0,
  "recipient": "recipient_address"
}
Request:
curl -X POST http://localhost:5000/api/contracts/timelock/create \
  -H "Content-Type: application/json" \
  -d '{
    "creator": "abc123...",
    "unlock_block": 100,
    "amount": 50.0,
    "recipient": "def456..."
  }'
Response:
{
  "success": true,
  "message": "Timelock contract created successfully",
  "data": {
    "contract_id": "TL-2",
    "contract_type": "timelock",
    "info": {
      "type": "Timelock",
      "unlock_block": 100,
      "amount": 50.0,
      "recipient": "def456...",
      "status": "Pending"
    }
  }
}
POST /api/contracts/multisig/create
Crea un contrato Multisig.
Request Body:
{
  "creator": "creator_address",
  "required_sigs": 2,
  "signers": ["address1", "address2", "address3"],
  "amount": 100.0,
  "recipient": "recipient_address"
}
Request:
curl -X POST http://localhost:5000/api/contracts/multisig/create \
  -H "Content-Type: application/json" \
  -d '{
    "creator": "abc123...",
    "required_sigs": 2,
    "signers": ["addr1...", "addr2...", "addr3..."],
    "amount": 100.0,
    "recipient": "def456..."
  }'
Response:
{
  "success": true,
  "message": "Multisig contract created successfully",
  "data": {
    "contract_id": "MS-1",
    "contract_type": "multisig",
    "info": {
      "type": "Multisig",
      "required_sigs": 2,
      "total_signers": 3,
      "current_sigs": 0,
      "amount": 100.0,
      "recipient": "def456...",
      "status": "0/2 sigs"
    }
  }
}
POST /api/contracts/escrow/create
Crea un contrato Escrow.
Request Body:
{
  "creator": "creator_address",
  "buyer": "buyer_address",
  "seller": "seller_address",
  "arbiter": "arbiter_address",
  "amount": 200.0
}
Request:
curl -X POST http://localhost:5000/api/contracts/escrow/create \
  -H "Content-Type: application/json" \
  -d '{
    "creator": "abc123...",
    "buyer": "buyer...",
    "seller": "seller...",
    "arbiter": "arbiter...",
    "amount": 200.0
  }'
Response:
{
  "success": true,
  "message": "Escrow contract created successfully",
  "data": {
    "contract_id": "ES-1",
    "contract_type": "escrow",
    "info": {
      "type": "Escrow",
      "buyer": "buyer...",
      "seller": "seller...",
      "arbiter": "arbiter...",
      "amount": 200.0,
      "status": "pending",
      "decision": null
    }
  }
}
POST /api/contracts/:id/execute
Ejecuta un contrato.
Parameters:
id: ID del contrato
Request:
curl -X POST http://localhost:5000/api/contracts/TL-1/execute
Response (éxito):
{
  "success": true,
  "message": "Script executed successfully. Gas used: 3",
  "data": {
    "contract_id": "TL-1",
    "execution_result": {
      "success": true,
      "gas_used": 3,
      "operations": [
        "PUSH 100",
        "CHECKLOCKTIMEVERIFY (height: 105 >= 100)",
        "PUSH 1"
      ],
      "final_stack": [1],
      "message": "Script executed successfully. Gas used: 3"
    }
  }
}
Response (fallo):
{
  "success": false,
  "message": "OP_CHECKLOCKTIMEVERIFY: Block height 50 < locktime 100",
  "data": null
}
POST /api/contracts/multisig/:id/sign
Firma un contrato Multisig.
Parameters:
id: ID del contrato
Request Body:
{
  "signer": "signer_address"
}
Request:
curl -X POST http://localhost:5000/api/contracts/multisig/MS-1/sign \
  -H "Content-Type: application/json" \
  -d '{"signer": "addr1..."}'
Response:
{
  "success": true,
  "message": "Signature added successfully",
  "data": {
    "contract_id": "MS-1",
    "info": {
      "type": "Multisig",
      "required_sigs": 2,
      "current_sigs": 1,
      "status": "1/2 sigs"
    }
  }
}
POST /api/contracts/escrow/:id/decide
Decide un contrato Escrow (solo el árbitro).
Parameters:
id: ID del contrato
Request Body:
{
  "arbiter": "arbiter_address",
  "approve": true
}
Request:
curl -X POST http://localhost:5000/api/contracts/escrow/ES-1/decide \
  -H "Content-Type: application/json" \
  -d '{
    "arbiter": "arbiter...",
    "approve": true
  }'
Response:
{
  "success": true,
  "message": "Decision: Approved",
  "data": {
    "contract_id": "ES-1",
    "info": {
      "type": "Escrow",
      "status": "approved",
      "decision": true
    }
  }
}
9️⃣ Endpoints de Red P2P
GET /api/network/info
Obtiene información del nodo P2P.
Request:
curl http://localhost:5000/api/network/info
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "node_id": "abc123def456",
    "host": "127.0.0.1",
    "port": 6000,
    "peers_count": 3,
    "peers": [
      "192.168.1.100:5000",
      "192.168.1.101:5000",
      "192.168.1.102:5000"
    ],
    "uptime": "2h 15m",
    "blocks_received": 15,
    "blocks_sent": 8,
    "transactions_received": 42,
    "transactions_sent": 30,
    "blockchain_height": 105
  }
}
GET /api/network/peers
Lista todos los peers conectados.
Request:
curl http://localhost:5000/api/network/peers
Response:
{
  "success": true,
  "message": "Success",
  "data": {
    "count": 3,
    "peers": [
      "192.168.1.100:5000",
      "192.168.1.101:5000",
      "192.168.1.102:5000"
    ]
  }
}
POST /api/network/peer/add
Agrega un peer a la red.
Request Body:
{
  "host": "192.168.1.103",
  "port": 5000
}
Request:
curl -X POST http://localhost:5000/api/network/peer/add \
  -H "Content-Type: application/json" \
  -d '{"host": "192.168.1.103", "port": 5000}'
Response:
{
  "success": true,
  "message": "Peer 192.168.1.103:5000 added",
  "data": {
    "peer": "192.168.1.103:5000",
    "peers_count": 4
  }
}
POST /api/network/peer/remove
Elimina un peer de la red.
Request Body:
{
  "host": "192.168.1.103",
  "port": 5000
}
Request:
curl -X POST http://localhost:5000/api/network/peer/remove \
  -H "Content-Type: application/json" \
  -d '{"host": "192.168.1.103", "port": 5000}'
Response:
{
  "success": true,
  "message": "Peer 192.168.1.103:5000 removed",
  "data": {
    "peer": "192.168.1.103:5000",
    "peers_count": 3
  }
}
POST /api/network/sync
Sincroniza con todos los peers de la red.
Request:
curl -X POST http://localhost:5000/api/network/sync
Response:
{
  "success": true,
  "message": "Network synchronized",
  "data": {
    "synced_peers": 3,
    "blockchain_height": 110
  }
}


POST /api/network/transaction
Recibe una transacción de otro nodo (uso interno).
Request Body:
{
  "sender": "address...",
  "recipient": "address...",
  "amount": 10.5,
  "fee": 0.5,
  "timestamp": 1700000700.123,
  "signature": "signature..."
}
Request:
curl -X POST http://localhost:5000/api/network/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "abc...",
    "recipient": "def...",
    "amount": 10.5,
    "fee": 0.5,
    "timestamp": 1700000700.123,
    "signature": "sig..."
  }'
Response:
{
  "success": true,
  "message": "Transaction received and added to pool",
  "data": {
    "transaction_added": true
  }
}
POST /api/network/block
Recibe un bloque de otro nodo (uso interno).
Request Body:
{
  "index": 43,
  "timestamp": 1700000800.456,
  "transactions": [...],
  "previous_hash": "0000abc...",
  "nonce": 12345,
  "hash": "0000def...",
  "miner_address": "miner..."
}
Response:
{
  "success": true,
  "message": "Block received",
  "data": {
    "block_received": true,
    "block_index": 43
  }
}
POST /api/network/discover
Descubre peers a través de nodos semilla.
Request Body:
{
  "seed_nodes": [
    "192.168.1.100:5000",
    "192.168.1.101:5000"
  ]
}
Request:
curl -X POST http://localhost:5000/api/network/discover \
  -H "Content-Type: application/json" \
  -d '{
    "seed_nodes": [
      "192.168.1.100:5000",
      "192.168.1.101:5000"
    ]
  }'
Response:
{
  "success": true,
  "message": "Discovered 5 new peers",
  "data": {
    "discovered": 5,
    "total_peers": 8
  }
}
🔴 Códigos de Error
Códigos HTTP
Código
Descripción
200
OK - Solicitud exitosa
400
Bad Request - Solicitud mal formada
404
Not Found - Recurso no encontrado
500
Internal Server Error - Error del servidor
Mensajes de Error Comunes
Blockchain:
{
  "success": false,
  "message": "Blockchain is corrupted",
  "data": null
}
Transacciones:
{
  "success": false,
  "message": "Insufficient balance",
  "data": null
}
Wallets:
{
  "success": false,
  "message": "Invalid private key",
  "data": null
}
Smart Contracts:
{
  "success": false,
  "message": "Contract TL-1 not found",
  "data": null
}
Red P2P:
{
  "success": false,
  "message": "Peer is not responding",
  "data": null
}
📝 Ejemplos de Uso
Ejemplo 1: Flujo Completo de Transacción
# 1. Crear wallet
curl -X POST http://localhost:5000/api/wallet/create \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

# Respuesta: {"address": "abc123...", "private_key": "key..."}

# 2. Usar faucet
curl -X POST http://localhost:5000/api/faucet/claim \
  -H "Content-Type: application/json" \
  -d '{"address": "abc123..."}'

# 3. Verificar balance
curl http://localhost:5000/api/wallet/balance/abc123...

# 4. Enviar transacción
curl -X POST http://localhost:5000/api/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "abc123...",
    "recipient": "def456...",
    "amount": 2.5,
    "fee": 0.1,
    "private_key": "key..."
  }'

# 5. Minar bloque
curl -X POST http://localhost:5000/api/mine \
  -H "Content-Type: application/json" \
  -d '{"miner_address": "abc123..."}'
Ejemplo 2: Crear y Ejecutar Contrato Timelock
# 1. Crear contrato
curl -X POST http://localhost:5000/api/contracts/timelock/create \
  -H "Content-Type: application/json" \
  -d '{
    "creator": "abc123...",
    "unlock_block": 100,
    "amount": 50.0,
    "recipient": "def456..."
  }'

# Respuesta: {"contract_id": "TL-1"}

# 2. Ver contrato
curl http://localhost:5000/api/contracts/TL-1

# 3. Intentar ejecutar (fallará si bloque < 100)
curl -X POST http://localhost:5000/api/contracts/TL-1/execute

# 4. Minar bloques hasta >= 100
for i in {1..50}; do
  curl -X POST http://localhost:5000/api/mine \
    -H "Content-Type: application/json" \
    -d '{"miner_address": "abc123..."}'
done

# 5. Ejecutar contrato (ahora exitoso)
curl -X POST http://localhost:5000/api/contracts/TL-1/execute
Ejemplo 3: Configurar Red P2P
# Nodo A (localhost:5000)

# 1. Ver info del nodo
curl http://localhost:5000/api/network/info

# 2. Agregar peer
curl -X POST http://localhost:5000/api/network/peer/add \
  -H "Content-Type: application/json" \
  -d '{"host": "192.168.1.100", "port": 5000}'

# 3. Listar peers
curl http://localhost:5000/api/network/peers

# 4. Sincronizar
curl -X POST http://localhost:5000/api/network/sync

# 5. Ver estadísticas actualizadas
curl http://localhost:5000/api/network/info
Ejemplo 4: Monitoreo de Blockchain
# Script de monitoreo continuo
while true; do
  echo "=== Blockchain Status ==="
  curl -s http://localhost:5000/api/blockchain/info | jq '.'
  echo ""
  echo "=== Mining Stats ==="
  curl -s http://localhost:5000/api/mining/stats | jq '.'
  echo ""
  echo "=== Network Info ==="
  curl -s http://localhost:5000/api/network/info | jq '.'
  echo ""
  sleep 10
done
🧪 Testing
Probar con cURL
Todos los ejemplos anteriores usan cURL. Instálalo con:
# Termux
pkg install curl

# Ubuntu/Debian
sudo apt install curl
Probar con Python
import requests

# Obtener info
response = requests.get('http://localhost:5000/api/info')
print(response.json())

# Crear transacción
tx_data = {
    'sender': 'abc123...',
    'recipient': 'def456...',
    'amount': 10.5,
    'fee': 0.5,
    'private_key': 'key...'
}
response = requests.post(
    'http://localhost:5000/api/transaction',
    json=tx_data
)
print(response.json())
Probar con JavaScript
// Obtener info
fetch('http://localhost:5000/api/info')
  .then(res => res.json())
  .then(data => console.log(data));

// Crear transacción
fetch('http://localhost:5000/api/transaction', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    sender: 'abc123...',
    recipient: 'def456...',
    amount: 10.5,
    fee: 0.5,
    private_key: 'key...'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
🔒 Seguridad
Buenas Prácticas
Nunca compartas tu clave privada
Guárdala de forma segura
No la envíes por canales inseguros
Usa HTTPS en producción
Configura SSL/TLS
No uses HTTP para datos sensibles
Valida siempre las entradas
La API valida, pero hazlo también en cliente
Rate Limiting
Implementa límites de requests
Previene abuso
CORS
En producción, limita orígenes permitidos
No uses * en producción
Configuración Segura
# En producción
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://tu-dominio.com"]
    }
})

# Rate limiting (ejemplo con flask-limiter)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
📚 Referencias
REST API Best Practices
HTTP Status Codes
JSON API Specification
Próximo: Smart Contracts Guide
