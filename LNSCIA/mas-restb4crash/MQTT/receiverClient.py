from datetime import datetime

import paho.mqtt.client as mqtt
import time

BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "/sensors/1"
CLIENT_ID = f'python-mqtt-3'
# username = 'emqx'
# password = 'public'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload) + 'received at: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    client.subscribe(TOPIC)
    client.on_message = on_message

    while client.loop() == 0:
        time.sleep(5)  # sleep for 5 seconds before next call


if __name__ == "__main__":
    run()
