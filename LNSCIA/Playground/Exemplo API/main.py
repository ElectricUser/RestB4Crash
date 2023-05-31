import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

# save this as app.py
from flask import Flask, request

app = Flask(__name__)
sensorValue = 0


@app.route("/")
def hello():
    # clientdummyagent = ClientDummyAgent(jid="c1@jabbers.one", password="teste_123")
    # clientdummyagent.start()
    # clientdummyagent.web.start(hostname="127.0.0.1", port="10000")
    #
    # while True:
    #     try:
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         break
    # clientdummyagent.stop()

    global sensorValue
    return "Hello, World! Current Sensor Value: {}".format(sensorValue)


@app.route('/sensorInputValue', methods=['POST'])
def add_value():
    if request.method == 'POST':
        data = request.get_json()
        if 'value' in data:
            value = data['value']
            print(value)
            global sensorValue
            sensorValue = value

    return "", 200


class ClientDummyAgent(Agent):

    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid
        self.counter = None

    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    class MyBehavior(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour...")
            self.counter = 0

        async def run(self):
            print("Current Sensor Value: {}".format(sensorValue))
            self.counter += 1
            if self.counter > 30:
                self.kill(exit_code=10)
                return
            await asyncio.sleep(1)

        async def on_end(self):
            print("Behaviour finished with exit code {}.".format(self.exit_code))

    async def setup(self):
        self.agent_say("Agent starting . . .")
        b = self.MyBehavior()
        self.add_behaviour(b)


if __name__ == "__main__":
    app.run(port=5001)
