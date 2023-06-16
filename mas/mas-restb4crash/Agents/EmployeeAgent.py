from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.template import Template
from BD.bd import add_stress


class EmployeeAgent(Agent):
    class ReceiveFirstTasks(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print(f"Message received on agent {self.agent.jid} with content: {msg.body}")
            else:
                print("Did not received any message after 10 seconds")

            # set status occupied with task
            self.status = "occupied" # Change with bd task query search

    class ReceiveSensorVals(CyclicBehaviour):
        async def run(self):
            print("ReceiveSensorVals running")
            msg = await self.receive(timeout=28800)

            if int(msg.body) >= 20:
                print(f'Sensor values {msg.body} from {msg.sender}')
                await add_stress(str(self.agent.jid))
            else:
                print("Message not received")
                self.kill()

    async def setup(self):
        print(f"Employee {self.jid} started")
        b = self.ReceiveFirstTasks()
        first_tasks_template = Template()
        first_tasks_template.set_metadata("type", f"first tasks list to {self.jid}")
        self.add_behaviour(b, first_tasks_template)

        b1 = self.ReceiveSensorVals()
        receive_sensor_vals_template = Template()
        receive_sensor_vals_template.set_metadata("type", f"sensor values to {self.jid}")
        self.add_behaviour(b1, receive_sensor_vals_template)
