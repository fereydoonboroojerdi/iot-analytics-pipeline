# Sample device simulator
import paho.mqtt.publish as publish
import json
import time

while True:
    payload = {
        "temp": 78 + random.random()*5,
        "vibration": 0.2 + random.random()/10
    }
    publish.single(
        "factory/Plant-17/sensors",
        json.dumps(payload),
        hostname="YOUR_IOT_ENDPOINT.amazonaws.com"
    )
    time.sleep(0.1)