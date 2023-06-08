from datetime import datetime

import time

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour, CyclicBehaviour
from spade.message import Message

from paho.mqtt import client as mqtt
from MQTT import receiverClient

BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "/sensors/1"

USERS = {
    1: {
        'email': 'meiaagent@lightwitch.org',
        'pw': 'Grupo3isbest'},
    2: {
        'email': 'meiaagent1@lightwitch.org',
        'pw': 'Grupo3isbest'},
    3: {
        'email': 'meiaagent2@lightwitch.org',
        'pw': 'Grupo3isbest'},
    4: {
            'email': 'meiaagent3@lightwitch.org',
            'pw': 'Grupo3isbest'},
    5: {
            'email': 'meiaagent4@lightwitch.org',
            'pw': 'Grupo3isbest'},
    6: {
            'email': 'meiaagent5@lightwitch.org',
            'pw': 'Grupo3isbest'
    },
    7: {
            'email': 'meiaagent6@lightwitch.org',
            'pw': 'Grupo3isbest'
    }
}

last_value = None


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload) + 'received at: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    global last_value
    last_value = str(msg.payload)


class SensorAgent(Agent):
    class GetSensorsValuesBehaviour(PeriodicBehaviour):

        async def run(self) -> None:
            print("SensorAgent Behaviour called")
            if self.agent.jid == "meiaagent1@lightwitch.org":
                to = USERS[1]['email']
            elif self.agent.jid == "meiaagent3@lightwitch.org":
                to = USERS[5]['email']
            else:
                to = USERS[7]['email']
            msg = Message(to=to)
            msg.set_metadata("type", "sensor values")

            # loop mqtt client
            self.agent.client.loop()
            if last_value is not None:
                sensor_vals = str(last_value).split()
                # print(sensor_vals)
                message = "" + sensor_vals[1] + "\n" + sensor_vals[3][:-1] + "\n" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                msg.body = message
                await self.send(msg)

    async def setup(self) -> None:
        print("SensorAgent Created")
        b1 = self.GetSensorsValuesBehaviour(period=2)
        self.add_behaviour(b1)
        self.client = mqtt.Client()
        self.client.on_connect = receiverClient.on_connect
        self.client.connect(BROKER, PORT)
        self.client.subscribe(TOPIC)
        self.client.on_message = on_message
