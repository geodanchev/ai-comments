from pymongo import MongoClient
from helpers.config_helper import getMongoAddress, getMongoDBName

# Constants
DB_NAME = getMongoDBName()
COLLECTION_NAME = "customerFeedback"

# Connect to MongoDB
client = MongoClient(getMongoAddress())
db = client[DB_NAME]
feedback_collection = db[COLLECTION_NAME]

# Function to store customer feedback


def store_customer_feedback(feedback):
    feedback_collection.insert_one(feedback)


def delete_all_data():
    feedback_collection.delete_many({})

# Function to retrieve all customer feedbacks


def retrieve_customer_feedbacks():
    feedbacks = []
    for feedback in feedback_collection.find():
        feedbacks.append(feedback)
    return feedbacks

# Example usage


def main():
    # Store feedback
    feedback1 = {
        "id": "2",
        "comment": "The roller coaster we purchased had top-notch quality and exceeded our expectations!",
        "date": "2023-02-03 14:45:08",
        "submitter": {
            "firstName": "Jane",
            "lastName": "Smith",
            "email": "jane.smith@themepark.com",
            "company": "ThemePark Central"
        },
        "temperament": "positive",
        "category": "product quality"
    }
    store_customer_feedback(feedback1)

    feedback2 = {
        "id": "1",
        "comment": "The sales team at Peter's Engineering was incredibly responsive and helpful!",
        "date": "2023-01-15 10:34:12",
        "submitter": {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@thrillworld.com",
            "company": "ThrillWorld Inc."
        },
        "temperament": "positive",
        "category": "customer service"
    }
    store_customer_feedback(feedback2)

    # Retrieve all feedbacks
    all_feedbacks = retrieve_customer_feedbacks()

    for feedback in all_feedbacks:
        print(
            f"Feedback: {feedback['id']}, temperament: {feedback['temperament']}")


if __name__ == "__main__":
    main()
