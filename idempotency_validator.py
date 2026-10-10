from datetime import datetime, timedelta

class IdempotencyValidator:
    def __init__(self, registry):
        self.registry = registry

    def validate(self, operation):
        if self.registry.is_key_registered(operation):
            return False
        self.registry.register_key(operation)
        return True

    def reprocess(self, operation):
        if self.registry.is_key_registered(operation):
            return self.registry.get_cached_result(operation)
        return None

    def get_cached_result(self, operation):
        # Simulate retrieving cached result
        return 'Cached result for operation: {}'.format(operation)

    def register_key(self, operation, lease_duration=timedelta(hours=1)):
        self.registry.register_key(operation, lease_duration)

    def is_key_registered(self, operation):
        return self.registry.is_key_registered(operation)