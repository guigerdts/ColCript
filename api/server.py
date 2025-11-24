# api/server.py - API REST para ColCript

import os
import sys
import time
from flask import send_from_directory
from flask import Flask, jsonify, request, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from blockchain.blockchain import Blockchain
from blockchain.storage import BlockchainStorage
from wallet.wallet import Wallet
from wallet.faucet import Faucet
from wallet.transaction_history import TransactionHistory
from blockchain.block_explorer import BlockExplorer
from utils.statistics import BlockchainStatistics
from contracts.smart_contract import ContractManager, ContractType
from network.node import Node
from mining.pool import MiningPool
from blockchain.hd_wallet import HDWallet
from utils.qr_generator import QRGenerator
from utils.event_system import event_system, EventType
from utils.backup_system import BackupSystem
from utils.metrics import metrics
import config

app = Flask(__name__,
            static_folder='../web',
            static_url_path='')

# Middleware para registrar métricas
# POR QUÉ: Rastrear todas las requests automáticamente
@app.before_request
def before_request():
    """Registra inicio de request"""
    from flask import g
    g.start_time = time.time()

@app.after_request
def after_request(response):
    """Registra métricas de request"""
    from flask import g, request
    
    try:
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            success = response.status_code < 400
            
            # Registrar en métricas
            metrics.record_request(request.path, duration, success)
    except:
        pass  # No romper si falla el logging

    return response

# Configurar Rate Limiter
# POR QUÉ: Prevenir spam y ataques DDoS
limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Limitar por IP
    default_limits=["200 per day", "50 per hour"],  # Límites globales
    storage_uri="memory://"  # Guardar en memoria (simple)
)

# Sistema de backups
backup_system = BackupSystem()

# Error handler para rate limit
# POR QUÉ: Devolver JSON en lugar de HTML
@app.errorhandler(429)
def ratelimit_handler(e):
    """
    Maneja errores de rate limit (429)
    
    POR QUÉ: Mensajes JSON consistentes con el resto de la API
    """
    return jsonify({
        "success": False,
        "error": "Rate limit exceeded",
        "message": str(e.description),
        "retry_after": e.description
    }), 429


# Estado global
blockchain = None
contract_manager = None
p2p_node = None
mining_pool = None
storage = BlockchainStorage()
current_wallet = None

# ==================== UTILIDADES ====================

def init_blockchain():
    """Inicializa o carga blockchain"""
    global blockchain, contract_manager, p2p_node, mining_pool
    
    if blockchain is None:
        try:
            blockchain = storage.load_blockchain("colcript_main.json")
            if blockchain:
                blockchain.storage = storage
                blockchain.save_filename = "colcript_main.json"
                blockchain.auto_save = True
            else:
                blockchain = Blockchain(auto_save=True)
        except:
            blockchain = Blockchain(auto_save=True)
    
    # Inicializar contract manager
    if contract_manager is None and blockchain is not None:
        contract_manager = ContractManager(blockchain)

    # Inicializar nodo P2P
    if p2p_node is None and blockchain is not None:
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            p2p_node = Node(host=local_ip, port=6000, blockchain=blockchain)
            p2p_node.start()
        except Exception as e:
            print(f"⚠️  No se pudo iniciar nodo P2P: {e}")
            # Crear nodo con localhost si falla
            p2p_node = Node(host='127.0.0.1', port=6000, blockchain=blockchain)
            p2p_node.start()

    # Inicializar nodo P2P
    if p2p_node is None and blockchain is not None:
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            p2p_node = Node(host=local_ip, port=6000, blockchain=blockchain)
            p2p_node.start()
        except Exception as e:
            print(f"⚠️  No se pudo iniciar nodo P2P: {e}")
            p2p_node = Node(host='127.0.0.1', port=6000, blockchain=blockchain)
            p2p_node.start()
    
    # Inicializar pool de minería
    if mining_pool is None and blockchain is not None:
        mining_pool = MiningPool(
            blockchain=blockchain,
            pool_name="ColCript Official Pool",
            pool_fee=1.5
        )


    return blockchain

def response_success(data, message="Success"):
    """Respuesta exitosa estándar"""
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), 200

def response_error(message, code=400):
    """Respuesta de error estándar"""
    return jsonify({
        "success": False,
        "error": message
    }), code

# ==================== ENDPOINTS DE INFO ====================

@app.route('/')
def index():
    """Página principal - Interfaz web"""
    try:
        return app.send_static_file('index.html')
    except:
        # Si no existe index.html, mostrar info de la API
        return jsonify({
            "name": "ColCript API",
            "version": config.VERSION,
            "description": "API REST para la criptomoneda ColCript",
            "endpoints": {
                "info": "/api/info",
                "blockchain": "/api/blockchain/*",
                "wallet": "/api/wallet/*",
                "transaction": "/api/transaction/*",
                "mining": "/api/mining/*",
                "explorer": "/api/explorer/*",
                "statistics": "/api/statistics/*",
                "faucet": "/api/faucet/*",
                "difficulty": "/api/difficulty/*"
            },
            "documentation": "/api/docs",
            "web_interface": "Coming soon..."
        })

@app.route('/api')
def api_index():
    """Información de la API en formato JSON"""
    return jsonify({
        "name": "ColCript API",
        "version": config.VERSION,
        "description": "API REST para la criptomoneda ColCript",
        "endpoints": {
            "info": "/api/info",
            "blockchain": "/api/blockchain/*",
            "wallet": "/api/wallet/*",
            "transaction": "/api/transaction/*",
            "mining": "/api/mining/*",
            "explorer": "/api/explorer/*",
            "statistics": "/api/statistics/*",
            "faucet": "/api/faucet/*",
            "difficulty": "/api/difficulty/*"
        },
        "documentation": "/api/docs"
    })

@app.route('/api/docs')
def docs():
    """Documentación completa de la API"""
    return jsonify({
        "ColCript API": "Documentación completa",
        "version": config.VERSION,
        "endpoints": {
            "GET /": "Información de la API",
            "GET /api/info": "Información de ColCript",
            "GET /api/blockchain": "Ver blockchain completa",
            "GET /api/blockchain/info": "Información de la blockchain",
            "GET /api/blockchain/validate": "Validar blockchain",
            "GET /api/blockchain/list": "Listar blockchains guardadas",
            "POST /api/blockchain/create": "Crear nueva blockchain",
            "POST /api/blockchain/load": "Cargar blockchain (body: {filename})",
            "POST /api/wallet/create": "Crear wallet (body: {name})",
            "POST /api/wallet/load": "Cargar wallet (body: {filename})",
            "GET /api/wallet/balance": "Ver balance de wallet actual",
            "GET /api/wallet/address": "Ver dirección de wallet actual",
            "GET /api/wallet/history": "Ver historial de transacciones",
            "POST /api/transaction/send": "Enviar CLC (body: {recipient, amount, fee?})",
            "GET /api/transaction/pending": "Ver transacciones pendientes",
            "POST /api/mining/mine": "Minar bloque",
            "GET /api/mining/stats": "Estadísticas de minería",
            "GET /api/explorer/block/:number": "Ver bloque por número",
            "GET /api/explorer/blocks": "Ver últimos bloques",
            "GET /api/explorer/search": "Buscar (query: hash, address)",
            "GET /api/statistics/dashboard": "Dashboard completo",
            "GET /api/statistics/supply": "Información de supply",
            "GET /api/statistics/wallets": "Top wallets",
            "GET /api/faucet/info": "Información del faucet",
            "POST /api/faucet/claim": "Reclamar del faucet",
            "GET /api/difficulty/info": "Información de dificultad",
            "POST /api/difficulty/set": "Configurar dificultad (body: {difficulty})",
            "POST /api/difficulty/toggle": "Habilitar/deshabilitar auto-ajuste (body: {enabled})",
            "POST /api/difficulty/config": "Configurar parámetros (body: {target_time, interval})",
            "GET /api/contracts/list": "Listar contratos (query: status)",
            "GET /api/contracts/:id": "Ver contrato",
            "POST /api/contracts/timelock/create": "Crear Timelock (body: {creator, unlock_block, amount, recipient})",
            "POST /api/contracts/multisig/create": "Crear Multisig (body: {creator, required_sigs, signers, amount, recipient})",
            "POST /api/contracts/escrow/create": "Crear Escrow (body: {creator, buyer, seller, arbiter, amount})",
            "POST /api/contracts/:id/execute": "Ejecutar contrato",
            "POST /api/contracts/multisig/:id/sign": "Firmar Multisig (body: {signer})",
            "POST /api/contracts/escrow/:id/decide": "Decidir Escrow (body: {arbiter, approve})",
            "GET /api/network/info": "Información del nodo P2P",
            "GET /api/network/peers": "Listar peers conectados",
            "POST /api/network/peer/add": "Agregar peer (body: {host, port})",
            "POST /api/network/peer/remove": "Eliminar peer (body: {host, port})",
            "POST /api/network/sync": "Sincronizar con red",
            "POST /api/network/transaction": "Recibir transacción de peer",
            "POST /api/network/block": "Recibir bloque de peer",
            "POST /api/network/discover": "Descubrir peers (body: {seed_nodes})",
            "GET /api/pool/info": "Información del pool",
            "GET /api/pool/miners": "Lista de mineros",
            "GET /api/pool/leaderboard": "Ranking de mineros (query: limit)",
            "GET /api/pool/miner/:id": "Estadísticas de minero",
            "POST /api/pool/join": "Unirse al pool (body: {miner_id, address})",
            "POST /api/pool/leave": "Salir del pool (body: {miner_id})",
            "POST /api/pool/mine": "Minar bloque colaborativo",
            "POST /api/pool/submit_share": "Enviar share (body: {miner_id, nonce, block_hash})",
            "POST /api/hdwallet/create": "Crear HD Wallet (body: {name?})",
            "POST /api/hdwallet/restore": "Restaurar desde mnemonic (body: {mnemonic, name?})",
            "GET /api/hdwallet/:file": "Cargar HD Wallet",
            "GET /api/hdwallet/:file/addresses": "Listar direcciones (query: limit, offset)",
            "POST /api/hdwallet/:file/derive": "Derivar nuevas direcciones (body: {count?})",
            "GET /api/hdwallet/:file/balance": "Balance total de todas las direcciones",
            "POST /api/hdwallet/:file/export": "Exportar mnemonic (body: {confirm: true})",
            "POST /api/hdwallet/:file/sign": "Firmar mensaje (body: {message, index})",
            "GET /api/qr/address/:address": "Generar QR de dirección (query: size, border)",
            "POST /api/qr/payment": "Generar QR de pago (body: {address, amount?, memo?, size?, border?})",
            "POST /api/qr/parse": "Parsear URI de pago (body: {uri})",
            "GET /api/events/history": "Historial de eventos (query: type, limit)",
            "GET /api/events/types": "Tipos de eventos disponibles",
            "GET /api/webhooks": "Lista de webhooks",
            "POST /api/webhooks/add": "Agregar webhook (body: {event_type, url})",
            "POST /api/webhooks/:id/remove": "Eliminar webhook",
            "POST /api/webhooks/:id/enable": "Habilitar webhook",
            "POST /api/webhooks/:id/disable": "Deshabilitar webhook",
            "POST /api/notifications/test": "Emitir evento de prueba (body: {event_type?, data?})",
            "GET /api/limits/status": "Ver límites de rate limiting actuales",
            "POST /api/backup/create": "Crear backup manual (body: {tag?})",
            "GET /api/backup/list": "Listar backups disponibles (query: pattern?)",
            "POST /api/backup/restore": "Restaurar desde backup (body: {backup_file})",
            "GET /api/backup/stats": "Estadísticas de backups",
            "GET /api/metrics/system": "Métricas del sistema (CPU, RAM, disco)",
            "GET /api/metrics/api": "Métricas de la API (requests, errors, uptime)",
            "GET /api/health": "Health check del servidor",
            "POST /api/metrics/reset": "Reiniciar métricas (1/hour)"
        },

        "rate_limits": {
            "note": "All endpoints have rate limits to prevent abuse",
            "global": "200 per day, 50 per hour per IP",
            "transaction_send": "10 per minute",
            "mining": "5 per minute",
            "faucet_claim": "1 per hour",
            "status_code": "429 when limit exceeded"
        }

    })

@app.route('/api/info')
def api_info():
    """Información general de ColCript"""
    init_blockchain()
    return response_success({
        "name": config.COIN_NAME,
        "symbol": config.COIN_SYMBOL,
        "version": config.VERSION,
        "total_supply": config.TOTAL_SUPPLY,
        "mining_reward": config.MINING_REWARD,
        "difficulty": config.MINING_DIFFICULTY,
        "min_fee": config.MIN_TRANSACTION_FEE,
        "default_fee": config.DEFAULT_TRANSACTION_FEE,
        "faucet_amount": config.FAUCET_AMOUNT,
        "faucet_cooldown_hours": config.FAUCET_COOLDOWN_HOURS,
        "blocks_count": len(blockchain.chain) if blockchain else 0
    })

# ==================== ENDPOINTS DE BLOCKCHAIN ====================

@app.route('/api/blockchain')
def get_blockchain():
    """Obtiene la blockchain completa"""
    init_blockchain()
    
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "miner": block.miner_address,
            "nonce": block.nonce,
            "transactions_count": len(block.transactions)
        })
    
    return response_success({
        "chain": chain_data,
        "length": len(blockchain.chain)
    })

@app.route('/api/blockchain/info')
def blockchain_info():
    """Información de la blockchain"""
    init_blockchain()
    return response_success(blockchain.get_chain_info())

@app.route('/api/blockchain/validate')
def validate_blockchain():
    """Valida la integridad de la blockchain"""
    init_blockchain()
    is_valid = blockchain.is_chain_valid()
    
    return response_success({
        "valid": is_valid,
        "blocks": len(blockchain.chain)
    }, "Blockchain is valid" if is_valid else "Blockchain is invalid")

@app.route('/api/blockchain/list')
def list_blockchains():
    """Lista blockchains guardadas"""
    blockchains = storage.list_blockchains()
    return response_success({"blockchains": blockchains})

@app.route('/api/blockchain/create', methods=['POST'])
def create_blockchain():
    """Crea una nueva blockchain"""
    global blockchain
    
    data = request.get_json() or {}
    filename = data.get('filename', 'colcript_api.json')
    
    blockchain = Blockchain(auto_save=True, save_filename=filename)
    
    return response_success({
        "message": "Blockchain created",
        "filename": filename,
        "genesis_hash": blockchain.chain[0].hash
    }, "Blockchain created successfully")

@app.route('/api/blockchain/load', methods=['POST'])
def load_blockchain():
    """Carga una blockchain existente"""
    global blockchain
    
    data = request.get_json()
    if not data or 'filename' not in data:
        return response_error("Filename required")
    
    filename = data['filename']
    loaded = storage.load_blockchain(filename)
    
    if not loaded:
        return response_error(f"Blockchain {filename} not found", 404)
    
    loaded.storage = storage
    loaded.save_filename = filename
    loaded.auto_save = True
    blockchain = loaded
    
    return response_success({
        "filename": filename,
        "blocks": len(blockchain.chain),
        "valid": blockchain.is_chain_valid()
    }, f"Blockchain {filename} loaded successfully")

# ==================== ENDPOINTS DE WALLET ====================

@app.route('/api/wallet/create', methods=['POST'])
def create_wallet():
    """Crea una nueva wallet"""
    global current_wallet
    
    data = request.get_json() or {}
    name = data.get('name', 'API Wallet')
    
    current_wallet = Wallet(name)
    
    return response_success({
        "name": current_wallet.name,
        "address": current_wallet.get_address()
    }, "Wallet created successfully")

@app.route('/api/wallet/load', methods=['POST'])
def load_wallet():
    """Carga una wallet existente"""
    global current_wallet
    
    data = request.get_json()
    if not data or 'filename' not in data:
        return response_error("Filename required")
    
    filename = data['filename']
    loaded = Wallet.load_from_file(filename)
    
    if not loaded:
        return response_error(f"Wallet {filename} not found", 404)
    
    current_wallet = loaded
    
    return response_success({
        "name": current_wallet.name,
        "address": current_wallet.get_address()
    }, f"Wallet {filename} loaded successfully")

@app.route('/api/wallet/balance')
def wallet_balance():
    """Obtiene el balance de la wallet actual"""
    if not current_wallet:
        return response_error("No wallet loaded. Use POST /api/wallet/create or /api/wallet/load", 400)
    
    init_blockchain()
    balance = current_wallet.get_balance(blockchain)
    
    return response_success({
        "wallet": current_wallet.name,
        "address": current_wallet.get_address(),
        "balance": balance,
        "symbol": config.COIN_SYMBOL
    })

@app.route('/api/wallet/address')
def wallet_address():
    """Obtiene la dirección de la wallet actual"""
    if not current_wallet:
        return response_error("No wallet loaded", 400)
    
    return response_success({
        "name": current_wallet.name,
        "address": current_wallet.get_address()
    })

@app.route('/api/wallet/history')
def wallet_history():
    """Obtiene el historial de transacciones de la wallet"""
    if not current_wallet:
        return response_error("No wallet loaded", 400)
    
    init_blockchain()
    history = TransactionHistory(blockchain, current_wallet.get_address())
    
    return response_success({
        "wallet": current_wallet.name,
        "summary": history.get_summary(),
        "transactions": history.get_all_transactions()
    })

# ==================== ENDPOINTS DE TRANSACCIONES ====================

@app.route('/api/transaction/send', methods=['POST'])
@limiter.limit("10 per minute")
def send_transaction():
    """Envía una transacción"""
    if not current_wallet:
        return response_error("No wallet loaded", 400)
    
    init_blockchain()
    
    data = request.get_json()
    if not data or 'recipient' not in data or 'amount' not in data:
        return response_error("Recipient and amount required")
    
    recipient = data['recipient']
    amount = float(data['amount'])
    fee = float(data.get('fee', config.DEFAULT_TRANSACTION_FEE))
    
    # Validar fondos
    balance = current_wallet.get_balance(blockchain)
    if balance < amount + fee:
        return response_error(f"Insufficient funds. Balance: {balance}, needed: {amount + fee}")
    
    # Crear transacción
    transaction = current_wallet.send_coins(recipient, amount, fee)
    
    if not transaction:
        return response_error("Failed to create transaction")
    
    # Agregar al pool
    blockchain.add_transaction(transaction)
    
    return response_success({
        "transaction": {
            "from": current_wallet.get_address(),
            "to": recipient,
            "amount": amount,
            "fee": fee,
            "total": amount + fee
        },
        "status": "pending",
        "message": "Transaction added to pending pool. Mine a block to confirm."
    }, "Transaction sent successfully")

@app.route('/api/transaction/pending')
def pending_transactions():
    """Obtiene transacciones pendientes"""
    init_blockchain()
    
    pending = []
    for tx in blockchain.pending_transactions:
        pending.append({
            "from": tx.sender,
            "to": tx.recipient,
            "amount": tx.amount,
            "fee": tx.fee,
            "timestamp": tx.timestamp
        })
    
    return response_success({
        "count": len(pending),
        "transactions": pending
    })

# ==================== ENDPOINTS DE MINERÍA ====================

@app.route('/api/mining/mine', methods=['POST'])
@limiter.limit("5 per minute")
def mine_block():
    """Mina un nuevo bloque"""
    if not current_wallet:
        return response_error("No wallet loaded. Need miner address.", 400)
    
    init_blockchain()
    
    import time
    start_time = time.time()
    
    pending_count = len(blockchain.pending_transactions)
    block = blockchain.mine_pending_transactions(current_wallet.get_address())
    
    end_time = time.time()
    mining_time = end_time - start_time

    # Emitir evento
    event_system.emit(EventType.BLOCK_MINED, {
        'block_index': block.index,
        'hash': block.hash,
        'miner': miner_address,
        'reward': blockchain.mining_reward,
        'transactions': len(block.transactions)
    })
    
    return response_success({
        "block": {
            "index": block.index,
            "hash": block.hash,
            "nonce": block.nonce,
            "transactions": len(block.transactions),
            "miner": current_wallet.get_address()
        },
        "mining_time": round(mining_time, 2),
        "pending_transactions": pending_count,
        "reward": config.MINING_REWARD
    }, "Block mined successfully")

@app.route('/api/mining/stats')
def mining_stats():
    """Estadísticas de minería"""
    init_blockchain()
    stats = BlockchainStatistics(blockchain)
    
    return response_success(stats.get_mining_stats())

# ==================== ENDPOINTS DE EXPLORADOR ====================

@app.route('/api/explorer/block/<int:block_number>')
def get_block(block_number):
    """Obtiene un bloque por número"""
    init_blockchain()
    explorer = BlockExplorer(blockchain)
    
    block = explorer.get_block_by_number(block_number)
    
    if not block:
        return response_error(f"Block {block_number} not found", 404)
    
    return response_success({
        "block": explorer.get_block_stats(block),
        "transactions": [tx.to_dict() for tx in block.transactions],
        "verification": explorer.verify_block(block)
    })

@app.route('/api/explorer/blocks')
def get_blocks():
    """Obtiene los últimos bloques"""
    init_blockchain()
    
    limit = int(request.args.get('limit', 10))
    blocks = blockchain.chain[-limit:]
    
    blocks_data = []
    for block in blocks:
        blocks_data.append({
            "index": block.index,
            "hash": block.hash,
            "timestamp": block.timestamp,
            "miner": block.miner_address,
            "transactions": len(block.transactions)
        })
    
    return response_success({
        "blocks": blocks_data,
        "count": len(blocks_data)
    })

@app.route('/api/explorer/search')
def search():
    """Busca por hash o dirección"""
    init_blockchain()
    explorer = BlockExplorer(blockchain)
    
    query = request.args.get('q', '')
    
    if not query:
        return response_error("Query parameter 'q' required")
    
    # Buscar por hash
    block = explorer.get_block_by_hash(query)
    if block:
        return response_success({
            "type": "block",
            "result": explorer.get_block_stats(block)
        })
    
    # Buscar por minero
    blocks = explorer.search_blocks_by_miner(query)
    if blocks:
        return response_success({
            "type": "miner",
            "blocks_count": len(blocks),
            "blocks": [{"index": b.index, "hash": b.hash} for b in blocks]
        })
    
    return response_error("No results found", 404)

# ==================== ENDPOINTS DE ESTADÍSTICAS ====================

@app.route('/api/statistics/dashboard')
def statistics_dashboard():
    """Dashboard completo de estadísticas"""
    init_blockchain()
    stats = BlockchainStatistics(blockchain)
    
    return response_success(stats.get_complete_dashboard())

@app.route('/api/statistics/supply')
def statistics_supply():
    """Información de supply"""
    init_blockchain()
    stats = BlockchainStatistics(blockchain)
    
    return response_success({
        "total": stats.get_total_supply(),
        "circulating": stats.get_circulating_supply(),
        "percentage": stats.get_supply_percentage()
    })

@app.route('/api/statistics/wallets')
def statistics_wallets():
    """Top wallets"""
    init_blockchain()
    stats = BlockchainStatistics(blockchain)
    
    limit = int(request.args.get('limit', 10))
    top = stats.get_top_wallets(limit)
    
    return response_success({
        "top_wallets": [{"address": addr, "balance": bal} for addr, bal in top],
        "total_wallets": len(stats.get_all_addresses())
    })

# ==================== ENDPOINTS DE FAUCET ====================

@app.route('/api/faucet/info')
def faucet_info():
    """Información del faucet"""
    init_blockchain()
    faucet = Faucet(blockchain)
    
    return response_success(faucet.get_faucet_info())

@app.route('/api/faucet/claim', methods=['POST'])
@limiter.limit("1 per hour")
def faucet_claim():
    """Reclama del faucet"""
    if not current_wallet:
        return response_error("No wallet loaded", 400)
    
    init_blockchain()
    faucet = Faucet(blockchain)
    
    success, message = faucet.claim(current_wallet.get_address())
    
    if success:
        return response_success({
            "amount": config.FAUCET_AMOUNT,
            "wallet": current_wallet.get_address(),
            "status": "pending"
        }, message)
    else:
        return response_error(message)

# ==================== ENDPOINTS DE DIFICULTAD ====================

@app.route('/api/difficulty/info')
def difficulty_info():
    """Obtiene información de dificultad"""
    init_blockchain()
    from blockchain.difficulty import DifficultyAdjustment
    
    info = DifficultyAdjustment.get_adjustment_info(blockchain)
    return response_success(info)

@app.route('/api/difficulty/set', methods=['POST'])
def set_difficulty():
    """Configura dificultad manualmente"""
    init_blockchain()
    
    data = request.get_json()
    if not data or 'difficulty' not in data:
        return response_error("Difficulty value required")
    
    new_diff = int(data['difficulty'])
    
    if new_diff < config.MIN_DIFFICULTY or new_diff > config.MAX_DIFFICULTY:
        return response_error(f"Difficulty must be between {config.MIN_DIFFICULTY} and {config.MAX_DIFFICULTY}")
    
    old_diff = blockchain.difficulty
    blockchain.difficulty = new_diff
    
    return response_success({
        "old_difficulty": old_diff,
        "new_difficulty": new_diff,
        "estimated_attempts": 16 ** new_diff
    }, f"Difficulty changed from {old_diff} to {new_diff}")

@app.route('/api/difficulty/toggle', methods=['POST'])
def toggle_auto_adjustment():
    """Habilita/deshabilita ajuste automático"""
    data = request.get_json() or {}
    enabled = data.get('enabled', not config.DIFFICULTY_ADJUSTMENT_ENABLED)
    
    config.DIFFICULTY_ADJUSTMENT_ENABLED = enabled
    
    return response_success({
        "auto_adjustment_enabled": enabled
    }, f"Auto adjustment {'enabled' if enabled else 'disabled'}")

@app.route('/api/difficulty/config', methods=['POST'])
def configure_difficulty():
    """Configura parámetros de ajuste automático"""
    data = request.get_json() or {}
    
    changes = {}
    
    if 'target_time' in data:
        target = int(data['target_time'])
        if 1 <= target <= 3600:
            old = config.TARGET_BLOCK_TIME
            config.TARGET_BLOCK_TIME = target
            changes['target_block_time'] = {'old': old, 'new': target}
    
    if 'interval' in data:
        interval = int(data['interval'])
        if 1 <= interval <= 1000:
            old = config.DIFFICULTY_ADJUSTMENT_INTERVAL
            config.DIFFICULTY_ADJUSTMENT_INTERVAL = interval
            changes['adjustment_interval'] = {'old': old, 'new': interval}
    
    if not changes:
        return response_error("No valid configuration provided")
    
    return response_success(changes, "Configuration updated")


# ==================== ENDPOINTS DE SMART CONTRACTS ====================

@app.route('/api/contracts/list')
def list_contracts():
    """Lista todos los contratos"""
    init_blockchain()
    
    status = request.args.get('status', None)
    contracts = contract_manager.list_contracts(status)
    
    contracts_data = []
    for contract in contracts:
        info = contract.get_info()
        contracts_data.append({
            'contract_id': contract.contract_id,
            'contract_type': contract.contract_type,
            'creator': contract.creator,
            'executed': contract.executed,
            'info': info
        })
    
    return response_success({
        'count': len(contracts_data),
        'contracts': contracts_data
    })

@app.route('/api/contracts/<contract_id>')
def get_contract(contract_id):
    """Obtiene detalles de un contrato"""
    init_blockchain()
    
    contract = contract_manager.get_contract(contract_id)
    
    if not contract:
        return response_error(f"Contract {contract_id} not found", 404)
    
    return response_success({
        'contract_id': contract.contract_id,
        'contract_type': contract.contract_type,
        'creator': contract.creator,
        'created_at': contract.created_at,
        'executed': contract.executed,
        'execution_block': contract.execution_block,
        'execution_result': contract.execution_result,
        'info': contract.get_info(),
        'data': contract.data
    })

@app.route('/api/contracts/timelock/create', methods=['POST'])
def create_timelock():
    """Crea un contrato timelock"""
    init_blockchain()
    
    data = request.get_json()
    if not data:
        return response_error("Request body required")
    
    required = ['creator', 'unlock_block', 'amount', 'recipient']
    for field in required:
        if field not in data:
            return response_error(f"Field '{field}' required")
    
    try:
        contract = contract_manager.create_timelock(
            creator=data['creator'],
            unlock_block=int(data['unlock_block']),
            amount=float(data['amount']),
            recipient=data['recipient']
        )
        
        return response_success({
            'contract_id': contract.contract_id,
            'contract_type': contract.contract_type,
            'info': contract.get_info()
        }, "Timelock contract created successfully")
        
    except Exception as e:
        return response_error(str(e))

@app.route('/api/contracts/multisig/create', methods=['POST'])
def create_multisig():
    """Crea un contrato multisig"""
    init_blockchain()
    
    data = request.get_json()
    if not data:
        return response_error("Request body required")
    
    required = ['creator', 'required_sigs', 'signers', 'amount', 'recipient']
    for field in required:
        if field not in data:
            return response_error(f"Field '{field}' required")
    
    try:
        contract = contract_manager.create_multisig(
            creator=data['creator'],
            required_sigs=int(data['required_sigs']),
            signers=data['signers'],
            amount=float(data['amount']),
            recipient=data['recipient']
        )
        
        return response_success({
            'contract_id': contract.contract_id,
            'contract_type': contract.contract_type,
            'info': contract.get_info()
        }, "Multisig contract created successfully")
        
    except Exception as e:
        return response_error(str(e))

@app.route('/api/contracts/escrow/create', methods=['POST'])
def create_escrow():
    """Crea un contrato escrow"""
    init_blockchain()
    
    data = request.get_json()
    if not data:
        return response_error("Request body required")
    
    required = ['creator', 'buyer', 'seller', 'arbiter', 'amount']
    for field in required:
        if field not in data:
            return response_error(f"Field '{field}' required")
    
    try:
        contract = contract_manager.create_escrow(
            creator=data['creator'],
            buyer=data['buyer'],
            seller=data['seller'],
            arbiter=data['arbiter'],
            amount=float(data['amount'])
        )
        
        return response_success({
            'contract_id': contract.contract_id,
            'contract_type': contract.contract_type,
            'info': contract.get_info()
        }, "Escrow contract created successfully")
        
    except Exception as e:
        return response_error(str(e))

@app.route('/api/contracts/<contract_id>/execute', methods=['POST'])
def execute_contract(contract_id):
    """Ejecuta un contrato"""
    init_blockchain()
    
    contract = contract_manager.get_contract(contract_id)
    
    if not contract:
        return response_error(f"Contract {contract_id} not found", 404)
    
    if contract.executed:
        return response_error("Contract already executed")
    
    context = {'block_height': len(blockchain.chain)}
    success, msg = contract_manager.execute_contract(contract_id, context)
    
    if success:
        return response_success({
            'contract_id': contract_id,
            'execution_result': contract.execution_result
        }, msg)
    else:
        return response_error(msg)

@app.route('/api/contracts/multisig/<contract_id>/sign', methods=['POST'])
def sign_multisig(contract_id):
    """Firma un contrato multisig"""
    init_blockchain()
    
    data = request.get_json()
    if not data or 'signer' not in data:
        return response_error("Signer address required")
    
    contract = contract_manager.get_contract(contract_id)
    
    if not contract:
        return response_error(f"Contract {contract_id} not found", 404)
    
    if contract.contract_type != ContractType.MULTISIG:
        return response_error("Contract is not multisig type")
    
    success = contract.add_signature(data['signer'])
    
    if success:
        contract_manager.save_contracts()
        return response_success({
            'contract_id': contract_id,
            'info': contract.get_info()
        }, "Signature added successfully")
    else:
        return response_error("Cannot sign this contract")

@app.route('/api/contracts/escrow/<contract_id>/decide', methods=['POST'])
def decide_escrow(contract_id):
    """Decide un contrato escrow"""
    init_blockchain()
    
    data = request.get_json()
    if not data:
        return response_error("Request body required")
    
    if 'arbiter' not in data or 'approve' not in data:
        return response_error("Arbiter and approve fields required")
    
    contract = contract_manager.get_contract(contract_id)
    
    if not contract:
        return response_error(f"Contract {contract_id} not found", 404)
    
    if contract.contract_type != ContractType.ESCROW:
        return response_error("Contract is not escrow type")
    
    success, msg = contract.make_decision(data['arbiter'], data['approve'])
    
    if success:
        contract_manager.save_contracts()
        return response_success({
            'contract_id': contract_id,
            'info': contract.get_info()
        }, msg)
    else:
        return response_error(msg)

# ==================== ENDPOINTS DE RED P2P ====================

@app.route('/api/network/info')
def network_info():
    """Información del nodo P2P"""
    init_blockchain()
    
    if not p2p_node:
        return response_error("P2P node not initialized")
    
    return response_success(p2p_node.get_network_info())

@app.route('/api/network/peers')
def list_peers():
    """Lista peers conectados"""
    init_blockchain()
    
    if not p2p_node:
        return response_error("P2P node not initialized")
    
    peers = [f"{h}:{p}" for h, p in p2p_node.peers]
    
    return response_success({
        'count': len(peers),
        'peers': peers
    })

@app.route('/api/network/peer/add', methods=['POST'])
def add_peer():
    """Agrega un peer a la red"""
    init_blockchain()
    
    if not p2p_node:
        return response_error("P2P node not initialized")
    
    data = request.get_json()
    if not data or 'host' not in data or 'port' not in data:
        return response_error("Host and port required")
    
    host = data['host']
    port = int(data['port'])
    
    success, msg = p2p_node.add_peer(host, port)
    
    if success:
        return response_success({
            'peer': f"{host}:{port}",
            'peers_count': len(p2p_node.peers)
        }, msg)
    else:
        return response_error(msg)

@app.route('/api/network/peer/remove', methods=['POST'])
def remove_peer():
    """Elimina un peer de la red"""
    init_blockchain()
    
    if not p2p_node:
        return response_error("P2P node not initialized")
    
    data = request.get_json()
    if not data or 'host' not in data or 'port' not in data:
        return response_error("Host and port required")
    
    host = data['host']
    port = int(data['port'])
    
    success, msg = p2p_node.remove_peer(host, port)
    
    if success:
        return response_success({
            'peer': f"{host}:{port}",
            'peers_count': len(p2p_node.peers)
        }, msg)
    else:
        return response_error(msg)

@app.route('/api/network/sync', methods=['POST'])
def sync_network():
    """Sincroniza con todos los peers"""
    init_blockchain()
    
    if not p2p_node:
        return response_error("P2P node not initialized")
    
    if not p2p_node.peers:
        return response_error("No peers connected")
    
    p2p_node.sync_with_network()
    
    return response_success({
        'synced_peers': len(p2p_node.peers),
        'blockchain_height': len(blockchain.chain)
    }, "Network synchronized")

@app.route('/api/network/transaction', methods=['POST'])
def receive_transaction():
    """Recibe una transacción de otro nodo"""
    init_blockchain()
    
    data = request.get_json()
    if not data:
        return response_error("Transaction data required")
    
    try:
        from blockchain.transaction import Transaction
        
        # Reconstruir transacción
        tx = Transaction(
            data['sender'],
            data['recipient'],
            data['amount']
        )
        tx.timestamp = data['timestamp']
        tx.signature = data.get('signature')
        tx.fee = data.get('fee', 0)
        
        # Validar y agregar al pool
        if tx.is_valid():
            blockchain.add_transaction(tx)
            
            if p2p_node:
                p2p_node.transactions_received += 1
            
            return response_success({
                'transaction_added': True
            }, "Transaction received and added to pool")
        else:
            return response_error("Invalid transaction")
            
    except Exception as e:
        return response_error(str(e))

@app.route('/api/network/block', methods=['POST'])
def receive_block():
    """Recibe un bloque de otro nodo"""
    init_blockchain()
    
    data = request.get_json()
    if not data:
        return response_error("Block data required")
    
    try:
        from blockchain.block import Block
        from blockchain.transaction import Transaction
        
        # Reconstruir transacciones
        transactions = []
        for tx_data in data['transactions']:
            tx = Transaction(
                tx_data['sender'],
                tx_data['recipient'],
                tx_data['amount']
            )
            tx.timestamp = tx_data['timestamp']
            tx.signature = tx_data.get('signature')
            tx.fee = tx_data.get('fee', 0)
            transactions.append(tx)
        
        # Reconstruir bloque
        block = Block(
            data['index'],
            transactions,
            data['previous_hash'],
            data['miner_address']
        )
        block.timestamp = data['timestamp']
        block.nonce = data['nonce']
        block.hash = data['hash']
        
        # Validar bloque
        if block.hash == block.calculate_hash():
            # Aquí deberías validar que el bloque es el siguiente válido
            # Por ahora solo lo aceptamos si es válido
            
            if p2p_node:
                p2p_node.blocks_received += 1
            
            return response_success({
                'block_received': True,
                'block_index': block.index
            }, "Block received")
        else:
            return response_error("Invalid block hash")
            
    except Exception as e:
        return response_error(str(e))

@app.route('/api/network/discover', methods=['POST'])
def discover_peers():
    """Descubre peers a través de nodos semilla"""
    init_blockchain()
    
    if not p2p_node:
        return response_error("P2P node not initialized")
    
    data = request.get_json()
    if not data or 'seed_nodes' not in data:
        return response_error("Seed nodes required (array of 'host:port')")
    
    seed_nodes = []
    for seed in data['seed_nodes']:
        host, port = seed.split(':')
        seed_nodes.append((host, int(port)))
    
    discovered = p2p_node.discover_peers(seed_nodes)
    
    return response_success({
        'discovered': discovered,
        'total_peers': len(p2p_node.peers)
    }, f"Discovered {discovered} new peers")

# ==================== ENDPOINTS DE MINING POOL ====================

@app.route('/api/pool/info')
def pool_info():
    """Información del pool de minería"""
    init_blockchain()
    
    if not mining_pool:
        return response_error("Mining pool not initialized")
    
    return response_success(mining_pool.get_stats())

@app.route('/api/pool/miners')
def pool_miners():
    """Lista de mineros en el pool"""
    init_blockchain()
    
    if not mining_pool:
        return response_error("Mining pool not initialized")
    
    miners = mining_pool.get_all_miners()
    
    return response_success({
        'count': len(miners),
        'miners': miners
    })

@app.route('/api/pool/leaderboard')
def pool_leaderboard():
    """Ranking de mineros"""
    init_blockchain()
    
    if not mining_pool:
        return response_error("Mining pool not initialized")
    
    limit = request.args.get('limit', 10, type=int)
    leaderboard = mining_pool.get_leaderboard(limit)
    
    return response_success({
        'count': len(leaderboard),
        'leaderboard': leaderboard
    })

@app.route('/api/pool/miner/<miner_id>')
def pool_miner_stats(miner_id):
    """Estadísticas de un minero específico"""
    init_blockchain()
    
    if not mining_pool:
        return response_error("Mining pool not initialized")
    
    stats = mining_pool.get_miner_stats(miner_id)
    
    if not stats:
        return response_error(f"Miner {miner_id} not found", 404)
    
    return response_success(stats)

@app.route('/api/pool/join', methods=['POST'])
def pool_join():
    """Unirse al pool"""
    init_blockchain()
    
    if not mining_pool:
        return response_error("Mining pool not initialized")
    
    data = request.get_json()
    if not data or 'miner_id' not in data or 'address' not in data:
        return response_error("miner_id and address required")
    
    success, msg = mining_pool.add_miner(data['miner_id'], data['address'])
    
    if success:
        return response_success({
            'miner_id': data['miner_id'],
            'pool_name': mining_pool.pool_name,
            'pool_fee': mining_pool.pool_fee
        }, msg)
    else:
        return response_error(msg)

@app.route('/api/pool/leave', methods=['POST'])
def pool_leave():
    """Salir del pool"""
    init_blockchain()
    
    if not mining_pool:
        return response_error("Mining pool not initialized")
    
    data = request.get_json()
    if not data or 'miner_id' not in data:
        return response_error("miner_id required")
    
    success, msg = mining_pool.remove_miner(data['miner_id'])
    
    if success:
        return response_success({
            'miner_id': data['miner_id']
        }, msg)
    else:
        return response_error(msg)

@app.route('/api/pool/mine', methods=['POST'])
def pool_mine():
    """Minar bloque colaborativamente"""
    init_blockchain()
    
    if not mining_pool:
        return response_error("Mining pool not initialized")
    
    if len(mining_pool.miners) == 0:
        return response_error("No miners in pool")
    
    # Minar bloque
    success, msg, distribution = mining_pool.mine_block()
    
    if success:
        return response_success({
            'block_index': len(blockchain.chain) - 1,
            'distribution': distribution,
            'pool_stats': mining_pool.get_stats()
        }, msg)
    else:
        return response_error(msg)

@app.route('/api/pool/submit_share', methods=['POST'])
def pool_submit_share():
    """Enviar share al pool"""
    init_blockchain()
    
    if not mining_pool:
        return response_error("Mining pool not initialized")
    
    data = request.get_json()
    required = ['miner_id', 'nonce', 'block_hash']
    
    for field in required:
        if field not in data:
            return response_error(f"Field '{field}' required")
    
    success, msg = mining_pool.submit_share(
        data['miner_id'],
        data['nonce'],
        data['block_hash']
    )
    
    if success:
        miner_stats = mining_pool.get_miner_stats(data['miner_id'])
        return response_success({
            'miner_stats': miner_stats,
            'pool_stats': mining_pool.get_stats()
        }, msg)
    else:
        return response_error(msg)

# ==================== ENDPOINTS DE HD WALLET ====================

@app.route('/api/hdwallet/create', methods=['POST'])
def hdwallet_create():
    """Crear nueva HD Wallet"""
    data = request.get_json() or {}
    name = data.get('name', 'HDWallet')
    
    try:
        wallet = HDWallet(name=name)
        wallet.save()
        
        # Derivar primera dirección
        first_address = wallet.get_next_address()
        
        return response_success({
            'name': wallet.name,
            'mnemonic': wallet.mnemonic,
            'first_address': first_address,
            'addresses_generated': 1,
            'warning': '⚠️ SAVE YOUR MNEMONIC! It\'s the only way to recover your wallet.'
        }, "HD Wallet created successfully")
    except Exception as e:
        return response_error(f"Error creating HD wallet: {str(e)}")

@app.route('/api/hdwallet/restore', methods=['POST'])
def hdwallet_restore():
    """Restaurar HD Wallet desde mnemonic"""
    data = request.get_json()
    
    if not data or 'mnemonic' not in data:
        return response_error("mnemonic required")
    
    name = data.get('name', 'RestoredHDWallet')
    
    try:
        wallet = HDWallet.from_mnemonic(data['mnemonic'], name=name)
        wallet.save()
        
        # Derivar primera dirección
        first_address = wallet.get_next_address()
        
        return response_success({
            'name': wallet.name,
            'first_address': first_address,
            'addresses_generated': 1
        }, "HD Wallet restored successfully")
    except Exception as e:
        return response_error(f"Error restoring HD wallet: {str(e)}")

@app.route('/api/hdwallet/<filename>')
def hdwallet_load(filename):
    """Cargar HD Wallet existente"""
    try:
        if not filename.endswith('.json'):
            filename += '.json'
        
        wallet = HDWallet.load(filename)
        
        return response_success({
            'name': wallet.name,
            'current_index': wallet.current_index,
            'addresses_count': len(wallet.derived_keys),
            'mnemonic_words': len(wallet.get_mnemonic_words())
        })
    except FileNotFoundError:
        return response_error("HD Wallet not found", 404)
    except Exception as e:
        return response_error(f"Error loading HD wallet: {str(e)}")

@app.route('/api/hdwallet/<filename>/addresses')
def hdwallet_addresses(filename):
    """Listar direcciones de HD Wallet"""
    try:
        if not filename.endswith('.json'):
            filename += '.json'
        
        wallet = HDWallet.load(filename)
        
        # Parámetros de paginación
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Generar más direcciones si es necesario
        needed = offset + limit
        while wallet.current_index < needed:
            wallet.get_next_address()
        
        addresses = wallet.get_all_addresses()
        paginated = addresses[offset:offset + limit]
        
        return response_success({
            'addresses': paginated,
            'total': len(addresses),
            'limit': limit,
            'offset': offset
        })
    except FileNotFoundError:
        return response_error("HD Wallet not found", 404)
    except Exception as e:
        return response_error(f"Error loading addresses: {str(e)}")

@app.route('/api/hdwallet/<filename>/derive', methods=['POST'])
def hdwallet_derive(filename):
    """Derivar nueva dirección"""
    try:
        if not filename.endswith('.json'):
            filename += '.json'
        
        wallet = HDWallet.load(filename)
        
        data = request.get_json() or {}
        count = data.get('count', 1)
        
        new_addresses = []
        for _ in range(count):
            addr = wallet.get_next_address()
            new_addresses.append({
                'index': wallet.current_index - 1,
                'address': addr
            })
        
        # Guardar cambios
        wallet.save(filename)
        
        return response_success({
            'new_addresses': new_addresses,
            'total_addresses': wallet.current_index
        }, f"{count} address(es) derived")
    except FileNotFoundError:
        return response_error("HD Wallet not found", 404)
    except Exception as e:
        return response_error(f"Error deriving address: {str(e)}")

@app.route('/api/hdwallet/<filename>/balance')
def hdwallet_balance(filename):
    """Ver balance total de todas las direcciones"""
    init_blockchain()
    
    try:
        if not filename.endswith('.json'):
            filename += '.json'
        
        wallet = HDWallet.load(filename)
        addresses = wallet.get_all_addresses()
        
        total_balance = 0
        address_balances = []
        
        for addr_info in addresses:
            addr = addr_info['address']
            balance = blockchain.get_balance(addr)
            total_balance += balance
            
            if balance > 0:  # Solo mostrar direcciones con balance
                address_balances.append({
                    'index': addr_info['index'],
                    'address': addr,
                    'balance': balance
                })
        
        return response_success({
            'total_balance': total_balance,
            'addresses_with_balance': len(address_balances),
            'total_addresses': len(addresses),
            'balances': address_balances
        })
    except FileNotFoundError:
        return response_error("HD Wallet not found", 404)
    except Exception as e:
        return response_error(f"Error calculating balance: {str(e)}")

@app.route('/api/hdwallet/<filename>/export', methods=['POST'])
def hdwallet_export_mnemonic(filename):
    """Exportar mnemonic (requiere confirmación)"""
    try:
        if not filename.endswith('.json'):
            filename += '.json'
        
        data = request.get_json() or {}
        confirm = data.get('confirm', False)
        
        if not confirm:
            return response_error("Confirmation required. Set 'confirm': true")
        
        wallet = HDWallet.load(filename)
        
        return response_success({
            'mnemonic': wallet.mnemonic,
            'words': wallet.get_mnemonic_words(),
            'warning': '⚠️ NEVER share your mnemonic! Anyone with these words can access ALL your funds.'
        })
    except FileNotFoundError:
        return response_error("HD Wallet not found", 404)
    except Exception as e:
        return response_error(f"Error exporting mnemonic: {str(e)}")

@app.route('/api/hdwallet/<filename>/sign', methods=['POST'])
def hdwallet_sign(filename):
    """Firmar mensaje con dirección específica"""
    try:
        if not filename.endswith('.json'):
            filename += '.json'
        
        data = request.get_json()
        
        if not data or 'message' not in data or 'index' not in data:
            return response_error("message and index required")
        
        wallet = HDWallet.load(filename)
        
        signature = wallet.sign_message(data['message'], data['index'])
        address = wallet.get_address(data['index'])
        
        return response_success({
            'message': data['message'],
            'signature': signature,
            'address': address,
            'index': data['index']
        })
    except FileNotFoundError:
        return response_error("HD Wallet not found", 404)
    except Exception as e:
        return response_error(f"Error signing message: {str(e)}")


# ==================== ENDPOINTS DE QR CODES ====================

@app.route('/api/qr/address/<address>')
def qr_address(address):
    """Generar QR de dirección"""
    try:
        size = request.args.get('size', 10, type=int)
        border = request.args.get('border', 2, type=int)
        
        qr_image = QRGenerator.generate_address_qr(address, size, border)
        
        return response_success({
            'address': address,
            'qr_image': qr_image,
            'format': 'base64'
        })
    except Exception as e:
        return response_error(f"Error generating QR: {str(e)}")

@app.route('/api/qr/payment', methods=['POST'])
def qr_payment():
    """Generar QR de pago"""
    data = request.get_json()
    
    if not data or 'address' not in data:
        return response_error("address required")
    
    try:
        size = data.get('size', 10)
        border = data.get('border', 2)
        
        qr_image = QRGenerator.generate_payment_qr(
            address=data['address'],
            amount=data.get('amount'),
            memo=data.get('memo'),
            size=size,
            border=border
        )
        
        # Generar URI
        uri = f"colcript:{data['address']}"
        params = []
        if data.get('amount'):
            params.append(f"amount={data['amount']}")
        if data.get('memo'):
            params.append(f"memo={data['memo']}")
        if params:
            uri += "?" + "&".join(params)
        
        return response_success({
            'address': data['address'],
            'amount': data.get('amount'),
            'memo': data.get('memo'),
            'uri': uri,
            'qr_image': qr_image,
            'format': 'base64'
        })
    except Exception as e:
        return response_error(f"Error generating payment QR: {str(e)}")

@app.route('/api/qr/parse', methods=['POST'])
def qr_parse():
    """Parsear URI de pago"""
    data = request.get_json()
    
    if not data or 'uri' not in data:
        return response_error("uri required")
    
    try:
        parsed = QRGenerator.parse_payment_uri(data['uri'])
        
        return response_success({
            'address': parsed['address'],
            'amount': parsed['amount'],
            'memo': parsed['memo']
        })
    except Exception as e:
        return response_error(f"Error parsing URI: {str(e)}")

# ==================== ENDPOINTS DE NOTIFICACIONES ====================

@app.route('/api/events/history')
def events_history():
    """Historial de eventos"""
    event_type = request.args.get('type')
    limit = request.args.get('limit', 50, type=int)
    
    history = event_system.get_history(event_type, limit)
    
    return response_success({
        'count': len(history),
        'events': history
    })

@app.route('/api/events/types')
def events_types():
    """Lista de tipos de eventos disponibles"""
    types = [
        {'type': EventType.TRANSACTION_CREATED, 'description': 'Nueva transacción creada'},
        {'type': EventType.TRANSACTION_CONFIRMED, 'description': 'Transacción confirmada en bloque'},
        {'type': EventType.BLOCK_MINED, 'description': 'Bloque minado'},
        {'type': EventType.BLOCK_ADDED, 'description': 'Bloque agregado a la cadena'},
        {'type': EventType.WALLET_CREATED, 'description': 'Wallet creada'},
        {'type': EventType.WALLET_LOADED, 'description': 'Wallet cargada'},
        {'type': EventType.FAUCET_CLAIMED, 'description': 'Faucet reclamado'},
        {'type': EventType.CONTRACT_CREATED, 'description': 'Contrato creado'},
        {'type': EventType.CONTRACT_EXECUTED, 'description': 'Contrato ejecutado'},
        {'type': EventType.PEER_CONNECTED, 'description': 'Peer conectado'},
        {'type': EventType.PEER_DISCONNECTED, 'description': 'Peer desconectado'},
        {'type': EventType.POOL_BLOCK_MINED, 'description': 'Bloque minado por pool'},
        {'type': EventType.POOL_MINER_JOINED, 'description': 'Minero se unió al pool'},
    ]
    
    return response_success({
        'count': len(types),
        'types': types
    })

@app.route('/api/webhooks', methods=['GET'])
def webhooks_list():
    """Lista de webhooks registrados"""
    webhooks = event_system.get_webhooks()
    
    return response_success({
        'count': len(webhooks),
        'webhooks': webhooks
    })

@app.route('/api/webhooks/add', methods=['POST'])
def webhooks_add():
    """Agregar webhook"""
    data = request.get_json()
    
    if not data or 'event_type' not in data or 'url' not in data:
        return response_error("event_type and url required")
    
    webhook_id = event_system.add_webhook(data['event_type'], data['url'])
    
    return response_success({
        'webhook_id': webhook_id,
        'event_type': data['event_type'],
        'url': data['url']
    }, "Webhook registered successfully")

@app.route('/api/webhooks/<webhook_id>/remove', methods=['POST'])
def webhooks_remove(webhook_id):
    """Eliminar webhook"""
    event_system.remove_webhook(webhook_id)
    
    return response_success({
        'webhook_id': webhook_id
    }, "Webhook removed")

@app.route('/api/webhooks/<webhook_id>/enable', methods=['POST'])
def webhooks_enable(webhook_id):
    """Habilitar webhook"""
    event_system.enable_webhook(webhook_id)
    
    return response_success({
        'webhook_id': webhook_id,
        'enabled': True
    }, "Webhook enabled")

@app.route('/api/webhooks/<webhook_id>/disable', methods=['POST'])
def webhooks_disable(webhook_id):
    """Deshabilitar webhook"""
    event_system.disable_webhook(webhook_id)
    
    return response_success({
        'webhook_id': webhook_id,
        'enabled': False
    }, "Webhook disabled")

@app.route('/api/notifications/test', methods=['POST'])
def notifications_test():
    """Emitir evento de prueba"""
    data = request.get_json() or {}
    event_type = data.get('event_type', EventType.TRANSACTION_CREATED)
    test_data = data.get('data', {'test': True, 'message': 'Test notification'})
    
    event_system.emit(event_type, test_data)
    
    return response_success({
        'event_type': event_type,
        'data': test_data
    }, "Test event emitted")

# ==================== RATE LIMIT INFO ====================

@app.route('/api/limits/status')
@limiter.exempt  # No aplicar límite a este endpoint
def limits_status():
    """Ver estado de rate limits"""
    try:
        # Información sobre límites configurados
        return response_success({
            'global_limits': {
                'daily': '200 requests per day',
                'hourly': '50 requests per hour'
            },
            'endpoint_limits': {
                '/api/transaction/send': '10 per minute',
                '/api/mining/mine': '5 per minute',
                '/api/faucet/claim': '1 per hour'
            },
            'your_ip': get_remote_address(),
            'note': 'Limits are per IP address'
        })
    except Exception as e:
        return response_error(f"Error: {str(e)}")

# ==================== ENDPOINTS DE BACKUP ====================

@app.route('/api/backup/create', methods=['POST'])
@limiter.limit("5 per hour")  # Límite: 5 backups manuales por hora
def create_backup():
    """
    Crear backup manual de blockchain
    
    POR QUÉ: Backup antes de operaciones críticas
    """
    try:
        data = request.get_json() or {}
        tag = data.get('tag', 'manual')
        
        # Ruta del archivo de blockchain
        blockchain_file = os.path.join(project_root, 'data', 'colcript_main.json')
        
        if not os.path.exists(blockchain_file):
            return response_error("Blockchain file not found")
        
        # Crear backup
        backup_path = backup_system.create_backup(blockchain_file, tag=tag)
        
        if backup_path:
            return response_success({
                'backup_created': os.path.basename(backup_path),
                'tag': tag,
                'size_mb': round(os.path.getsize(backup_path) / (1024 * 1024), 2)
            }, "Backup created successfully")
        else:
            return response_error("Failed to create backup")
    
    except Exception as e:
        return response_error(f"Error: {str(e)}")

@app.route('/api/backup/list')
def list_backups():
    """
    Listar backups disponibles
    
    POR QUÉ: Ver puntos de restauración
    """
    try:
        pattern = request.args.get('pattern', 'colcript_main')
        backups = backup_system.list_backups(pattern)
        
        return response_success({
            'count': len(backups),
            'backups': backups
        })
    
    except Exception as e:
        return response_error(f"Error: {str(e)}")

@app.route('/api/backup/restore', methods=['POST'])
@limiter.limit("3 per hour")  # Muy restrictivo - operación crítica
def restore_backup():
    """
    Restaurar blockchain desde backup
    
    POR QUÉ: Recuperación ante fallos
    ADVERTENCIA: Operación crítica - crea backup del estado actual
    """
    try:
        data = request.get_json()
        
        if not data or 'backup_file' not in data:
            return response_error("backup_file required")
        
        backup_file = data['backup_file']
        blockchain_file = os.path.join(project_root, 'data', 'colcript_main.json')
        
        # Restaurar
        success = backup_system.restore_backup(backup_file, blockchain_file)
        
        if success:
            # Recargar blockchain
            global blockchain
            blockchain = storage.load_blockchain("colcript_main.json")
            
            return response_success({
                'restored_from': backup_file,
                'blocks': len(blockchain.chain) if blockchain else 0
            }, "Blockchain restored successfully")
        else:
            return response_error("Failed to restore backup")
    
    except Exception as e:
        return response_error(f"Error: {str(e)}")

@app.route('/api/backup/stats')
def backup_stats():
    """
    Estadísticas de backups
    
    POR QUÉ: Monitorear espacio y cantidad de backups
    """
    try:
        stats = backup_system.get_backup_stats()
        
        return response_success(stats)
    
    except Exception as e:
        return response_error(f"Error: {str(e)}")

# ==================== ENDPOINTS DE MONITOREO ====================

@app.route('/api/metrics/system')
def metrics_system():
    """
    Métricas del sistema
    
    POR QUÉ: Monitorear CPU, RAM, disco
    """
    try:
        system_metrics = metrics.get_system_metrics()
        return response_success(system_metrics)
    except Exception as e:
        return response_error(f"Error: {str(e)}")

@app.route('/api/metrics/api')
def metrics_api():
    """
    Métricas de la API
    
    POR QUÉ: Ver uso de endpoints y performance
    """
    try:
        api_metrics = metrics.get_api_metrics()
        return response_success(api_metrics)
    except Exception as e:
        return response_error(f"Error: {str(e)}")

@app.route('/api/health')
def health_check():
    """
    Health check del servidor
    
    POR QUÉ: Verificar que el servidor está funcionando
    """
    try:
        health = metrics.get_health_status()
        
        # Retornar código HTTP según estado
        status_code = 200 if health['status'] == 'healthy' else (503 if health['status'] == 'unhealthy' else 200)
        
        return jsonify({
            'success': True,
            'data': health
        }), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 503

@app.route('/api/metrics/reset', methods=['POST'])
@limiter.limit("1 per hour")  # Solo admin debería hacer esto
def metrics_reset():
    """
    Reiniciar métricas
    
    POR QUÉ: Limpiar estadísticas periódicamente
    """
    try:
        metrics.reset_metrics()
        return response_success({'message': 'Metrics reset successfully'})
    except Exception as e:
        return response_error(f"Error: {str(e)}")


# ==================== INICIO DEL SERVIDOR ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print(f"🌐 ColCript API Server v{config.VERSION}")
    print("="*60)
    print("\n📡 Starting server...")
    print(f"🔗 API URL: http://localhost:5000")
    print(f"📖 Documentation: http://localhost:5000/api/docs")
    print("\n⚠️  Press CTRL+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
