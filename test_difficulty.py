#!/usr/bin/env python3
# test_difficulty.py - Prueba del ajuste automático de dificultad

import os
import sys

project_root = '/data/data/com.termux/files/home/ColCript'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet
import config

print("\n🧪 PRUEBA DE AJUSTE AUTOMÁTICO DE DIFICULTAD\n")

# Configurar para pruebas rápidas
config.DIFFICULTY_ADJUSTMENT_INTERVAL = 5
config.TARGET_BLOCK_TIME = 10
config.DIFFICULTY_ADJUSTMENT_ENABLED = True

print("Configuración de prueba:")
print(f"  Intervalo de ajuste: cada {config.DIFFICULTY_ADJUSTMENT_INTERVAL} bloques")
print(f"  Tiempo objetivo: {config.TARGET_BLOCK_TIME}s por bloque")
print(f"  Dificultad inicial: 2\n")

# Crear blockchain
bc = Blockchain(auto_save=False)
bc.difficulty = 2

# Crear wallet
wallet = Wallet("Test Miner")

print("Minando bloques...\n")

for i in range(15):
    print(f"Bloque {i+1}:")
    bc.mine_pending_transactions(wallet.get_address())
    print()

print("✅ Prueba completada\n")
