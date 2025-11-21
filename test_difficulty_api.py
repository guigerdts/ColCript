#!/usr/bin/env python3
# test_difficulty_api.py - Prueba endpoints de dificultad

import requests
import json

BASE = "http://localhost:5000"

def print_json(title, data):
    print(f"\n{'='*60}")
    print(f"📡 {title}")
    print(f"{'='*60}")
    print(json.dumps(data, indent=2))

print("\n🧪 PROBANDO API DE DIFICULTAD\n")

try:
    # 1. Crear blockchain de prueba
    print("0️⃣ Creando blockchain de prueba...")
    r = requests.post(f"{BASE}/api/blockchain/create", 
                      json={"filename": "diff_test.json"})
    print_json("POST /api/blockchain/create", r.json())
    
    # 2. Crear wallet
    print("\n1️⃣ Creando wallet...")
    r = requests.post(f"{BASE}/api/wallet/create",
                      json={"name": "Difficulty Tester"})
    print_json("POST /api/wallet/create", r.json())
    
    # 3. Ver info de dificultad inicial
    print("\n2️⃣ Información de dificultad inicial...")
    r = requests.get(f"{BASE}/api/difficulty/info")
    print_json("GET /api/difficulty/info", r.json())
    
    # 4. Minar algunos bloques con dificultad inicial
    print("\n3️⃣ Minando 3 bloques con dificultad actual...")
    for i in range(3):
        r = requests.post(f"{BASE}/api/mining/mine")
        data = r.json()
        print(f"   Bloque {i+1}: {data['data']['mining_time']}s")
    
    # 5. Ver info de dificultad después de minar
    print("\n4️⃣ Información de dificultad después de minar...")
    r = requests.get(f"{BASE}/api/difficulty/info")
    print_json("GET /api/difficulty/info", r.json())
    
    # 6. Configurar dificultad manual
    print("\n5️⃣ Configurar dificultad manualmente a 3...")
    r = requests.post(f"{BASE}/api/difficulty/set", 
                      json={"difficulty": 3})
    print_json("POST /api/difficulty/set", r.json())
    
    # 7. Minar un bloque con nueva dificultad
    print("\n6️⃣ Minando bloque con nueva dificultad...")
    r = requests.post(f"{BASE}/api/mining/mine")
    data = r.json()
    print(f"   Tiempo de minado: {data['data']['mining_time']}s")
    print(f"   Nonce: {data['data']['block']['nonce']}")
    
    # 8. Configurar parámetros de ajuste automático
    print("\n7️⃣ Configurando parámetros de ajuste automático...")
    r = requests.post(f"{BASE}/api/difficulty/config",
                      json={"target_time": 30, "interval": 5})
    print_json("POST /api/difficulty/config", r.json())
    
    # 9. Deshabilitar ajuste automático
    print("\n8️⃣ Deshabilitando ajuste automático...")
    r = requests.post(f"{BASE}/api/difficulty/toggle",
                      json={"enabled": False})
    print_json("POST /api/difficulty/toggle", r.json())
    
    # 10. Habilitar ajuste automático
    print("\n9️⃣ Habilitando ajuste automático...")
    r = requests.post(f"{BASE}/api/difficulty/toggle",
                      json={"enabled": True})
    print_json("POST /api/difficulty/toggle", r.json())
    
    # 11. Ver info final
    print("\n🔟 Información final de dificultad...")
    r = requests.get(f"{BASE}/api/difficulty/info")
    print_json("GET /api/difficulty/info", r.json())
    
    # 12. Ver blockchain resultante
    print("\n1️⃣1️⃣ Información de blockchain resultante...")
    r = requests.get(f"{BASE}/api/blockchain/info")
    print_json("GET /api/blockchain/info", r.json())
    
    print("\n" + "="*60)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("="*60)
    print()

except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: No se puede conectar al servidor API")
    print("   Asegúrate de que el servidor esté corriendo:")
    print("   Terminal 1: python api/server.py\n")
except Exception as e:
    print(f"\n❌ ERROR: {e}\n")
