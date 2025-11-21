# 🌐 Guía de la Interfaz Web de ColCript

Guía completa para usar la interfaz web de ColCript.

---

## 🚀 Acceso

### Desde el mismo dispositivo:
http://localhost:5000
### Desde otro dispositivo en la red:
http://[IP_DEL_SERVIDOR]:5000
Para conocer tu IP:
```bash
hostname -I

📊 Dashboard
La página principal muestra:
Stats Cards
Supply Circulante: CLC en circulación vs total
Total Bloques: Número de bloques en la cadena
Dificultad: Dificultad actual de minado
Mi Balance: Tu balance actual (si hay wallet cargada)
Gráficas
Supply en Circulación: Gráfica de dona mostrando distribución
Top Wallets: Ranking de las 5 wallets con más CLC
Últimos Bloques
Lista de los 5 bloques más recientes
Click en cualquier hash para copiar
Botón "Ver" para detalles completos

💼 Wallet
Crear Nueva Wallet
Ingresa un nombre
Click en "Crear Nueva Wallet"
La wallet se crea automáticamente
Cargar Wallet Existente
Ingresa el nombre del archivo (ej: mi_wallet.json)
Click en "Cargar Wallet"
Se muestra tu información y balance
Enviar ColCript
Ingresa dirección destino (completa)
Cantidad a enviar
Fee (0.5 CLC recomendado)
Click en "Enviar Transacción"
Importante: Mina un bloque para confirmar
Historial
Últimas 10 transacciones
Tipo: Minado, Enviado, Recibido
Fecha, monto y fees

⛏️ Minería
Control de Minería
Recompensa: 50 CLC por bloque
Dificultad: Dificultad actual
Tx Pendientes: Transacciones sin confirmar
Minar Bloque
Asegúrate de tener una wallet cargada
Click en "⛏️ Minar Bloque"
Espera (puede tomar 1-5 segundos)
¡Recibes 50 CLC + fees!
Estadísticas
Mineros activos
Bloques minados
Tiempo promedio
Hashrate estimado

🔍 Explorador
Buscar Bloque
Ingresa número de bloque
Click en "Buscar"
Se muestran todos los detalles
Información del Bloque
Índice, hash, hash anterior
Minero, timestamp, nonce
Dificultad, transacciones
Lista completa de transacciones
Todos los Bloques
Lista completa de la blockchain
Click en cualquier bloque para ver detalles

🎁 Faucet
Reclamar CLC Gratis
Carga una wallet
Verifica que puedes reclamar:
Balance menor a 50 CLC
No has reclamado en 24 horas
El faucet tiene fondos
Click en "Reclamar Ahora"
Mina un bloque para confirmar
¡Recibes 5 CLC gratis!
Información
Cantidad por reclamo
Cooldown (24 horas)
Balance del faucet
Total distribuido
Usuarios que han reclamado

⚙️ Ajustes
Información Actual
Dificultad actual
Tiempo promedio de minado
Tiempo objetivo
Próximo ajuste
Estado del ajuste automático
Configuración Manual
Ingresa nueva dificultad (2-8)
Click en "Aplicar Dificultad"
Afecta inmediatamente al próximo bloque
Ajuste Automático
Activa/desactiva el toggle
Click en "Guardar Cambios"
El sistema ajusta la dificultad automáticamente

💡 Consejos
Para Nuevos Usuarios
Crea una wallet
Reclama del faucet (5 CLC gratis)
Mina para confirmar
Ya tienes 55 CLC (5 + 50)
Para Obtener Más CLC
Minar: 50 CLC por bloque
Faucet: 5 CLC cada 24 horas
Recibir: Que alguien te envíe
Antes de Enviar CLC
Verifica la dirección destino
Asegúrate de tener balance suficiente
Considera el fee (0.5 CLC recomendado)
Recuerda minar para confirmar
Auto-actualización
El dashboard se actualiza automáticamente cada 30 segundos.

📱 Acceso Móvil
La interfaz es completamente responsive:
Conecta tu móvil a la misma red WiFi
En el servidor, anota la IP mostrada
En tu móvil, abre el navegador
Ve a http://[IP]:5000
¡Listo! Funciona igual que en desktop

🐛 Solución de Problemas
"Desconectado" en el header
Solución: Verifica que el servidor API esté corriendo
python api/server.py
"Error cargando wallet"
Solución: Verifica que el archivo existe en wallet/
"Error minando bloque"
Solución: Asegúrate de tener una wallet cargada
La página no carga
Solución:
Verifica que el servidor esté corriendo
Prueba limpiar caché del navegador
Verifica la URL correcta
Gráficas no se muestran
Solución:
Verifica conexión a internet (Chart.js se carga desde CDN)
Recarga la página

🔒 Seguridad
La interfaz web NO guarda claves privadas
Todo se procesa en el servidor
Las wallets están en wallet/ en el servidor
No compartas tu wallet con nadie
Haz backups regularmente

📞 Soporte
¿Problemas con la interfaz web?
Revisa la consola del navegador (F12)
Verifica los logs del servidor
Consulta la documentación de la API
¡Disfruta usando ColCript! 🪙
