# Under Explore
# Ref https://www.youtube.com/watch?v=Q4XA5nUpLeo

from faker import Faker

# Create a Faker instance
fake = Faker()

# Function to generate a registered user with fake data
def get_registered_user():
    return {
        "name": fake.name(),        # Generate a fake name
        "address": fake.address(),  # Generate a fake address
        "created_at": fake.year()   # Generate a fake year for the creation date
    }

# Entry point of the script
if __name__ == "__main__":
    # Print the details of a generated registered user
    print(get_registered_user())
