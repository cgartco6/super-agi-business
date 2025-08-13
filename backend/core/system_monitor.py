import psutil
import time
from typing import Dict, List
from .logging_setup import Logger
from .utilities.api_client import APIClient

class SystemMonitor:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        self.api_client = APIClient()
        self.metrics = {
            'cpu': [],
            'memory': [],
            'disk': [],
            'network': []
        }
        self.thresholds = {
            'cpu': 80,
            'memory': 85,
            'disk': 90,
            'network': 70
        }

    def start_monitoring(self, interval: int = 60):
        """Continuous system monitoring"""
        while True:
            self._collect_metrics()
            self._check_thresholds()
            time.sleep(interval)

    def _collect_metrics(self):
        """Gather system performance metrics"""
        timestamp = time.time()
        
        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.metrics['cpu'].append((timestamp, cpu_percent))
        
        # Memory Usage
        mem = psutil.virtual_memory()
        self.metrics['memory'].append((timestamp, mem.percent))
        
        # Disk Usage
        disk = psutil.disk_usage('/')
        self.metrics['disk'].append((timestamp, disk.percent))
        
        # Network Usage
        net = psutil.net_io_counters()
        self.metrics['network'].append((timestamp, net.bytes_sent + net.bytes_recv))

    def _check_thresholds(self):
        """Check if any metrics exceed thresholds"""
        alerts = []
        
        for metric, values in self.metrics.items():
            if not values:
                continue
                
            current_value = values[-1][1]
            if current_value > self.thresholds[metric]:
                alerts.append({
                    'metric': metric,
                    'value': current_value,
                    'threshold': self.thresholds[metric],
                    'timestamp': values[-1][0]
                })
        
        if alerts:
            self._trigger_alert(alerts)

    def _trigger_alert(self, alerts: List[Dict]):
        """Handle system alerts"""
        self.logger.warning(f"System thresholds exceeded: {alerts}")
        
        # Send alerts to monitoring dashboard
        self.api_client.post('monitoring/alerts', {'alerts': alerts})
        
        # Implement auto-healing for critical issues
        if any(alert['value'] > 95 for alert in alerts):
            self._activate_healing_protocol()

    def _activate_healing_protocol(self):
        """Initiate automatic healing procedures"""
        self.logger.info("Activating healing protocols")
        
        # Example healing actions
        healing_actions = {
            'high_cpu': self._reduce_cpu_load,
            'high_memory': self._free_up_memory,
            'high_disk': self._clean_up_disk,
            'network_congestion': self._adjust_network_settings
        }
        
        for alert in self.metrics:
            if alert[-1][1] > 95:
                healing_actions.get(alert, lambda: None)()

    def _reduce_cpu_load(self):
        """Reduce CPU usage by scaling down non-critical processes"""
        pass

    def _free_up_memory(self):
        """Free up memory by clearing caches and buffers"""
        pass

    def get_system_report(self) -> Dict:
        """Generate comprehensive system report"""
        return {
            'status': 'healthy' if not self._check_thresholds() else 'warning',
            'metrics': self.metrics,
            'uptime': time.time() - self.start_time,
            'recommendations': self._generate_recommendations()
        }
