import requests
import json
import time

FIREBASE_URL = "https://sensormonitor-65813-default-rtdb.europe-west1.firebasedatabase.app/device1.json"

def send_data(temp, hum):
    data = {
        "temperature": temp,
        "humidity": hum
    }
    response = requests.put(FIREBASE_URL, json=data)
    print(response.status_code, response.text)

# Simulate sensor read
while True:
    temp = 22.5  # replace with actual sensor read
    hum = 50.1   # replace with actual sensor read
    send_data(temp, hum)
    time.sleep(5)
