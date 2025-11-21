#!/usr/bin/env python3
# test_api.py - Script para probar la API de ColCript

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Imprime respuesta formateada"""
    print(f"\n{'='*60}")
    print(f"📡 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print()

def test_api():
    """Prueba completa de la API"""
    print("\n🧪 PROBANDO API DE COLCRIPT\n")
    
    # 1. Info de la API
    print("1️⃣ Obteniendo información de la API...")
    r = requests.get(f"{BASE_URL}/")
    print_response("GET /", r)
    
    # 2. Info de ColCript
    print("2️⃣ Obteniendo información de ColCript...")
    r = requests.get(f"{BASE_URL}/api/info")
    print_response("GET /api/info", r)
    
    # 3. Crear blockchain
    print("3️⃣ Creando blockchain...")
    r = requests.post(f"{BASE_URL}/api/blockchain/create", 
                      json={"filename": "api_test.json"})
    print_response("POST /api/blockchain/create", r)
    
    # 4. Info de blockchain
    print("4️⃣ Información de blockchain...")
    r = requests.get(f"{BASE_URL}/api/blockchain/info")
    print_response("GET /api/blockchain/info", r)
    
    # 5. Crear wallet
    print("5️⃣ Creando wallet...")
    r = requests.post(f"{BASE_URL}/api/wallet/create",
                      json={"name": "API Test Wallet"})
    print_response("POST /api/wallet/create", r)
    
    if r.status_code == 200:
        wallet_address = r.json()['data']['address']
        print(f"✅ Wallet creada: {wallet_address[:30]}...")
    
    # 6. Ver balance
    print("6️⃣ Ver balance...")
    r = requests.get(f"{BASE_URL}/api/wallet/balance")
    print_response("GET /api/wallet/balance", r)
    
    # 7. Minar bloque
    print("7️⃣ Minando bloque...")
    r = requests.post(f"{BASE_URL}/api/mining/mine")
    print_response("POST /api/mining/mine", r)
    
    # 8. Ver balance después de minar
    print("8️⃣ Ver balance después de minar...")
    r = requests.get(f"{BASE_URL}/api/wallet/balance")
    print_response("GET /api/wallet/balance", r)
    
    # 9. Ver blockchain
    print("9️⃣ Ver blockchain...")
    r = requests.get(f"{BASE_URL}/api/blockchain")
    print_response("GET /api/blockchain", r)
    
    # 10. Ver último bloque
    print("🔟 Ver último bloque...")
    r = requests.get(f"{BASE_URL}/api/explorer/block/1")
    print_response("GET /api/explorer/block/1", r)
    
    # 11. Dashboard de estadísticas
    print("1️⃣1️⃣ Dashboard de estadísticas...")
    r = requests.get(f"{BASE_URL}/api/statistics/dashboard")
    print_response("GET /api/statistics/dashboard", r)
    
    # 12. Info del faucet
    print("1️⃣2️⃣ Información del faucet...")
    r = requests.get(f"{BASE_URL}/api/faucet/info")
    print_response("GET /api/faucet/info", r)
    
    print("\n✅ PRUEBAS COMPLETADAS\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor API")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   python api/server.py")
    except Exception as e:
        print(f"❌ Error: {e}")
