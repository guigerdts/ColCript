# 🌐 ColCript API Documentation

API REST completa para interactuar con ColCript.

## 📡 Base URL
http://localhost:5000
## 🔑 Autenticación

Actualmente no requiere autenticación (v1.0.0).

## 📋 Respuestas

Todas las respuestas siguen este formato:

**Éxito:**
```json
{
  "success": true,
  "message": "Success",
  "data": { ... }
}
Error:
{
  "success": false,
  "error": "Error message"
}
🚀 Endpoints
[Ver documentación completa en /api/docs]
Ejemplo de flujo completo:
import requests

BASE = "http://localhost:5000"

# 1. Crear blockchain
r = requests.post(f"{BASE}/api/blockchain/create")

# 2. Crear wallet
r = requests.post(f"{BASE}/api/wallet/create", 
                 json={"name": "Mi Wallet"})

# 3. Minar
r = requests.post(f"{BASE}/api/mining/mine")

# 4. Ver balance
r = requests.get(f"{BASE}/api/wallet/balance")
print(r.json())  # {"data": {"balance": 50, ...}}
Para más ejemplos, ver test_api.py.
