from google.cloud import pubsub_v1
import glob
import json
import os
import csv

# Look for the service account key in the current folder and use it
key_files = glob.glob("*.json")
if len(key_files) == 0:
    raise FileNotFoundError("No .json service key found in the current folder.")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_files[0]

# Project & topic 
project_id = "project-22d45b0d-1857-45b7-b34"
topic_name = "designTopic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
print("Publishing CSV records to:", topic_path)

# Read Labels.csv and send each row as a separate message
csv_file_name = "Labels.csv"

sent_count = 0

with open(csv_file_name, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        # Each row is already a dictionary 
        payload = json.dumps(row).encode("utf-8")

        # Publish and wait for Pub/Sub to confirm it was accepted
        future = publisher.publish(topic_path, payload)
        future.result()

        sent_count += 1
        print(f"Published record {sent_count}")

print(f"Done. Total records published: {sent_count}")
