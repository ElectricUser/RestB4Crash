from dotenv import dotenv_values
import time
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

config = dotenv_values(".env")
UNAME = config['UNAME']
PW = config['PW']


class DummyAgent(Agent):
    class MyBehavior(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.counter = None

        async def on_start(self):
            print("Starting behaviour . . .")
            self.counter = 0

        async def run(self):
            print("Counter: {}".format(self.counter))
            self.counter += 1
            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting . . .")
        b = self.MyBehavior()
        self.add_behaviour(b)


if __name__ == "__main__":
    dummy = DummyAgent(UNAME, PW)
    future = dummy.start()
    future.result()

    print("Wait until user interrupts with ctrl+C")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    dummy.stop()
