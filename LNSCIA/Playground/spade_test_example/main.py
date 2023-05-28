from ReceiverAgent import ReceiverAgent
from SenderAgent import SenderAgent
import time
from dotenv import dotenv_values

config = dotenv_values(".env")
UNAME = config['UNAME']
UNAME1 = config['UNAME1']
PW = config['PW']


if __name__ == "__main__":
    receiveragent = ReceiverAgent(UNAME, PW)
    future = receiveragent.start()
    future.wait() # wait for receiver agent to be prepared.
    senderagent = SenderAgent(UNAME1, PW)
    senderagent.start()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")
