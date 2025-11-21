# utils/qr_generator.py - Generador de códigos QR

import qrcode
import io
import base64
from typing import Optional

class QRGenerator:
    """
    Generador de códigos QR para direcciones y pagos
    
    Formatos soportados:
    - Dirección simple: "address"
    - Pago con cantidad: "colcript:address?amount=10.5&memo=Payment"
    """
    
    @staticmethod
    def generate_address_qr(address: str, size: int = 10, border: int = 2) -> str:
        """
        Genera QR de una dirección
        
        Args:
            address: Dirección de wallet
            size: Tamaño del QR (1-40)
            border: Grosor del borde
        
        Returns:
            Imagen QR en base64
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        
        qr.add_data(address)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    @staticmethod
    def generate_payment_qr(address: str, amount: Optional[float] = None, 
                           memo: Optional[str] = None, 
                           size: int = 10, border: int = 2) -> str:
        """
        Genera QR de pago con cantidad y memo
        
        Args:
            address: Dirección de destino
            amount: Cantidad a pagar (opcional)
            memo: Nota/concepto (opcional)
            size: Tamaño del QR
            border: Grosor del borde
        
        Returns:
            Imagen QR en base64
        """
        # Formato: colcript:address?amount=10.5&memo=Payment
        uri = f"colcript:{address}"
        
        params = []
        if amount is not None:
            params.append(f"amount={amount}")
        if memo:
            params.append(f"memo={memo}")
        
        if params:
            uri += "?" + "&".join(params)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    @staticmethod
    def parse_payment_uri(uri: str) -> dict:
        """
        Parsea un URI de pago
        
        Args:
            uri: URI formato "colcript:address?amount=10&memo=text"
        
        Returns:
            {address, amount, memo}
        """
        if not uri.startswith('colcript:'):
            return {'address': uri, 'amount': None, 'memo': None}
        
        uri = uri.replace('colcript:', '')
        
        # Separar dirección y parámetros
        if '?' in uri:
            address, params_str = uri.split('?', 1)
            params = {}
            for param in params_str.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value
            
            return {
                'address': address,
                'amount': float(params.get('amount')) if params.get('amount') else None,
                'memo': params.get('memo')
            }
        else:
            return {'address': uri, 'amount': None, 'memo': None}


# Test
if __name__ == "__main__":
    print("\n📱 Probando generador de QR...\n")
    
    test_address = "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz"
    
    # Test 1: QR de dirección simple
    print("1️⃣  Generando QR de dirección...")
    qr_address = QRGenerator.generate_address_qr(test_address)
    print(f"   Longitud base64: {len(qr_address)} caracteres")
    print(f"   Formato: {qr_address[:50]}...")
    
    # Test 2: QR de pago
    print("\n2️⃣  Generando QR de pago...")
    qr_payment = QRGenerator.generate_payment_qr(
        address=test_address,
        amount=10.5,
        memo="Test payment"
    )
    print(f"   Longitud base64: {len(qr_payment)} caracteres")
    
    # Test 3: Parse URI
    print("\n3️⃣  Parseando URI de pago...")
    test_uri = f"colcript:{test_address}?amount=10.5&memo=Test payment"
    parsed = QRGenerator.parse_payment_uri(test_uri)
    print(f"   Address: {parsed['address'][:20]}...")
    print(f"   Amount: {parsed['amount']}")
    print(f"   Memo: {parsed['memo']}")
    
    # Test 4: QR solo dirección
    print("\n4️⃣  QR de dirección sin monto...")
    qr_simple = QRGenerator.generate_payment_qr(test_address)
    print(f"   ✅ Generado correctamente")
    
    print("\n✅ Generador de QR funcionando\n")
