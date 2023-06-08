from SensorAgent import SensorAgent
from EmployeeAgent import EmployeeAgent
from ManagerAgent import ManagerAgent
from spade import quit_spade
import time


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
            'pw': 'Grupo3isbest'},
    5: {
            'email': 'meiaagent4@lightwitch.org',
            'pw': 'Grupo3isbest'},
    6: {
            'email': 'meiaagent5@lightwitch.org',
            'pw': 'Grupo3isbest'
    },
    7: {
            'email': 'meiaagent6@lightwitch.org',
            'pw': 'Grupo3isbest'
    }
}

if __name__ == '__main__':
    receiver = EmployeeAgent(USERS[1]['email'], USERS[1]['pw'])
    receiver.set("id", "meiaagent@lightwitch.org")
    print(receiver.get("id"))
    future = receiver.start()
    future.wait()

    receiver1 = EmployeeAgent(USERS[4]['email'], USERS[1]['pw'])
    receiver1.set("id", "meiaagent3@lightwitch.org")
    future1 = receiver.start()
    future1.wait()

    receiver2 = EmployeeAgent(USERS[6]['email'], USERS[1]['pw'])
    receiver2.set("id", "meiaagent5@lightwitch.org")
    future2 = receiver.start()
    future2.wait()

    manager = ManagerAgent(USERS[3]['email'], USERS[1]['pw'])
    manager.set("id", "meiaagent2@lightwitch.org")
    future3 = manager.start()
    future3.wait()

    sender = SensorAgent(USERS[2]['email'], USERS[1]['pw'])
    sender.set("father_id", "meiaagent@lightwitch.org")
    sender.start()

    sender1 = SensorAgent(USERS[5]['email'], USERS[1]['pw'])
    sender1.set("father_id", "meiaagent3@lightwitch.org")
    sender1.start()

    sender2 = SensorAgent(USERS[7]['email'], USERS[1]['pw'])
    sender2.set("father_id", "meiaagent5@lightwitch.org")
    sender2.start()

    while receiver.is_alive():
        try:
            time.sleep(1)
            print("\n##########################\n")
        except KeyboardInterrupt:
            receiver.stop()
            sender.stop()
            receiver1.stop()
            receiver2.stop()
            sender1.stop()
            sender2.stop()
            manager.stop()
            break

    quit_spade()
