# utils/crypto.py - Funciones criptográficas para ColCript

import hashlib
import json
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import binascii

def hash_data(data):
    """
    Genera un hash SHA-256 de cualquier dato
    """
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()

def generate_keypair():
    """
    Genera un par de claves (privada y pública) para una wallet
    Returns: (private_key_hex, public_key_hex)
    """
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    
    private_key_hex = binascii.hexlify(private_key.to_string()).decode()
    public_key_hex = binascii.hexlify(public_key.to_string()).decode()
    
    return private_key_hex, public_key_hex

def sign_data(private_key_hex, data):
    """
    Firma datos con una clave privada
    """
    private_key = SigningKey.from_string(
        binascii.unhexlify(private_key_hex),
        curve=SECP256k1
    )
    
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    
    signature = private_key.sign(data.encode())
    return binascii.hexlify(signature).decode()

def verify_signature(public_key_hex, signature_hex, data):
    """
    Verifica la firma de datos con una clave pública
    """
    try:
        public_key = VerifyingKey.from_string(
            binascii.unhexlify(public_key_hex),
            curve=SECP256k1
        )
        
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        
        signature = binascii.unhexlify(signature_hex)
        return public_key.verify(signature, data.encode())
    except:
        return False

# Test
if __name__ == "__main__":
    print("🔐 Probando funciones criptográficas...")
    
    # Generar claves
    priv, pub = generate_keypair()
    print(f"✅ Claves generadas")
    print(f"   Clave pública: {pub[:20]}...")
    
    # Hash
    test_hash = hash_data("ColCript Blockchain")
    print(f"✅ Hash generado: {test_hash[:20]}...")
    
    # Firma
    mensaje = "Transacción de prueba"
    firma = sign_data(priv, mensaje)
    print(f"✅ Firma generada: {firma[:20]}...")
    
    # Verificación
    es_valida = verify_signature(pub, firma, mensaje)
    print(f"✅ Verificación de firma: {es_valida}")
