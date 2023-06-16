from datetime import datetime
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from credentials import *


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
            msg.body = "66"
            await self.send(msg)

    async def setup(self):
        print("SensorAgent Created")
        b = self.GetSensorsValuesBehaviour(period=2)
        self.add_behaviour(b)
