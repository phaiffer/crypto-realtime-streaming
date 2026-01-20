import time
import json
import requests
from confluent_kafka import Producer
from datetime import datetime

# --- Configuration ---
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'crypto_prices'

# List of symbols to track
SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'ADAUSDT']


# --- Delivery Report Callback ---
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        # Debug print disabled to reduce console noise with multiple symbols
        pass

    # --- Producer Initialization ---


conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
}

try:
    producer = Producer(conf)
    print(f"Connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}")
except Exception as e:
    print(f"Error connecting to Kafka: {e}")
    exit()

# --- Main Loop ---
if __name__ == "__main__":
    print(f"Starting streaming for symbols: {SYMBOLS}")

    try:
        while True:
            for symbol in SYMBOLS:
                try:
                    # 1. Fetch data from Binance API
                    api_url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
                    response = requests.get(api_url)
                    data = response.json()

                    # 2. Enrich data
                    payload = {
                        'symbol': data['symbol'],
                        'price': float(data['price']),
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    # 3. Send to Kafka
                    producer.produce(
                        KAFKA_TOPIC,
                        value=json.dumps(payload).encode('utf-8'),
                        callback=delivery_report
                    )

                    print(f"Sent: {payload['symbol']} - ${payload['price']}")

                except Exception as req_error:
                    print(f"Error fetching {symbol}: {req_error}")

            # Serve delivery callback queue
            producer.poll(0)

            # Wait 5 seconds before the next batch of requests
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nStreaming stopped by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        producer.flush()