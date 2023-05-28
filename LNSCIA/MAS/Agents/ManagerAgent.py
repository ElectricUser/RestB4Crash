from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
#from FilmPressureAgent import FilmPressureAgent


# Receiver Agent
class ManagerAgent(Agent):
    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.thread = "sensorVal"
        self.add_behaviour(b, template)

    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")
                self.kill()

    """class CreateBehav(OneShotBehaviour):
        async def run(self, ):
            agent2 = FilmPressureAgent("agent2_example@your_xmpp_server", "fake_password")
            # This start is inside an async def, so it must be awaited
            await agent2.start(auto_register=True)

        async def on_end(self):
            await self.agent.stop()"""
