#Functions

import random

def GenerateRandomNumbers():
    random_numbers = []
    for i in range(1000):
        random_numbers.append(random.randint(0, 100000))

    return random_numbers

#End Points

from flask import Flask
from gcloud import storage

app = Flask(__name__)

random_numbers_storage = 'random-numbers-storage'

@app.route('/')
def root():
    return 'This is the Api'

@app.route('/GenerateNumbers')
def GenerateNumbers():
    random_numbers = [random.randint(0,1000) for i in range(100000)]

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(random_numbers_storage)

    blob = bucket.blob('random_numbers.txt')
    blob.upload_from_string(','.join(str(number) for number in random_numbers))
    
    return 'Random Numbers Have Been Generated'

@app.route('/GetResults')
def GetResults():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(random_numbers_storage)

    blob = bucket.blob('random_numbers.txt')
    content = blob.download_as_string().decode('utf-8')
    random_numbers = [int(number) for number in content.split(',') if number]

    largest = max(random_numbers)
    smallest = min(random_numbers)
    return "Smallest Number Generated by System: "+str(smallest)+" Largest Number Generated by System: "+str(largest)


if __name__ == '__main__':
    app.run()
