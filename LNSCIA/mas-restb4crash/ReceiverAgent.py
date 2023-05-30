import random

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.template import Template

USERS = {
    1: {
        'email': 'meiaagent@lightwitch.org',
        'pw': 'Grupo3isbest'
    },
    2: {
        'email': 'meiaagent1@lightwitch.org',
        'pw': 'Grupo3isbest'}
}


class ReceiverAgent(Agent):
    class RecvBehaviour(CyclicBehaviour):
        async def run(self) -> None:
            print("Recv")
            msg = await self.receive(timeout=3)

            if msg:
                print(f'From: {msg.sender} >>> \n{msg.body}')
            else:
                print("Message not received")
                self.kill()

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

    class HandleStressBehaviour(PeriodicBehaviour):
        async def run(self) -> None:

            print("Stress")

            msg = await self.receive(timeout=3)

            if msg:
                print(f'From: {msg.sender} >>> \n{msg.body}')
            else:
                print("Message not received")
                self.kill()

    class HandlePausesBehaviour(PeriodicBehaviour):

        async def run(self) -> None:
            print("Pauses")

            msg = await self.receive(timeout=3)

            if msg:
                print(f'From: {msg.sender} >>> \n{msg.body}')
            else:
                print("Message not received")
                self.kill()

    async def setup(self) -> None:
        print("Receiver Agent Created")
        b1 = self.RecvBehaviour()
        general_template = Template()
        general_template.set_metadata("type", "broadcast")
        self.add_behaviour(b1, general_template)

        # Stress handler
        stress_behaviour = self.HandleStressBehaviour(period=2)

        stress_template = Template()
        stress_template.set_metadata("type", "stress")
        self.add_behaviour(stress_behaviour, stress_template)

        # Pauses handler
        pauses_behaviour = self.HandlePausesBehaviour(period=2)

        pauses_template = Template()
        pauses_template.set_metadata("type", "pause")
        self.add_behaviour(pauses_behaviour, pauses_template)

