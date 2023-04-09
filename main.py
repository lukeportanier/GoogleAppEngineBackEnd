#End Points

from flask import Flask
from gcloud import storage

app = Flask(__name__)

random_numbers_storage = 'random-numbers-storage'

import google.auth
from google.auth.compute_engine import Credentials
from flask import Flask
import os
import random

app = Flask(__name__)

@app.route("/")
def index():
    instance_id = os.environ.get("GAE_INSTANCE", "unknown")
    return "Instance_Id: "+instance_id

@app.route("/GenerateNumbers")
def GenerateNumbers():
    # Get the App Engine instance ID from the environment variables, if available
    instance_id = os.environ.get("GAE_INSTANCE", "unknown")

    # Generate random numbers
    random_numbers = [random.randint(0,1000) for i in range(100)]

    # Concatenate random numbers and instance ID with the pipe character '|'
    random_numbers_with_instance = [f"{number}|{instance_id}" for number in random_numbers]
    content = ','.join(random_numbers_with_instance)

    # Upload random numbers to Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(random_numbers_storage)
    blob = bucket.blob('random_numbers.txt')
    blob.upload_from_string(content)

    return 'Random Numbers Have Been Generated'

@app.route('/GetResults')
def GetResults():
    # Retrieve random numbers from Google Cloud Storage and split them into pairs of numbers and instance IDs
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(random_numbers_storage)
    blob = bucket.blob('random_numbers.txt')
    content = blob.download_as_string().decode('utf-8')
    random_numbers_with_instance = content.split(',')

    # Display smallest and largest numbers with their respective instance IDs
    smallest_number_with_instance = min(random_numbers_with_instance)
    largest_number_with_instance = max(random_numbers_with_instance)
    smallest_number, smallest_instance = smallest_number_with_instance.split('|')
    largest_number, largest_instance = largest_number_with_instance.split('|')
    return f"Smallest Number Generated by Instance {smallest_instance}: {smallest_number}\nLargest Number Generated by Instance {largest_instance}: {largest_number}"


if __name__ == '__main__':
    app.run()
