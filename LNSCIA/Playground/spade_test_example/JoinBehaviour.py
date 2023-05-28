import asyncio
import getpass

from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from dotenv import dotenv_values
import time

config = dotenv_values(".env")

UNAME = config['UNAME']
UNAME1 = config['UNAME1']
PW = config['PW']


class DummyAgent(Agent):
    class LongBehav(OneShotBehaviour):
        async def run(self):
            await asyncio.sleep(5)
            print("Long Behaviour has finished")

    class WaitingBehav(OneShotBehaviour):
        async def run(self):
            self.start_time = time.time()
            await self.agent.behav.join()  # this join must be awaited
            print("Waiting Behaviour has finished")

        async def on_end(self):
            print("--- {0:.3f} seconds ---".format(time.time() - self.start_time))

    async def setup(self):
        print("Agent starting . . .")
        self.behav = self.LongBehav()
        self.add_behaviour(self.behav)
        self.behav2 = self.WaitingBehav()
        self.add_behaviour(self.behav2)




if __name__ == "__main__":

    #jid = input("JID> ")
    #passwd = getpass.getpass()
    jid = UNAME
    passwd = PW
    dummy = DummyAgent(jid, passwd)
    future = dummy.start()
    future.result()

    dummy.behav2.join()  # this join must not be awaited

    print("Stopping agent.")
    dummy.stop()

    quit_spade()
