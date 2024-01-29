# Under Explore
# Ref: https://kafkaide.com/learn/how-to-start-using-apache-kafka-in-python/


import json
from kafka import KafkaProducer

# Function to publish a message to a Kafka topic
def publish_message(kafka_producer, topic_name, key, value):
    try:
        # Convert key and value to bytes
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        
        # Send the message to the Kafka topic
        kafka_producer.send(topic_name, key=key_bytes, value=value_bytes)
        
        # Flush the producer to ensure the message is sent immediately
        kafka_producer.flush()
        
        print('Message published successfully.')
    except Exception as ex:
        print(str(ex))

# Entry point of the script
if __name__ == '__main__':
    # Creating a KafkaProducer instance
    kafka_producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    
    # Sample employee data
    employees = [
        {"name": "John Smith", "id": "1"},
        {"name": "Susan Doe", "id": "2"},
        {"name": "Karen Rock", "id": "3"},
    ]
    
    # Loop through each employee and publish their information to the Kafka topic
    for employee in employees:
        publish_message(
            kafka_producer=kafka_producer,
            topic_name='explore-kafka',
            key=employee['id'],
            value=json.dumps(employee)
        )
    
    # Close the KafkaProducer when done
    if kafka_producer is not None:
        kafka_producer.close()
