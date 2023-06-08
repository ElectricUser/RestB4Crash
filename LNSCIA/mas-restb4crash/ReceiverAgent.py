from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.template import Template

# Define the Receiver Agents Credentials.
USERS = {
    1: {
        'email': 'meiaagent@lightwitch.org',
        'pw': 'Grupo3isbest'
    },
    2: {
        'email': 'meiaagent1@lightwitch.org',
        'pw': 'Grupo3isbest'}
}


class ReceiverAgent(Agent):
    # Cyclic behavior for general message handling.
    class RecvBehaviour(CyclicBehaviour):
        async def run(self) -> None:
            print("Recv")

            # Waits for a message with a timeout of 3 seconds.
            msg = await self.receive(timeout=3)

            if msg:
                print(f'From: {msg.sender} >>> \n{msg.body}')
            else:
                print("Message not received")
                self.kill()

        async def on_end(self):
            # Stop agent from behavior.
            await self.agent.stop()

    # Periodic behavior for handling stress messages.
    class HandleStressBehaviour(CyclicBehaviour):
        async def run(self) -> None:
            print("Stress")

            # Waits for a message with a timeout of 3 seconds.
            msg = await self.receive(timeout=3)

            if msg:
                print(f'From: {msg.sender} >>> \n{msg.body}')

    # Periodic behavior for handling pause messages.
    class HandlePausesBehaviour(PeriodicBehaviour):
        async def run(self) -> None:
            print("Pauses")

            # Waits for a message with a timeout of 3 seconds.
            msg = await self.receive(timeout=3)

            if msg:
                print(f'From: {msg.sender} >>> \n{msg.body}')

    async def setup(self) -> None:
        print("Receiver Agent Created")

        # Create and add the RecvBehaviour to handle general messages.
        b1 = self.RecvBehaviour()
        general_template = Template()
        general_template.set_metadata("type", "task complete")
        self.add_behaviour(b1, general_template)

        # Create and add the HandleStressBehaviour to handle stress messages
        stress_behaviour = self.HandleStressBehaviour()
        stress_template = Template()
        stress_template.set_metadata("type", "stress")
        self.add_behaviour(stress_behaviour, stress_template)

        # Create and add the HandlePausesBehaviour to handle pause messages
        pauses_behaviour = self.HandlePausesBehaviour(period=2)
        pauses_template = Template()
        pauses_template.set_metadata("type", "pause")
        self.add_behaviour(pauses_behaviour, pauses_template)
