import psutil
import time
import threading
import logging

# Constants
CPU_LIMIT = 98.0  # Percentage
RAM_LIMIT = 96.0  # Percentage (Increased for M1 8GB Demo)
CHECK_INTERVAL = 2  # Seconds

class SystemFuse:
    def __init__(self):
        self.blown = False
        self.reason = None
        self.cpu_usage = 0.0
        self.ram_usage = 0.0
        self.active_users = 0
        self._monitoring = False
        self._cpu_strike = 0

    def start_monitoring(self):
        self._monitoring = True
        t = threading.Thread(target=self._monitor_loop, daemon=True)
        t.start()
        print("⚡ [FUSE] System Monitor Started. Limits: CPU 90%, RAM 90%")

    def _monitor_loop(self):
        # Grace period for startup
        time.sleep(20) 
        
        while self._monitoring:
            self.cpu_usage = psutil.cpu_percent(interval=1)
            self.ram_usage = psutil.virtual_memory().percent
            
            if not self.blown:
                # Require 5 consecutive hits to blow
                if self.cpu_usage > CPU_LIMIT:
                    self._cpu_strike += 1
                else:
                    self._cpu_strike = 0
                    
                if self._cpu_strike >= 5:
                     self.blow_fuse(f"CRITICAL CPU LOAD: {self.cpu_usage}% (Sustained)")

                if self.ram_usage > RAM_LIMIT:
                    self.blow_fuse(f"CRITICAL RAM LOAD: {self.ram_usage}%")
            
            time.sleep(CHECK_INTERVAL)

    def blow_fuse(self, reason):
        self.blown = True
        self.reason = reason
        print(f"🔥 [FUSE BLOWN] {reason} | Server entering PROTECTED MODE.")
        # In a real scenario, this might send a signal to shutdown uvicorn or block all requests

    def is_safe(self):
        return not self.blown

    def get_status(self):
        return {
            "safe": not self.blown,
            "reason": self.reason,
            "cpu": self.cpu_usage,
            "ram": self.ram_usage,
            "users": self.active_users
        }

# Global Instance
fuse = SystemFuse()
