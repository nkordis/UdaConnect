from kafka import KafkaConsumer
from services import LocationService
import os
import sys
from __init__ import app

kafka_topic = os.environ.get("KAFKA_TOPIC") 
kafka_url = os.environ.get("KAFKA_URL") 
consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_url, group_id='my_group')

for message in consumer:
    try:
        sys.stdout.write(f"Received message: {message.value}\n") 
        with app.app_context():
            LocationService.create(message.value)
    except Exception as e:
        sys.stderr.write(f"Exception occurred while processing message: {e}\n")
        pass

