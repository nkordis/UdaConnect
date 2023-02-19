from kafka import KafkaConsumer
import os
import sys
from services import LocationService
#from app import create_app, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaConsumer
from config import DevelopmentConfig
from services import LocationService
import os, sys
from __init__ import app, db
from kafka import KafkaConsumer

kafka_topic = os.environ.get("KAFKA_TOPIC") 
kafka_url =   os.environ.get("KAFKA_URL") 
consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_url, group_id='my_group')

for message in consumer:
    try:
        sys.stdout.write(f"Received message: {message.value}\n") 
        with app.app_context():
            LocationService.create(message.value)
    except Exception as e:
        sys.stderr.write(f"Exception occurred while processing message: {e}\n")
        pass

@app.route("/")
def index():
    return "Location app is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
