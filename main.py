#End Points

app = Flask(__name__)

@app.route("/")
def index():
    instance_id = os.environ.get("GAE_INSTANCE", "unknown")
    return "Instance_Id: "+instance_id

import os
import random
from gcloud import memcache
from flask import Flask
from pymemcache.client.base import Client

app = Flask(__name__)
memcache_client = memcache.Client()

@app.route("/GenerateNumbers")
def GenerateNumbers():
    instance_id = os.environ.get("GAE_INSTANCE", "unknown")

    # Generate a random number
    random_number = random.randint(0,100000)

    # Store the random number in memcache with instance ID as the key
    #memcache_client.set(instance_id, random_number)

    return f"Random Number {random_number} Has Been Generated and Stored in Memcache"

"""
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
"""

if __name__ == '__main__':
    app.run()
