import pytest
from your_library import process_message

@pytest.mark.parametrize('message, expected_result', [
    ('message1', 'result1'),
    ('message2', 'result2'),
])
def test_concurrency(message, expected_result):
    # Simulate concurrent processing
    result = process_message(message)
    assert result == expected_result
    # Additional checks for uniqueness and idempotency can be added here