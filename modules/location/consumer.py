from kafka import KafkaConsumer
import os
import sys

kafka_topic = os.environ.get("KAFKA_TOPIC") 
kafka_url =   os.environ.get("KAFKA_URL") 
consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_url)

for message in consumer:
   sys.stdout.write(f"Received message: {message.value}\n") 

@app.route("/")
def index():
    return "Location app is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
