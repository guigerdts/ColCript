# contracts/smart_contract.py - Sistema de Smart Contracts

import os
import sys
import json
import time
from datetime import datetime

# Obtener ruta absoluta del proyecto
project_root = '/data/data/com.termux/files/home/ColCript'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from contracts.opcodes import ScriptEngine, OpCode
import config

class ContractType:
    """Tipos de contratos soportados"""
    TIMELOCK = "timelock"
    MULTISIG = "multisig"
    ESCROW = "escrow"
    CONDITIONAL = "conditional"
    CUSTOM = "custom"


class SmartContract:
    """
    Clase base para Smart Contracts
    """
    
    def __init__(self, contract_id, contract_type, creator, script, data=None):
        self.contract_id = contract_id
        self.contract_type = contract_type
        self.creator = creator
        self.script = script
        self.data = data or {}
        self.created_at = time.time()
        self.executed = False
        self.execution_result = None
        self.execution_block = None
    
    def execute(self, blockchain, context=None):
        """Ejecuta el contrato"""
        if self.executed:
            return False, "Contract already executed"
        
        engine = ScriptEngine(blockchain)
        
        # Preparar contexto
        if context is None:
            context = {}
        
        context['contract_id'] = self.contract_id
        context['creator'] = self.creator
        context['block_height'] = len(blockchain.chain) if blockchain else 0
        context['timestamp'] = time.time()
        
        # Ejecutar script
        success, msg = engine.execute(self.script, context)
        
        if success:
            self.executed = True
            self.execution_result = {
                'success': True,
                'message': msg,
                'gas_used': engine.gas_used,
                'operations': engine.executed_ops,
                'final_stack': engine.stack
            }
            self.execution_block = context.get('block_height', 0)
        else:
            self.execution_result = {
                'success': False,
                'message': msg,
                'gas_used': engine.gas_used
            }
        
        return success, msg

    def get_info(self):
        """Información del contrato (implementación por defecto)"""
        return {
            'type': self.contract_type,
            'creator': self.creator,
            'created_at': self.created_at,
            'executed': self.executed,
            'execution_block': self.execution_block,
            'data': self.data
        }

    def to_dict(self):
        """Serializa el contrato a diccionario"""
        return {
            'contract_id': self.contract_id,
            'contract_type': self.contract_type,
            'creator': self.creator,
            'script': [str(op) if isinstance(op, OpCode) else op for op in self.script],
            'data': self.data,
            'created_at': self.created_at,
            'executed': self.executed,
            'execution_result': self.execution_result,
            'execution_block': self.execution_block
        }

    @staticmethod
    def from_dict(data):
        """Reconstruye un contrato desde diccionario"""
        contract_type = data['contract_type']
        
        # Reconstruir el tipo específico de contrato
        if contract_type == ContractType.TIMELOCK:
            contract = TimelockContract(
                data['contract_id'],
                data['creator'],
                data['data']['unlock_block'],
                data['data']['amount'],
                data['data']['recipient']
            )
        elif contract_type == ContractType.MULTISIG:
            contract = MultisigContract(
                data['contract_id'],
                data['creator'],
                data['data']['required_sigs'],
                data['data']['signers'],
                data['data']['amount'],
                data['data']['recipient']
            )
            contract.data['signatures'] = data['data'].get('signatures', [])
        elif contract_type == ContractType.ESCROW:
            contract = EscrowContract(
                data['contract_id'],
                data['creator'],
                data['data']['buyer'],
                data['data']['seller'],
                data['data']['arbiter'],
                data['data']['amount']
            )
            contract.data['status'] = data['data'].get('status', 'pending')
            contract.data['decision'] = data['data'].get('decision')
        elif contract_type == ContractType.CONDITIONAL:
            contract = ConditionalContract(
                data['contract_id'],
                data['creator'],
                data['script'],
                data['data']['amount'],
                data['data']['recipient']
            )
        else:
            # Contrato genérico
            contract = SmartContract(
                data['contract_id'],
                data['contract_type'],
                data['creator'],
                data['script'],
                data.get('data')
            )
        
        contract.created_at = data.get('created_at', time.time())
        contract.executed = data.get('executed', False)
        contract.execution_result = data.get('execution_result')
        contract.execution_block = data.get('execution_block')
        return contract


    
    @staticmethod
    def from_dict(data):
        """Reconstruye un contrato desde diccionario"""
        contract = SmartContract(
            data['contract_id'],
            data['contract_type'],
            data['creator'],
            data['script'],
            data.get('data')
        )
        contract.created_at = data.get('created_at', time.time())
        contract.executed = data.get('executed', False)
        contract.execution_result = data.get('execution_result')
        contract.execution_block = data.get('execution_block')
        return contract


class TimelockContract(SmartContract):
    """
    Contrato Timelock: Libera CLC después de cierta altura de bloque
    """
    
    def __init__(self, contract_id, creator, unlock_block, amount, recipient):
        """
        Args:
            unlock_block: Número de bloque para desbloquear
            amount: Cantidad de CLC
            recipient: Dirección que recibirá los CLC
        """
        # Script: Verificar que block_height >= unlock_block
        script = [
            unlock_block,
            OpCode.OP_CHECKLOCKTIMEVERIFY,
            1  # Push true si pasa la verificación
        ]
        
        data = {
            'unlock_block': unlock_block,
            'amount': amount,
            'recipient': recipient
        }
        
        super().__init__(contract_id, ContractType.TIMELOCK, creator, script, data)
    
    def can_execute(self, current_block):
        """Verifica si el contrato puede ejecutarse"""
        return current_block >= self.data['unlock_block']
    
    def get_info(self):
        """Información del contrato"""
        return {
            'type': 'Timelock',
            'unlock_block': self.data['unlock_block'],
            'amount': self.data['amount'],
            'recipient': self.data['recipient'],
            'status': 'Executed' if self.executed else 'Pending'
        }


class MultisigContract(SmartContract):
    """
    Contrato Multisig: Requiere N de M firmas
    """

    def __init__(self, contract_id, creator, required_sigs, signers, amount, recipient):
        """
        Args:
            required_sigs: Número de firmas requeridas
            signers: Lista de direcciones que pueden firmar
            amount: Cantidad de CLC
            recipient: Dirección que recibirá los CLC
        """
        # Script: Verificar que signatures >= required
        # Simplificado: solo verifica que tengamos suficientes firmas
        script = [
            required_sigs,
            len(signers),
            OpCode.OP_LESSTHANOREQUAL,  # required <= total (debe ser true)
            1  # Push true al final
        ]
        
        data = {
            'required_sigs': required_sigs,
            'signers': signers,
            'amount': amount,
            'recipient': recipient,
            'signatures': []
        }
        
        super().__init__(contract_id, ContractType.MULTISIG, creator, script, data)


    def add_signature(self, signer_address):
        """Añade una firma al contrato"""
        if signer_address in self.data['signers']:
            if signer_address not in self.data['signatures']:
                self.data['signatures'].append(signer_address)
                return True
        return False
    
    def can_execute(self):
        """Verifica si tiene suficientes firmas"""
        return len(self.data['signatures']) >= self.data['required_sigs']
    
    def get_info(self):
        """Información del contrato"""
        return {
            'type': 'Multisig',
            'required_sigs': self.data['required_sigs'],
            'total_signers': len(self.data['signers']),
            'current_sigs': len(self.data['signatures']),
            'amount': self.data['amount'],
            'recipient': self.data['recipient'],
            'status': 'Executed' if self.executed else f"{len(self.data['signatures'])}/{self.data['required_sigs']} sigs"
        }


class EscrowContract(SmartContract):
    """
    Contrato Escrow: Mediador entre dos partes
    """
    
    def __init__(self, contract_id, creator, buyer, seller, arbiter, amount):
        """
        Args:
            buyer: Dirección del comprador
            seller: Dirección del vendedor
            arbiter: Dirección del árbitro (quien decide)
            amount: Cantidad de CLC en escrow
        """
        # Script: El árbitro decide
        script = [1]  # Placeholder
        
        data = {
            'buyer': buyer,
            'seller': seller,
            'arbiter': arbiter,
            'amount': amount,
            'status': 'pending',  # pending, approved, rejected
            'decision': None
        }
        
        super().__init__(contract_id, ContractType.ESCROW, creator, script, data)
    
    def make_decision(self, arbiter_address, approve):
        """El árbitro toma una decisión"""
        if arbiter_address != self.data['arbiter']:
            return False, "Only arbiter can make decision"
        
        if self.data['status'] != 'pending':
            return False, "Decision already made"
        
        self.data['status'] = 'approved' if approve else 'rejected'
        self.data['decision'] = approve
        return True, f"Decision: {'Approved' if approve else 'Rejected'}"
    
    def can_execute(self):
        """Verifica si puede ejecutarse"""
        return self.data['status'] == 'approved'
    
    def get_info(self):
        """Información del contrato"""
        return {
            'type': 'Escrow',
            'buyer': self.data['buyer'],
            'seller': self.data['seller'],
            'arbiter': self.data['arbiter'],
            'amount': self.data['amount'],
            'status': self.data['status'],
            'decision': self.data['decision']
        }


class ConditionalContract(SmartContract):
    """
    Contrato Condicional: Ejecuta si se cumple una condición
    """
    
    def __init__(self, contract_id, creator, condition_script, amount, recipient):
        """
        Args:
            condition_script: Script que debe evaluarse a True
            amount: Cantidad de CLC
            recipient: Dirección que recibirá los CLC
        """
        data = {
            'amount': amount,
            'recipient': recipient,
            'condition_description': 'Custom condition'
        }
        
        super().__init__(contract_id, ContractType.CONDITIONAL, creator, condition_script, data)
    
    def get_info(self):
        """Información del contrato"""
        return {
            'type': 'Conditional',
            'amount': self.data['amount'],
            'recipient': self.data['recipient'],
            'condition': self.data['condition_description'],
            'status': 'Executed' if self.executed else 'Pending'
        }


class ContractManager:
    """
    Gestor de Smart Contracts
    """
    
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.contracts = {}
        self.storage_file = "data/contracts.json"
        self.next_id = 1
        self.load_contracts()
    
    def create_timelock(self, creator, unlock_block, amount, recipient):
        """Crea un contrato timelock"""
        contract_id = f"TL-{self.next_id}"
        self.next_id += 1
        
        contract = TimelockContract(contract_id, creator, unlock_block, amount, recipient)
        self.contracts[contract_id] = contract
        self.save_contracts()
        
        return contract
    
    def create_multisig(self, creator, required_sigs, signers, amount, recipient):
        """Crea un contrato multisig"""
        contract_id = f"MS-{self.next_id}"
        self.next_id += 1
        
        contract = MultisigContract(contract_id, creator, required_sigs, signers, amount, recipient)
        self.contracts[contract_id] = contract
        self.save_contracts()
        
        return contract
    
    def create_escrow(self, creator, buyer, seller, arbiter, amount):
        """Crea un contrato escrow"""
        contract_id = f"ES-{self.next_id}"
        self.next_id += 1
        
        contract = EscrowContract(contract_id, creator, buyer, seller, arbiter, amount)
        self.contracts[contract_id] = contract
        self.save_contracts()
        
        return contract
    
    def create_conditional(self, creator, condition_script, amount, recipient):
        """Crea un contrato condicional"""
        contract_id = f"CD-{self.next_id}"
        self.next_id += 1
        
        contract = ConditionalContract(contract_id, creator, condition_script, amount, recipient)
        self.contracts[contract_id] = contract
        self.save_contracts()
        
        return contract
    
    def get_contract(self, contract_id):
        """Obtiene un contrato por ID"""
        return self.contracts.get(contract_id)
    
    def execute_contract(self, contract_id, context=None):
        """Ejecuta un contrato"""
        contract = self.get_contract(contract_id)
        
        if not contract:
            return False, "Contract not found"
        
        success, msg = contract.execute(self.blockchain, context)
        self.save_contracts()
        
        return success, msg
    
    def list_contracts(self, status=None):
        """Lista contratos (todos o filtrados por estado)"""
        contracts = list(self.contracts.values())
        
        if status == 'pending':
            contracts = [c for c in contracts if not c.executed]
        elif status == 'executed':
            contracts = [c for c in contracts if c.executed]
        
        return contracts
    
    def save_contracts(self):
        """Guarda contratos en archivo"""
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            
            data = {
                'next_id': self.next_id,
                'contracts': {
                    cid: contract.to_dict()
                    for cid, contract in self.contracts.items()
                }
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving contracts: {e}")
    
    def load_contracts(self):
        """Carga contratos desde archivo"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                
                self.next_id = data.get('next_id', 1)
                
                for cid, cdata in data.get('contracts', {}).items():
                    self.contracts[cid] = SmartContract.from_dict(cdata)
        except Exception as e:
            print(f"Error loading contracts: {e}")


# Test
if __name__ == "__main__":
    print("\n📜 Probando Smart Contracts...\n")
    
    from blockchain.blockchain import Blockchain
    
    # Crear blockchain de prueba
    bc = Blockchain(auto_save=False)
    
    # Crear gestor de contratos
    manager = ContractManager(bc)
    
    # Test 1: Timelock
    print("Test 1: Contrato Timelock")
    
    # Minar algunos bloques para tener altura suficiente
    print("  Minando 15 bloques para prueba...")
    for i in range(15):
        bc.mine_pending_transactions("test_miner")
    
    contract = manager.create_timelock(
        creator="Alice",
        unlock_block=10,
        amount=100,
        recipient="Bob"
    )
    print(f"  ID: {contract.contract_id}")
    print(f"  Info: {contract.get_info()}")
    print(f"  Altura actual: {len(bc.chain)}")
    print(f"  Puede ejecutar (bloque 5): {contract.can_execute(5)}")
    print(f"  Puede ejecutar (bloque actual): {contract.can_execute(len(bc.chain))}")
    
    # Ejecutar con contexto actual
    success, msg = manager.execute_contract(contract.contract_id, {'block_height': len(bc.chain)})
    print(f"  Ejecución: {'✅' if success else '❌'} {msg}")
    if success:
        print(f"  Gas usado: {contract.execution_result['gas_used']}")
        print(f"  Operaciones: {contract.execution_result['operations']}")
    print()
    
    # Test 2: Multisig
    print("Test 2: Contrato Multisig (2 de 3)")
    contract = manager.create_multisig(
        creator="Alice",
        required_sigs=2,
        signers=["Alice", "Bob", "Charlie"],
        amount=50,
        recipient="Dave"
    )
    print(f"  ID: {contract.contract_id}")
    print(f"  Info: {contract.get_info()}")
    print(f"  Añadiendo firma de Alice...")
    contract.add_signature("Alice")
    print(f"  Info: {contract.get_info()}")
    print(f"  Añadiendo firma de Bob...")
    contract.add_signature("Bob")
    print(f"  Info: {contract.get_info()}")
    print(f"  Puede ejecutar: {contract.can_execute()}")
    
    success, msg = manager.execute_contract(contract.contract_id)
    print(f"  Ejecución: {'✅' if success else '❌'} {msg}")
    if success:
        print(f"  Gas usado: {contract.execution_result['gas_used']}")
    print()
    
    # Test 3: Escrow
    print("Test 3: Contrato Escrow")
    contract = manager.create_escrow(
        creator="Alice",
        buyer="Alice",
        seller="Bob",
        arbiter="Charlie",
        amount=200
    )
    print(f"  ID: {contract.contract_id}")
    print(f"  Info: {contract.get_info()}")
    print(f"  Árbitro aprueba transacción...")
    success, msg = contract.make_decision("Charlie", approve=True)
    print(f"  Decisión: {msg}")
    print(f"  Info: {contract.get_info()}")
    print(f"  Puede ejecutar: {contract.can_execute()}")
    print()
    
    # Listar contratos
    print("Contratos creados:")
    for c in manager.list_contracts():
        print(f"  - {c.contract_id}: {c.contract_type} (executed: {c.executed})")
    
    print("\n✅ Smart Contracts funcionando\n")
