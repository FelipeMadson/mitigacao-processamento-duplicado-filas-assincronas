from idempotency_repository import IdempotencyRepository
from idempotency_serializer import IdempotencySerializer

class IdempotencyTransaction:
    def __init__(self, repository: IdempotencyRepository, serializer: IdempotencySerializer):
        self.repository = repository
        self.serializer = serializer

    def execute(self, key: str, data: dict):
        serialized_data = self.serializer.serialize(data)
        if not self.repository.is_idempotent(key):
            self.repository.save_idempotency(key)
            # Execute the transactional logic here
            print(f'Transaction executed for key: {key} with data: {serialized_data}')
        else:
            print(f'Transaction already executed for key: {key}')