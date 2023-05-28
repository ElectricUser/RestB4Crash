from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.template import Template


class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        # The template is used to match with messages with the same format
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
