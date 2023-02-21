import time
import time
import json
import random
import sys
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka-service:9092')
topic = 'location'


while True:
    latitude = round(random.uniform(-90, 90), 4)
    longitude = round(random.uniform(-180, 180), 4)
    data = {'user_id': 1, 'latitude': latitude, 'longitude': longitude}
    message = json.dumps(data).encode()
    producer.send(topic, message)
    sys.stdout.write(f"Sent message to Kafka: {message}\n")
    sys.stdout.flush()
    time.sleep(20)

sys.stdout.write("Finished sending messages to Kafka\n")
sys.stdout.flush()

