from SenderAgent import SenderAgent
from ReceiverAgent import ReceiverAgent
from spade import quit_spade
import time

# Define the Agents Credentials.
USERS = {
    1: {
        'email': 'meiaagent@lightwitch.org',
        'pw': 'Grupo3isbest'},
    2: {
        'email': 'meiaagent1@lightwitch.org',
        'pw': 'Grupo3isbest'},
    3: {
        'email': 'meiaagent2@lightwitch.org',
        'pw': 'Grupo3isbest'},
    4: {
        'email': 'meiaagent3@lightwitch.org',
        'pw': 'Grupo3isbest'}
}

if __name__ == '__main__':
    # Create and start the Receiver Agent.
    receiver = ReceiverAgent(USERS[1]['email'], USERS[1]['pw'])
    future = receiver.start()
    future.wait()

    # Create and start the Sender Agents.
    sender = SenderAgent(USERS[2]['email'], USERS[1]['pw'])
    sender.start()

    while receiver.is_alive():
        try:
            time.sleep(1)
            print("\n##########################\n")
        except KeyboardInterrupt:
            # Stop the agents if interrupted by KeyboardInterrupt
            receiver.stop()
            sender.stop()
            """sender1.stop()
            sender2.stop()"""
            break

    # Quit the SPADE platform.
    quit_spade()


""" sender1 = SenderAgent(USERS[3]['email'], USERS[1]['pw'])
    sender1.start()

    sender2 = SenderAgent(USERS[4]['email'], USERS[1]['pw'])
    sender2.start()"""
