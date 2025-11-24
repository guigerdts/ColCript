# 🪙 ColCript (CLC)

[![Tests](https://github.com/guigerdts/ColCript/actions/workflows/tests.yml/badge.svg)](https://github.com/guigerdts/ColCript/actions/workflows/tests.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


**Una criptomoneda blockchain completa construida desde cero en Python**
[![Versión](https://img.shields.io/badge/versión-1.3.0-blue.svg)](https://github.com/tu-usuario/colcript)
[![Python](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org/)
[![Licencia](https://img.shields.io/badge/licencia-MIT-orange.svg)](LICENSE)

---

## 📖 Descripción

ColCript es una criptomoneda funcional con tecnología blockchain, construida completamente en Python. Implementa conceptos fundamentales de criptomonedas como Bitcoin, incluyendo Proof of Work, transacciones firmadas digitalmente, sistema de fees, y más.

## ✨ Características Principales

### 🔗 Blockchain
- **Proof of Work (PoW)** con SHA-256
- **Ajuste automático de dificultad** cada 10 bloques
- **Validación completa** de cadena y bloques
- **Persistencia** en JSON con auto-guardado
- **Explorador de bloques** integrado

### 💰 Sistema de Transacciones
- **Firmadas digitalmente** con ECDSA (secp256k1)
- **Sistema de fees** dinámico
- **Priorización** por fee
- **Pool de transacciones** pendientes
- **Historial completo** por wallet

### 👛 Wallets
- **Generación segura** de claves públicas/privadas
- **Múltiples wallets** simultáneas
- **Balance en tiempo real**
- **Exportar/importar** wallets
- **Historial** de transacciones

### 📜 Smart Contracts
- **Script Engine** stack-based (inspirado en Bitcoin Script)
- **30+ opcodes** implementados
- **3 tipos de contratos**:
  - ⏰ **Timelock**: Desbloqueo por altura de bloque
  - ✍️ **Multisig**: Firmas múltiples (2-of-3, etc)
  - 🤝 **Escrow**: Arbitraje de terceros
- **Sistema de Gas** para ejecución
- **Persistencia** de contratos

### 🌐 Red P2P
- **Nodos independientes** y descentralizados
- **Descubrimiento automático** de peers
- **Sincronización** de blockchain
- **Propagación** de transacciones y bloques
- **Consenso** por cadena más larga
- **Estadísticas** de red en tiempo real

### 🎁 Faucet
- **5 CLC gratis** cada 24 horas
- **Control anti-abuso** por dirección
- **Cooldown** automático
- Integrado en CLI, API y Web

### 🔧 Interfaces Completas

#### 1. CLI (Línea de Comandos)
- 19 opciones de menú
- Gestión completa de blockchain y wallets
- Smart Contracts y Red P2P
- Explorador y estadísticas

#### 2. API REST
- **50+ endpoints** funcionales
- Documentación integrada en `/api/docs`
- CORS habilitado
- Respuestas JSON estandarizadas

#### 3. Interfaz Web
- **8 páginas** interactivas
- Dashboard con gráficas
- Gestión visual de wallets
- Minería en tiempo real
- Explorador de bloques
- Smart Contracts UI
- Red P2P management

### 📊 Advanced Wallet (v1.3.0)
- **Estadísticas detalladas** de wallet (balance, transacciones, fees, net flow)
- **Contact Management** - Gestión de contactos con notas
- **Address Labels** - Etiquetado de direcciones para organización
- **Transaction History** - Análisis completo del historial
- **Data Export** - Exportación a JSON y CSV

### 🔍 Advanced Explorer (v1.3.0)
- **Real-Time Network Status** - Estado de la red en vivo
- **Top Holders Analysis** - Ranking de wallets
- **Miner Ranking** - Top mineros por bloques
- **Network Activity Charts** - Visualización de actividad
- **Transaction Search** - Búsqueda avanzada


---

## 📦 Instalación

### Requisitos
- Python 3.12+
- pip
- Termux (para Android) o cualquier sistema Unix/Linux

### Paso 1: Clonar o descargar

(bash)
cd ~/
mkdir ColCript
cd ColCript
Paso 2: Instalar dependencias
pip install ecdsa requests flask flask-cors
Paso 3: Configuración inicial
El archivo config.json se genera automáticamente con valores por defecto.
🚀 Uso Rápido
1. CLI (Interfaz de Línea de Comandos)
python colcript.py
Flujo básico:
Crear blockchain (opción 1)
Crear wallet (opción 4)
Minar bloques (opción 12)
Enviar CLC (opción 11)
2. API REST
python api/server.py
El servidor inicia en http://localhost:5000
Endpoints principales:
GET /api/info - Información de la blockchain
GET /api/blockchain - Ver cadena completa
POST /api/transaction - Crear transacción
POST /api/mine - Minar bloque
GET /api/docs - Documentación completa
3. Interfaz Web
Con el servidor API corriendo, abre en tu navegador:
http://localhost:5000
📚 Documentación Completa
Arquitectura - Diseño técnico del sistema
API Reference - Documentación de endpoints
Smart Contracts - Guía de contratos
Red P2P - Sistema de red descentralizada
Instalación - Guía detallada de instalación
Uso - Guía de uso completa
🎯 Ejemplos
Crear y enviar una transacción (CLI)
# 1. Iniciar ColCript
python colcript.py

# 2. Crear wallet
Opción 4

# 3. Usar faucet para obtener CLC
Opción 10

# 4. Enviar CLC
Opción 11
Crear un contrato Timelock (API)
curl -X POST http://localhost:5000/api/contracts/timelock/create \
  -H "Content-Type: application/json" \
  -d '{
    "creator": "tu_direccion",
    "unlock_block": 100,
    "amount": 50,
    "recipient": "direccion_destinatario"
  }'
Conectar nodos P2P
# Nodo 1 (puerto 5000)
python api/server.py

# Nodo 2 (puerto 5001)
# Agregar peer al nodo 1
curl -X POST http://localhost:5000/api/network/peer/add \
  -H "Content-Type: application/json" \
  -d '{"host": "127.0.0.1", "port": 5001}'
🏗️ Arquitectura
ColCript/
├── blockchain/          # Core blockchain
│   ├── blockchain.py    # Clase principal
│   ├── block.py         # Bloques
│   ├── transaction.py   # Transacciones
│   ├── wallet.py        # Wallets
│   ├── difficulty.py    # Ajuste de dificultad
│   └── storage.py       # Persistencia
├── contracts/           # Smart Contracts
│   ├── opcodes.py       # Script Engine
│   └── smart_contract.py # Contratos
├── network/             # Red P2P
│   └── node.py          # Nodos
├── api/                 # API REST
│   └── server.py        # Servidor Flask
├── web/                 # Interfaz Web
│   ├── index.html
│   ├── css/
│   └── js/
├── utils/               # Utilidades
│   ├── faucet.py
│   └── helpers.py
├── data/                # Datos persistentes
├── config.json          # Configuración
└── colcript.py          # CLI principal
🔬 Comparación con Otras Criptomonedas
Característica
Bitcoin
Ethereum
Cardano
ColCript
Blockchain PoW
✅
❌
❌
✅
Smart Contracts
❌
✅
✅
✅
API REST
❌
✅
✅
✅
Interfaz Web
❌
❌
❌
✅
CLI Completa
✅
✅
✅
✅
Faucet Integrado
❌
❌
❌
✅
Red P2P
✅
✅
✅
✅
Todo en Python
❌
❌
❌
✅
📊 Estadísticas del Proyecto
~9,500 líneas de código
30+ archivos Python/JS/CSS/HTML
50+ endpoints API
30+ opcodes de contratos
85+ funcionalidades implementadas
3 interfaces completas (CLI, API, Web)
🤝 Contribuir
Este es un proyecto educativo. Si encuentras bugs o quieres agregar características:
Fork el proyecto
Crea una rama (git checkout -b feature/NuevaCaracteristica)
Commit tus cambios (git commit -m 'Agregar nueva característica')
Push a la rama (git push origin feature/NuevaCaracteristica)
Abre un Pull Request
📝 Licencia
Este proyecto está bajo la Licencia MIT. Ver archivo LICENSE para más detalles.
👨‍💻 Autor
Guillo - Proyecto educativo de criptomoneda completa
🙏 Agradecimientos
Inspirado en Bitcoin, Ethereum y el whitepaper de Satoshi Nakamoto
Comunidad de Python y blockchain
Stack Overflow y la comunidad open source
🔗 Enlaces Útiles
Bitcoin Whitepaper
Ethereum Documentation
ECDSA Python
Flask Documentation
⭐ Si te gustó este proyecto, dale una estrella!
