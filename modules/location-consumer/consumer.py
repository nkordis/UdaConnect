from kafka import KafkaConsumer
from datetime import datetime
import os
import json
import psycopg2
import sys

kafka_topic = os.environ["KAFKA_TOPIC"]
kafka_url = os.environ["KAFKA_URL"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

DATE_FORMAT = "%Y-%m-%d"

print("Consumer started...", file=sys.stderr)
sys.stdout.write("Consumer started...")

consumer = KafkaConsumer(
    kafka_topic, bootstrap_servers=kafka_url, group_id='my_group'
)

print("Consumer connected to Kafka broker...", file=sys.stderr)

# Connect to database
connection = psycopg2.connect(
    dbname=DB_NAME, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST
)

print("Consumer connected to the database...", file=sys.stderr)


for message in consumer:
    print(f"Received message: {message.value}\n", file=sys.stderr)
    try:       
        location = json.loads(message.value.decode("utf-8"))
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO location (person_id, coordinate, creation_time) VALUES ({}, ST_Point({}, {}), \'{}\');'.format(
                    int(location["user_id"]), float(location["latitude"]), float(location["longitude"]), datetime.now().strftime(DATE_FORMAT)
                )
            )
            connection.commit()
        
        print("Location added to the database!", file=sys.stderr)
    except Exception as e:
        print(f"Exception occurred while processing message: {e}", file=sys.stderr)
        connection.rollback()
        pass

# Close database connection
connection.close()


