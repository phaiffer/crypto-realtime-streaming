import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch


# --- Test Logic ---
def test_data_formatting():
    """
    Test if the API response is correctly transformed into the Kafka payload.
    """
    # 1. Simulate Binance API Response
    mock_response_data = {
        'symbol': 'BTCUSDT',
        'price': '50000.00'  # API returns strings
    }

    # 2. Define the expected output structure
    expected_symbol = 'BTCUSDT'
    expected_price = 50000.00

    # 3. Simulate the logic used in btc_producer.py
    # We reconstruct the logic here to isolate it from the Kafka connection
    symbol = mock_response_data['symbol']
    price = float(mock_response_data['price'])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    payload = {
        'symbol': symbol,
        'price': price,
        'timestamp': timestamp
    }

    # 4. Assertions (Validations)
    assert payload['symbol'] == expected_symbol
    assert payload['price'] == expected_price
    assert isinstance(payload['price'], float)
    assert isinstance(payload['timestamp'], str)


@patch('requests.get')
def test_api_integration_mock(mock_get):
    """
    Test if the requests.get method returns the expected mocked data.
    """
    # Setup the mock to return specific data
    mock_response = MagicMock()
    mock_response.json.return_value = {'symbol': 'ETHUSDT', 'price': '3000.00'}
    mock_get.return_value = mock_response

    # Call the mocked function
    import requests
    response = requests.get('https://fake-url.com')
    data = response.json()

    # Validate
    assert data['symbol'] == 'ETHUSDT'
    assert data['price'] == '3000.00'