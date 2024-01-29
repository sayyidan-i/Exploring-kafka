import json
from time import sleep

# Under Explore
# Ref: https://kafkaide.com/learn/how-to-start-using-apache-kafka-in-python/

# Entry point of the script
if __name__ == '__main__':
    # Creating a KafkaConsumer instance
    consumer = KafkaConsumer(
        'explore-kafka',                     # Topic to subscribe to
        auto_offset_reset='earliest',       # Set offset to the earliest available when no initial offset is present
        bootstrap_servers=['localhost:9092'],# Kafka broker addresses
        api_version=(0, 10),                 # Kafka API version
        consumer_timeout_ms=1000              # Timeout for the consumer to wait for new messages (1 second in this case)
    )
    
    # Iterate over messages received from the Kafka topic
    for msg in consumer:
        # Parse the JSON message payload
        record = json.loads(msg.value)
        
        # Extracting relevant information from the JSON data
        employee_id = int(record['id'])
        name = record['name']

        # Printing information about the employee
        print(f'Employee ID: {employee_id} is {name}')

    # Close the KafkaConsumer when done
    if consumer is not None:
        consumer.close()