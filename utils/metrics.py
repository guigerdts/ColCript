# utils/metrics.py - Sistema de métricas y monitoreo

import time
import os
from collections import defaultdict
from datetime import datetime
from typing import Dict

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

class MetricsCollector:
    """Sistema de métricas"""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.endpoint_metrics = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'errors': 0
        })
    
    def record_request(self, endpoint: str, duration: float, success: bool = True):
        """Registra una request"""
        self.request_count += 1
        
        if not success:
            self.error_count += 1
            self.endpoint_metrics[endpoint]['errors'] += 1
        
        self.endpoint_metrics[endpoint]['count'] += 1
        self.endpoint_metrics[endpoint]['total_time'] += duration
    
    def get_system_metrics(self) -> Dict:
        """Métricas del sistema"""
        if not HAS_PSUTIL:
            return {'error': 'psutil not available'}
        
        metrics = {
            'uptime_seconds': round(time.time() - self.start_time, 2)
        }
        
        # CPU
        try:
            metrics['cpu'] = {
                'percent': psutil.cpu_percent(interval=0.1),
                'count': psutil.cpu_count()
            }
        except:
            metrics['cpu'] = {'error': 'unavailable'}
        
        # Memory
        try:
            process = psutil.Process(os.getpid())
            vm = psutil.virtual_memory()
            metrics['memory'] = {
                'percent': vm.percent,
                'used_mb': round(process.memory_info().rss / (1024 * 1024), 2),
                'available_mb': round(vm.available / (1024 * 1024), 2)
            }
        except:
            metrics['memory'] = {'error': 'unavailable'}
        
        # Disk
        try:
            disk = psutil.disk_usage('/')
            metrics['disk'] = {
                'percent': disk.percent,
                'free_gb': round(disk.free / (1024 * 1024 * 1024), 2)
            }
        except:
            metrics['disk'] = {'error': 'unavailable'}
        
        return metrics
    
    def get_api_metrics(self) -> Dict:
        """Métricas de la API"""
        uptime = time.time() - self.start_time
        
        top_endpoints = sorted(
            self.endpoint_metrics.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:10]
        
        endpoint_stats = []
        for endpoint, m in top_endpoints:
            avg = (m['total_time'] / m['count']) if m['count'] > 0 else 0
            err_rate = (m['errors'] / m['count']) if m['count'] > 0 else 0
            
            endpoint_stats.append({
                'endpoint': endpoint,
                'requests': m['count'],
                'avg_time_ms': round(avg * 1000, 2),
                'error_rate': round(err_rate * 100, 2),
                'errors': m['errors']
            })
        
        return {
            'uptime_seconds': round(uptime, 2),
            'uptime_formatted': self._format_uptime(uptime),
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'error_rate': round((self.error_count / self.request_count * 100) if self.request_count > 0 else 0, 2),
            'requests_per_second': round(self.request_count / uptime if uptime > 0 else 0, 2),
            'top_endpoints': endpoint_stats
        }
    
    def get_health_status(self) -> Dict:
        """Estado de salud"""
        system = self.get_system_metrics()
        issues = []
        
        if 'error' not in system:
            cpu = system.get('cpu', {})
            if 'error' not in cpu and cpu.get('percent', 0) > 90:
                issues.append('High CPU usage')
            
            mem = system.get('memory', {})
            if 'error' not in mem and mem.get('percent', 0) > 90:
                issues.append('High memory usage')
            
            disk = system.get('disk', {})
            if 'error' not in disk and disk.get('percent', 0) > 90:
                issues.append('Low disk space')
        
        if self.request_count > 100 and (self.error_count / self.request_count) > 0.1:
            issues.append('High error rate (>10%)')
        
        status = 'healthy' if not issues else ('degraded' if len(issues) == 1 else 'unhealthy')
        
        return {
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'issues': issues
        }
    
    def _format_uptime(self, seconds: float) -> str:
        """Formatea uptime"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        
        parts = []
        if days > 0: parts.append(f"{days}d")
        if hours > 0: parts.append(f"{hours}h")
        if minutes > 0 or not parts: parts.append(f"{minutes}m")
        
        return " ".join(parts)

# Instancia global
metrics = MetricsCollector()

# Test
if __name__ == "__main__":
    print("\n📊 Probando sistema de métricas...\n")
    
    print("1️⃣  Simulando requests...")
    metrics.record_request('/api/blockchain/info', 0.05, success=True)
    metrics.record_request('/api/wallet/balance', 0.03, success=True)
    metrics.record_request('/api/mining/mine', 2.5, success=True)
    metrics.record_request('/api/transaction/send', 0.1, success=False)
    
    print("\n2️⃣  Métricas de sistema:")
    system = metrics.get_system_metrics()
    
    if 'error' in system:
        print(f"   Error: {system['error']}")
    else:
        cpu = system.get('cpu', {})
        if 'error' not in cpu:
            print(f"   CPU: {cpu.get('percent', 0)}%")
        
        mem = system.get('memory', {})
        if 'error' not in mem:
            print(f"   Memory: {mem.get('percent', 0)}% ({mem.get('used_mb', 0)} MB)")
        
        disk = system.get('disk', {})
        if 'error' not in disk:
            print(f"   Disk: {disk.get('percent', 0)}% ({disk.get('free_gb', 0)} GB free)")
    
    print("\n3️⃣  Métricas de API:")
    api = metrics.get_api_metrics()
    print(f"   Requests: {api['total_requests']}")
    print(f"   Error rate: {api['error_rate']}%")
    print(f"   Uptime: {api['uptime_formatted']}")
    
    print("\n4️⃣  Health check:")
    health = metrics.get_health_status()
    print(f"   Status: {health['status']}")
    print(f"   Issues: {len(health['issues'])}")
    
    print("\n✅ Sistema de métricas funcionando\n")
