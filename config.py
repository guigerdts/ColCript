# config.py - Configuración de ColCript

# Información de la criptomoneda
COIN_NAME = "ColCript"
COIN_SYMBOL = "CLC"
TOTAL_SUPPLY = 21000000  # 21 millones de monedas totales

# Configuración del blockchain
MINING_DIFFICULTY = 4  # Número de ceros iniciales en el hash
MINING_REWARD = 50  # Recompensa por minar un bloque
BLOCK_TIME = 60  # Tiempo objetivo entre bloques (segundos)

# Configuración de red
DEFAULT_PORT = 5000
NODES = []  # Lista de nodos conocidos

# Versión
VERSION = "1.0.0"

# Configuración de fees (comisiones)
MIN_TRANSACTION_FEE = 0.1  # Fee mínimo por transacción (CLC)
DEFAULT_TRANSACTION_FEE = 0.5  # Fee recomendado (CLC)
MAX_TRANSACTION_FEE = 10  # Fee máximo permitido (CLC)

# Configuración del mempool (pool de transacciones)
MEMPOOL_MAX_SIZE = 100  # Máximo de transacciones pendientes
PRIORITIZE_BY_FEE = True  # Ordenar por fee (mayor fee primero)

# Configuración del Faucet (grifo de CLC gratis)
FAUCET_ENABLED = True  # Activar/desactivar faucet
FAUCET_AMOUNT = 5  # Cantidad de CLC que regala
FAUCET_COOLDOWN_HOURS = 24  # Horas entre reclamos
FAUCET_MAX_BALANCE = 50  # Balance máximo para poder reclamar
FAUCET_WALLET_NAME = "ColCript Faucet"  # Nombre de la wallet del faucet

# Configuración de ajuste automático de dificultad
DIFFICULTY_ADJUSTMENT_ENABLED = True  # Activar/desactivar ajuste automático
DIFFICULTY_ADJUSTMENT_INTERVAL = 10  # Ajustar cada N bloques
TARGET_BLOCK_TIME = 60  # Tiempo objetivo entre bloques (segundos)
MIN_DIFFICULTY = 2  # Dificultad mínima permitida
MAX_DIFFICULTY = 8  # Dificultad máxima permitida


print(f"✅ Configuración de {COIN_NAME} ({COIN_SYMBOL}) cargada")
