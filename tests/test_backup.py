# tests/test_backup.py - Tests para sistema de backups

import pytest
import sys
import os
import json
import tempfile

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.backup_system import BackupSystem

class TestBackupSystem:
    """Tests para sistema de backups"""
    
    @pytest.fixture
    def backup_system(self, tmp_path):
        """
        Fixture: Sistema de backups con directorio temporal
        
        POR QUÉ: Usar tmp_path para no llenar disco con backups de prueba
        """
        return BackupSystem(backup_dir=str(tmp_path))
    
    @pytest.fixture
    def test_file(self, tmp_path):
        """
        Fixture: Archivo de prueba
        
        POR QUÉ: Necesitamos un archivo para hacer backup
        """
        test_file = tmp_path / "test_blockchain.json"
        test_data = {
            "chain": [{"index": 0, "data": "genesis"}],
            "blocks": 1
        }
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        return str(test_file)
    
    def test_backup_system_initialization(self, backup_system):
        """
        Test: Sistema se inicializa correctamente
        
        POR QUÉ: Verificar configuración básica
        """
        assert backup_system.backup_dir is not None
        assert os.path.exists(backup_system.backup_dir)
        assert backup_system.max_backups == 10
    
    def test_create_backup(self, backup_system, test_file):
        """
        Test: Crear backup de un archivo
        
        POR QUÉ: Funcionalidad core del sistema
        """
        backup_path = backup_system.create_backup(test_file, tag="test")
        
        assert backup_path is not None
        assert os.path.exists(backup_path)
        assert backup_path.endswith('.bak')
        assert 'test' in backup_path
    
    def test_backup_contains_data(self, backup_system, test_file):
        """
        Test: Backup contiene los datos originales
        
        POR QUÉ: Backup inútil si no tiene los datos correctos
        """
        # Crear backup
        backup_path = backup_system.create_backup(test_file, tag="data_test")
        
        # Leer backup
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        
        # Leer original
        with open(test_file, 'r') as f:
            original_data = json.load(f)
        
        # Verificar que sean idénticos
        assert backup_data == original_data
    
    def test_list_backups(self, backup_system, test_file):
        """
        Test: Listar backups creados
        
        POR QUÉ: Usuario necesita ver backups disponibles
        """
        # Crear varios backups
        backup_system.create_backup(test_file, tag="backup1")
        backup_system.create_backup(test_file, tag="backup2")
        
        # Listar
        backups = backup_system.list_backups()
        
        assert len(backups) >= 2
        assert all('filename' in b for b in backups)
        assert all('size_mb' in b for b in backups)
        assert all('tag' in b for b in backups)
    
    def test_restore_backup(self, backup_system, test_file, tmp_path):
        """
        Test: Restaurar desde backup
        
        POR QUÉ: Funcionalidad crítica de recuperación
        """
        # Crear backup
        backup_path = backup_system.create_backup(test_file, tag="restore_test")
        backup_filename = os.path.basename(backup_path)
        
        # Crear archivo de destino diferente
        restore_target = tmp_path / "restored.json"
        
        # Restaurar
        success = backup_system.restore_backup(backup_filename, str(restore_target))
        
        assert success == True
        assert os.path.exists(restore_target)
        
        # Verificar que datos son correctos
        with open(test_file, 'r') as f:
            original = json.load(f)
        
        with open(restore_target, 'r') as f:
            restored = json.load(f)
        
        assert original == restored
    
    def test_backup_cleanup(self, backup_system, test_file):
        """
        Test: Limpieza automática de backups antiguos
        
        POR QUÉ: No llenar disco infinitamente
        """
        # Crear más backups que el límite
        for i in range(12):
            backup_system.create_backup(test_file, tag=f"cleanup_{i}")
        
        # Verificar que solo quedan max_backups
        backups = backup_system.list_backups()
        
        assert len(backups) <= backup_system.max_backups
    
    def test_backup_stats(self, backup_system, test_file):
        """
        Test: Estadísticas de backups
        
        POR QUÉ: Monitorear espacio usado
        """
        # Crear algunos backups
        backup_system.create_backup(test_file, tag="stats1")
        backup_system.create_backup(test_file, tag="stats2")
        
        # Obtener stats
        stats = backup_system.get_backup_stats()
        
        assert 'total_backups' in stats
        assert 'total_size_mb' in stats
        assert 'backup_dir' in stats
        assert stats['total_backups'] >= 2
    
    def test_backup_nonexistent_file(self, backup_system):
        """
        Test: Intentar backup de archivo inexistente
        
        POR QUÉ: Manejar errores gracefully
        """
        result = backup_system.create_backup("nonexistent.json", tag="fail")
        
        assert result is None

# Test de integración
@pytest.mark.integration
def test_backup_full_workflow(tmp_path):
    """
    Test de integración: Flujo completo de backup
    
    POR QUÉ: Verificar que todo funcione junto
    """
    # 1. Crear sistema
    backup_sys = BackupSystem(backup_dir=str(tmp_path))
    
    # 2. Crear archivo de prueba
    test_file = tmp_path / "workflow_test.json"
    data = {"test": "workflow", "version": 1}
    
    with open(test_file, 'w') as f:
        json.dump(data, f)
    
    # 3. Crear backup
    backup_path = backup_sys.create_backup(str(test_file), tag="workflow")
    assert backup_path is not None
    
    # 4. Modificar archivo original
    data['version'] = 2
    with open(test_file, 'w') as f:
        json.dump(data, f)
    
    # 5. Restaurar backup
    success = backup_sys.restore_backup(
        os.path.basename(backup_path),
        str(test_file)
    )
    assert success == True
    
    # 6. Verificar que se restauró versión 1
    with open(test_file, 'r') as f:
        restored = json.load(f)
    
    assert restored['version'] == 1  # Versión restaurada, no la modificada

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
