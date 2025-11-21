# 📥 Guía de Instalación de ColCript

Esta guía te llevará paso a paso para instalar y configurar ColCript en tu sistema.

---

## 🎯 Requisitos del Sistema

### Mínimos
- **Python:** 3.12 o superior
- **RAM:** 512 MB
- **Almacenamiento:** 50 MB libres
- **Sistema Operativo:** Linux, Unix, macOS, Windows (con WSL), Termux (Android)

### Recomendados
- **Python:** 3.12+
- **RAM:** 1 GB
- **Almacenamiento:** 100 MB libres

---

## 📱 Instalación en Termux (Android)

### Paso 1: Instalar Termux
1. Descarga Termux desde [F-Droid](https://f-droid.org/en/packages/com.termux/)
2. Abre Termux

### Paso 2: Actualizar paquetes
```bash
pkg update
pkg upgrade
Paso 3: Instalar Python
pkg install python
Paso 4: Instalar Git
pkg install git
Paso 5: Instalar dependencias de compilación
pkg install clang
Paso 6: Clonar ColCript
cd ~
git clone https://github.com/tu-usuario/colcript.git
cd colcript
Paso 7: Instalar librerías Python
pip install cryptography ecdsa requests flask
Paso 8: Verificar instalación
python config.py
Deberías ver:
✅ Configuración de ColCript (CLC) cargada
Paso 9: Ejecutar ColCript
python colcript.py
🐧 Instalación en Linux/Unix
Ubuntu/Debian
# Actualizar sistema
sudo apt update
sudo apt upgrade

# Instalar Python y pip
sudo apt install python3.12 python3-pip git

# Clonar repositorio
git clone https://github.com/tu-usuario/colcript.git
cd colcript

# Instalar dependencias
pip3 install cryptography ecdsa requests flask

# Ejecutar
python3 colcript.py
Arch Linux
# Instalar Python
sudo pacman -S python python-pip git

# Clonar repositorio
git clone https://github.com/tu-usuario/colcript.git
cd colcript

# Instalar dependencias
pip install cryptography ecdsa requests flask

# Ejecutar
python colcript.py
Fedora/RHEL/CentOS
# Instalar Python
sudo dnf install python3 python3-pip git

# Clonar repositorio
git clone https://github.com/tu-usuario/colcript.git
cd colcript

# Instalar dependencias
pip3 install cryptography ecdsa requests flask

# Ejecutar
python3 colcript.py
🍎 Instalación en macOS
Paso 1: Instalar Homebrew (si no lo tienes)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Paso 2: Instalar Python y Git
brew install python git
Paso 3: Clonar ColCript
git clone https://github.com/tu-usuario/colcript.git
cd colcript
Paso 4: Instalar dependencias
pip3 install cryptography ecdsa requests flask
Paso 5: Ejecutar
python3 colcript.py
🪟 Instalación en Windows
Opción 1: WSL (Recomendado)
Instalar WSL
wsl --install
Reiniciar el sistema
Abrir Ubuntu (WSL)
Seguir los pasos de instalación para Ubuntu/Debian
Opción 2: Python Nativo
Descargar Python
Ve a python.org
Descarga Python 3.12 o superior
✅ Marca "Add Python to PATH"
Instalar Git
Descarga desde git-scm.com
Instala con opciones por defecto
Abrir PowerShell o CMD
Clonar repositorio
git clone https://github.com/tu-usuario/colcript.git
cd colcript
Instalar dependencias
pip install cryptography ecdsa requests flask
Ejecutar
python colcript.py
🔧 Instalación desde Código Fuente
Paso 1: Descargar código fuente
wget https://github.com/tu-usuario/colcript/archive/refs/heads/main.zip
unzip main.zip
cd colcript-main
Paso 2: Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
Paso 3: Instalar dependencias
pip install -r requirements.txt
Paso 4: Ejecutar
python colcript.py
📦 Crear archivo requirements.txt
Si no existe, crea este archivo:
nano requirements.txt
Contenido:
cryptography>=44.0.0
ecdsa>=0.19.0
requests>=2.32.0
flask>=3.0.0
Instalar con:
pip install -r requirements.txt
✅ Verificación de la Instalación
Test 1: Verificar Python
python --version
# Debe mostrar: Python 3.12.x o superior
Test 2: Verificar dependencias
pip list | grep -E "cryptography|ecdsa|requests|flask"
Debe mostrar:
cryptography    44.x.x
ecdsa           0.19.x
flask           3.x.x
requests        2.32.x
Test 3: Verificar configuración
python config.py
Debe mostrar:
✅ Configuración de ColCript (CLC) cargada
Test 4: Verificar funcionalidades
# Test de criptografía
python utils/crypto.py

# Test de transacciones
python blockchain/transaction.py

# Test de bloques
python blockchain/block.py
Todos deben mostrar mensajes de ✅ éxito.
🚀 Primera Ejecución
Paso 1: Ejecutar ColCript
python colcript.py
Paso 2: Crear blockchain
📋 MENÚ PRINCIPAL:
Selecciona una opción: 1
Paso 3: Activar auto-guardado
¿Activar auto-guardado? (S/n): S
Nombre del archivo (Enter para 'colcript_main.json'): [Enter]
Paso 4: Crear tu wallet
Selecciona una opción: 4
💼 Nombre de la wallet: MiWallet
Paso 5: Minar tu primer bloque
Selecciona una opción: 12
¡Felicidades! Ya tienes 50 CLC 🎉
🔄 Actualización
Actualizar desde Git
cd colcript
git pull origin main
pip install -r requirements.txt --upgrade
Actualizar dependencias
pip install --upgrade cryptography ecdsa requests flask
🐛 Solución de Problemas
Error: "ModuleNotFoundError: No module named 'cryptography'"
Solución:
pip install cryptography
Error: "command not found: python"
Solución:
Intenta con python3:
python3 colcript.py
Error: "Permission denied"
Solución:
chmod +x colcript.py
Error al instalar en Termux: "pip install forbidden"
Solución:
Esto es normal en Termux. Omite el comando pip install --upgrade pip.
Error: "No module named 'utils'"
Solución:
touch utils/__init__.py
touch blockchain/__init__.py
touch wallet/__init__.py
La blockchain no se guarda
Solución:
Verifica que la carpeta data/ existe:
mkdir -p data
📁 Estructura de Archivos Después de la Instalación
colcript/
├── colcript.py              # ✅ Ejecutable principal
├── config.py                # ✅ Configuración
├── README.md                # ✅ Documentación
├── INSTALLATION.md          # ✅ Esta guía
├── requirements.txt         # ✅ Dependencias
├── blockchain/              # ✅ Core
│   ├── __init__.py
│   ├── block.py
│   ├── transaction.py
│   ├── blockchain.py
│   ├── storage.py
│   └── block_explorer.py
├── wallet/                  # ✅ Wallets
│   ├── __init__.py
│   ├── wallet.py
│   ├── faucet.py
│   └── transaction_history.py
├── utils/                   # ✅ Utilidades
│   ├── __init__.py
│   ├── crypto.py
│   ├── statistics.py
│   └── charts.py
└── data/                    # 📦 Se crea al usar
    ├── colcript_main.json
    └── faucet_claims.json
🎓 Próximos Pasos
Una vez instalado ColCript:
📗 Lee el Manual de Usuario
📕 Consulta la Documentación Técnica
🎮 Empieza a usar ColCript
💬 Soporte
Si tienes problemas con la instalación:
📧 Email: soporte@colcript.com
💬 Issues: GitHub Issues
📖 Wiki: GitHub Wiki
¡Disfruta usando ColCript! 🪙
