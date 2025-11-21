# contracts/opcodes.py - Sistema de Opcodes para Smart Contracts

import hashlib
import time
from enum import IntEnum

class OpCode(IntEnum):
    """Códigos de operación para el script engine"""
    
    # Stack operations
    OP_DUP = 0x76
    OP_DROP = 0x75
    OP_SWAP = 0x7c
    OP_OVER = 0x78
    OP_PICK = 0x79
    OP_ROLL = 0x7a
    
    # Arithmetic operations
    OP_ADD = 0x93
    OP_SUB = 0x94
    OP_MUL = 0x95
    OP_DIV = 0x96
    OP_MOD = 0x97
    OP_INC = 0x8b
    OP_DEC = 0x8c
    
    # Comparison operations
    OP_EQUAL = 0x87
    OP_NOTEQUAL = 0x91
    OP_LESSTHAN = 0x9f
    OP_GREATERTHAN = 0xa0
    OP_LESSTHANOREQUAL = 0xa1
    OP_GREATERTHANOREQUAL = 0xa2
    OP_MIN = 0xa3
    OP_MAX = 0xa4
    
    # Logic operations
    OP_NOT = 0x91
    OP_AND = 0x84
    OP_OR = 0x85
    OP_XOR = 0x86
    
    # Crypto operations
    OP_SHA256 = 0xa8
    OP_HASH160 = 0xa9
    OP_CHECKSIG = 0xac
    OP_CHECKMULTISIG = 0xae
    
    # Flow control
    OP_IF = 0x63
    OP_ELSE = 0x67
    OP_ENDIF = 0x68
    OP_VERIFY = 0x69
    OP_RETURN = 0x6a
    
    # Time operations
    OP_CHECKLOCKTIMEVERIFY = 0xb1
    OP_CHECKSEQUENCEVERIFY = 0xb2
    
    # Data operations
    OP_PUSH = 0x01
    OP_PUSHDATA = 0x4e
    
    # Contract operations
    OP_CALL = 0xf0
    OP_CREATE = 0xf1
    OP_SELFDESTRUCT = 0xff

# contracts/opcodes.py - Sistema de Opcodes para Smart Contracts

import hashlib
import time
from enum import IntEnum

class OpCode(IntEnum):
    """Códigos de operación para el script engine"""
    
    # Stack operations
    OP_DUP = 0x76
    OP_DROP = 0x75
    OP_SWAP = 0x7c
    OP_OVER = 0x78
    OP_PICK = 0x79
    OP_ROLL = 0x7a
    
    # Arithmetic operations
    OP_ADD = 0x93
    OP_SUB = 0x94
    OP_MUL = 0x95
    OP_DIV = 0x96
    OP_MOD = 0x97
    OP_INC = 0x8b
    OP_DEC = 0x8c
    
    # Comparison operations
    OP_EQUAL = 0x87
    OP_NOTEQUAL = 0x91
    OP_LESSTHAN = 0x9f
    OP_GREATERTHAN = 0xa0
    OP_LESSTHANOREQUAL = 0xa1
    OP_GREATERTHANOREQUAL = 0xa2
    OP_MIN = 0xa3
    OP_MAX = 0xa4
    
    # Logic operations
    OP_NOT = 0x91
    OP_AND = 0x84
    OP_OR = 0x85
    OP_XOR = 0x86
    
    # Crypto operations
    OP_SHA256 = 0xa8
    OP_HASH160 = 0xa9
    OP_CHECKSIG = 0xac
    OP_CHECKMULTISIG = 0xae
    
    # Flow control
    OP_IF = 0x63
    OP_ELSE = 0x67
    OP_ENDIF = 0x68
    OP_VERIFY = 0x69
    OP_RETURN = 0x6a
    
    # Time operations
    OP_CHECKLOCKTIMEVERIFY = 0xb1
    OP_CHECKSEQUENCEVERIFY = 0xb2
    
    # Data operations
    OP_PUSH = 0x01
    OP_PUSHDATA = 0x4e
    
    # Contract operations
    OP_CALL = 0xf0
    OP_CREATE = 0xf1
    OP_SELFDESTRUCT = 0xff

class ScriptEngine:
    """Motor de ejecución de scripts"""
    
    def __init__(self, blockchain=None):
        self.stack = []
        self.alt_stack = []
        self.blockchain = blockchain
        self.gas_used = 0
        self.gas_limit = 10000
        self.executed_ops = []
        
    def reset(self):
        """Reinicia el engine"""
        self.stack = []
        self.alt_stack = []
        self.gas_used = 0
        self.executed_ops = []
    
    def execute(self, script, context=None):
        """Ejecuta un script"""
        self.reset()
        
        if context is None:
            context = {}
        
        try:
            for instruction in script:
                if self.gas_used >= self.gas_limit:
                    raise Exception("Gas limit exceeded")
                
                self._execute_instruction(instruction, context)
                self.gas_used += 1
            
            if len(self.stack) == 0:
                return False, "Empty stack"
            
            result = self.stack[-1]
            return bool(result), f"Script executed successfully. Gas used: {self.gas_used}"
            
        except Exception as e:
            return False, f"Script execution failed: {str(e)}"
    
    def _execute_instruction(self, instruction, context):
        """Ejecuta una instrucción individual"""
        
        if isinstance(instruction, OpCode):
            self._execute_opcode(instruction, context)
            return
        
        if isinstance(instruction, (int, float, bool)):
            if isinstance(instruction, int) and instruction in [op.value for op in OpCode]:
                try:
                    opcode = OpCode(instruction)
                    self._execute_opcode(opcode, context)
                    return
                except:
                    pass
            
            self.stack.append(instruction)
            self.executed_ops.append(f"PUSH {instruction}")
            return
        
        if isinstance(instruction, str):
            instruction_upper = instruction.upper()
            if not instruction_upper.startswith("0X") and hasattr(OpCode, instruction_upper):
                opcode = getattr(OpCode, instruction_upper)
                self._execute_opcode(opcode, context)
                return
            
            if instruction.startswith("0x") or instruction.startswith("0X"):
                self.stack.append(instruction)
                self.executed_ops.append(f"PUSH {instruction}")
                return
            
            self.stack.append(instruction)
            self.executed_ops.append(f"PUSH {instruction}")
            return
        
        raise Exception(f"Unknown instruction: {instruction}")

    def _execute_opcode(self, opcode, context):
        """Ejecuta un opcode específico"""
        
        # Stack operations
        if opcode == OpCode.OP_DUP:
            if len(self.stack) < 1:
                raise Exception("OP_DUP: Stack underflow")
            self.stack.append(self.stack[-1])
            self.executed_ops.append("DUP")
        
        elif opcode == OpCode.OP_DROP:
            if len(self.stack) < 1:
                raise Exception("OP_DROP: Stack underflow")
            self.stack.pop()
            self.executed_ops.append("DROP")
        
        elif opcode == OpCode.OP_SWAP:
            if len(self.stack) < 2:
                raise Exception("OP_SWAP: Stack underflow")
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
            self.executed_ops.append("SWAP")
        
        # Arithmetic operations
        elif opcode == OpCode.OP_ADD:
            if len(self.stack) < 2:
                raise Exception("OP_ADD: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)
            self.executed_ops.append(f"ADD ({a} + {b} = {a+b})")
        
        elif opcode == OpCode.OP_SUB:
            if len(self.stack) < 2:
                raise Exception("OP_SUB: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)
            self.executed_ops.append(f"SUB ({a} - {b} = {a-b})")
        
        elif opcode == OpCode.OP_MUL:
            if len(self.stack) < 2:
                raise Exception("OP_MUL: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a * b)
            self.executed_ops.append(f"MUL ({a} * {b} = {a*b})")
        
        elif opcode == OpCode.OP_DIV:
            if len(self.stack) < 2:
                raise Exception("OP_DIV: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            if b == 0:
                raise Exception("OP_DIV: Division by zero")
            self.stack.append(a // b)
            self.executed_ops.append(f"DIV ({a} / {b} = {a//b})")
        
        # Comparison operations
        elif opcode == OpCode.OP_EQUAL:
            if len(self.stack) < 2:
                raise Exception("OP_EQUAL: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a == b else 0)
            self.executed_ops.append(f"EQUAL ({a} == {b} = {a==b})")
        
        elif opcode == OpCode.OP_LESSTHAN:
            if len(self.stack) < 2:
                raise Exception("OP_LESSTHAN: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a < b else 0)
            self.executed_ops.append(f"LESSTHAN ({a} < {b} = {a<b})")
        
        elif opcode == OpCode.OP_GREATERTHAN:
            if len(self.stack) < 2:
                raise Exception("OP_GREATERTHAN: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a > b else 0)
            self.executed_ops.append(f"GREATERTHAN ({a} > {b} = {a>b})")
        
        elif opcode == OpCode.OP_LESSTHANOREQUAL:
            if len(self.stack) < 2:
                raise Exception("OP_LESSTHANOREQUAL: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a <= b else 0)
            self.executed_ops.append(f"LESSTHANOREQUAL ({a} <= {b} = {a<=b})")
        
        elif opcode == OpCode.OP_GREATERTHANOREQUAL:
            if len(self.stack) < 2:
                raise Exception("OP_GREATERTHANOREQUAL: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a >= b else 0)
            self.executed_ops.append(f"GREATERTHANOREQUAL ({a} >= {b} = {a>=b})")
        
        elif opcode == OpCode.OP_MIN:
            if len(self.stack) < 2:
                raise Exception("OP_MIN: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(min(a, b))
            self.executed_ops.append(f"MIN (min({a}, {b}) = {min(a, b)})")
        
        elif opcode == OpCode.OP_MAX:
            if len(self.stack) < 2:
                raise Exception("OP_MAX: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(max(a, b))
            self.executed_ops.append(f"MAX (max({a}, {b}) = {max(a, b)})")
        
        # Logic operations
        elif opcode == OpCode.OP_NOT:
            if len(self.stack) < 1:
                raise Exception("OP_NOT: Stack underflow")
            a = self.stack.pop()
            self.stack.append(0 if a else 1)
            self.executed_ops.append(f"NOT (!{a} = {not a})")
        
        elif opcode == OpCode.OP_AND:
            if len(self.stack) < 2:
                raise Exception("OP_AND: Stack underflow")
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if (a and b) else 0)
            self.executed_ops.append(f"AND ({a} && {b} = {a and b})")
        
        # Crypto operations
        elif opcode == OpCode.OP_SHA256:
            if len(self.stack) < 1:
                raise Exception("OP_SHA256: Stack underflow")
            data = str(self.stack.pop())
            hash_result = hashlib.sha256(data.encode()).hexdigest()
            self.stack.append(hash_result)
            self.executed_ops.append(f"SHA256")
        
        # Time operations
        elif opcode == OpCode.OP_CHECKLOCKTIMEVERIFY:
            if len(self.stack) < 1:
                raise Exception("OP_CHECKLOCKTIMEVERIFY: Stack underflow")
            locktime = self.stack.pop()
            current_height = context.get('block_height', 0)
            
            if current_height < locktime:
                raise Exception(f"OP_CHECKLOCKTIMEVERIFY: Block height {current_height} < locktime {locktime}")
            
            self.executed_ops.append(f"CHECKLOCKTIMEVERIFY (height: {current_height} >= {locktime})")
        
        # Verify operation
        elif opcode == OpCode.OP_VERIFY:
            if len(self.stack) < 1:
                raise Exception("OP_VERIFY: Stack underflow")
            value = self.stack.pop()
            if not value:
                raise Exception("OP_VERIFY: Verification failed")
            self.executed_ops.append("VERIFY (passed)")
        
        else:
            raise Exception(f"Opcode not implemented: {opcode}")


# Test del script engine
if __name__ == "__main__":
    print("\n⚙️  Probando Script Engine...\n")
    
    engine = ScriptEngine()
    
    # Test 1: Operaciones aritméticas
    print("Test 1: Aritmética (2 + 3)")
    script = [2, 3, OpCode.OP_ADD]
    success, msg = engine.execute(script)
    print(f"  Resultado: {engine.stack[-1] if engine.stack else 'N/A'}")
    print(f"  Estado: {'✅' if success else '❌'} {msg}")
    print(f"  Ops ejecutadas: {engine.executed_ops}\n")
    
    # Test 2: Comparación
    print("Test 2: Comparación (5 > 3)")
    script = [5, 3, OpCode.OP_GREATERTHAN]
    success, msg = engine.execute(script)
    print(f"  Resultado: {engine.stack[-1] if engine.stack else 'N/A'}")
    print(f"  Estado: {'✅' if success else '❌'} {msg}")
    print(f"  Ops ejecutadas: {engine.executed_ops}\n")
    
    # Test 3: Stack operations
    print("Test 3: Stack (DUP y ADD)")
    script = [10, OpCode.OP_DUP, OpCode.OP_ADD]
    success, msg = engine.execute(script)
    print(f"  Resultado: {engine.stack[-1] if engine.stack else 'N/A'}")
    print(f"  Estado: {'✅' if success else '❌'} {msg}")
    print(f"  Ops ejecutadas: {engine.executed_ops}\n")
    
    # Test 4: SHA256
    print("Test 4: SHA256")
    script = ["hello", OpCode.OP_SHA256]
    success, msg = engine.execute(script)
    print(f"  Resultado: {engine.stack[-1][:16] if engine.stack else 'N/A'}...")
    print(f"  Estado: {'✅' if success else '❌'} {msg}")
    print(f"  Ops ejecutadas: {engine.executed_ops}\n")
    
    # Test 5: Timelock
    print("Test 5: Timelock (altura 100, requiere >= 50)")
    script = [50, OpCode.OP_CHECKLOCKTIMEVERIFY, 1]
    context = {'block_height': 100}
    success, msg = engine.execute(script, context)
    print(f"  Resultado: {engine.stack[-1] if engine.stack else 'N/A'}")
    print(f"  Estado: {'✅' if success else '❌'} {msg}")
    print(f"  Ops ejecutadas: {engine.executed_ops}\n")
    
    # Test 6: Comparación >=
    print("Test 6: Comparación (3 >= 2)")
    script = [3, 2, OpCode.OP_GREATERTHANOREQUAL]
    success, msg = engine.execute(script)
    print(f"  Resultado: {engine.stack[-1] if engine.stack else 'N/A'}")
    print(f"  Estado: {'✅' if success else '❌'} {msg}")
    print(f"  Ops ejecutadas: {engine.executed_ops}\n")
    
    print("✅ Script Engine funcionando\n")
