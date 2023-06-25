from spade.message import Message
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour
from credentials import *
from BD.bd import ask_tasks, assign_next_day_tasks, assigned_tasks
from redistribue__taskV2 import distributeTask


class ManagerAgent(Agent):
    class DistributeTasks(PeriodicBehaviour):
        async def run(self):
            print("DistributeTasks Periodic Behaviour was called")

            tasks = await assigned_tasks()
            # There are scheduled tasks for the next day
            if tasks and self.agent.first_tasks_distribution:
                print("Distributing scheduled tasks....\n")
                await assign_next_day_tasks()

                msg = Message(to=USERS[1]['email'])
                msg.set_metadata("type", f"first tasks list to {msg.to}")
                msg.body = f"Tasks list scheduled received"

                await self.send(msg)

                msg2 = Message(to=USERS[4]['email'])
                msg2.set_metadata("type", f"first tasks list to {msg2.to}")
                msg2.body = f"Tasks list scheduled received"

                await self.send(msg2)

                msg1 = Message(to=USERS[6]['email'])
                msg1.set_metadata("type", f"first tasks list to {msg1.to}")
                msg1.body = f"Tasks list scheduled received"

                await self.send(msg1)
            else:
                print("DistributeFirstTasks running")
                # Assign tasks in db
                tasks_l1 = await ask_tasks(USERS[1]['email'])
                tasks_l2 = await ask_tasks(USERS[4]['email'])
                tasks_l3 = await ask_tasks(USERS[6]['email'])

                msg = Message(to=USERS[1]['email'])
                msg.set_metadata("type", f"first tasks list to {msg.to}")
                msg.body = f"Tasks list: {tasks_l1}"

                await self.send(msg)

                msg2 = Message(to=USERS[4]['email'])
                msg2.set_metadata("type", f"first tasks list to {msg2.to}")
                msg2.body = f"Tasks list {tasks_l2}"

                await self.send(msg2)

                msg1 = Message(to=USERS[6]['email'])
                msg1.set_metadata("type", f"first tasks list to {msg1.to}")
                msg1.body = f"Tasks list {tasks_l3}"

                await self.send(msg1)

                self.agent.first_tasks_distribution = True

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print(f"ManagerAgent {self.jid} started")
        # in a period of 8hours the agent behaviour is executed
        b = self.DistributeTasks(period=120)
        self.add_behaviour(b)
        self.first_tasks_distribution = False
