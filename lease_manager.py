from datetime import datetime, timedelta

class LeaseManager:
    def __init__(self, lease_duration=timedelta(hours=1)):
        self.leases = {}
        self.lease_duration = lease_duration

    def acquire_lease(self, key):
        if key in self.leases:
            return False
        self.leases[key] = datetime.now()
        return True

    def release_lease(self, key):
        if key in self.leases:
            del self.leases[key]

    def heartbeat_lease(self, key):
        if key in self.leases:
            self.leases[key] = datetime.now()
            return True
        return False

    def is_lease_active(self, key):
        if key in self.leases:
            return datetime.now() - self.leases[key] < self.lease_duration
        return False

    def clean_expired_leases(self):
        current_time = datetime.now()
        expired_keys = [key for key, lease_time in self.leases.items() if current_time - lease_time >= self.lease_duration]
        for key in expired_keys:
            del self.leases[key]
