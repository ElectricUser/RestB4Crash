from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from dotenv import dotenv_values

config = dotenv_values(".env")
UNAME = config['UNAME']
PW = config['PW']


class AgentExample(Agent):
    async def setup(self):
        print(f"{self.jid} created.")


class CreateBehavior(OneShotBehaviour):
    async def run(self):
        agent2 = AgentExample(UNAME, PW)
        # This start is inside an async def, so it must be awaited
        await agent2.start(auto_register=True)


if __name__ == "__main__":
    agent1 = AgentExample(UNAME, PW)
    behavior = CreateBehavior()
    agent1.add_behaviour(behavior)
    # This start is in a synchronous piece of code, so it must NOT be awaited
    future = agent1.start(auto_register=True)
    future.result()

    behavior.join()
    # Terminates all agents and behaviours running inn the process
    # Also free all pending resources (threads, etc...)
    quit_spade()
