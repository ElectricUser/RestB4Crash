import datetime
import random

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour, CyclicBehaviour
from spade.message import Message

from paho.mqtt import client as mqtt
from MQTT import receiverClient


USERS = {
    1: {
        'email': 'meiaagent@lightwitch.org',
        'pw': 'Grupo3isbest'
    },
    2: {
        'email': 'meiaagent1@lightwitch.org',
        'pw': 'Grupo3isbest'}
}

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-1'

stress_values = list()

x = 3


class SenderAgent(Agent):

    class InfBehaviour(PeriodicBehaviour):
        async def run(self) -> None:
            # Message Format
            msg = Message(to=USERS[1]['email'])
            msg.set_metadata("type", "task complete")
            msg.body = f"\nAlert: Task Complete\n" \
                       f"JID> {self.agent.jid}" \
                       f"\nDatetime> {datetime.datetime.now()}\n"

            await self.send(msg)

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

    class StressNotifBehaviour(PeriodicBehaviour):
        async def run(self):
            if self.agent.stress_lvl == 0:  # Change
                msg = Message(to=USERS[1]['email'])
                msg.set_metadata("type", "stress")
                msg.sender = str(self.agent.jid)
                msg.body = f"\nAlert: Stress\n" \
                           f"JID> {self.agent.jid}\n" \
                           f"Datetime> {datetime.datetime.now()}\n"

                await self.send(msg)
            self.agent.stress_lvl = random.randint(0, 10)  # Change

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

    class PauseNotiBehaviour(PeriodicBehaviour):
        async def run(self) -> None:
            if self.agent.paused:
                msg = Message(to=USERS[1]['email'])
                msg.set_metadata("type", "pause")
                msg.sender = str(self.agent.jid)
                msg.body = f"\nAlert: Pause\n" \
                           f"JID> {self.agent.jid}\n" \
                           f"Datetime> {datetime.datetime.now()}\n"

                await self.send(msg)
            self.agent.paused = not bool(self.agent.paused)  # Change

    async def setup(self) -> None:
        print("Sender Agent Created")

        b1 = self.InfBehaviour(period=1)
        self.add_behaviour(b1)

        self.stress_lvl = 0  # Change

        b2 = self.StressNotifBehaviour(period=1)
        self.add_behaviour(b2)

        self.paused = False  # Change

        b3 = self.PauseNotiBehaviour(period=1)
        self.add_behaviour(b3)
"""
        self.client = mqtt.Client(client_id="2")
        self.client.on_connect = receiverClient.on_connect()
        self.client.connect(broker, port)
        self.client.subscribe('/sensors/1')
        self.client.on_message = receiverClient.on_message()
        self.client.loop_forever()"""
