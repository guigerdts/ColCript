#!/usr/bin/env python3
# colcript.py - Interfaz principal de ColCript

import os
import sys

# Obtener ruta absoluta del proyecto
project_root = '/data/data/com.termux/files/home/ColCript'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet
from blockchain.storage import BlockchainStorage
from wallet.transaction_history import TransactionHistory
from blockchain.block_explorer import BlockExplorer
from utils.statistics import BlockchainStatistics
from utils.charts import create_bar_chart, create_progress_bar, create_percentage_bar, print_table
from wallet.faucet import Faucet
from contracts.smart_contract import ContractManager, ContractType
from network.node import Node
import config

class ColCriptCLI:
    def __init__(self):
        self.blockchain = None
        self.wallet = None
        self.running = True
        self.contract_manager = None
        self.p2p_node = None
        self.storage = BlockchainStorage()
    
    def show_banner(self):
        """Muestra el banner de ColCript"""
        print("\n" + "="*60)
        print(f"{'🪙  ' + config.COIN_NAME + ' (' + config.COIN_SYMBOL + ')':^60}")
        print(f"{'Criptomoneda Blockchain v' + config.VERSION:^60}")
        print("="*60 + "\n")

    def show_menu(self):

        """Muestra el menú principal"""
        print("\n📋 MENÚ PRINCIPAL:")
        print("  1. Crear nueva blockchain")
        print("  2. Cargar blockchain existente")
        print("  3. Listar blockchains guardadas")
        print("  4. Crear nueva wallet")
        print("  5. Cargar wallet existente")
        print("  6. Ver   balance")
        print("  7. Ver historial de transacciones")
        print("  8. Explorador de bloques")
        print("  9. Estadísticas y métricas")
        print(" 10. Faucet (CLC gratis)")
        print(" 11. Enviar ColCript")
        print(" 12. Minar bloque")
        print(" 13. Ver blockchain")
        print(" 14. Ver información")
        print(" 15. Guardar wallet")
        print(" 16. Guardar blockchain manualmente")
        print(" 17. Ajuste de dificultad")
        print(" 18. Smart Contract")
        print(" 19. Red P2P")
        print("  0. Salir")
        print()

    def create_blockchain(self):
        """Crea una nueva blockchain"""
        print("\n⛓️  Creando nueva blockchain...")
        
        # Preguntar si desea auto-guardado
        auto_save_input = input("¿Activar auto-guardado? (S/n): ").strip().lower()
        auto_save = auto_save_input != 'n'
        
        if auto_save:
            filename = input("Nombre del archivo (Enter para 'colcript_main.json'): ").strip()
            if not filename:
                filename = "colcript_main.json"
            self.blockchain = Blockchain(auto_save=True, save_filename=filename)
        else:
            self.blockchain = Blockchain(auto_save=False)
        
        print("✅ Blockchain creada exitosamente\n")
    
    def load_blockchain(self):
        """Carga una blockchain existente"""
        blockchains = self.storage.list_blockchains()
        
        if not blockchains:
            return
        
        choice = input("\nNúmero de blockchain a cargar (0 para cancelar): ").strip()
        
        try:
            choice_num = int(choice)
            if choice_num == 0:
                print("Cancelado\n")
                return
            
            if 1 <= choice_num <= len(blockchains):
                filename = blockchains[choice_num - 1]['filename']
                
                print(f"\n📂 Cargando {filename}...")
                loaded_bc = self.storage.load_blockchain(filename)
                
                if loaded_bc:
                    # Configurar auto-guardado
                    loaded_bc.storage = self.storage
                    loaded_bc.save_filename = filename
                    loaded_bc.auto_save = True
                    
                    self.blockchain = loaded_bc
                    print(f"✅ Blockchain cargada con {len(self.blockchain.chain)} bloques\n")
                else:
                    print("❌ Error al cargar blockchain\n")
            else:
                print("❌ Opción inválida\n")
        except ValueError:
            print("❌ Entrada inválida\n")
    
    def list_saved_blockchains(self):
        """Lista todas las blockchains guardadas"""
        self.storage.list_blockchains()
        input("\nPresiona Enter para continuar...")
    
    def create_wallet(self):
        """Crea una nueva wallet"""
        name = input("\n💼 Nombre de la wallet: ").strip()
        if not name:
            name = "My Wallet"
        self.wallet = Wallet(name)
        print()
    
    def load_wallet(self):
        """Carga una wallet desde archivo"""
        filename = input("\n📂 Nombre del archivo (ej: Mi_Wallet.json): ").strip()
        if not filename.endswith('.json'):
            filename += '.json'
        
        self.wallet = Wallet.load_from_file(filename)
        print()
    
    def view_balance(self):
        """Muestra el balance de la wallet"""
        if not self.wallet:
            print("\n❌ Primero debes crear o cargar una wallet\n")
            return
        
        if not self.blockchain:
            print("\n❌ Primero debes crear una blockchain\n")
            return
        
        balance = self.wallet.get_balance(self.blockchain)
        print(f"\n💰 Balance de '{self.wallet.name}':")
        print(f"   {balance} {config.COIN_SYMBOL}")
        print(f"   Dirección: {self.wallet.get_address()[:40]}...\n")
    
    def view_transaction_history(self):
        """Muestra el menú de historial de transacciones"""
        if not self.wallet:
            print("\n❌ Primero debes crear o cargar una wallet\n")
            return
        
        if not self.blockchain:
            print("\n❌ Primero debes crear una blockchain\n")
            return
        
        # Crear analizador de historial
        history = TransactionHistory(self.blockchain, self.wallet.get_address())
        
        while True:
            print("\n📜 MENÚ DE HISTORIAL")
            print("  1. Ver resumen")
            print("  2. Ver todas las transacciones")
            print("  3. Ver solo transacciones enviadas")
            print("  4. Ver solo transacciones recibidas")
            print("  5. Ver solo recompensas de minado")
            print("  6. Exportar historial a JSON")
            print("  0. Volver al menú principal")
            print()
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                history.print_summary()
                input("\nPresiona Enter para continuar...")
            
            elif choice == '2':
                history.print_all_transactions()
                input("\nPresiona Enter para continuar...")
            
            elif choice == '3':
                sent = history.get_sent_transactions()
                if not sent:
                    print("\n📭 No hay transacciones enviadas\n")
                else:
                    print(f"\n📤 TRANSACCIONES ENVIADAS ({len(sent)})")
                    for i, tx in enumerate(sent, 1):
                        history.print_transaction(tx, i)
                input("\nPresiona Enter para continuar...")
            
            elif choice == '4':
                received = history.get_received_transactions()
                if not received:
                    print("\n📭 No hay transacciones recibidas\n")
                else:
                    print(f"\n📥 TRANSACCIONES RECIBIDAS ({len(received)})")
                    for i, tx in enumerate(received, 1):
                        history.print_transaction(tx, i)
                input("\nPresiona Enter para continuar...")
            
            elif choice == '5':
                mining = history.get_mining_rewards()
                if not mining:
                    print("\n📭 No hay recompensas de minado\n")
                else:
                    print(f"\n⛏️  RECOMPENSAS DE MINADO ({len(mining)})")
                    for i, tx in enumerate(mining, 1):
                        history.print_transaction(tx, i)
                input("\nPresiona Enter para continuar...")
            
            elif choice == '6':
                filename = input("\nNombre del archivo (Enter para automático): ").strip()
                if filename:
                    history.export_to_json(filename)
                else:
                    history.export_to_json()
                input("Presiona Enter para continuar...")
            
            elif choice == '0':
                break
            
            else:
                print("\n❌ Opción inválida\n")
    
    def block_explorer_menu(self):
        """Muestra el menú del explorador de bloques"""
        if not self.blockchain:
            print("\n❌ Primero debes crear o cargar una blockchain\n")
            return
        
        explorer = BlockExplorer(self.blockchain)
        
        while True:
            print("\n🔍 EXPLORADOR DE BLOQUES")
            print("  1. Ver estadísticas de la blockchain")
            print("  2. Ver bloque por número")
            print("  3. Buscar bloque por hash")
            print("  4. Buscar bloques por minero")
            print("  5. Ver último bloque")
            print("  6. Navegar por bloques")
            print("  7. Verificar bloque específico")
            print("  8. Exportar bloque a JSON")
            print("  0. Volver al menú principal")
            print()
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                explorer.print_blockchain_stats()
                input("\nPresiona Enter para continuar...")
            
            elif choice == '2':
                try:
                    num = int(input("\nNúmero de bloque: ").strip())
                    block = explorer.get_block_by_number(num)
                    if block:
                        explorer.print_block_detailed(block)
                    else:
                        print(f"\n❌ Bloque #{num} no existe\n")
                except ValueError:
                    print("\n❌ Número inválido\n")
                input("\nPresiona Enter para continuar...")
            
            elif choice == '3':
                hash_input = input("\nHash del bloque (completo o parcial): ").strip()
                if hash_input:
                    block = explorer.get_block_by_hash(hash_input)
                    if block:
                        explorer.print_block_detailed(block)
                    else:
                        print(f"\n❌ No se encontró bloque con ese hash\n")
                else:
                    print("\n❌ Hash inválido\n")
                input("\nPresiona Enter para continuar...")
            
            elif choice == '4':
                address = input("\nDirección del minero (completa o parcial): ").strip()
                if address:
                    blocks = explorer.search_blocks_by_miner(address)
                    if blocks:
                        print(f"\n⛏️  BLOQUES MINADOS POR {address[:40]}...")
                        print(f"   Total encontrados: {len(blocks)}\n")
                        for block in blocks:
                            explorer.print_block_summary(block)
                    else:
                        print(f"\n❌ No se encontraron bloques minados por esa dirección\n")
                else:
                    print("\n❌ Dirección inválida\n")
                input("\nPresiona Enter para continuar...")
            
            elif choice == '5':
                last_block = self.blockchain.get_latest_block()
                print("\n🆕 ÚLTIMO BLOQUE:")
                explorer.print_block_detailed(last_block)
                input("\nPresiona Enter para continuar...")
            
            elif choice == '6':
                self._navigate_blocks(explorer)
            
            elif choice == '7':
                try:
                    num = int(input("\nNúmero de bloque a verificar: ").strip())
                    block = explorer.get_block_by_number(num)
                    if block:
                        verification = explorer.verify_block(block)
                        print(f"\n🔍 VERIFICACIÓN DEL BLOQUE #{num}")
                        print("="*60)
                        if verification['valid']:
                            print("✅ El bloque es válido")
                        else:
                            print("❌ El bloque tiene problemas:")
                            for issue in verification['issues']:
                                print(f"   • {issue}")
                        print("="*60 + "\n")
                    else:
                        print(f"\n❌ Bloque #{num} no existe\n")
                except ValueError:
                    print("\n❌ Número inválido\n")
                input("\nPresiona Enter para continuar...")
            
            elif choice == '8':
                try:
                    num = int(input("\nNúmero de bloque a exportar: ").strip())
                    block = explorer.get_block_by_number(num)
                    if block:
                        filename = input("Nombre del archivo (Enter para automático): ").strip()
                        if filename:
                            explorer.export_block(block, filename)
                        else:
                            explorer.export_block(block)
                    else:
                        print(f"\n❌ Bloque #{num} no existe\n")
                except ValueError:
                    print("\n❌ Número inválido\n")
                input("\nPresiona Enter para continuar...")
            
            elif choice == '0':
                break
            
            else:
                print("\n❌ Opción inválida\n")

    def statistics_menu(self):
        """Muestra el menú de estadísticas y métricas"""
        if not self.blockchain:
            print("\n❌ Primero debes crear o cargar una blockchain\n")
            return
    
        stats = BlockchainStatistics(self.blockchain)
    
        while True:
            print("\n📊 ESTADÍSTICAS Y MÉTRICAS")
            print("  1. Dashboard completo")
            print("  2. Supply y circulación")
            print("  3. Top wallets")
            print("  4. Distribución de riqueza")
            print("  5. Estadísticas de minería")
            print("  6. Estadísticas de transacciones")
            print("  7. Salud de la red")
            print("  0. Volver al menú principal")
            print()
        
            choice = input("Selecciona una opción: ").strip()
        
            if choice == '1':
                self._show_complete_dashboard(stats)
            elif choice == '2':
                self._show_supply_stats(stats)
            elif choice == '3':
                self._show_top_wallets(stats)
            elif choice == '4':
                self._show_wealth_distribution(stats)
            elif choice == '5':
                self._show_mining_stats(stats)
            elif choice == '6':
                self._show_transaction_stats(stats)
            elif choice == '7':
                self._show_network_health(stats)
            elif choice == '0':
                break
            else:
                print("\n❌ Opción inválida\n")

    def difficulty_menu(self):
        """Muestra el menú de ajuste de dificultad"""
        if not self.blockchain:
            print("\n❌ Primero debes crear o cargar una blockchain\n")
            return
    
        from blockchain.difficulty import DifficultyAdjustment
    
        while True:
            print("\n⚙️  AJUSTE DE DIFICULTAD")
            print("  1. Ver información de dificultad")
            print("  2. Configurar dificultad manual")
            print("  3. Habilitar/deshabilitar ajuste automático")
            print("  4. Configurar tiempo objetivo")
            print("  5. Configurar intervalo de ajuste")
            print("  0. Volver al menú principal")
            print()
        
            choice = input("Selecciona una opción: ").strip()
        
            if choice == '1':
                self._show_difficulty_info()
            elif choice == '2':
                self._set_manual_difficulty()
            elif choice == '3':
                self._toggle_auto_adjustment()
            elif choice == '4':
                self._set_target_block_time()
            elif choice == '5':
                self._set_adjustment_interval()
            elif choice == '0':
                break
            else:
                print("\n❌ Opción inválida\n")

    def contracts_menu(self):
        """Muestra el menú de smart contracts"""
        if not self.blockchain:
            print("\n❌ Primero debes crear o cargar una blockchain\n")
            return
    
        # Inicializar contract manager si no existe
        if self.contract_manager is None:
            self.contract_manager = ContractManager(self.blockchain)
    
        while True:
            print("\n📜 SMART CONTRACTS")
            print("  1. Crear Timelock")
            print("  2. Crear Multisig")
            print("  3. Crear Escrow")
            print("  4. Listar contratos")
            print("  5. Ver contrato")
            print("  6. Ejecutar contrato")
            print("  7. Firmar contrato (Multisig)")
            print("  8. Decidir Escrow")
            print("  0. Volver al menú principal")
            print()
        
            choice = input("Selecciona una opción: ").strip()

            if choice == '1':
                self._create_timelock()
            elif choice == '2':
                self._create_multisig()
            elif choice == '3':
                self._create_escrow()
            elif choice == '4':
                self._list_contracts()
            elif choice == '5':
                self._view_contract()
            elif choice == '6':
                self._execute_contract()
            elif choice == '7':
                self._sign_multisig()
            elif choice == '8':
                self._decide_escrow()
            elif choice == '0':
                break
            else:
                print("\n❌ Opción inválida\n")

    def network_menu(self):
        """Muestra el menú de red P2P"""
        if not self.blockchain:
            print("\n❌ Primero debes crear o cargar una blockchain\n")
            return
    
        # Inicializar nodo P2P si no existe
        if self.p2p_node is None:
            print("\n🌐 Iniciando nodo P2P...")
            self.p2p_node = Node(host='127.0.0.1', port=6000, blockchain=self.blockchain)
            self.p2p_node.start()
    
        while True:
            print("\n🌐 RED P2P")
            print("  1. Información del nodo")
            print("  2. Listar peers")
            print("  3. Agregar peer")
            print("  4. Eliminar peer")
            print("  5. Sincronizar con red")
            print("  6. Descubrir peers")
            print("  7. Detener nodo")
            print("  0. Volver al menú principal")
            print()
        
            choice = input("Selecciona una opción: ").strip()
        
            if choice == '1':
                self._show_node_info()
            elif choice == '2':
                self._list_peers()
            elif choice == '3':
                self._add_peer()
            elif choice == '4':
                self._remove_peer()
            elif choice == '5':
                self._sync_network()
            elif choice == '6':
                self._discover_peers()
            elif choice == '7':
                self._stop_node()
            elif choice == '0':
                break
            else:
                print("\n❌ Opción inválida\n")

    def _show_node_info(self):
        """Muestra información del nodo"""
        print("\n" + "="*60)
        print("INFORMACIÓN DEL NODO P2P")
        print("="*60)
    
        info = self.p2p_node.get_network_info()
    
        print(f"\nID del Nodo: {info['node_id']}")
        print(f"Host: {info['host']}")
        print(f"Puerto: {info['port']}")
        print(f"Peers Conectados: {info['peers_count']}")
        print(f"Uptime: {info['uptime']}")
        print(f"\nBlockchain:")
        print(f"  Altura: {info['blockchain_height']} bloques")
        print(f"\nEstadísticas:")
        print(f"  Bloques recibidos: {info['blocks_received']}")
        print(f"  Bloques enviados: {info['blocks_sent']}")
        print(f"  Transacciones recibidas: {info['transactions_received']}")
        print(f"  Transacciones enviadas: {info['transactions_sent']}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _list_peers(self):
        """Lista los peers conectados"""
        print("\n" + "="*60)
        print("PEERS CONECTADOS")
        print("="*60)
    
        if not self.p2p_node.peers:
            print("\nNo hay peers conectados")
        else:
            print(f"\nTotal: {len(self.p2p_node.peers)} peers\n")
            for i, (host, port) in enumerate(self.p2p_node.peers, 1):
                print(f"{i}. {host}:{port}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _add_peer(self):
        """Agrega un peer"""
        print("\n📡 AGREGAR PEER")
        print("="*60)
    
        host = input("Host/IP del peer: ").strip()
        port = input("Puerto del peer: ").strip()
    
        if not host or not port:
            print("❌ Host y puerto son requeridos\n")
            input("Presiona Enter para continuar...")
            return
    
        try:
            port = int(port)
            print(f"\n🔄 Conectando con {host}:{port}...")
            success, msg = self.p2p_node.add_peer(host, port)
        
            if success:
                print(f"✅ {msg}")
                print(f"   Total peers: {len(self.p2p_node.peers)}")
            else:
                print(f"❌ {msg}")
        except ValueError:
            print("❌ Puerto inválido")
        except Exception as e:
            print(f"❌ Error: {e}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _remove_peer(self):
        """Elimina un peer"""
        if not self.p2p_node.peers:
            print("\n❌ No hay peers conectados\n")
            input("Presiona Enter para continuar...")
            return
    
        print("\n❌ ELIMINAR PEER")
        print("="*60)
    
        print("\nPeers conectados:")
        peers_list = list(self.p2p_node.peers)
        for i, (host, port) in enumerate(peers_list, 1):
            print(f"{i}. {host}:{port}")
    
        choice = input("\nNúmero de peer a eliminar (0 para cancelar): ").strip()
    
        try:
            choice = int(choice)
            if choice == 0:
                return
        
            if 1 <= choice <= len(peers_list):
                host, port = peers_list[choice - 1]
                success, msg = self.p2p_node.remove_peer(host, port)
            
                if success:
                    print(f"\n✅ {msg}")
                else:
                    print(f"\n❌ {msg}")
            else:
                print("\n❌ Número inválido")
        except ValueError:
            print("\n❌ Entrada inválida")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _sync_network(self):
        """Sincroniza con la red"""
        if not self.p2p_node.peers:
            print("\n❌ No hay peers conectados para sincronizar\n")
            input("Presiona Enter para continuar...")
            return
    
        print("\n🔄 SINCRONIZAR CON RED")
        print("="*60)
    
        print(f"\nSincronizando con {len(self.p2p_node.peers)} peers...")
        self.p2p_node.sync_with_network()
    
        print(f"\n✅ Sincronización completada")
        print(f"   Altura blockchain: {len(self.blockchain.chain)} bloques")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _discover_peers(self):
        """Descubre nuevos peers"""
        print("\n🔍 DESCUBRIR PEERS")
        print("="*60)
    
        print("\nIngresa nodos semilla (host:puerto), uno por línea")
        print("Deja vacío para terminar:")
    
        seed_nodes = []
        while True:
            seed = input("> ").strip()
            if not seed:
                break
        
            try:
                host, port = seed.split(':')
                seed_nodes.append((host, int(port)))
            except:
                print("❌ Formato inválido. Usa: host:puerto")
    
        if not seed_nodes:
            print("\n❌ No se ingresaron nodos semilla")
            input("Presiona Enter para continuar...")
            return
    
        print(f"\n🔄 Descubriendo peers a través de {len(seed_nodes)} nodos semilla...")
        discovered = self.p2p_node.discover_peers(seed_nodes)
    
        print(f"\n✅ Descubrimiento completado")
        print(f"   Peers descubiertos: {discovered}")
        print(f"   Total peers: {len(self.p2p_node.peers)}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _stop_node(self):
        """Detiene el nodo P2P"""
        confirm = input("\n¿Detener el nodo P2P? (S/n): ").strip().lower()
    
        if confirm != 'n':
            self.p2p_node.stop()
            self.p2p_node = None
            print("\n🛑 Nodo P2P detenido\n")
    
        input("Presiona Enter para continuar...")


    def _create_timelock(self):
        """Crea un contrato timelock"""
        if not self.wallet:
            print("\n❌ Primero debes cargar una wallet\n")
            input("Presiona Enter para continuar...")
            return
    
        print("\n📜 CREAR CONTRATO TIMELOCK")
        print("="*60)
    
        try:
            unlock_block = int(input("Número de bloque para desbloquear: ").strip())
            amount = float(input("Cantidad de CLC: ").strip())
            recipient = input("Dirección del destinatario: ").strip()
        
            contract = self.contract_manager.create_timelock(
                creator=self.wallet.get_address(),
                unlock_block=unlock_block,
                amount=amount,
                recipient=recipient
            )
        
            print(f"\n✅ Contrato Timelock creado")
            print(f"   ID: {contract.contract_id}")
            print(f"   Se desbloqueará en bloque: {unlock_block}")
            print(f"   Cantidad: {amount} CLC")
            print(f"   Destinatario: {recipient[:20]}...")
        
        except ValueError:
            print("❌ Valor inválido\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _create_multisig(self):
        """Crea un contrato multisig"""
        if not self.wallet:
            print("\n❌ Primero debes cargar una wallet\n")
            input("Presiona Enter para continuar...")
            return
    
        print("\n📜 CREAR CONTRATO MULTISIG")
        print("="*60)
    
        try:
            required_sigs = int(input("Firmas requeridas: ").strip())
            num_signers = int(input("Número total de firmantes: ").strip())
        
            signers = []
            print("\nIngresa las direcciones de los firmantes:")
            for i in range(num_signers):
                signer = input(f"  Firmante {i+1}: ").strip()
                signers.append(signer)
        
            amount = float(input("\nCantidad de CLC: ").strip())
            recipient = input("Dirección del destinatario: ").strip()
        
            contract = self.contract_manager.create_multisig(
                creator=self.wallet.get_address(),
                required_sigs=required_sigs,
                signers=signers,
                amount=amount,
                recipient=recipient
            )
        
            print(f"\n✅ Contrato Multisig creado")
            print(f"   ID: {contract.contract_id}")
            print(f"   Requiere: {required_sigs} de {num_signers} firmas")
            print(f"   Cantidad: {amount} CLC")
        
        except ValueError:
            print("❌ Valor inválido\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _create_escrow(self):
        """Crea un contrato escrow"""
        if not self.wallet:
            print("\n❌ Primero debes cargar una wallet\n")
            input("Presiona Enter para continuar...")
            return
    
        print("\n📜 CREAR CONTRATO ESCROW")
        print("="*60)
    
        try:
            buyer = input("Dirección del comprador: ").strip()
            seller = input("Dirección del vendedor: ").strip()
            arbiter = input("Dirección del árbitro: ").strip()
            amount = float(input("Cantidad de CLC: ").strip())
        
            contract = self.contract_manager.create_escrow(
                creator=self.wallet.get_address(),
                buyer=buyer,
                seller=seller,
                arbiter=arbiter,
                amount=amount
            )
        
            print(f"\n✅ Contrato Escrow creado")
            print(f"   ID: {contract.contract_id}")
            print(f"   Comprador: {buyer[:20]}...")
            print(f"   Vendedor: {seller[:20]}...")
            print(f"   Árbitro: {arbiter[:20]}...")
            print(f"   Cantidad: {amount} CLC")
        
        except ValueError:
            print("❌ Valor inválido\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _list_contracts(self):
        """Lista todos los contratos"""
        print("\n📜 CONTRATOS")
        print("="*60)
    
        contracts = self.contract_manager.list_contracts()
    
        if not contracts:
            print("\nNo hay contratos creados")
        else:
            for contract in contracts:
                info = contract.get_info()
                status = "✅ Ejecutado" if contract.executed else "⏳ Pendiente"
            
                print(f"\n{contract.contract_id}: {info['type']}")
                print(f"  Estado: {status}")
            
                if contract.contract_type == ContractType.TIMELOCK:
                    print(f"  Desbloqueo: Bloque {info['unlock_block']}")
                    print(f"  Cantidad: {info['amount']} CLC")
                elif contract.contract_type == ContractType.MULTISIG:
                    print(f"  Firmas: {info['status']}")
                    print(f"  Cantidad: {info['amount']} CLC")
                elif contract.contract_type == ContractType.ESCROW:
                    print(f"  Estado: {info['status']}")
                    print(f"  Cantidad: {info['amount']} CLC")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _view_contract(self):
        """Ver detalles de un contrato"""
        contract_id = input("\nID del contrato: ").strip()
    
        contract = self.contract_manager.get_contract(contract_id)
    
        if not contract:
            print(f"❌ Contrato {contract_id} no encontrado\n")
            input("Presiona Enter para continuar...")
            return
    
        print("\n" + "="*60)
        print(f"CONTRATO {contract_id}")
        print("="*60)
    
        info = contract.get_info()
    
        print(f"\nTipo: {info['type']}")
        print(f"Creador: {contract.creator[:20]}...")
        print(f"Estado: {'✅ Ejecutado' if contract.executed else '⏳ Pendiente'}")
    
        for key, value in info.items():
            if key != 'type':
                print(f"{key}: {value}")
    
        if contract.execution_result:
            print(f"\nResultado de ejecución:")
            print(f"  Éxito: {contract.execution_result['success']}")
            print(f"  Gas usado: {contract.execution_result.get('gas_used', 'N/A')}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _execute_contract(self):
        """Ejecuta un contrato"""
        contract_id = input("\nID del contrato: ").strip()
    
        contract = self.contract_manager.get_contract(contract_id)
    
        if not contract:
            print(f"❌ Contrato {contract_id} no encontrado\n")
            input("Presiona Enter para continuar...")
            return
    
        if contract.executed:
            print(f"❌ El contrato ya fue ejecutado\n")
            input("Presiona Enter para continuar...")
            return
    
        print(f"\n⚙️  Ejecutando contrato {contract_id}...")
    
        context = {'block_height': len(self.blockchain.chain)}
        success, msg = self.contract_manager.execute_contract(contract_id, context)
    
        if success:
            print(f"✅ {msg}")
            if contract.execution_result:
                print(f"   Gas usado: {contract.execution_result['gas_used']}")
        else:
            print(f"❌ {msg}")
    
        input("\nPresiona Enter para continuar...")

    def _sign_multisig(self):
        """Firma un contrato multisig"""
        if not self.wallet:
            print("\n❌ Primero debes cargar una wallet\n")
            input("Presiona Enter para continuar...")
            return
    
        contract_id = input("\nID del contrato Multisig: ").strip()

        contract = self.contract_manager.get_contract(contract_id)
    
        if not contract:
            print(f"❌ Contrato {contract_id} no encontrado\n")
            input("Presiona Enter para continuar...")
            return
    
        if contract.contract_type != ContractType.MULTISIG:
            print(f"❌ El contrato no es tipo Multisig\n")
            input("Presiona Enter para continuar...")
            return
    
        success = contract.add_signature(self.wallet.get_address())
    
        if success:
            print(f"✅ Firma agregada exitosamente")
            info = contract.get_info()
            print(f"   Estado: {info['status']}")
            self.contract_manager.save_contracts()
        else:
            print(f"❌ No puedes firmar este contrato")
    
        input("\nPresiona Enter para continuar...")

    def _decide_escrow(self):
        """Decide un contrato escrow"""
        if not self.wallet:
            print("\n❌ Primero debes cargar una wallet\n")
            input("Presiona Enter para continuar...")
            return
    
        contract_id = input("\nID del contrato Escrow: ").strip()
    
        contract = self.contract_manager.get_contract(contract_id)
    
        if not contract:
            print(f"❌ Contrato {contract_id} no encontrado\n")
            input("Presiona Enter para continuar...")
            return
    
        if contract.contract_type != ContractType.ESCROW:
            print(f"❌ El contrato no es tipo Escrow\n")
            input("Presiona Enter para continuar...")
            return
    
        decision = input("\n¿Aprobar transacción? (S/n): ").strip().lower()
        approve = decision != 'n'
    
        success, msg = contract.make_decision(self.wallet.get_address(), approve)
    
        if success:
            print(f"✅ {msg}")
            self.contract_manager.save_contracts()
        else:
            print(f"❌ {msg}")
    
        input("\nPresiona Enter para continuar...")



    def _show_difficulty_info(self):
        """Muestra información sobre la dificultad"""
        from blockchain.difficulty import DifficultyAdjustment
    
        info = DifficultyAdjustment.get_adjustment_info(self.blockchain)
    
        print("\n" + "="*60)
        print("⚙️  INFORMACIÓN DE DIFICULTAD")
        print("="*60)
    
        print(f"\n📊 Estado Actual:")
        print(f"   Dificultad: {info['current_difficulty']} ceros")
        print(f"   Tiempo promedio por bloque: {info['current_avg_time']:.2f}s")
        print(f"   Tiempo objetivo: {info['target_block_time']}s")
    
        if info['current_avg_time'] > 0:
            if info['current_avg_time'] < info['target_block_time'] * 0.5:
                status = "⚡ Muy rápido"
            elif info['current_avg_time'] < info['target_block_time'] * 0.75:
                status = "🔥 Rápido"
            elif info['current_avg_time'] > info['target_block_time'] * 2:
                status = "🐌 Muy lento"
            elif info['current_avg_time'] > info['target_block_time'] * 1.5:
                status = "🕐 Lento"
            else:
                status = "✅ Óptimo"
            print(f"   Estado: {status}")
    
        print(f"\n🔧 Ajuste Automático:")
        estado = "✅ Habilitado" if info['adjustment_enabled'] else "❌ Deshabilitado"
        print(f"   Estado: {estado}")
        print(f"   Intervalo: cada {info['adjustment_interval']} bloques")
        print(f"   Bloques hasta próximo ajuste: {info['blocks_until_adjustment']}")
    
        print(f"\n📈 Límites:")
        print(f"   Dificultad mínima: {info['min_difficulty']}")
        print(f"   Dificultad máxima: {info['max_difficulty']}")
    
        # Complejidad estimada
        attempts = 16 ** info['current_difficulty']
        print(f"\n💪 Complejidad:")
        print(f"   Intentos promedio: ~{attempts:,}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _set_manual_difficulty(self):
        """Configura dificultad manualmente"""
        print("\n⚙️  CONFIGURAR DIFICULTAD MANUAL")
        print(f"   Dificultad actual: {self.blockchain.difficulty}")
        print(f"   Rango permitido: {config.MIN_DIFFICULTY} - {config.MAX_DIFFICULTY}")
    
        try:
            new_diff = int(input("\nNueva dificultad: ").strip())
        
            if new_diff < config.MIN_DIFFICULTY or new_diff > config.MAX_DIFFICULTY:
                print(f"❌ Dificultad fuera de rango ({config.MIN_DIFFICULTY}-{config.MAX_DIFFICULTY})\n")
                input("Presiona Enter para continuar...")
                return
        
            old_diff = self.blockchain.difficulty
            self.blockchain.difficulty = new_diff
        
            print(f"\n✅ Dificultad cambiada: {old_diff} → {new_diff}")
        
            # Calcular complejidad
            attempts = 16 ** new_diff
            print(f"   Intentos promedio: ~{attempts:,}")
        
        except ValueError:
            print("❌ Valor inválido\n")
    
        input("\nPresiona Enter para continuar...")

    def _toggle_auto_adjustment(self):
        """Habilita/deshabilita ajuste automático"""
        current = config.DIFFICULTY_ADJUSTMENT_ENABLED
        estado_actual = "Habilitado" if current else "Deshabilitado"
    
        print(f"\n⚙️  AJUSTE AUTOMÁTICO DE DIFICULTAD")
        print(f"   Estado actual: {estado_actual}")
    
        nuevo = input("\n¿Habilitar ajuste automático? (S/n): ").strip().lower()
    
        if nuevo == 's':
            config.DIFFICULTY_ADJUSTMENT_ENABLED = True
            print("✅ Ajuste automático habilitado")
        else:
            config.DIFFICULTY_ADJUSTMENT_ENABLED = False
            print("❌ Ajuste automático deshabilitado")
    
        input("\nPresiona Enter para continuar...")

    def _set_target_block_time(self):
        """Configura el tiempo objetivo entre bloques"""
        print(f"\n⚙️  CONFIGURAR TIEMPO OBJETIVO")
        print(f"   Tiempo actual: {config.TARGET_BLOCK_TIME}s")
    
        try:
            new_time = int(input("\nNuevo tiempo objetivo (segundos): ").strip())
        
            if new_time < 1 or new_time > 3600:
                print("❌ Tiempo fuera de rango (1-3600 segundos)\n")
                input("Presiona Enter para continuar...")
                return
        
            old_time = config.TARGET_BLOCK_TIME
            config.TARGET_BLOCK_TIME = new_time
        
            print(f"\n✅ Tiempo objetivo cambiado: {old_time}s → {new_time}s")
        
        except ValueError:
            print("❌ Valor inválido\n")
    
        input("\nPresiona Enter para continuar...")

    def _set_adjustment_interval(self):
        """Configura el intervalo de ajuste"""
        print(f"\n⚙️  CONFIGURAR INTERVALO DE AJUSTE")
        print(f"   Intervalo actual: cada {config.DIFFICULTY_ADJUSTMENT_INTERVAL} bloques")
    
        try:
            new_interval = int(input("\nNuevo intervalo (bloques): ").strip())
        
            if new_interval < 1 or new_interval > 1000:
                print("❌ Intervalo fuera de rango (1-1000 bloques)\n")
                input("Presiona Enter para continuar...")
                return
        
            old_interval = config.DIFFICULTY_ADJUSTMENT_INTERVAL
            config.DIFFICULTY_ADJUSTMENT_INTERVAL = new_interval
        
            print(f"\n✅ Intervalo cambiado: cada {old_interval} → {new_interval} bloques")
        
        except ValueError:
            print("❌ Valor inválido\n")
    
        input("\nPresiona Enter para continuar...")

    def faucet_menu(self):
        """Muestra el menú del faucet"""
        if not self.blockchain:
            print("\n❌ Primero debes crear o cargar una blockchain\n")
            return
    
        faucet = Faucet(self.blockchain)
    
        while True:
            print("\n🎁 FAUCET - CLC GRATIS")
            print("  1. Reclamar CLC gratis")
            print("  2. Ver información del faucet")
            print("  3. Ver mi historial de reclamos")
            print("  4. Donar al faucet")
            print("  5. Financiar faucet (minando)")
            print("  0. Volver al menú principal")
            print()
        
            choice = input("Selecciona una opción: ").strip()
        
            if choice == '1':
                self._claim_from_faucet(faucet)
            elif choice == '2':
                self._show_faucet_info(faucet)
            elif choice == '3':
                self._show_my_claims(faucet)
            elif choice == '4':
                self._donate_to_faucet(faucet)
            elif choice == '5':
                self._fund_faucet_by_mining(faucet)
            elif choice == '0':
                break
            else:
                print("\n❌ Opción inválida\n")

    def _claim_from_faucet(self, faucet):
        """Reclama CLC del faucet"""
        if not self.wallet:
            print("\n❌ Primero debes crear o cargar una wallet\n")
            input("Presiona Enter para continuar...")
            return
    
        print(f"\n🎁 RECLAMAR {config.FAUCET_AMOUNT} CLC GRATIS")
        print("="*60)
    
        wallet_addr = self.wallet.get_address()
        balance = self.blockchain.get_balance(wallet_addr)
    
        print(f"Tu wallet: {self.wallet.name}")
        print(f"Balance actual: {balance} CLC")
        print(f"Recibirás: {config.FAUCET_AMOUNT} CLC")
    
        # Verificar elegibilidad
        can_claim, message = faucet.can_claim(wallet_addr)
    
        if not can_claim:
            print(f"\n❌ {message}\n")
            input("Presiona Enter para continuar...")
            return
    
        print(f"\n✅ {message}")
        confirm = input("\n¿Confirmar reclamo? (S/n): ").strip().lower()
    
        if confirm == 'n':
            print("❌ Reclamo cancelado\n")
            input("Presiona Enter para continuar...")
            return
    
        success, msg = faucet.claim(wallet_addr)
    
        if success:
            print(f"\n✅ {msg}")
            print("\n⚠️  IMPORTANTE: La transacción está pendiente.")
            print("    Debes minar un bloque para confirmarla.")
            print(f"    Después tendrás {balance + config.FAUCET_AMOUNT} CLC")
        else:
            print(f"\n❌ {msg}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _show_faucet_info(self, faucet):
        """Muestra información del faucet"""
        info = faucet.get_faucet_info()
    
        print("\n" + "="*60)
        print("🎁 INFORMACIÓN DEL FAUCET")
        print("="*60)
    
        status = "✅ Habilitado" if info['enabled'] else "❌ Deshabilitado"
        print(f"\nEstado: {status}")
        print(f"Cantidad por reclamo: {info['amount_per_claim']} {config.COIN_SYMBOL}")
        print(f"Cooldown: {info['cooldown_hours']} horas")
        print(f"Balance máximo permitido: {info['max_balance_allowed']} {config.COIN_SYMBOL}")
    
        print(f"\n💰 Fondos del faucet:")
        print(f"   Balance actual: {info['faucet_balance']} {config.COIN_SYMBOL}")
        reclamos_disponibles = int(info['faucet_balance'] / info['amount_per_claim'])
        print(f"   Reclamos disponibles: ~{reclamos_disponibles}")
    
        print(f"\n📊 Estadísticas:")
        print(f"   Usuarios que han reclamado: {info['total_users']}")
        print(f"   Total distribuido: {info['total_distributed']} {config.COIN_SYMBOL}")
    
        print(f"\n📍 Dirección del faucet:")
        print(f"   {info['faucet_address']}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _show_my_claims(self, faucet):
        """Muestra el historial de reclamos del usuario"""
        if not self.wallet:
            print("\n❌ Primero debes crear o cargar una wallet\n")
            input("Presiona Enter para continuar...")
            return
    
        claim_info = faucet.get_claim_info(self.wallet.get_address())
    
        print("\n" + "="*60)
        print("📜 MI HISTORIAL DE RECLAMOS")
        print("="*60)
        print(f"\nWallet: {self.wallet.name}")
    
        if not claim_info['has_claimed']:
            print("\n📭 Aún no has reclamado del faucet")
            print(f"✅ Puedes reclamar ahora mismo!")
        else:
            print(f"\n✅ Has reclamado {claim_info['claim_count']} veces")
            print(f"💰 Total reclamado: {claim_info['total_claimed']} {config.COIN_SYMBOL}")
            print(f"📅 Último reclamo: {claim_info['last_claim'].strftime('%Y-%m-%d %H:%M:%S')}")
        
            from datetime import datetime
            now = datetime.now()
            if now >= claim_info['can_claim_at']:
                print(f"\n✅ Puedes reclamar ahora")
            else:
                time_left = claim_info['can_claim_at'] - now
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                print(f"\n⏰ Próximo reclamo disponible en: {hours}h {minutes}m")
                print(f"   Fecha: {claim_info['can_claim_at'].strftime('%Y-%m-%d %H:%M:%S')}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _donate_to_faucet(self, faucet):
        """Permite donar CLC al faucet"""
        if not self.wallet:
            print("\n❌ Primero debes crear o cargar una wallet\n")
            input("Presiona Enter para continuar...")
            return
   
        balance = self.blockchain.get_balance(self.wallet.get_address())
    
        print("\n" + "="*60)
        print("💝 DONAR AL FAUCET")
        print("="*60)
        print(f"\nTu balance: {balance} {config.COIN_SYMBOL}")
    
        if balance <= 0:
            print("❌ No tienes fondos para donar\n")
            input("Presiona Enter para continuar...")
            return
    
        try:
            amount = float(input("\nCantidad a donar: ").strip())
        
            if amount <= 0:
                print("❌ La cantidad debe ser mayor a 0\n")
                input("Presiona Enter para continuar...")
                return
        
            if amount > balance:
                print(f"❌ Fondos insuficientes. Balance: {balance} {config.COIN_SYMBOL}\n")
                input("Presiona Enter para continuar...")
                return
        
            confirm = input(f"\n¿Donar {amount} CLC al faucet? (S/n): ").strip().lower()
        
            if confirm == 'n':
                print("❌ Donación cancelada\n")
                input("Presiona Enter para continuar...")
                return
        
            success, msg = faucet.fund_faucet(amount, self.wallet)
        
            if success:
                print(f"\n✅ {msg}")
                print("   ¡Gracias por ayudar a la comunidad!")
                print("   La donación se confirmará al minar el próximo bloque")
            else:
                print(f"\n❌ {msg}")
        
        except ValueError:
            print("❌ Cantidad inválida\n")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _fund_faucet_by_mining(self, faucet):
        """Mina un bloque para el faucet"""
        print("\n" + "="*60)
        print("⛏️  FINANCIAR FAUCET MINANDO")
        print("="*60)
        print("\nEsto minará un bloque usando la wallet del faucet.")
        print(f"El faucet recibirá {config.MINING_REWARD} {config.COIN_SYMBOL}")
    
        confirm = input("\n¿Continuar? (S/n): ").strip().lower()
    
        if confirm == 'n':
            print("❌ Cancelado\n")
            input("Presiona Enter para continuar...")
            return
    
        print(f"\n⛏️  Minando para el faucet...")
        print(f"   Transacciones pendientes: {len(self.blockchain.pending_transactions)}")
    
        # Guardar wallet actual
        current_wallet = self.wallet
    
        # Temporalmente usar la wallet del faucet
        self.wallet = faucet.faucet_wallet
    
        # Minar
        block = self.blockchain.mine_pending_transactions(faucet.faucet_wallet.get_address())
    
        # Restaurar wallet
        self.wallet = current_wallet
    
        new_balance = self.blockchain.get_balance(faucet.faucet_wallet.get_address())
    
        print(f"\n✅ ¡Bloque minado exitosamente!")
        print(f"   Nuevo balance del faucet: {new_balance} {config.COIN_SYMBOL}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")


    def _show_complete_dashboard(self, stats):
        """Muestra el dashboard completo"""
        dashboard = stats.get_complete_dashboard()
    
        print("\n" + "="*70)
        print(" "*20 + "📊 DASHBOARD COLCRIPT")
        print("="*70)
    
        # Supply
        supply = dashboard['supply']
        print(f"\n💰 SUPPLY:")
        print(f"   Total: {supply['total']:,} {config.COIN_SYMBOL}")
        print(f"   En circulación: {supply['circulating']:,} {config.COIN_SYMBOL}")
        print(create_progress_bar(
            supply['circulating'], 
            supply['total'], 
            width=50,
            label="   Progreso"
        ))
        print(f"   Porcentaje minado: {supply['percentage']:.4f}%")
    
        # Wallets
        wallets_info = dashboard['wallets']
        print(f"\n💼 WALLETS:")
        print(f"   Total de wallets activas: {wallets_info['total_wallets']}")
        print(f"\n   Top 5 Wallets:")
        top_data = [
            (f"{addr[:15]}...", balance)
            for addr, balance in wallets_info['top_wallets']
        ]
        if top_data:
            print("   " + "\n   ".join(create_bar_chart(top_data, max_width=40).split("\n")))
    
        # Distribución
        dist = wallets_info['distribution']
        print(f"\n   Distribución de riqueza:")
        print(f"   " + create_percentage_bar("Top 1% controla", dist['top_1_percent'], width=35))
        print(f"   " + create_percentage_bar("Top 10% controla", dist['top_10_percent'], width=35))
        print(f"   Balance mediano: {dist['median_balance']:.2f} {config.COIN_SYMBOL}")
    
        # Minería
        mining = dashboard['mining']
        print(f"\n⛏️  MINERÍA:")
        print(f"   Mineros activos: {mining['total_miners']}")
        print(f"   Bloques minados: {mining['total_blocks_mined']}")
        print(f"   Tiempo promedio por bloque: {mining['avg_block_time']:.2f}s")
        if mining['top_miner']:
            print(f"   Top minero: {mining['top_miner'][:30]}...")
            print(f"   Bloques del top minero: {mining['top_miner_blocks']}")
    
        # Transacciones
        tx = dashboard['transactions']
        print(f"\n💸 TRANSACCIONES:")
        print(f"   Total: {tx['total_transactions']}")
        print(f"   Transferencias: {tx['transfers']}")
        print(f"   Recompensas de minado: {tx['mining_rewards']}")
        print(f"   Volumen total: {tx['total_volume']:,} {config.COIN_SYMBOL}")
        print(f"   Fees pagados: {tx['total_fees_paid']:.2f} {config.COIN_SYMBOL}")
    
        # Red
        net = dashboard['network']
        print(f"\n🌐 SALUD DE LA RED:")
        status = "✅ Válida" if net['blockchain_valid'] else "❌ Inválida"
        print(f"   Estado: {status}")
        print(f"   Bloques totales: {net['total_blocks']}")
        print(f"   Dificultad: {net['network_difficulty']}")
        print(f"   " + create_percentage_bar("Descentralización", net['decentralization_score'], width=35))
    
        print("\n" + "="*70)
        input("\nPresiona Enter para continuar...")

    def _show_supply_stats(self, stats):
        """Muestra estadísticas de supply"""
        total = stats.get_total_supply()
        circulating = stats.get_circulating_supply()
        percentage = stats.get_supply_percentage()
    
        print("\n" + "="*60)
        print("💰 ESTADÍSTICAS DE SUPPLY")
        print("="*60)
        print(f"\nTotal configurado: {total:,} {config.COIN_SYMBOL}")
        print(f"En circulación: {circulating:,} {config.COIN_SYMBOL}")
        print(f"Por minar: {total - circulating:,} {config.COIN_SYMBOL}")
        print(f"\n{create_progress_bar(circulating, total, width=50, label='Progreso de minado')}")
        print(f"\nPorcentaje minado: {percentage:.6f}%")
    
        # Proyecciones
        blocks_needed = (total - circulating) / config.MINING_REWARD
        print(f"\nBloques necesarios para minar todo: {int(blocks_needed):,}")
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _show_top_wallets(self, stats):
        """Muestra ranking de wallets"""
        top_wallets = stats.get_top_wallets(10)
    
        print("\n" + "="*70)
        print("🏆 TOP 10 WALLETS")
        print("="*70)
    
        if not top_wallets:
            print("\nNo hay wallets con balance")
        else:
            headers = ["#", "Dirección", "Balance"]
            rows = []
            for i, (addr, balance) in enumerate(top_wallets, 1):
                short_addr = addr[:40] + "..."
                rows.append([str(i), short_addr, f"{balance:.2f} {config.COIN_SYMBOL}"])
        
            print(print_table(headers, rows, [5, 45, 18]))
        
            # Gráfico de barras
            print("\nVisualización:")
            chart_data = [
                (f"#{i} {addr[:12]}...", balance)
                for i, (addr, balance) in enumerate(top_wallets, 1)
            ]
            print(create_bar_chart(chart_data, max_width=40))
    
        print("="*70)
        input("\nPresiona Enter para continuar...")

    def _show_wealth_distribution(self, stats):
        """Muestra distribución de riqueza"""
        dist = stats.get_wealth_distribution()
        circulating = stats.get_circulating_supply()
    
        print("\n" + "="*60)
        print("📊 DISTRIBUCIÓN DE RIQUEZA")
        print("="*60)
        print(f"\nTotal de wallets: {dist['total_wallets']}")
        print(f"CLC en circulación: {circulating:,}")
        print(f"Balance mediano: {dist['median_balance']:.2f} {config.COIN_SYMBOL}")
    
        print(f"\n{create_percentage_bar('Top 1% de wallets controla', dist['top_1_percent'], width=40)}")
        print(f"{create_percentage_bar('Top 10% de wallets controla', dist['top_10_percent'], width=40)}")
    
        # Interpretación
        print("\n💡 Interpretación:")
        if dist['top_1_percent'] > 50:
            print("   ⚠️  Alta concentración de riqueza")
        elif dist['top_1_percent'] > 30:
            print("   ℹ️  Concentración moderada")
        else:
            print("   ✅ Distribución relativamente equitativa")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _show_mining_stats(self, stats):
        """Muestra estadísticas de minería"""
        mining = stats.get_mining_stats()
    
        print("\n" + "="*60)
        print("⛏️  ESTADÍSTICAS DE MINERÍA")
        print("="*60)
        print(f"\nMineros activos: {mining['total_miners']}")
        print(f"Bloques minados: {mining['total_blocks_mined']}")
        print(f"Tiempo promedio por bloque: {mining['avg_block_time']:.2f} segundos")
        print(f"Nonce promedio: {mining['avg_nonce']:,.0f}")
    
        if mining['top_miner']:
            print(f"\n🏆 Top Minero:")
            print(f"   Dirección: {mining['top_miner'][:50]}...")
            print(f"   Bloques minados: {mining['top_miner_blocks']}")
            percentage = (mining['top_miner_blocks'] / mining['total_blocks_mined'] * 100) if mining['total_blocks_mined'] > 0 else 0
            print(f"   {create_percentage_bar('Participación', percentage, width=35)}")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _show_transaction_stats(self, stats):
        """Muestra estadísticas de transacciones"""
        tx = stats.get_transaction_stats()
    
        print("\n" + "="*60)
        print("💸 ESTADÍSTICAS DE TRANSACCIONES")
        print("="*60)
        print(f"\nTotal de transacciones: {tx['total_transactions']}")
        print(f"   Transferencias: {tx['transfers']}")
        print(f"   Recompensas de minado: {tx['mining_rewards']}")
    
        print(f"\nVolumen total: {tx['total_volume']:,} {config.COIN_SYMBOL}")
        print(f"Fees pagados: {tx['total_fees_paid']:.2f} {config.COIN_SYMBOL}")
        print(f"Promedio tx por bloque: {tx['avg_tx_per_block']:.2f}")
    
        # Gráfico de distribución
        if tx['transfers'] > 0 or tx['mining_rewards'] > 0:
            print("\nDistribución por tipo:")
            type_data = [
                ("Transferencias", tx['transfers']),
                ("Recompensas", tx['mining_rewards'])
            ]
            print(create_bar_chart(type_data, max_width=40))
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    def _show_network_health(self, stats):
        """Muestra salud de la red"""
        net = stats.get_network_health()
    
        print("\n" + "="*60)
        print("🌐 SALUD DE LA RED")
        print("="*60)
    
        status = "✅ VÁLIDA" if net['blockchain_valid'] else "❌ INVÁLIDA"
        print(f"\nEstado de blockchain: {status}")
        print(f"Total de bloques: {net['total_blocks']}")
        print(f"Dificultad actual: {net['network_difficulty']}")
        print(f"Recompensa por bloque: {net['block_reward']} {config.COIN_SYMBOL}")
    
        print(f"\n{create_percentage_bar('Score de descentralización', net['decentralization_score'], width=40)}")
    
        # Interpretación
        print("\n💡 Evaluación:")
        if not net['blockchain_valid']:
            print("   ❌ La blockchain tiene problemas de integridad")
        else:
            print("   ✅ La blockchain es íntegra y válida")
    
        if net['decentralization_score'] > 80:
            print("   ✅ Red altamente descentralizada")
        elif net['decentralization_score'] > 50:
            print("   ℹ️  Descentralización moderada")
        else:
            print("   ⚠️  Red concentrada, considera más mineros")
    
        print("="*60)
        input("\nPresiona Enter para continuar...")

    
    def _navigate_blocks(self, explorer):
        """Navegación interactiva por bloques"""
        current = 0
        max_block = len(self.blockchain.chain) - 1
        
        while True:
            block = explorer.get_block_by_number(current)
            if not block:
                break
            
            print("\n" + "="*70)
            print(f"📍 NAVEGANDO: Bloque {current} de {max_block}")
            print("="*70)
            
            explorer.print_block_summary(block)
            
            print("\nNavegación:")
            if current > 0:
                print("  [P] Bloque anterior")
            if current < max_block:
                print("  [N] Bloque siguiente")
            print("  [D] Ver detalles completos")
            print(f"  [G] Ir a bloque específico (0-{max_block})")
            print("  [V] Volver al explorador")
            print()
            
            nav = input("Opción: ").strip().upper()
            
            if nav == 'P' and current > 0:
                current -= 1
            elif nav == 'N' and current < max_block:
                current += 1
            elif nav == 'D':
                explorer.print_block_detailed(block)
                input("\nPresiona Enter para continuar...")
            elif nav == 'G':
                try:
                    goto = int(input(f"Ir al bloque (0-{max_block}): ").strip())
                    if 0 <= goto <= max_block:
                        current = goto
                    else:
                        print(f"❌ Debe ser entre 0 y {max_block}")
                        input("\nPresiona Enter para continuar...")
                except ValueError:
                    print("❌ Número inválido")
                    input("\nPresiona Enter para continuar...")
            elif nav == 'V':
                break
            else:
                print("❌ Opción inválida")
                input("\nPresiona Enter para continuar...")

    def send_coins(self):
        """Envía ColCript a otra dirección"""
        if not self.wallet:
            print("\n❌ Primero debes crear o cargar una wallet\n")
            return
    
        if not self.blockchain:
            print("\n❌ Primero debes crear una blockchain\n")
            return
    
        balance = self.wallet.get_balance(self.blockchain)
        print(f"\n💸 Enviar {config.COIN_SYMBOL}")
        print(f"   Balance actual: {balance} {config.COIN_SYMBOL}")
    
        recipient = input("   Dirección destino: ").strip()
        if not recipient:
            print("❌ Dirección inválida\n")
            return
    
        try:
            amount = float(input("   Cantidad: ").strip())
            if amount <= 0:
                print("❌ La cantidad debe ser mayor a 0\n")
                return
        
            # Preguntar por el fee
            print(f"\n💰 Configuración de fee:")
            print(f"   Mínimo: {config.MIN_TRANSACTION_FEE} CLC")
            print(f"   Recomendado: {config.DEFAULT_TRANSACTION_FEE} CLC")
            print(f"   Máximo: {config.MAX_TRANSACTION_FEE} CLC")
        
            fee_input = input(f"   Fee (Enter para usar {config.DEFAULT_TRANSACTION_FEE} CLC): ").strip()
        
            if fee_input:
                fee = float(fee_input)
                if fee < config.MIN_TRANSACTION_FEE:
                    print(f"⚠️  Fee muy bajo, usando mínimo: {config.MIN_TRANSACTION_FEE} CLC")
                    fee = config.MIN_TRANSACTION_FEE
                elif fee > config.MAX_TRANSACTION_FEE:
                    print(f"⚠️  Fee muy alto, usando máximo: {config.MAX_TRANSACTION_FEE} CLC")
                    fee = config.MAX_TRANSACTION_FEE
            else:
                fee = config.DEFAULT_TRANSACTION_FEE
        
            # Verificar fondos incluyendo fee
            total_cost = amount + fee
            if total_cost > balance:
                print(f"❌ Fondos insuficientes.")
                print(f"   Necesitas: {total_cost} CLC (cantidad: {amount} + fee: {fee})")
                print(f"   Tienes: {balance} {config.COIN_SYMBOL}\n")
                return
        
            print(f"\n📋 Resumen de la transacción:")
            print(f"   Cantidad: {amount} CLC")
            print(f"   Fee: {fee} CLC")
            print(f"   Total a descontar: {total_cost} CLC")
        
            confirm = input("\n¿Confirmar transacción? (S/n): ").strip().lower()
            if confirm == 'n':
                print("❌ Transacción cancelada\n")
                return
        
            transaction = self.wallet.send_coins(recipient, amount, fee)
            if transaction:
                self.blockchain.add_transaction(transaction)
                print(f"✅ Transacción agregada al pool de transacciones pendientes\n")
        except ValueError:
            print("❌ Valor inválido\n")

    def mine_block(self):
        """Mina un nuevo bloque"""
        if not self.wallet:
            print("\n❌ Primero debes crear o cargar una wallet\n")
            return
        
        if not self.blockchain:
            print("\n❌ Primero debes crear una blockchain\n")
            return
        
        print(f"\n⛏️  Minando bloque para '{self.wallet.name}'...")
        print(f"   Transacciones pendientes: {len(self.blockchain.pending_transactions)}")
        
        block = self.blockchain.mine_pending_transactions(self.wallet.get_address())
        
        print(f"\n✅ ¡Bloque minado exitosamente!")
        print(f"   Recompensa: {config.MINING_REWARD} {config.COIN_SYMBOL}")
        print(f"   Nuevo balance: {self.wallet.get_balance(self.blockchain)} {config.COIN_SYMBOL}\n")
    
    def view_blockchain(self):
        """Muestra información de la blockchain"""
        if not self.blockchain:
            print("\n❌ Primero debes crear una blockchain\n")
            return
        
        print(f"\n⛓️  BLOCKCHAIN {config.COIN_NAME}")
        print(f"   Total de bloques: {len(self.blockchain.chain)}")
        print(f"   Transacciones pendientes: {len(self.blockchain.pending_transactions)}")
        print(f"   Válida: {self.blockchain.is_chain_valid()}\n")
        
        for i, block in enumerate(self.blockchain.chain[-5:]):
            print(f"   Bloque #{block.index}:")
            print(f"     Hash: {block.hash[:40]}...")
            print(f"     Transacciones: {len(block.transactions)}")
            print(f"     Minero: {block.miner_address[:30]}...")
            print()
    
    def view_info(self):
        """Muestra información general"""
        info = {
            'Nombre': config.COIN_NAME,
            'Símbolo': config.COIN_SYMBOL,
            'Supply Total': f"{config.TOTAL_SUPPLY:,}",
            'Recompensa de Minado': config.MINING_REWARD,
            'Dificultad': config.MINING_DIFFICULTY,
            'Versión': config.VERSION
        }
        
        print(f"\n📊 INFORMACIÓN DE {config.COIN_NAME}:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        print()
    
    def save_wallet(self):
        """Guarda la wallet actual"""
        if not self.wallet:
            print("\n❌ No hay wallet para guardar\n")
            return
        
        self.wallet.save_to_file()
        print()
    
    def save_blockchain_manually(self):
        """Guarda la blockchain manualmente"""
        if not self.blockchain:
            print("\n❌ No hay blockchain para guardar\n")
            return
        
        filename = input("\nNombre del archivo (Enter para usar actual): ").strip()
        
        if not filename:
            filename = getattr(self.blockchain, 'save_filename', 'colcript_manual.json')
        
        self.storage.save_blockchain(self.blockchain, filename)
        print()
    
    def run(self):
        """Ejecuta la interfaz CLI"""
        self.show_banner()
        
        while self.running:
            self.show_menu()
            choice = input("Selecciona una opción: ").strip()


            if choice == '1':
                self.create_blockchain()
            elif choice == '2':
                self.load_blockchain()
            elif choice == '3':
                self.list_saved_blockchains()
            elif choice == '4':
                self.create_wallet()
            elif choice == '5':
                self.load_wallet()
            elif choice == '6':
                self.view_balance()
            elif choice == '7':
                self.view_transaction_history()
            elif choice == '8':
                self.block_explorer_menu()
            elif choice == '9':
                self.statistics_menu()
            elif choice == '10':
                self.faucet_menu()
            elif choice == '11':
                self.send_coins()
            elif choice == '12':
                self.mine_block()
            elif choice == '13':
                self.view_blockchain()
            elif choice == '14':
                self.view_info()
            elif choice == '15':
                self.save_wallet()
            elif choice == '16':
                self.save_blockchain_manually()
            elif choice == '17':
                self.difficulty_menu()
            elif choice == '18':
                self.contracts_menu()
            elif choice == '19':
                self.network_menu()
            elif choice == '0':
                print("\n👋 ¡Gracias por usar ColCript!\n")
                self.running = False
            else:
                print("\n❌ Opción inválida\n")

if __name__ == "__main__":
    cli = ColCriptCLI()
    cli.run()
