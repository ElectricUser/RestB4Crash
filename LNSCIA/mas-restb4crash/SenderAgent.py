import datetime
import random

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour, CyclicBehaviour
from spade.message import Message


USERS = {
    1: {
        'email': 'meiaagent@lightwitch.org',
        'pw': 'Grupo3isbest'
    },
    2: {
        'email': 'meiaagent1@lightwitch.org',
        'pw': 'Grupo3isbest'}
}

stress_values = list()

x = 3


class SenderAgent(Agent):
    class InfBehaviour(PeriodicBehaviour):
        async def run(self) -> None:
            # Message Format
            msg = Message(to=USERS[1]['email'])
            msg.set_metadata("performative", "broadcast")
            msg.body = f"\nhello from agent {self.agent.jid}"

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
                msg.thread = "3"
                msg.body = f"\nAlert> Stress\n" \
                           f"JID> {self.agent.jid}\n" \
                           f"Datetime> {datetime.datetime.now()}"

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
                msg.thread = "3"
                msg.body = f"\nAlert> Pause\n" \
                           f"JID> {self.agent.jid}\n" \
                           f"Datetime> {datetime.datetime.now()}"

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
