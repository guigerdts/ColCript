# utils/backup_system.py - Sistema de backups automáticos

import os
import json
import shutil
import time
from datetime import datetime
from typing import Optional, List

class BackupSystem:
    """
    Sistema automático de backups para blockchain
    
    POR QUÉ:
    - Prevenir pérdida de datos
    - Recuperación rápida ante fallos
    - Múltiples puntos de restauración
    """
    
    def __init__(self, backup_dir: str = None):
        """
        Inicializa el sistema de backups
        
        Args:
            backup_dir: Directorio para guardar backups
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if backup_dir is None:
            self.backup_dir = os.path.join(project_root, 'backups')
        else:
            self.backup_dir = backup_dir
        
        # Crear directorio si no existe
        os.makedirs(self.backup_dir, exist_ok=True)
        
        self.max_backups = 10  # Mantener últimos 10 backups
    
    def create_backup(self, source_file: str, tag: str = "auto") -> Optional[str]:
        """
        Crea un backup de un archivo
        
        POR QUÉ: Guardar estado actual antes de cambios críticos
        
        Args:
            source_file: Archivo a respaldar
            tag: Etiqueta del backup (auto, manual, pre-update, etc.)
        
        Returns:
            Path del backup creado o None si falla
        """
        if not os.path.exists(source_file):
            print(f"❌ Archivo no encontrado: {source_file}")
            return None
        
        try:
            # Nombre del backup con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(source_file)
            backup_name = f"{filename}.{tag}.{timestamp}.bak"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Copiar archivo
            shutil.copy2(source_file, backup_path)
            
            # Obtener tamaño
            size_bytes = os.path.getsize(backup_path)
            size_mb = size_bytes / (1024 * 1024)
            
            print(f"💾 Backup creado: {backup_name}")
            print(f"   Tamaño: {size_mb:.2f} MB")
            print(f"   Tag: {tag}")
            
            # Limpiar backups antiguos
            self._cleanup_old_backups(filename)
            
            return backup_path
        
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
            return None
    
    def restore_backup(self, backup_file: str, target_file: str) -> bool:
        """
        Restaura un backup
        
        POR QUÉ: Recuperar datos ante fallos
        
        Args:
            backup_file: Archivo de backup
            target_file: Destino de la restauración
        
        Returns:
            True si éxito, False si falla
        """
        backup_path = os.path.join(self.backup_dir, backup_file)
        
        if not os.path.exists(backup_path):
            print(f"❌ Backup no encontrado: {backup_file}")
            return False
        
        try:
            # Crear backup del archivo actual antes de sobrescribir
            if os.path.exists(target_file):
                temp_backup = f"{target_file}.pre-restore.bak"
                shutil.copy2(target_file, temp_backup)
                print(f"🔄 Backup de seguridad creado: {os.path.basename(temp_backup)}")
            
            # Restaurar
            shutil.copy2(backup_path, target_file)
            
            print(f"✅ Backup restaurado: {backup_file}")
            print(f"   → {target_file}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error restaurando backup: {e}")
            return False
    
    def list_backups(self, filename_pattern: str = None) -> List[dict]:
        """
        Lista backups disponibles
        
        POR QUÉ: Ver puntos de restauración disponibles
        
        Args:
            filename_pattern: Filtrar por patrón (ej: "colcript_main")
        
        Returns:
            Lista de backups con metadata
        """
        backups = []
        
        try:
            files = os.listdir(self.backup_dir)
            
            for file in files:
                if not file.endswith('.bak'):
                    continue
                
                # Filtrar por patrón si se especifica
                if filename_pattern and filename_pattern not in file:
                    continue
                
                filepath = os.path.join(self.backup_dir, file)
                stat = os.stat(filepath)
                
                # Parsear info del nombre
                parts = file.split('.')
                tag = parts[-3] if len(parts) >= 3 else "unknown"
                timestamp_str = parts[-2] if len(parts) >= 2 else "unknown"
                
                backups.append({
                    'filename': file,
                    'size_mb': stat.st_size / (1024 * 1024),
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'tag': tag,
                    'timestamp': timestamp_str
                })
            
            # Ordenar por fecha (más recientes primero)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
            return backups
        
        except Exception as e:
            print(f"❌ Error listando backups: {e}")
            return []
    
    def _cleanup_old_backups(self, filename: str):
        """
        Limpia backups antiguos manteniendo solo max_backups
        
        POR QUÉ: No llenar el disco con backups infinitos
        """
        try:
            # Obtener todos los backups de este archivo
            all_backups = [
                f for f in os.listdir(self.backup_dir)
                if f.startswith(filename) and f.endswith('.bak')
            ]
            
            # Ordenar por fecha de modificación (más recientes primero)
            all_backups.sort(
                key=lambda x: os.path.getmtime(os.path.join(self.backup_dir, x)),
                reverse=True
            )
            
            # Eliminar los más antiguos si exceden el límite
            if len(all_backups) > self.max_backups:
                to_delete = all_backups[self.max_backups:]
                
                for old_backup in to_delete:
                    old_path = os.path.join(self.backup_dir, old_backup)
                    os.remove(old_path)
                    print(f"🗑️  Backup antiguo eliminado: {old_backup}")
        
        except Exception as e:
            print(f"⚠️  Error limpiando backups: {e}")
    
    def get_backup_stats(self) -> dict:
        """
        Obtiene estadísticas de backups
        
        POR QUÉ: Monitorear espacio usado y cantidad de backups
        
        Returns:
            Dict con estadísticas
        """
        try:
            backups = os.listdir(self.backup_dir)
            total_size = sum(
                os.path.getsize(os.path.join(self.backup_dir, f))
                for f in backups
                if f.endswith('.bak')
            )
            
            return {
                'total_backups': len([f for f in backups if f.endswith('.bak')]),
                'total_size_mb': total_size / (1024 * 1024),
                'backup_dir': self.backup_dir,
                'max_backups_per_file': self.max_backups
            }
        
        except Exception as e:
            print(f"❌ Error obteniendo stats: {e}")
            return {}

# Test
if __name__ == "__main__":
    print("\n💾 Probando sistema de backups...\n")
    
    # Crear sistema de backups
    backup_sys = BackupSystem()
    
    # Test 1: Crear archivo de prueba
    print("1️⃣  Creando archivo de prueba...")
    test_file = "test_data.json"
    test_data = {"test": "data", "blocks": 100}
    
    with open(test_file, 'w') as f:
        json.dump(test_data, f)
    print(f"   Archivo creado: {test_file}")
    
    # Test 2: Crear backup
    print("\n2️⃣  Creando backup...")
    backup_path = backup_sys.create_backup(test_file, tag="manual")
    
    # Test 3: Listar backups
    print("\n3️⃣  Listando backups...")
    backups = backup_sys.list_backups()
    print(f"   Total backups: {len(backups)}")
    for backup in backups:
        print(f"   - {backup['filename']} ({backup['size_mb']:.2f} MB)")
    
    # Test 4: Stats
    print("\n4️⃣  Estadísticas de backups...")
    stats = backup_sys.get_backup_stats()
    print(f"   Total: {stats['total_backups']} backups")
    print(f"   Espacio: {stats['total_size_mb']:.2f} MB")
    
    # Test 5: Restaurar
    print("\n5️⃣  Probando restauración...")
    if backups:
        restored = backup_sys.restore_backup(backups[0]['filename'], "test_restored.json")
        if restored:
            print("   ✅ Restauración exitosa")
    
    # Cleanup
    os.remove(test_file) if os.path.exists(test_file) else None
    os.remove("test_restored.json") if os.path.exists("test_restored.json") else None
    
    print("\n✅ Sistema de backups funcionando\n")
