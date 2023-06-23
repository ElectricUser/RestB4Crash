from paho.mqtt import client as mqtt
import time
import datetime

Broker = 'broker.emqx.io'
PORT = 1883
TOPIC = "/sensors/3"
CLIENT_ID = f'python-mqtt-1'


# username = 'emqx'
# password = 'public'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/sensors/1")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


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
        # message = str("force 19 pos 34")
        message = "F1:1040 F2:1397 M:0, F1:1051 F2:1408 M:0, F1:1031 F2:1351 M:0, " \
                  "F1:1039 F2:1407 M:0, F1:976 F2:1344 M:0, F1:1046 F2:1419 M:0, F1:1040 " \
                  "F2:1409 M:0, F1:1058 F2:1415 M:0, F1:1038 F2:1362 M:0, F1:993 F2:1328 M:0"
        client.publish(TOPIC, message)


if __name__ == "__main__":
    run()
