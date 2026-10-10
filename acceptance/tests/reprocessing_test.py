import pytest
from your_library import process_message

@pytest.mark.parametrize('message, expected_result', [
    ('message1', 'result1'),
    ('message2', 'result2'),
])
def test_reprocessing(message, expected_result):
    # Simulate processing and then reprocessing
    result1 = process_message(message)
    assert result1 == expected_result
    result2 = process_message(message)
    assert result2 == expected_result
    # Check if the result is retrieved from cache
    assert result2 == result1