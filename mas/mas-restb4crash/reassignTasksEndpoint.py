from flask import Flask, jsonify
from flask_cors import CORS
from redistribue__taskV2 import distributeTask

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/reassignTasks', methods=['GET'])
def reassign_tasks():
    distributeTask()
    # Handle the request and prepare the response
    data = {'message': 'Reassignment of the Task was successful!'}
    return jsonify(data)


if __name__ == '__main__':
    app.run()
