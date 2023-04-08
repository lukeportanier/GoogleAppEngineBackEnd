#Functions

import random

def GenerateRandomNumbers():
    random_numbers = []
    for i in range(1000):
        random_numbers.append(random.randint(0, 100000))

    return random_numbers

#End Points

from flask import Flask
from google.cloud import storage
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

random_numbers_storage = 'random-numbers-storage'

@app.route('/GenerateNumbers')
def GenerateNumbers():
    random_numbers = [random.randint(0,100000) for i in range(1000)]

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(random_numbers_storage)

    blob = bucket.blob('random_numbers.txt')
    blob.upload_from_string('n'.join(str(number) for number in random_numbers))
    
    return 'Random Numbers Have Been Generated'

@app.route('/GetResults')
def GetResults():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(random_numbers_storage)

    blob = bucket.blob('random_numbers.txt')
    content = blob.download_as_string().decode('utf-8')
    random_numbers = [int(number) for number in content.split('\n') if number]

    largest = max(random_numbers)
    smallest = min(random_numbers)

    return "Smallest Number Generated by System: "+str(smallest)+" Largest Number Generated by System: "+str(largest)
