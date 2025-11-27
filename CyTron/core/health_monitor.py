# aiva_core/health_monitor.py
import psutil
import random

class HealthMonitor:
    def __init__(self, memory):
        self.memory = memory

    def get_system_stats(self):
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        return {'cpu': cpu, 'mem': mem}

    def get_manual_health(self):
        # placeholder: in real system read from device or ask user
        # Here we will simulate by asking user input (for demo)
        print("Nhập dữ liệu sức khỏe hôm nay (sleep_hours, steps, heart_rate) cách nhau bằng dấu phẩy, hoặc để trống để giả lập:")
        s = input("health> ").strip()
        if not s:
            return {'sleep_hours': 7 + random.random(), 'steps': int(1000 + random.random()*8000), 'hr': 60 + int(random.random()*30)}
        try:
            a, b, c = s.split(',')
            return {'sleep_hours': float(a.strip()), 'steps': int(b.strip()), 'hr': int(c.strip())}
        except:
            return {'note': 'invalid input'}
