from Agents.ManagerAgent import ManagerAgent
from Agents.FilmPressureAgent import FilmPressureAgent
from dotenv import dotenv_values
from spade import quit_spade
import time
config = dotenv_values(".env")

UNAME = config['UNAME']
UNAME1 = config['UNAME1']
UNAME2 = config['UNAME2']
UNAME3 = config['UNAME3']
UNAME4 = config['UNAME4']
UNAME5 = config['UNAME5']
PW = config['PW']
PW1 = config['PW1']


if __name__ == "__main__":
    receiveragent = ManagerAgent(UNAME, PW)
    senderagent = FilmPressureAgent(UNAME1, PW)

    future = receiveragent.start()
    receiveragent.web.start(hostname="127.0.0.1", port="10000")
    future.result()  # wait for receiver agent to be prepared.

    senderagent.start()
    senderagent.web.start(hostname="127.0.0.1", port="10001")

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")
    quit_spade()
