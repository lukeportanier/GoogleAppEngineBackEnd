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
        cursor.execute("SELECT number, instance FROM storagedata WHERE number = (SELECT MIN(number) FROM storagedata) OR number = (SELECT MAX(number) FROM storagedata)")
        results = cursor.fetchall()

    # Display smallest and largest numbers with their respective instance IDs
    smallest_number_with_instance = [f"{row[0]}|{row[1]}" for row in results if row[0] == min([r[0] for r in results])][0]
    largest_number_with_instance = [f"{row[0]}|{row[1]}" for row in results if row[0] == max([r[0] for r in results])][0]
    smallest_number, smallest_instance = smallest_number_with_instance.split('|')
    largest_number, largest_instance = largest_number_with_instance.split('|')

    # Close the database connection
    conn.close()

    return f"Smallest Number Was Generated by Instance {smallest_instance} - {smallest_number}\n\nLargest Number Was Generated by Instance {largest_instance} - {largest_number}"



if __name__ == '__main__':
    app.run()
