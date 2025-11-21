# 📗 Manual de Usuario de ColCript

Guía completa para usar todas las funcionalidades de ColCript.

---

## 📖 Tabla de Contenidos

1. [Inicio Rápido](#inicio-rápido)
2. [Gestión de Blockchain](#gestión-de-blockchain)
3. [Gestión de Wallets](#gestión-de-wallets)
4. [Transacciones](#transacciones)
5. [Minería](#minería)
6. [Explorador de Bloques](#explorador-de-bloques)
7. [Estadísticas](#estadísticas)
8. [Faucet](#faucet)
9. [Consejos y Trucos](#consejos-y-trucos)
10. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🚀 Inicio Rápido

### Ejecutar ColCript

```bash
cd ~/ColCript
python colcript.py
Verás el menú principal:
============================================================
                     🪙  ColCript (CLC)
               Criptomoneda Blockchain v1.0.0
============================================================

📋 MENÚ PRINCIPAL:
  1. Crear nueva blockchain
  2. Cargar blockchain existente
  ...
⛓️ Gestión de Blockchain
1️⃣ Crear Nueva Blockchain
Cuándo usar: Primera vez que usas ColCript o quieres empezar de cero.
Pasos:
Selecciona opción 1
Confirma auto-guardado: S (recomendado)
Nombre del archivo: Presiona Enter para usar colcript_main.json
Resultado:
Se crea el bloque génesis
La blockchain se guarda automáticamente
Ejemplo:
Selecciona una opción: 1

⛓️  Creando nueva blockchain...
¿Activar auto-guardado? (S/n): S
Nombre del archivo (Enter para 'colcript_main.json'): [Enter]

⛏️  Minando bloque 0...
✅ Bloque minado! Nonce: 36358
✅ Blockchain creada exitosamente
2️⃣ Cargar Blockchain Existente
Cuándo usar: Para continuar trabajando con una blockchain guardada.
Pasos:
Selecciona opción 2
Elige el número de la blockchain que quieres cargar
Resultado:
La blockchain se carga con todos sus bloques
Puedes continuar donde lo dejaste
Ejemplo:
Selecciona una opción: 2

📁 Blockchains guardadas (2):
  1. colcript_main.json
     Bloques: 6
     Guardada: 2025-11-17 18:08:11

Número de blockchain a cargar: 1

✅ Blockchain cargada con 6 bloques
3️⃣ Listar Blockchains Guardadas
Cuándo usar: Para ver todas tus blockchains disponibles.
Pasos:
Selecciona opción 3
Resultado:
Lista de todas las blockchains en data/
Información de cada una (bloques, fecha)
💼 Gestión de Wallets
4️⃣ Crear Nueva Wallet
Cuándo usar: Para crear una nueva billetera.
Pasos:
Selecciona opción 4
Ingresa un nombre descriptivo (ej: "Mi Wallet", "Juan", "Empresa")
Resultado:
Se genera un par de claves (privada/pública)
La wallet está lista para usar
Importante:
La clave privada se genera automáticamente
Guarda tu wallet (opción 15) para no perderla
Ejemplo:
Selecciona una opción: 4

💼 Nombre de la wallet: Juan
✅ Wallet 'Juan' creada
   Dirección: 687cfe4fe819dc4160a0c9...
5️⃣ Cargar Wallet Existente
Cuándo usar: Para usar una wallet que ya guardaste.
Pasos:
Selecciona opción 5
Ingresa el nombre del archivo (ej: Juan.json)
Resultado:
Tu wallet se carga con sus claves
Puedes ver tu balance y hacer transacciones
Ejemplo:
Selecciona una opción: 5

📂 Nombre del archivo: Juan.json
✅ Wallet 'Juan' cargada desde archivo
   Dirección: 687cfe4fe819dc4160a0c9...
6️⃣ Ver Balance
Cuándo usar: Para ver cuántos CLC tienes.
Requisitos:
Tener una wallet cargada
Tener una blockchain cargada
Pasos:
Selecciona opción 6
Resultado:
Muestra tu balance actual en CLC
Muestra tu dirección
Ejemplo:
Selecciona una opción: 6

💰 Balance de 'Juan':
   90.0 CLC
   Dirección: 687cfe4fe819dc4160a0c9...
Cómo se calcula:
Se suman todas las CLC que recibiste
Se restan todas las CLC que enviaste
Se restan todos los fees que pagaste
15. Guardar Wallet
Cuándo usar: Después de crear una wallet nueva.
Pasos:
Selecciona opción 15
Resultado:
La wallet se guarda en wallet/NombreWallet.json
Puedes cargarla después con la opción 5
Ejemplo:
Selecciona una opción: 15

💾 Wallet guardada en: Juan.json
⚠️ Importante: Guarda este archivo de forma segura. Contiene tu clave privada.
💸 Transacciones
11. Enviar ColCript
Cuándo usar: Para transferir CLC a otra wallet.
Requisitos:
Tener una wallet cargada
Tener balance suficiente
Conocer la dirección destino
Pasos:
Selecciona opción 11
Ingresa la dirección destino (completa)
Ingresa la cantidad a enviar
Configura el fee (o presiona Enter para usar el recomendado)
Confirma la transacción
Resultado:
La transacción queda pendiente
Debes minar un bloque (opción 12) para confirmarla
Ejemplo:
Selecciona una opción: 11

💸 Enviar CLC
   Balance actual: 90 CLC
   Dirección destino: 3fbb02f306140c43c201bb64...
   Cantidad: 10

💰 Configuración de fee:
   Mínimo: 0.1 CLC
   Recomendado: 0.5 CLC
   Máximo: 10 CLC
   Fee (Enter para usar 0.5 CLC): [Enter]

📋 Resumen de la transacción:
   Cantidad: 10 CLC
   Fee: 0.5 CLC
   Total a descontar: 10.5 CLC

¿Confirmar transacción? (S/n): S

✅ Transacción agregada al pool de transacciones pendientes
Importante:
La transacción NO se ejecuta inmediatamente
Está en el "pool de transacciones pendientes"
Alguien debe minar un bloque para confirmarla
Sobre los Fees (Comisiones)
¿Qué son?
Son comisiones que pagas por cada transacción
Van al minero que confirme tu transacción
¿Cuánto pagar?
Mínimo: 0.1 CLC
Recomendado: 0.5 CLC (confirmación rápida)
Alto: 1-10 CLC (prioridad máxima)
¿Por qué pagar más?
Mayor fee = mayor prioridad
Tu transacción se mina primero
⛏️ Minería
12. Minar Bloque
Cuándo usar:
Para ganar CLC (50 CLC de recompensa)
Para confirmar transacciones pendientes
Para ayudar a la red
Requisitos:
Tener una wallet cargada
Pasos:
Selecciona opción 12
Espera a que se mine el bloque
Resultado:
Ganas 50 CLC de recompensa base
Ganas todos los fees de las transacciones pendientes
Todas las transacciones pendientes se confirman
Ejemplo:
Selecciona una opción: 12

⛏️  Minando bloque para 'Juan'...
   Transacciones pendientes: 1
⛏️  Minando bloque 6...
   Intentos: 10000, Hash: a3e4f0a381...
✅ Bloque minado! Nonce: 59319
💰 Fees recolectados: 0.5 CLC
💎 Recompensa total: 50.5 CLC
✅ Bloque #6 añadido a la cadena

✅ ¡Bloque minado exitosamente!
   Recompensa: 50 CLC
   Nuevo balance: 140.5 CLC
Cálculo del balance:
Balance anterior: 90 CLC
Enviaste: -10 CLC
Fee pagado: -0.5 CLC
Recompensa: +50 CLC
Fee recolectado: +0.5 CLC
Nuevo balance: 90 - 10 - 0.5 + 50 + 0.5 = 130 CLC ✅
Tiempo de minado:
Depende de tu dispositivo
Generalmente: 0.5 - 3 segundos
Dificultad: 4 ceros (configurable)
🔍 Explorador de Bloques
8. Explorador de Bloques
Cuándo usar: Para inspeccionar la blockchain en detalle.
Opciones disponibles:
8.1 - Ver estadísticas de la blockchain
📊 ESTADÍSTICAS:
   Total de bloques: 6
   Transacciones totales: 8
   Mineros únicos: 3
   CLC en circulación: 251.0
8.2 - Ver bloque por número
Número de bloque: 3

📊 INFORMACIÓN GENERAL:
   Hash: 0000b0809f35bb42e0a7...
   Minero: 687cfe4fe819dc4160a0c9...
   Fecha: 2025-11-17 18:04:28
   Nonce: 13,472
   Transacciones: 1
8.3 - Buscar bloque por hash
Hash del bloque: 0000b0809

[Muestra el bloque que coincida]
8.4 - Buscar bloques por minero
Dirección del minero: 687cfe4

⛏️  BLOQUES MINADOS POR 687cfe4...
   Total encontrados: 2 bloques
8.5 - Ver último bloque
Muestra el bloque más reciente con todos sus detalles.
8.6 - Navegar por bloques
Navegación interactiva:
[N] - Siguiente bloque
[P] - Bloque anterior
[D] - Ver detalles completos
[G] - Ir a bloque específico
[V] - Volver
8.7 - Verificar bloque específico
Verifica la integridad criptográfica de un bloque.
8.8 - Exportar bloque a JSON
Guarda la información del bloque en un archivo.
📊 Estadísticas
9. Estadísticas y Métricas
Cuándo usar: Para analizar el estado de la blockchain.
Opciones disponibles:
9.1 - Dashboard completo
Vista general con todas las métricas:
Supply y circulación
Top wallets
Distribución de riqueza
Estadísticas de minería
Transacciones
Salud de la red
Ejemplo:
============================================================
                    📊 DASHBOARD COLCRIPT
============================================================

💰 SUPPLY:
   Total: 21,000,000 CLC
   En circulación: 251.0 CLC
   Progreso: [░░░░░░░] 0.00%

💼 WALLETS:
   Top 5 Wallets:
   Juan                  ████████████████████ 90.00
   Bob                   ███████████████ 70.50
9.2 - Supply y circulación
💰 ESTADÍSTICAS DE SUPPLY
Total configurado: 21,000,000 CLC
En circulación: 251.0 CLC
Por minar: 20,999,749 CLC
Porcentaje minado: 0.001195%
9.3 - Top wallets
Ranking de las 10 wallets con más CLC.
9.4 - Distribución de riqueza
📊 DISTRIBUCIÓN DE RIQUEZA
Top 1% de wallets controla: 44.78%
Top 10% de wallets controla: 80.09%
Balance mediano: 29.50 CLC
9.5 - Estadísticas de minería
⛏️  ESTADÍSTICAS DE MINERÍA
Mineros activos: 3
Bloques minados: 5
Tiempo promedio por bloque: 1.09s
Top minero: 687cfe4fe819...
9.6 - Estadísticas de transacciones
💸 ESTADÍSTICAS DE TRANSACCIONES
Total: 8
Transferencias: 3
Recompensas de minado: 5
Volumen total: 281.0 CLC
Fees pagados: 1.5 CLC
9.7 - Salud de la red
🌐 SALUD DE LA RED
Estado: ✅ VÁLIDA
Total de bloques: 6
Dificultad: 4
Score de descentralización: 66.67%
🎁 Faucet (CLC Gratis)
10. Faucet
¿Qué es?
Un sistema que regala 5 CLC gratis cada 24 horas.
¿Para qué sirve?
Obtener tus primeros CLC sin minar
Probar transacciones sin invertir
Facilitar el acceso a nuevos usuarios
Opciones disponibles:
10.1 - Reclamar CLC gratis
Requisitos:
Tener una wallet cargada
Balance menor a 50 CLC
No haber reclamado en las últimas 24 horas
Que el faucet tenga fondos
Pasos:
Selecciona opción 10 → 1
Confirma el reclamo
Mina un bloque para confirmar
Ejemplo:
🎁 RECLAMAR 5 CLC GRATIS
Tu wallet: Juan
Balance actual: 10.0 CLC
Recibirás: 5 CLC

✅ Puede reclamar

¿Confirmar reclamo? (S/n): S

✅ ¡Reclamo exitoso! 5 CLC agregados al pool

⚠️  IMPORTANTE: La transacción está pendiente.
    Debes minar un bloque para confirmarla.
    Después tendrás 15.0 CLC
10.2 - Ver información del faucet
🎁 INFORMACIÓN DEL FAUCET
Estado: ✅ Habilitado
Cantidad por reclamo: 5 CLC
Cooldown: 24 horas
Balance del faucet: 45 CLC
Reclamos disponibles: ~9
10.3 - Ver mi historial de reclamos
📜 MI HISTORIAL DE RECLAMOS
✅ Has reclamado 1 veces
💰 Total reclamado: 5 CLC
📅 Último reclamo: 2025-11-17 18:30:00
⏰ Próximo reclamo disponible en: 23h 45m
10.4 - Donar al faucet
Puedes donar tus CLC para ayudar a otros usuarios.
10.5 - Financiar faucet (minando)
Mina un bloque y la recompensa va al faucet.
💡 Consejos y Trucos
1. Guarda tus wallets regularmente
Después de crear una wallet → Opción 15
2. Usa fees apropiados
Transacción normal: 0.5 CLC
Urgente: 1-2 CLC
No urgente: 0.1 CLC
3. Mina tus propias transacciones
Si envías CLC y luego minas:
Confirmas tu transacción
Recuperas el fee que pagaste
Ganas la recompensa (50 CLC)
4. Verifica antes de enviar
Opción 6 → Ver balance
Opción 11 → Revisar resumen antes de confirmar
5. Usa el faucet
Si empiezas desde cero:
Opción 10 → Reclama 5 CLC gratis
Opción 12 → Mina para confirmar
6. Revisa estadísticas
Opción 9 → Dashboard completo
Para entender el estado de la red.
7. Exporta tu historial
Opción 7 → Opción 6
Para guardar un registro de tus transacciones.
❓ Preguntas Frecuentes
¿Cuánto tarda en minar un bloque?
Entre 0.5 y 3 segundos en dispositivos modernos.
¿Pierdo mis CLC si cierro el programa?
No, si usas auto-guardado (recomendado).
¿Puedo tener múltiples wallets?
Sí, crea y guarda tantas como quieras.
¿Qué pasa si envío a una dirección incorrecta?
La transacción es irreversible. Verifica bien la dirección.
¿Cuántos CLC puedo minar en total?
21,000,000 CLC (como Bitcoin).
¿El faucet se queda sin fondos?
Sí, pero puedes donarlo o minarlo.
¿Puedo cambiar la dificultad?
Sí, editando config.py → MINING_DIFFICULTY.
¿Las transacciones pendientes se pierden?
No, se mantienen hasta que alguien las mina.
¿Puedo ver transacciones de otras wallets?
Sí, con el explorador de bloques (opción 8).
¿Cómo sé que la blockchain es válida?
Opción 9 → Opción 7 → Salud de la red
🎮 Flujo de Trabajo Típico
Primer día (nuevo usuario)
Crear blockchain (opción 1)
Crear wallet (opción 4)
Guardar wallet (opción 15)
Reclamar del faucet (opción 10 → 1)
Minar para confirmar (opción 12)
Ver balance (opción 6) → Tienes 55 CLC
Día a día (usuario regular)
Cargar blockchain (opción 2)
Cargar wallet (opción 5)
Enviar/Recibir CLC (opción 11)
Minar bloques (opción 12)
Ver estadísticas (opción 9)
Usuario avanzado
Usar el explorador de bloques
Analizar distribución de riqueza
Optimizar fees según prioridad
Exportar datos
Donar al faucet
📞 Soporte
¿Necesitas ayuda?
📧 Email: soporte@colcript.com
💬 Issues: GitHub Issues
📖 Wiki: GitHub Wiki
¡Disfruta usando ColCript! 🪙
