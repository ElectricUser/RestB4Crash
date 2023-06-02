import datetime
import random

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

# Define the Sender Agents Credentials.
USERS = {
    1: {
        'email': 'meiaagent@lightwitch.org',
        'pw': 'Grupo3isbest'
    },
    2: {
        'email': 'meiaagent1@lightwitch.org',
        'pw': 'Grupo3isbest'}
}

# Create a list to store stress values.
stress_values = list()

# Set an initial value for x.
x = 3


class SenderAgent(Agent):
    # Define the behavior for sending messages periodically.
    class InfBehaviour(PeriodicBehaviour):
        async def run(self) -> None:
            # Create a new message with a specific format.
            msg = Message(to=USERS[1]['email'])
            msg.set_metadata("type", "task complete")
            msg.body = f"\nAlert: Task Complete\n" \
                       f"JID> {self.agent.jid}" \
                       f"\nDatetime> {datetime.datetime.now()}\n"

            # Send the message
            await self.send(msg)

        async def on_end(self):
            # Stop the agent from this behavior.
            await self.agent.stop()

    # Define the behavior for sending stress notifications periodically.
    class StressNotifBehaviour(PeriodicBehaviour):
        async def run(self):
            # Check the stress level and send a notification if it's zero.
            if self.agent.stress_lvl == 0:  # TODO: Change
                msg = Message(to=USERS[1]['email'])
                msg.set_metadata("type", "stress")
                msg.sender = str(self.agent.jid)
                msg.body = f"\nAlert: Stress\n" \
                           f"JID> {self.agent.jid}\n" \
                           f"Datetime> {datetime.datetime.now()}\n"

                # Send the message
                await self.send(msg)

            # Update the stress level with a random value.
            self.agent.stress_lvl = random.randint(0, 10)  # TODO: Change

        async def on_end(self):
            # Stop the agent from this behavior.
            await self.agent.stop()

    # Define the behavior for sending pause notifications periodically.
    class PauseNotiBehaviour(PeriodicBehaviour):
        async def run(self) -> None:
            # Check if the agent is paused and send a notification if it is.
            if self.agent.paused:
                msg = Message(to=USERS[1]['email'])
                msg.set_metadata("type", "pause")
                msg.sender = str(self.agent.jid)
                msg.body = f"\nAlert: Pause\n" \
                           f"JID> {self.agent.jid}\n" \
                           f"Datetime> {datetime.datetime.now()}\n"

                # Send the message.
                await self.send(msg)

            # Toggle the paused state.
            self.agent.paused = not bool(self.agent.paused)  # TODO: Change

    async def setup(self) -> None:
        print("Sender Agent Created")

        # Create and add the InfBehaviour for sending messages periodically.
        b1 = self.InfBehaviour(period=1)
        self.add_behaviour(b1)

        # Set the initial stress level to zero
        self.stress_lvl = 0  # TODO: Change

        # Create and add the StressNotifBehaviour for sending stress notifications periodically.
        b2 = self.StressNotifBehaviour(period=1)
        self.add_behaviour(b2)

        # Set the initial paused state to False.
        self.paused = False  # TODO: Change

        # Create and add the PauseNotiBehaviour for sending pause notifications periodically.
        b3 = self.PauseNotiBehaviour(period=1)
        self.add_behaviour(b3)
