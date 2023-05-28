from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class SenderAgent(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="receiver@your_xmpp_server")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()
        self.add_behaviour(b)
