# aiva_core/collector.py
import schedule
import time
import threading
from .health_monitor import HealthMonitor

class Collector:
    def __init__(self, cfg, memory):
        self.memory = memory
        self.cfg = cfg
        self.health = HealthMonitor(memory)

    def start_schedule(self):
        # example: collect system stats every 30 minutes
        schedule.every(30).minutes.do(self.collect_system_stats)
        schedule.every().day.at("20:00").do(self.collect_daily_health)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def collect_system_stats(self):
        st = self.health.get_system_stats()
        self.memory.add_conversation('system', f"system_stats: {st}")
        print("Collector: collected system stats")

    def collect_daily_health(self):
        h = self.health.get_manual_health()
        self.memory.add_conversation('health', h)
        print("Collector: collected daily health")
