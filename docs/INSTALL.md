# 🔧 Guía de Instalación - ColCript

Guía completa para instalar y configurar ColCript en diferentes plataformas.

---

## 📋 Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación en Termux (Android)](#instalación-en-termux-android)
3. [Instalación en Linux](#instalación-en-linux)
4. [Instalación en macOS](#instalación-en-macos)
5. [Instalación en Windows](#instalación-en-windows)
6. [Verificación de Instalación](#verificación-de-instalación)
7. [Configuración Inicial](#configuración-inicial)
8. [Instalación de Múltiples Nodos](#instalación-de-múltiples-nodos)
9. [Actualización](#actualización)
10. [Desinstalación](#desinstalación)

---

## 💻 Requisitos del Sistema

### Mínimos

| Componente | Requisito |
|------------|-----------|
| **Python** | 3.12 o superior |
| **RAM** | 512 MB |
| **Almacenamiento** | 100 MB (más espacio para blockchain) |
| **Red** | Conexión a Internet (opcional para P2P) |

### Recomendados

| Componente | Requisito |
|------------|-----------|
| **Python** | 3.12+ |
| **RAM** | 2 GB+ |
| **Almacenamiento** | 1 GB+ |
| **Red** | Banda ancha estable |
| **CPU** | Multi-core para minería |

---

## 📱 Instalación en Termux (Android)

### Paso 1: Instalar Termux

1. Descargar desde [F-Droid](https://f-droid.org/packages/com.termux/)
2. Abrir Termux

### Paso 2: Actualizar Termux

(bash)
pkg update && pkg upgrade -y
Paso 3: Instalar Dependencias
# Instalar Python
pkg install python -y

# Instalar git (opcional)
pkg install git -y

# Verificar instalación
python --version
# Debería mostrar: Python 3.12.x
Paso 4: Instalar Librerías Python
pip install --upgrade pip
pip install ecdsa requests flask flask-cors
Paso 5: Descargar ColCript
Opción A: Clonar repositorio (si tienes git)
cd ~
git clone https://github.com/tuusuario/ColCript.git
cd ColCript
Opción B: Crear manualmente
cd ~
mkdir ColCript
cd ColCript

# Copiar todos los archivos del proyecto aquí
# (Usar editor de texto o transferir archivos)
Paso 6: Configurar Permisos
chmod +x colcript.py
chmod +x api/server.py
Paso 7: Verificar Instalación
python colcript.py
Deberías ver el menú principal de ColCript.
🐧 Instalación en Linux
Ubuntu/Debian
Paso 1: Actualizar Sistema
sudo apt update && sudo apt upgrade -y
Paso 2: Instalar Python
# Verificar si Python está instalado
python3 --version

# Si no está instalado o es versión antigua
sudo apt install python3.12 python3-pip -y
Paso 3: Instalar Dependencias
pip3 install ecdsa requests flask flask-cors
Paso 4: Descargar ColCript
cd ~
git clone https://github.com/tuusuario/ColCript.git
cd ColCript
Paso 5: Crear Alias (Opcional)
echo "alias colcript='cd ~/ColCript && python3 colcript.py'" >> ~/.bashrc
source ~/.bashrc

# Ahora puedes ejecutar con:
colcript
Fedora/CentOS/RHEL
Paso 1: Actualizar Sistema
sudo dnf update -y
Paso 2: Instalar Python
sudo dnf install python3.12 python3-pip -y
Paso 3: Instalar Dependencias
pip3 install ecdsa requests flask flask-cors
Paso 4: Descargar e Instalar
cd ~
git clone https://github.com/tuusuario/ColCript.git
cd ColCript
python3 colcript.py
Arch Linux
Paso 1: Actualizar Sistema
sudo pacman -Syu
Paso 2: Instalar Python
sudo pacman -S python python-pip
Paso 3: Instalar Dependencias
pip install ecdsa requests flask flask-cors
Paso 4: Descargar e Instalar
cd ~
git clone https://github.com/tuusuario/ColCript.git
cd ColCript
python colcript.py
🍎 Instalación en macOS
Paso 1: Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Paso 2: Instalar Python
brew install python@3.12
Paso 3: Verificar Instalación
python3 --version
pip3 --version
Paso 4: Instalar Dependencias
pip3 install ecdsa requests flask flask-cors
Paso 5: Descargar ColCript
cd ~
git clone https://github.com/tuusuario/ColCript.git
cd ColCript
Paso 6: Ejecutar
python3 colcript.py
🪟 Instalación en Windows
Paso 1: Instalar Python
Descargar Python 3.12+ desde python.org
Ejecutar instalador
✅ IMPORTANTE: Marcar "Add Python to PATH"
Completar instalación
Paso 2: Verificar Instalación
Abrir PowerShell o CMD:
python --version
pip --version
Paso 3: Instalar Dependencias
pip install ecdsa requests flask flask-cors
Paso 4: Descargar ColCript
Opción A: Con Git
cd %USERPROFILE%
git clone https://github.com/tuusuario/ColCript.git
cd ColCript
Opción B: Descarga Manual
Descargar ZIP del repositorio
Extraer en C:\Users\TuUsuario\ColCript
Paso 5: Ejecutar
cd ColCript
python colcript.py
Paso 6: Crear Acceso Directo (Opcional)
Crear archivo ColCript.bat:
@echo off
cd C:\Users\TuUsuario\ColCript
python colcript.py
pause
Guardar y hacer doble clic para ejecutar.
✅ Verificación de Instalación
Test 1: CLI
cd ~/ColCript
python colcript.py
Resultado esperado:
✅ Configuración de ColCript (CLC) cargada

============================================================
                     🪙  ColCript (CLC)
               Criptomoneda Blockchain v1.0.0
============================================================

📋 MENÚ PRINCIPAL:
  1. Crear nueva blockchain
  ...
Test 2: API REST
# Terminal 1: Iniciar servidor
cd ~/ColCript
python api/server.py
Resultado esperado:
🌐 Nodo P2P iniciado
   ID: abc123...
   Host: 127.0.0.1
   Puerto: 6000
   Peers: 0

 * Running on http://0.0.0.0:5000
# Terminal 2: Probar endpoint
curl http://localhost:5000/api/info
Respuesta esperada:
{
  "success": true,
  "data": {
    "nombre": "ColCript",
    "simbolo": "CLC",
    "version": "1.0.0",
    ...
  }
}
Test 3: Interfaz Web
Iniciar servidor API:
python api/server.py
Abrir navegador:
http://localhost:5000
Deberías ver el dashboard de ColCript
Test 4: Importación de Módulos
python3 -c "
from blockchain.blockchain import Blockchain
from blockchain.wallet import Wallet
from contracts.smart_contract import ContractManager
from network.node import Node
print('✅ Todos los módulos importados correctamente')
"
⚙️ Configuración Inicial
Crear config.json
ColCript crea automáticamente config.json en la primera ejecución. Valores por defecto:
{
  "nombre": "ColCript",
  "simbolo": "CLC",
  "version": "1.0.0",
  "difficulty": 4,
  "block_time": 10,
  "mining_reward": 50,
  "max_supply": 21000000,
  "faucet_amount": 5.0,
  "faucet_cooldown_hours": 24
}
Personalizar Configuración
nano config.json
Ejemplo de configuración personalizada:
{
  "nombre": "MiCripto",
  "simbolo": "MIC",
  "version": "1.0.0",
  "difficulty": 3,
  "block_time": 15,
  "mining_reward": 100,
  "max_supply": 50000000,
  "faucet_amount": 10.0,
  "faucet_cooldown_hours": 12
}
Configurar Directorios
Estructura recomendada:
~/ColCript/
├── blockchain/          # Módulo blockchain
├── contracts/           # Smart contracts
├── network/             # Red P2P
├── api/                 # API REST
├── web/                 # Interfaz web
├── utils/               # Utilidades
├── data/                # Datos persistentes
│   ├── blockchains/     # Archivos .json
│   └── wallets/         # Archivos .json
├── logs/                # Logs del sistema
├── config.json          # Configuración
└── colcript.py          # CLI principal
Crear directorios:
cd ~/ColCript
mkdir -p data/blockchains data/wallets logs
🌐 Instalación de Múltiples Nodos
Red Local (Misma Máquina)
Nodo 1 (Puerto 5000)
cd ~/ColCript
python api/server.py
Nodo 2 (Puerto 5001)
Opción A: Duplicar Directorio
cp -r ~/ColCript ~/ColCript-Node2
cd ~/ColCript-Node2

# Editar config o usar variable de entorno
PORT=5001 python api/server.py
Opción B: Usar Virtualenv
# Crear entorno virtual
python3 -m venv ~/colcript-node2
source ~/colcript-node2/bin/activate

# Instalar dependencias
pip install ecdsa requests flask flask-cors

# Copiar proyecto
cp -r ~/ColCript ~/ColCript-Node2
cd ~/ColCript-Node2

# Ejecutar en puerto diferente
PORT=5001 python api/server.py
Red Distribuida (Múltiples Máquinas)
Máquina 1 (192.168.1.100)
cd ~/ColCript
python api/server.py

# API: http://192.168.1.100:5000
# P2P: 192.168.1.100:6000
Máquina 2 (192.168.1.101)
cd ~/ColCript
python api/server.py

# Conectar con Máquina 1
curl -X POST http://localhost:5000/api/network/peer/add \
  -H "Content-Type: application/json" \
  -d '{"host": "192.168.1.100", "port": 5000}'
Máquina 3 (192.168.1.102)
cd ~/ColCript
python api/server.py

# Conectar con Máquina 1 (descubre Máquina 2 automáticamente)
curl -X POST http://localhost:5000/api/network/peer/add \
  -H "Content-Type: application/json" \
  -d '{"host": "192.168.1.100", "port": 5000}'
Docker (Avanzado)
Crear Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copiar archivos
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir ecdsa requests flask flask-cors

# Exponer puertos
EXPOSE 5000 6000

# Comando por defecto
CMD ["python", "api/server.py"]
Construir Imagen
docker build -t colcript:latest .
Ejecutar Contenedor
# Nodo 1
docker run -d -p 5000:5000 -p 6000:6000 \
  --name colcript-node1 \
  colcript:latest

# Nodo 2
docker run -d -p 5001:5000 -p 6001:6000 \
  --name colcript-node2 \
  colcript:latest

# Nodo 3
docker run -d -p 5002:5000 -p 6002:6000 \
  --name colcript-node3 \
  colcript:latest
Docker Compose
version: '3.8'

services:
  node1:
    build: .
    ports:
      - "5000:5000"
      - "6000:6000"
    volumes:
      - node1-data:/app/data
    
  node2:
    build: .
    ports:
      - "5001:5000"
      - "6001:6000"
    volumes:
      - node2-data:/app/data
    
  node3:
    build: .
    ports:
      - "5002:5000"
      - "6002:6000"
    volumes:
      - node3-data:/app/data

volumes:
  node1-data:
  node2-data:
  node3-data:
docker-compose up -d
🔄 Actualización
Actualizar desde Git
cd ~/ColCript

# Backup de datos
cp -r data data.backup

# Actualizar código
git pull origin main

# Reinstalar dependencias (si hay nuevas)
pip install -r requirements.txt

# Verificar
python colcript.py
Actualización Manual
Descargar nueva versión
Backup de directorio data/:
cp -r ~/ColCript/data ~/ColCript-backup
Extraer nueva versión sobre la antigua
Restaurar datos:
cp -r ~/ColCript-backup ~/ColCript/data
Verificar funcionamiento
Migración de Datos
Si hay cambios en formato de datos:
# ColCript incluye script de migración
python utils/migrate.py --from 1.0.0 --to 1.1.0
🗑️ Desinstalación
Desinstalación Completa
Linux/macOS/Termux
# Detener todos los procesos
pkill -f "python.*colcript"
pkill -f "python.*api/server"

# Eliminar directorio
rm -rf ~/ColCript

# Eliminar dependencias (opcional)
pip uninstall -y ecdsa requests flask flask-cors

# Eliminar alias (si lo creaste)
# Editar ~/.bashrc y eliminar línea de alias
nano ~/.bashrc
Windows
Cerrar todos los procesos de Python
Eliminar carpeta C:\Users\TuUsuario\ColCript
Desinstalar dependencias (opcional):
pip uninstall ecdsa requests flask flask-cors
Desinstalación Conservando Datos
# Backup de datos importantes
cp -r ~/ColCript/data ~/ColCript-data-backup

# Eliminar ColCript
rm -rf ~/ColCript

# Para reinstalar más tarde, restaurar datos:
# cp -r ~/ColCript-data-backup ~/ColCript/data
🔍 Solución de Problemas de Instalación
Problema 1: Python no encontrado
Error:
python: command not found
Solución:
# Linux/macOS/Termux
which python3
python3 --version

# Usar python3 en lugar de python
python3 colcript.py

# Crear alias
alias python=python3
Problema 2: pip no encontrado
Error:
pip: command not found
Solución:
# Ubuntu/Debian
sudo apt install python3-pip

# macOS
brew install python

# Termux
pkg install python
Problema 3: Error al instalar ecdsa
Error:
ERROR: Could not build wheels for ecdsa
Solución:
# Instalar compilador
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# macOS
xcode-select --install

# Termux
pkg install clang

# Intentar de nuevo
pip install ecdsa
Problema 4: Puerto 5000 en uso
Error:
Address already in use
Solución:
# Encontrar proceso usando el puerto
# Linux/macOS
lsof -i :5000
kill -9 [PID]

# Termux
netstat -tulpn | grep 5000

# Windows
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# O usar puerto diferente
PORT=5001 python api/server.py
Problema 5: Permisos denegados
Error:
Permission denied
Solución:
# Dar permisos de ejecución
chmod +x colcript.py
chmod +x api/server.py

# O ejecutar con Python directamente
python colcript.py
📚 Siguientes Pasos
Después de instalar:
Leer la Guía de Uso: USAGE.md
Explorar la API: API.md
Crear Smart Contracts: CONTRACTS.md
Configurar Red P2P: NETWORK.md
🆘 Soporte
Si encuentras problemas:
Verificar Issues en GitHub
Consultar documentación completa
Crear nuevo issue con:
Sistema operativo
Versión de Python
Mensaje de error completo
Pasos para reproducir
¡Instalación completada! Ahora puedes comenzar a usar ColCript. 🎉
