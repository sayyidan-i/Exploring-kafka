# Under Explore
# Ref https://www.youtube.com/watch?v=Q4XA5nUpLeo

from kafka import KafkaConsumer
import json

# Entry point of the script
if __name__ == "__main__":
    # Creating a KafkaConsumer instance
    consumer = KafkaConsumer(
        "explore-kafka",                    # Topic to subscribe to
        bootstrap_servers='localhost:9092', # Kafka broker address
        auto_offset_reset='earliest',      # Set offset to the earliest available when no initial offset is present
        api_version=(0, 10)                 # Kafka API version
    )
    
    # Print a message indicating the start of the consumer
    print("Starting the consumer")
    
    # Loop to consume messages from the Kafka topic
    for msg in consumer:
        # Print the deserialized message (assuming it contains JSON data)
        print("Registered User = {}".format(json.loads(msg.value)))
