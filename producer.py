# Under Explore
# Ref https://www.youtube.com/watch?v=Q4XA5nUpLeo

from kafka import KafkaProducer
import json
from data import get_registered_user  # Assuming there's a custom function 'get_registered_user' in the 'data' module
import time

# Custom JSON serializer function
def json_serializer(data):
    return json.dumps(data).encode("utf-8")

# Creating a KafkaProducer instance
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=json_serializer, api_version=(0, 10))

# Entry point of the script
if __name__ == "__main__":
    # Continuous loop to produce messages
    while True:
        # Retrieve registered user data using a custom function
        registered_user = get_registered_user()
        
        # Print the registered user data
        print(registered_user)
        
        # Send the registered user data as a message to the 'explore-kafka' topic
        producer.send("explore-kafka", registered_user)
        
        # Introduce a delay of 4 seconds before the next iteration
        time.sleep(4)