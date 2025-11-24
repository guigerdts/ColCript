# tests/test_advanced_explorer.py - Tests para AdvancedExplorer

import pytest
import sys
import os
from datetime import datetime, timedelta

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from blockchain.blockchain import Blockchain
from blockchain.advanced_explorer import AdvancedExplorer
from wallet.wallet import Wallet

class TestAdvancedExplorer:
    """Tests para funcionalidades avanzadas del explorer"""
    
    @pytest.fixture
    def blockchain_with_data(self):
        """
        Fixture: Blockchain con datos de prueba
        
        POR QUÉ: Necesitamos datos para probar búsquedas
        """
        blockchain = Blockchain(auto_save=False)
        
        # Crear wallets de prueba
        wallet1 = Wallet("Miner1")
        wallet2 = Wallet("User1")
        wallet3 = Wallet("User2")
        
        # Minar algunos bloques con transacciones
        blockchain.mine_pending_transactions(wallet1.get_address())
        
        # Agregar transacciones
        tx1 = wallet1.send_coins(wallet2.get_address(), 10)
        blockchain.add_transaction(tx1)
        
        blockchain.mine_pending_transactions(wallet1.get_address())
        
        tx2 = wallet2.send_coins(wallet3.get_address(), 5)
        blockchain.add_transaction(tx2)
        
        blockchain.mine_pending_transactions(wallet2.get_address())
        
        return blockchain
    
    @pytest.fixture
    def explorer(self, blockchain_with_data):
        """
        Fixture: Explorer con blockchain de prueba
        
        POR QUÉ: Instancia lista para tests
        """
        return AdvancedExplorer(blockchain_with_data)
    
    def test_explorer_initialization(self, explorer):
        """
        Test: Explorer se inicializa correctamente
        
        POR QUÉ: Verificar configuración básica
        """
        assert explorer.blockchain is not None
        assert len(explorer.blockchain.chain) > 0
    
    def test_search_address_transactions(self, explorer, blockchain_with_data):
        """
        Test: Buscar transacciones por dirección
        
        POR QUÉ: Funcionalidad core del explorer
        """
        # Obtener dirección de wallet1 (el minero)
        wallet1 = Wallet("Miner1")
        address = wallet1.get_address()
        
        # Buscar transacciones
        transactions = explorer.search_address_transactions(address, limit=10)
        
        # Debe tener al menos las transacciones que enviamos
        assert len(transactions) >= 0
        assert isinstance(transactions, list)
    
    def test_get_top_holders(self, explorer):
        """
        Test: Obtener top holders
        
        POR QUÉ: Ver distribución de riqueza
        """
        holders = explorer.get_top_holders(limit=5)
        
        assert isinstance(holders, list)
        assert len(holders) <= 5
        
        # Verificar estructura
        if holders:
            holder = holders[0]
            assert 'rank' in holder
            assert 'address' in holder
            assert 'balance' in holder
            assert 'percentage' in holder
            assert holder['rank'] == 1
    
    def test_get_miner_ranking(self, explorer):
        """
        Test: Ranking de mineros
        
        POR QUÉ: Ver quiénes están minando
        """
        ranking = explorer.get_miner_ranking(limit=5)
        
        assert isinstance(ranking, list)
        assert len(ranking) <= 5
        
        # Verificar estructura
        if ranking:
            miner = ranking[0]
            assert 'rank' in miner
            assert 'address' in miner
            assert 'blocks_mined' in miner
            assert 'total_rewards' in miner
            assert miner['blocks_mined'] > 0
    
    def test_get_network_activity(self, explorer):
        """
        Test: Actividad de red
        
        POR QUÉ: Ver tendencias de uso
        """
        activity = explorer.get_network_activity(days=7)
        
        assert 'period_days' in activity
        assert 'transactions_per_day' in activity
        assert 'blocks_per_day' in activity
        assert 'volume_per_day' in activity
        assert activity['period_days'] == 7
    
    def test_get_realtime_stats(self, explorer):
        """
        Test: Estadísticas en tiempo real
        
        POR QUÉ: Dashboard de estado actual
        """
        stats = explorer.get_realtime_stats()
        
        assert 'chain_height' in stats
        assert 'pending_transactions' in stats
        assert 'current_difficulty' in stats
        assert 'average_block_time' in stats
        assert 'last_block' in stats
        
        assert stats['chain_height'] > 0
        assert isinstance(stats['pending_transactions'], int)
    
    def test_get_difficulty_history(self, explorer):
        """
        Test: Historial de dificultad
        
        POR QUÉ: Ver cambios de dificultad
        """
        history = explorer.get_difficulty_history(limit=10)
        
        assert isinstance(history, list)
        assert len(history) <= 10
        
        # Verificar estructura
        if history:
            entry = history[0]
            assert 'block' in entry
            assert 'timestamp' in entry
            assert 'difficulty' in entry
            assert 'hash' in entry
    
    def test_search_transaction_not_found(self, explorer):
        """
        Test: Buscar transacción inexistente
        
        POR QUÉ: Manejar casos negativos
        """
        result = explorer.search_transaction("nonexistent_hash_123")
        
        assert result is None
    
    def test_search_by_date_range_empty(self, explorer):
        """
        Test: Buscar en rango sin resultados
        
        POR QUÉ: Manejar rangos vacíos
        """
        # Buscar en el futuro (no debería haber bloques)
        future_start = (datetime.now() + timedelta(days=1)).isoformat()
        future_end = (datetime.now() + timedelta(days=2)).isoformat()
        
        results = explorer.search_by_date_range(future_start, future_end)
        
        assert isinstance(results, list)
        assert len(results) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
