import random
from abc import ABC

from spade.message import Message
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
        'pw': 'Grupo3isbest'},
    3: {
        'email': 'meiaagent2@lightwitch.org',
        'pw': 'Grupo3isbest'},
}


class EmployeeAgent(Agent):
    class ReceiveSensorVals(CyclicBehaviour):
        async def run(self) -> None:
            print("Manager Behaviour called")
            msg = await self.receive(timeout=60)

            if msg:
                print(f'From: {msg.sender} >>> \n{msg.body}')
                if int(msg.body.split("\n")[0]) > 20:
                    self.agent.n_pauses += 1
                    self.agent.n_stresses += 1
                    notification_message = Message(to=USERS[3]['email'])
                    notification_message.set_metadata("type", "stress notification")
                    notification_message.body = "!!!!!ALERT STRESSED OUT!!!!!!!"
                    await self.send(notification_message)
            else:
                print("Message not received")
                self.kill()

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

    # It's the first behaviour of the chain
    class ReceiveFirstTasks(OneShotBehaviour):
        async def run(self) -> None:
            print("Receiver First tasks behaviour called")
            msg = await self.receive(timeout=60)
            if msg:
                print("!!!!!First tasks list received!!!!!")
                print(self.agent.jid)
                self.kill()
            else:
                print("!!!!!FIRST TASKS NOT RECEIVED!!!!!!")
                self.kill()

    async def setup(self) -> None:
        print("Receiver Agent Created")
        b1 = self.ReceiveSensorVals()
        general_template = Template()
        general_template.set_metadata("type", "sensor values")
        self.add_behaviour(b1, general_template)
        self.n_pauses = 0
        self.n_stresses = 0

        b2 = self.ReceiveFirstTasks()
        first_tasks_template = Template()
        first_tasks_template.set_metadata("type", f"first tasks {self.jid}")
        self.add_behaviour(b2, first_tasks_template)
