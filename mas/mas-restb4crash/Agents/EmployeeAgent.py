from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from BD.bd import add_stress, add_pause, get_user_avg_force
from utils import has_paused, has_stressed


class EmployeeAgent(Agent):
    class ReceiveFirstTasks(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=2880)  # wait for a message for 10 seconds
            if msg:
                print(f"Message received on agent {self.agent.jid} with content: {msg.body}")
            else:
                print("Did not received any message after 120 seconds")

            # set status occupied with task
            self.status = "occupied"  # Change with bd task query search

    class ReceiveSensorVals(CyclicBehaviour):
        async def run(self):
            print("ReceiveSensorVals running")
            msg = await self.receive(timeout=28800)
            print(f'Sensor values {msg.body} from {msg.sender}')

            await add_stress(str(self.agent.jid))
            if msg:
                sensor_vals = str(msg.body).split(",")
                F1s = []
                F2s = []
                Ms = []
                for x in sensor_vals:
                    F1s.append(int(x.split(":")[1].split()[0]))
                    F2s.append(int(x.split()[1].split(":")[1].split()[0].split(":")[0]))
                    Ms.append(int(x.split()[2].split(":")[1]))
                print("F1s:", F1s)
                print("F2s:", F2s)
                print("Ms:", Ms)
                if has_paused(Ms, F1s, F2s):
                    await add_pause(str(self.agent.jid))
                avg_force = await get_user_avg_force(str(self.agent.jid))
                if avg_force and has_stressed(F1s, avg_force):
                    await add_stress(str(self.agent.jid))

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
