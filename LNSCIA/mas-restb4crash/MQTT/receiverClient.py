import paho.mqtt.client as mqtt

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-3'
# username = 'emqx'
# password = 'public'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.subscribe(topic)
    client.on_message = on_message

    client.loop_forever()


if __name__ == "__main__":
    run()
