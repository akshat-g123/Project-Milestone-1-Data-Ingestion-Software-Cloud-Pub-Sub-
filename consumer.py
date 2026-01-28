import glob
import json
import os
from google.cloud import pubsub_v1

# GCP project and subscription details
PROJECT_ID = "project-22d45b0d-1857-45b7-b34"
SUBSCRIPTION_ID = "designTopic-sub"

# Locate the service account key and set it for authentication
json_files = glob.glob("*.json")
if not json_files:
    raise FileNotFoundError("Service account JSON key not found in this folder.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_files[0]

# Create the subscriber client and subscription path
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

print("Waiting for messages on:", subscription_path)

# Function that runs whenever a message is received
def receive_message(message: pubsub_v1.subscriber.message.Message) -> None:
    # Convert message bytes back into a dictionary
    record = json.loads(message.data.decode("utf-8"))

    # Print the dictionary values
    print("Consumed record:")
    for key, value in record.items():
        print(f"{key}: {value}")
    print("-" * 30)

    # Acknowledge successful processing
    message.ack()

# Start listening for messages
streaming_pull = subscriber.subscribe(
    subscription_path,
    callback=receive_message
)

try:
    streaming_pull.result()
except KeyboardInterrupt:
    streaming_pull.cancel()
