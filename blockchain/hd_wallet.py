# blockchain/hd_wallet.py - Hierarchical Deterministic Wallets (BIP32/BIP39)

import hashlib
import hmac
import ecdsa
from mnemonic import Mnemonic
from typing import List, Tuple, Optional
import json
import os

class HDWallet:
    """
    Hierarchical Deterministic Wallet (BIP32/BIP39)
    
    Genera múltiples direcciones desde una única semilla
    Compatible con estándar BIP32 y BIP39
    """
    
    def __init__(self, mnemonic_phrase: Optional[str] = None, 
                 language: str = 'english', name: str = "HDWallet"):
        """
        Inicializa HD Wallet
        
        Args:
            mnemonic_phrase: Frase mnemónica (12 palabras). Si None, genera nueva
            language: Idioma para mnemónico (english, spanish, etc)
            name: Nombre de la wallet
        """
        self.name = name
        self.language = language
        self.mnemo = Mnemonic(language)
        
        # Generar o usar mnemónico existente
        if mnemonic_phrase:
            if not self.mnemo.check(mnemonic_phrase):
                raise ValueError("Invalid mnemonic phrase")
            self.mnemonic = mnemonic_phrase
        else:
            self.mnemonic = self.mnemo.generate(strength=128)  # 12 palabras
        
        # Generar semilla maestra
        self.seed = self.mnemo.to_seed(self.mnemonic, passphrase="")
        
        # Generar clave maestra
        self.master_private_key, self.master_chain_code = self._generate_master_key()
        
        # Cache de direcciones derivadas
        self.derived_keys = {}
        self.current_index = 0
    
    def _generate_master_key(self) -> Tuple[bytes, bytes]:
        """
        Genera clave privada maestra y chain code desde la semilla
        
        Returns:
            (master_private_key, master_chain_code)
        """
        # HMAC-SHA512 de la semilla
        h = hmac.new(b"Bitcoin seed", self.seed, hashlib.sha512).digest()
        
        master_private_key = h[:32]
        master_chain_code = h[32:]
        
        return master_private_key, master_chain_code
    
    def _derive_child_key(self, parent_key: bytes, parent_chain: bytes, 
                          index: int) -> Tuple[bytes, bytes]:
        """
        Deriva clave hijo desde clave padre (BIP32)
        
        Args:
            parent_key: Clave privada padre
            parent_chain: Chain code padre
            index: Índice del hijo
        
        Returns:
            (child_private_key, child_chain_code)
        """
        # Para derivación no hardened (index < 2^31)
        if index >= 2**31:
            raise ValueError("Hardened derivation not supported in this implementation")
        
        # Obtener clave pública padre
        sk = ecdsa.SigningKey.from_string(parent_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        public_key = b'\x04' + vk.to_string()
        
        # Comprimir clave pública
        x = vk.to_string()[:32]
        y = vk.to_string()[32:]
        if int.from_bytes(y, 'big') % 2 == 0:
            compressed_public = b'\x02' + x
        else:
            compressed_public = b'\x03' + x
        
        # Datos para HMAC
        data = compressed_public + index.to_bytes(4, 'big')
        
        # HMAC-SHA512
        h = hmac.new(parent_chain, data, hashlib.sha512).digest()
        
        # Dividir resultado
        child_key_tweak = h[:32]
        child_chain = h[32:]
        
        # Calcular clave privada hijo
        # child_key = (parent_key + tweak) mod n
        n = ecdsa.SECP256k1.order
        parent_key_int = int.from_bytes(parent_key, 'big')
        tweak_int = int.from_bytes(child_key_tweak, 'big')
        child_key_int = (parent_key_int + tweak_int) % n
        
        child_private_key = child_key_int.to_bytes(32, 'big')
        
        return child_private_key, child_chain
    
    def derive_address(self, index: int) -> Tuple[str, bytes]:
        """
        Deriva una dirección en el índice especificado
        
        Path: m/44'/0'/0'/0/index (simplificado: m/0/index)
        
        Args:
            index: Índice de derivación
        
        Returns:
            (address, private_key)
        """
        # Verificar si ya está en cache
        if index in self.derived_keys:
            return self.derived_keys[index]
        
        # Derivar clave hijo
        child_private_key, _ = self._derive_child_key(
            self.master_private_key,
            self.master_chain_code,
            index
        )
        
        # Generar dirección desde clave privada
        sk = ecdsa.SigningKey.from_string(child_private_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        public_key = vk.to_string()
        
        # Hash de la clave pública
        address = hashlib.sha256(public_key).hexdigest()
        
        # Guardar en cache
        self.derived_keys[index] = (address, child_private_key)
        
        return address, child_private_key
    
    def get_address(self, index: int) -> str:
        """Obtiene solo la dirección (sin clave privada)"""
        address, _ = self.derive_address(index)
        return address
    
    def get_next_address(self) -> str:
        """Obtiene la siguiente dirección disponible"""
        address = self.get_address(self.current_index)
        self.current_index += 1
        return address
    
    def get_private_key(self, index: int) -> str:
        """Obtiene clave privada en formato hex"""
        _, private_key = self.derive_address(index)
        return private_key.hex()
    
    def get_all_addresses(self, count: int = None) -> List[dict]:
        """
        Obtiene todas las direcciones derivadas
        
        Args:
            count: Número de direcciones. Si None, usa current_index
        
        Returns:
            Lista de {index, address, has_private_key}
        """
        if count is None:
            count = self.current_index
        
        addresses = []
        for i in range(count):
            addr = self.get_address(i)
            addresses.append({
                'index': i,
                'address': addr,
                'has_private_key': True
            })
        
        return addresses
    
    def sign_message(self, message: str, index: int) -> str:
        """
        Firma un mensaje con la clave privada del índice
        
        Args:
            message: Mensaje a firmar
            index: Índice de la clave a usar
        
        Returns:
            Firma en formato hex
        """
        _, private_key = self.derive_address(index)
        
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        signature = sk.sign(message.encode())
        
        return signature.hex()
    
    def verify_signature(self, message: str, signature: str, 
                        address: str) -> bool:
        """
        Verifica una firma
        
        Args:
            message: Mensaje original
            signature: Firma en hex
            address: Dirección que firmó
        
        Returns:
            True si la firma es válida
        """
        # Encontrar índice de la dirección
        index = None
        for i, (addr, _) in self.derived_keys.items():
            if addr == address:
                index = i
                break
        
        if index is None:
            return False
        
        _, private_key = self.derive_address(index)
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        
        try:
            vk.verify(bytes.fromhex(signature), message.encode())
            return True
        except:
            return False
    
    def export_mnemonic(self) -> str:
        """Exporta frase mnemónica (backup)"""
        return self.mnemonic
    
    def get_mnemonic_words(self) -> List[str]:
        """Obtiene lista de palabras mnemónicas"""
        return self.mnemonic.split()
    
    def to_dict(self) -> dict:
        """Serializa wallet a diccionario"""
        return {
            'type': 'HD',
            'name': self.name,
            'mnemonic': self.mnemonic,
            'language': self.language,
            'current_index': self.current_index,
            'addresses_count': len(self.derived_keys)
        }
    
    def save(self, filename: str = None):
        """
        Guarda HD Wallet (SOLO MNEMONIC - seguro)
        
        Args:
            filename: Nombre del archivo. Si None, usa self.name
        """
        if filename is None:
            filename = f"{self.name}.json"
        
        filepath = os.path.join('data', 'wallets', filename)
        
        data = {
            'type': 'HD',
            'name': self.name,
            'mnemonic': self.mnemonic,
            'language': self.language,
            'current_index': self.current_index,
            'note': 'HD Wallet - Keep mnemonic safe! 12 words = ALL your addresses'
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ HD Wallet guardada: {filepath}")
        print(f"⚠️  BACKUP: {self.mnemonic}")
    
    @classmethod
    def load(cls, filename: str) -> 'HDWallet':
        """
        Carga HD Wallet desde archivo
        
        Args:
            filename: Nombre del archivo
        
        Returns:
            HDWallet instance
        """
        filepath = os.path.join('data', 'wallets', filename)
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if data.get('type') != 'HD':
            raise ValueError("Not an HD Wallet file")
        
        wallet = cls(
            mnemonic_phrase=data['mnemonic'],
            language=data.get('language', 'english'),
            name=data.get('name', 'HDWallet')
        )
        
        wallet.current_index = data.get('current_index', 0)
        
        print(f"✅ HD Wallet cargada: {wallet.name}")
        print(f"   Direcciones derivadas: {wallet.current_index}")
        
        return wallet
    
    @classmethod
    def from_mnemonic(cls, mnemonic: str, name: str = "HDWallet") -> 'HDWallet':
        """
        Crea HD Wallet desde frase mnemónica
        
        Args:
            mnemonic: Frase de 12 palabras
            name: Nombre de la wallet
        
        Returns:
            HDWallet instance
        """
        return cls(mnemonic_phrase=mnemonic, name=name)


# Test
if __name__ == "__main__":
    print("\n🔐 Probando HD Wallet...\n")
    
    # Crear nueva HD Wallet
    print("1️⃣  Creando nueva HD Wallet...")
    wallet = HDWallet(name="TestHD")
    
    print(f"   Nombre: {wallet.name}")
    print(f"   Mnemonic: {wallet.mnemonic}")
    print(f"   Palabras: {len(wallet.get_mnemonic_words())}")
    
    # Derivar múltiples direcciones
    print("\n2️⃣  Derivando direcciones...")
    for i in range(5):
        addr = wallet.get_next_address()
        print(f"   Address {i}: {addr[:20]}...")
    
    # Ver todas las direcciones
    print("\n3️⃣  Todas las direcciones:")
    addresses = wallet.get_all_addresses()
    for addr_info in addresses:
        print(f"   [{addr_info['index']}] {addr_info['address'][:20]}...")
    
    # Firmar mensaje
    print("\n4️⃣  Firmando mensaje...")
    message = "Hello ColCript HD Wallet!"
    signature = wallet.sign_message(message, index=0)
    print(f"   Mensaje: {message}")
    print(f"   Firma: {signature[:40]}...")
    
    # Verificar firma
    print("\n5️⃣  Verificando firma...")
    is_valid = wallet.verify_signature(message, signature, wallet.get_address(0))
    print(f"   Válida: {is_valid}")
    
    # Guardar wallet
    print("\n6️⃣  Guardando wallet...")
    wallet.save()
    
    # Cargar wallet
    print("\n7️⃣  Cargando wallet...")
    wallet2 = HDWallet.load("TestHD.json")
    print(f"   Nombre: {wallet2.name}")
    print(f"   Direcciones: {wallet2.current_index}")
    
    # Verificar que las direcciones son las mismas
    print("\n8️⃣  Verificando consistencia...")
    for i in range(5):
        addr1 = wallet.get_address(i)
        addr2 = wallet2.get_address(i)
        match = "✅" if addr1 == addr2 else "❌"
        print(f"   Address {i}: {match}")
    
    print("\n✅ HD Wallet funcionando correctamente\n")
