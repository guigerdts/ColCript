#!/usr/bin/env python3
# fix_paths.py - Arregla paths hardcoded de Termux

import os
import re

# Archivos a arreglar
files = [
    './blockchain/transaction.py',
    './blockchain/block.py',
    './blockchain/blockchain.py',
    './blockchain/block_explorer.py',
    './blockchain/difficulty.py',
    './blockchain/storage.py',
    './wallet/wallet.py',
    './wallet/transaction_history.py',
    './wallet/faucet.py',
    './network/node.py',
    './utils/statistics.py',
    './colcript.py',
    './api/server.py',
    './test_difficulty.py',
    './contracts/smart_contract.py',
    './mining/pool.py'
]

old_pattern = "project_root = '/data/data/com.termux/files/home/ColCript'"
new_code = """# Obtener ruta absoluta del proyecto de forma dinámica
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))"""

# Para archivos en la raíz (solo un nivel arriba)
root_files_pattern = ['./colcript.py', './test_difficulty.py']

print("🔧 Arreglando paths hardcoded...\n")

for filepath in files:
    if not os.path.exists(filepath):
        print(f"⚠️  Archivo no encontrado: {filepath}")
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    if old_pattern in content:
        # Archivos en raíz necesitan solo un dirname
        if filepath in root_files_pattern:
            replacement = "project_root = os.path.dirname(os.path.abspath(__file__))"
        else:
            replacement = "project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))"
        
        content = content.replace(old_pattern, replacement)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✅ {filepath}")
    else:
        print(f"⏭️  {filepath} (ya arreglado o sin path)")

print("\n✅ Todos los paths arreglados!\n")
print("🧪 Probando que funcione:")
print("   python -c 'from blockchain.blockchain import Blockchain; print(\"OK\")'")
