from paho.mqtt import client as mqtt
import time
import datetime

Broker = 'broker.emqx.io'
PORT = 1883
TOPIC = "/sensors/1"
CLIENT_ID = f'python-mqtt-1'
# username = 'emqx'
# password = 'public'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/sensors/1")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(TOPIC, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{TOPIC}`")
        else:
            print(f"Failed to send message to topic {TOPIC}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = mqtt.Client(client_id="2")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(Broker, PORT)

    while True:
        message = str("force 19 pos 34")
        client.publish(TOPIC, message)


if __name__ == "__main__":
    run()
