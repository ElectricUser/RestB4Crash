from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
import datetime
from spade.message import Message
from dotenv import dotenv_values
from spade.template import Template

config = dotenv_values(".env")
UNAME = config['UNAME']
UNAME1 = config['UNAME1']
PW = config['PW']


# Sender Agent
class FilmPressureAgent(Agent):
    class InformBehav(PeriodicBehaviour):
        async def run(self):
            print(f"PeriodicSenderBehaviour running at {datetime.datetime.now().time()}: {self.counter}")
            """msg = Message(to=UNAME)  # Instantiate the message
            msg.body = "Hello World"  # Set the message content
            msg.set_metadata("sensorVal", "sensorVal")
            msg.thread = "sensorVal"""

            template = Template()
            template.sender = UNAME1
            template.to = UNAME
            template.body = "HelloWorld"
            template.thread = "xptoVal"
            template.metadata = {"performative": "query"}
            message = Message()
            message.sender = UNAME1
            message.to = UNAME
            message.body = "HelloWorld"
            message.thread = "xptoVal"
            message.set_metadata("performative", "query")

            assert template.match(message)

            await self.send(message)
            print("Message sent!")

            self.counter += 1

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

        async def on_start(self):
            self.counter = 0

    async def setup(self):
        print(f"PeriodicSenderAgent started at {datetime.datetime.now().time()}")
        b = self.InformBehav(period=2)
        self.add_behaviour(b)
