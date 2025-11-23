# blockchain/difficulty.py - Sistema de ajuste automático de dificultad

import os
import sys

# Obtener ruta absoluta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import config

class DifficultyAdjustment:
    """
    Sistema de ajuste automático de dificultad
    Inspirado en Bitcoin
    """
    
    @staticmethod
    def should_adjust(blockchain):
        """
        Determina si es momento de ajustar la dificultad
        """
        if not config.DIFFICULTY_ADJUSTMENT_ENABLED:
            return False
        
        # Ajustar cada N bloques
        current_height = len(blockchain.chain)
        return current_height > 0 and current_height % config.DIFFICULTY_ADJUSTMENT_INTERVAL == 0
    
    @staticmethod
    def calculate_new_difficulty(blockchain):
        """
        Calcula la nueva dificultad basándose en el tiempo de minado
        """
        current_difficulty = blockchain.difficulty
        chain_length = len(blockchain.chain)
        
        # Necesitamos al menos INTERVAL bloques para calcular
        if chain_length < config.DIFFICULTY_ADJUSTMENT_INTERVAL:
            return current_difficulty
        
        # Obtener bloques del último intervalo
        start_index = chain_length - config.DIFFICULTY_ADJUSTMENT_INTERVAL
        start_block = blockchain.chain[start_index]
        end_block = blockchain.chain[-1]
        
        # Calcular tiempo real transcurrido
        actual_time = end_block.timestamp - start_block.timestamp
        
        # Tiempo esperado para el intervalo
        expected_time = config.TARGET_BLOCK_TIME * config.DIFFICULTY_ADJUSTMENT_INTERVAL
        
        # Calcular ratio
        time_ratio = actual_time / expected_time
        
        # Ajustar dificultad
        # Si minado muy rápido (ratio < 1) → aumentar dificultad
        # Si minado muy lento (ratio > 1) → disminuir dificultad
        
        if time_ratio < 0.5:
            # Minado muy rápido, aumentar dificultad
            new_difficulty = current_difficulty + 1
        elif time_ratio < 0.75:
            # Minado rápido, aumentar un poco
            new_difficulty = current_difficulty + 1
        elif time_ratio > 2.0:
            # Minado muy lento, disminuir dificultad
            new_difficulty = current_difficulty - 1
        elif time_ratio > 1.5:
            # Minado lento, disminuir un poco
            new_difficulty = current_difficulty - 1
        else:
            # Tiempo aceptable, mantener dificultad
            new_difficulty = current_difficulty
        
        # Aplicar límites
        new_difficulty = max(config.MIN_DIFFICULTY, new_difficulty)
        new_difficulty = min(config.MAX_DIFFICULTY, new_difficulty)
        
        return new_difficulty
    
    @staticmethod
    def adjust_if_needed(blockchain):
        """
        Ajusta la dificultad si es necesario
        Retorna (adjusted: bool, old_diff: int, new_diff: int, reason: str)
        """
        if not DifficultyAdjustment.should_adjust(blockchain):
            return False, blockchain.difficulty, blockchain.difficulty, "No adjustment needed"
        
        old_difficulty = blockchain.difficulty
        new_difficulty = DifficultyAdjustment.calculate_new_difficulty(blockchain)
        
        if old_difficulty == new_difficulty:
            return False, old_difficulty, new_difficulty, "Difficulty unchanged"
        
        # Determinar razón
        if new_difficulty > old_difficulty:
            reason = f"Blocks mined too fast, increasing difficulty"
        else:
            reason = f"Blocks mined too slow, decreasing difficulty"
        
        # Aplicar nueva dificultad
        blockchain.difficulty = new_difficulty
        
        return True, old_difficulty, new_difficulty, reason
    
    @staticmethod
    def get_adjustment_info(blockchain):
        """
        Obtiene información sobre el próximo ajuste
        """
        current_height = len(blockchain.chain)
        blocks_until_adjustment = config.DIFFICULTY_ADJUSTMENT_INTERVAL - (current_height % config.DIFFICULTY_ADJUSTMENT_INTERVAL)
        
        if blocks_until_adjustment == config.DIFFICULTY_ADJUSTMENT_INTERVAL:
            blocks_until_adjustment = 0
        
        # Calcular tiempo promedio actual
        if current_height >= 2:
            recent_blocks = min(10, current_height - 1)
            start_block = blockchain.chain[-(recent_blocks + 1)]
            end_block = blockchain.chain[-1]
            
            time_span = end_block.timestamp - start_block.timestamp
            avg_time = time_span / recent_blocks
        else:
            avg_time = 0
        
        return {
            "current_difficulty": blockchain.difficulty,
            "blocks_until_adjustment": blocks_until_adjustment,
            "adjustment_interval": config.DIFFICULTY_ADJUSTMENT_INTERVAL,
            "target_block_time": config.TARGET_BLOCK_TIME,
            "current_avg_time": round(avg_time, 2),
            "min_difficulty": config.MIN_DIFFICULTY,
            "max_difficulty": config.MAX_DIFFICULTY,
            "adjustment_enabled": config.DIFFICULTY_ADJUSTMENT_ENABLED
        }

# Test
if __name__ == "__main__":
    print("\n⚙️  Probando ajuste automático de dificultad...\n")
    
    from blockchain.blockchain import Blockchain
    from utils.crypto import generate_keypair
    import time
    
    # Crear blockchain
    print("1. Creando blockchain de prueba...")
    bc = Blockchain(auto_save=False)
    bc.difficulty = 2  # Empezar con dificultad baja para pruebas rápidas
    
    print(f"   Dificultad inicial: {bc.difficulty}")
    print(f"   Intervalo de ajuste: cada {config.DIFFICULTY_ADJUSTMENT_INTERVAL} bloques")
    print(f"   Tiempo objetivo: {config.TARGET_BLOCK_TIME}s por bloque\n")
    
    # Crear minero
    priv, pub = generate_keypair()
    
    # Minar bloques
    print("2. Minando bloques para probar ajuste...\n")
    
    for i in range(config.DIFFICULTY_ADJUSTMENT_INTERVAL + 2):
        print(f"   Minando bloque {i + 1}...")
        start = time.time()
        bc.mine_pending_transactions(pub)
        elapsed = time.time() - start
        
        print(f"   ✅ Minado en {elapsed:.2f}s (dificultad: {bc.difficulty})")
        
        # Verificar si hubo ajuste
        if i > 0 and len(bc.chain) % config.DIFFICULTY_ADJUSTMENT_INTERVAL == 0:
            adjusted, old_d, new_d, reason = DifficultyAdjustment.adjust_if_needed(bc)
            if adjusted:
                print(f"\n   🔧 AJUSTE DE DIFICULTAD:")
                print(f"      {old_d} → {new_d}")
                print(f"      Razón: {reason}\n")
    
    # Info de ajuste
    print("\n3. Información de ajuste:")
    info = DifficultyAdjustment.get_adjustment_info(bc)
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Sistema de ajuste automático funcionando\n")
