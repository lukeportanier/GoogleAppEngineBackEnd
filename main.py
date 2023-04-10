import os
import random
from flask import Flask
import mysql.connector

# Configure the database connection
DB_USER = "api"
DB_PASSWORD = "YOtaPe7zrDlb0BiIMFCxmpSt"
DB_NAME = "random-number-storage"
CLOUD_SQL_CONNECTION_NAME = "cloud-test-1232:europe-west1:db-instance"

app = Flask(__name__)

# Create a function to connect to the database
def get_db():
    # Configure the database connection
    config = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME,
        "unix_socket": f"/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
    }

    # Connect to the database using the Cloud SQL Proxy
    return mysql.connector.connect(**config)

@app.route("/")
def index():
    instance_id = os.environ.get("GAE_INSTANCE", "unknown")
    return "Instance_Id: "+instance_id

@app.route("/GenerateNumbers")
def GenerateNumbers():
    instance_id = os.environ.get("GAE_INSTANCE", "unknown")

    # Generate a random number
    random_number = random.randint(0, 100000)

    # Insert the random number and instance ID into the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO storagedata (number, instance) VALUES ({random_number}, '{instance_id}')")
    conn.commit()
    conn.close()

    # Return a response to the client
    return f"Random Number {random_number} Has Been Generated and Stored in MySQL Database"

@app.route("/GetResults")
def GetResults():
    # Connect to the database
    conn = get_db()

    # Query the database to get the smallest and largest numbers and their instance IDs
    with conn.cursor() as cursor:
        cursor.execute("SELECT number, instance FROM storagedata WHERE number = (SELECT MIN(number) FROM storagedata)")
        result = cursor.fetchall()
        smallest_number = result[0]
        smallest_instance = result[1]

        cursor.execute("SELECT number, instance FROM storagedata WHERE number = (SELECT MAX(number) FROM storagedata)")
        result = cursor.fetchall()
        largest_number = result[0]
        largest_instance = result[1]

    # Close the database connection
    conn.close()
    
    return f"{smallest_number} was the smallest number generated by the system, it was generated by Instance: {smallest_instance}. \n\n {largest_number} was the largest number generated by the system, it was generated by Instance: {largest_instance}."



if __name__ == '__main__':
    app.run()
