from dotenv import dotenv_values
import time
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade import quit_spade

config = dotenv_values(".env")
UNAME = config['UNAME']
PW = config['PW']


async def on_end():
    print("Ending behaviour . . .")


class DummyAgent(Agent):
    # Inherits from the default behaviour class CyclicBehavior (Loop)
    class MyBehavior(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.counter = None

        # Similar to setup() method but async
        # It's the first method called before the main iteration
        async def on_start(self):
            print("Starting behaviour . . .")
            self.counter = 0

        # Most important method
        # It's called on each iteration on the behavior loop
        async def run(self):
            print("Counter: {}".format(self.counter))
            self.counter += 1
            if self.counter > 3:
                # Killing a behavior does not cancel its current loop
                self.kill(exit_code=10)
                return
            await asyncio.sleep(1)

        # Called when a behavior ends or is killed
        async def on_end(self):
            print("Behaviour finished with exit code {}.".format(self.exit_code))

    # Attribute behavior class to agent
    async def setup(self):
        print("Agent starting . . .")
        b = self.MyBehavior()
        self.add_behaviour(b)


if __name__ == "__main__":
    dummy = DummyAgent(UNAME, PW)
    future = dummy.start()
    # result() makes sure that start routine has finished
    future.result()

    print("Wait until user interrupts with ctrl+C")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    dummy.stop()

    # Killing a behavior does not cancel its current loop
    # To finish the current iteration call quit_spade()
    quit_spade()

