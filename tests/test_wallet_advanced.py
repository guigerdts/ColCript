# tests/test_wallet_advanced.py - Tests para AdvancedWallet

import pytest
import sys
import os
import json

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from wallet.advanced import AdvancedWallet

class TestAdvancedWallet:
    """Tests para funcionalidades avanzadas de wallet"""
    
    @pytest.fixture
    def test_wallet(self, tmp_path):
        """
        Fixture: Wallet avanzada de prueba con archivos temporales
        
        POR QUÉ: Usar tmp_path para evitar persistencia entre tests
        """
        # Crear wallet con dirección temporal
        test_address = "test_address_12345"
        wallet = AdvancedWallet(test_address)
        
        # Sobrescribir rutas de archivos para usar directorio temporal
        wallet.contacts_file = tmp_path / f"wallet_{test_address[:10]}_contacts.json"
        wallet.labels_file = tmp_path / f"wallet_{test_address[:10]}_labels.json"
        
        # Reiniciar contactos y etiquetas (vacíos)
        wallet.contacts = {}
        wallet.labels = {}
        
        return wallet
    
    def test_wallet_initialization(self, test_wallet):
        """
        Test: Wallet se inicializa correctamente
        
        POR QUÉ: Verificar configuración básica
        """
        assert test_wallet.address == "test_address_12345"
        assert test_wallet.node_url == "http://localhost:5000"
        assert isinstance(test_wallet.contacts, dict)
        assert isinstance(test_wallet.labels, dict)
    
    def test_add_contact(self, test_wallet):
        """
        Test: Agregar contacto al libro
        
        POR QUÉ: Funcionalidad core de contactos
        """
        result = test_wallet.add_contact("Alice", "alice_addr_123", "Test contact")
        
        assert result == True
        assert "Alice" in test_wallet.contacts
        assert test_wallet.contacts["Alice"]["address"] == "alice_addr_123"
        assert test_wallet.contacts["Alice"]["notes"] == "Test contact"
    
    def test_list_contacts(self, test_wallet):
        """
        Test: Listar contactos
        
        POR QUÉ: Verificar recuperación de contactos
        """
        test_wallet.add_contact("Bob", "bob_addr_456")
        test_wallet.add_contact("Carol", "carol_addr_789", "Friend")
        
        contacts = test_wallet.list_contacts()
        
        assert len(contacts) == 2
        assert "Bob" in contacts
        assert "Carol" in contacts
    
    def test_remove_contact(self, test_wallet):
        """
        Test: Eliminar contacto
        
        POR QUÉ: Verificar eliminación de contactos
        """
        test_wallet.add_contact("Dave", "dave_addr_000")
        
        result = test_wallet.remove_contact("Dave")
        assert result == True
        assert "Dave" not in test_wallet.contacts
        
        # Intentar eliminar contacto inexistente
        result = test_wallet.remove_contact("NonExistent")
        assert result == False
    
    def test_get_contact(self, test_wallet):
        """
        Test: Obtener contacto por nombre
        
        POR QUÉ: Verificar búsqueda de contacto
        """
        test_wallet.add_contact("Eve", "eve_addr_111", "Colleague")
        
        contact = test_wallet.get_contact("Eve")
        
        assert contact is not None
        assert contact["address"] == "eve_addr_111"
        assert contact["notes"] == "Colleague"
        
        # Contacto inexistente
        contact = test_wallet.get_contact("Unknown")
        assert contact is None
    
    def test_find_contact_by_address(self, test_wallet):
        """
        Test: Buscar contacto por dirección
        
        POR QUÉ: Verificar búsqueda inversa
        """
        test_wallet.add_contact("Frank", "frank_addr_222")
        
        name = test_wallet.find_contact_by_address("frank_addr_222")
        assert name == "Frank"
        
        # Dirección inexistente
        name = test_wallet.find_contact_by_address("unknown_addr")
        assert name is None
    
    def test_add_label(self, test_wallet):
        """
        Test: Agregar etiqueta a dirección
        
        POR QUÉ: Funcionalidad core de etiquetas
        """
        result = test_wallet.add_label("miner_addr_333", "My Mining Pool")
        
        assert result == True
        assert "miner_addr_333" in test_wallet.labels
        assert test_wallet.labels["miner_addr_333"] == "My Mining Pool"
    
    def test_remove_label(self, test_wallet):
        """
        Test: Eliminar etiqueta
        
        POR QUÉ: Verificar eliminación de etiquetas
        """
        test_wallet.add_label("exchange_addr_444", "Binance")
        
        result = test_wallet.remove_label("exchange_addr_444")
        assert result == True
        assert "exchange_addr_444" not in test_wallet.labels
        
        # Intentar eliminar etiqueta inexistente
        result = test_wallet.remove_label("nonexistent_addr")
        assert result == False
    
    def test_get_label(self, test_wallet):
        """
        Test: Obtener etiqueta de dirección
        
        POR QUÉ: Verificar recuperación de etiquetas
        """
        test_wallet.add_label("cold_wallet_555", "Cold Storage")
        
        label = test_wallet.get_label("cold_wallet_555")
        assert label == "Cold Storage"
        
        # Dirección sin etiqueta
        label = test_wallet.get_label("unknown_addr")
        assert label is None
    
    def test_get_label_from_contact(self, test_wallet):
        """
        Test: Obtener etiqueta desde contacto
        
        POR QUÉ: Verificar integración contactos-etiquetas
        """
        test_wallet.add_contact("George", "george_addr_666")
        
        label = test_wallet.get_label("george_addr_666")
        assert label == "Contact: George"
    
    def test_transaction_stats_empty(self, test_wallet):
        """
        Test: Estadísticas sin transacciones
        
        POR QUÉ: Verificar respuesta con blockchain vacía
        """
        stats = test_wallet.get_transaction_stats()
        
        assert stats["total_transactions"] == 0
        assert stats["sent_count"] == 0
        assert stats["received_count"] == 0
        assert stats["total_sent"] == 0
        assert stats["total_received"] == 0
        assert stats["total_fees"] == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
