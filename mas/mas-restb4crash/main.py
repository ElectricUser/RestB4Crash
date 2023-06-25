from Agents.ManagerAgent import ManagerAgent
from Agents.EmployeeAgent import EmployeeAgent
from Agents.SensorAgent import SensorAgent
import spade
from config.credentials import *


async def main():
    # Employee Agents
    employee_agent = EmployeeAgent(USERS[1]['email'], PASSWORD)
    await employee_agent.start()

    employee_agent1 = EmployeeAgent(USERS[4]['email'], PASSWORD)
    await employee_agent1.start()

    employee_agent2 = EmployeeAgent(USERS[6]['email'], PASSWORD)
    await employee_agent2.start()

    # Manager Agent
    manager_agent = ManagerAgent(USERS[3]['email'], PASSWORD)
    await manager_agent.start()

    # Sensor Agents
    sensor_agent = SensorAgent(USERS[2]['email'], PASSWORD)
    await sensor_agent.start()

    sensor_agent1 = SensorAgent(USERS[5]['email'], PASSWORD)
    await sensor_agent1.start()

    sensor_agent2 = SensorAgent(USERS[7]['email'], PASSWORD)
    await sensor_agent2.start()

    await spade.wait_until_finished(manager_agent)
    print("Agents finished")


if __name__ == "__main__":
    print("hello")
    spade.run(main())
