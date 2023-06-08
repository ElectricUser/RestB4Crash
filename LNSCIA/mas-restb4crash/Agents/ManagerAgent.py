import sys
import os
sys.path.append(os.path.abspath("/Users/marceloamado/ISEP/LNSCIA/RestB4Crash/LNSCIA/mas-restb4crash"))
from BD.bd import ask_tasks
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
    4: {
        'email': 'meiaagent3@lightwitch.org',
        'pw': 'Grupo3isbest'},
    5: {
        'email': 'meiaagent4@lightwitch.org',
        'pw': 'Grupo3isbest'},
    6: {
        'email': 'meiaagent5@lightwitch.org',
        'pw': 'Grupo3isbest'}
}


class ManagerAgent(Agent):
    class ReceiveStressNotification(CyclicBehaviour):
        async def run(self) -> None:
            print("Manager Behaviour called")
            # 7200 = number of seconds in 2 hours
            msg = await self.receive(timeout=7200)

            if msg:
                print(f'From: {msg.sender} >>> \n{msg.body}')
            else:
                print("Message not received")
                self.kill()

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

    # It is called at the end of the 8 hours
    class DistributeFistTasksList(OneShotBehaviour):
        async def run(self) -> None:
            print("Distribute Tasks Behaviour Called")

            agent1_tasks_list = ask_tasks(USERS[1]['email'])
            agent2_tasks_list = ask_tasks(USERS[4]['email'])
            agent3_tasks_list = ask_tasks(USERS[6]['email'])

            print("agent1 tasks list: ", agent1_tasks_list)
            print("agent2 tasks list: ", agent2_tasks_list)
            print("agent3 tasks list: ", agent3_tasks_list)
            if agent1_tasks_list and agent2_tasks_list and agent3_tasks_list:
                msg_task1 = Message(to=USERS[1]['email'])
                msg_task1.set_metadata("type", f"first tasks {USERS[1]['email']}")
                msg_task2 = Message(to=USERS[4]['email'])
                msg_task2.set_metadata("type", f"first tasks {USERS[4]['email']}")
                msg_task3 = Message(to=USERS[6]['email'])
                msg_task3.set_metadata("type", f"first tasks {USERS[6]['email']}")

                # Send message with tasks list to employee agents
                await self.send(msg_task1)
                await self.send(msg_task2)
                await self.send(msg_task3)

    async def setup(self) -> None:
        print("Manager Agent Created")
        b1 = self.ReceiveStressNotification()
        general_template = Template()
        general_template.set_metadata("type", "stress notification")
        self.add_behaviour(b1, general_template)

        b2 = self.DistributeFistTasksList()
        self.add_behaviour(b2)
