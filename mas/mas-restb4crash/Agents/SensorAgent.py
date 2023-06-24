import pprint
from datetime import datetime
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from credentials import *
from utils import has_paused

# MQTT
from paho.mqtt import client as mqtt
from MQTT import receiverClient

last_value = None


def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload) + 'received at: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    global last_value
    # last_value = str(msg.payload)
    last_value = msg.payload.decode("utf-8")
    # print("last value: ", last_value)


class SensorAgent(Agent):
    class GetSensorsValuesBehaviour(PeriodicBehaviour):
        async def run(self):
            to = None
            # Assign Recipient Employee
            if str(self.agent.jid) == USERS[2]['email']:
                to = USERS[1]['email']
            elif str(self.agent.jid) == USERS[5]['email']:
                to = USERS[4]['email']
            elif str(self.agent.jid) == USERS[7]['email']:
                to = USERS[6]['email']

            msg = Message(to=to)
            msg.sender = str(self.agent.jid)
            msg.set_metadata("type", f"sensor values to {to}")

            self.agent.client.loop()

            if last_value is not None:
                msg.body = str(last_value)
                await self.send(msg)
                """msg.body = str(sensor_vals)
                await self.send(msg)"""
                """message = "" + sensor_vals[1] + "\n" + sensor_vals[3][:-1] + "\n" + str(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"))"""

    async def setup(self):
        print("SensorAgent Created")
        b = self.GetSensorsValuesBehaviour(period=2)
        self.add_behaviour(b)
        self.client = mqtt.Client()
        self.client.on_connect = receiverClient.on_connect
        self.client.connect(BROKER, PORT)
        self.client.subscribe(TOPIC)
        self.client.on_message = on_message
