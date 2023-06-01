from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
app = Flask(__name__)

users = list()


"""@app.route("/")
def main():
    return "<p>Hello, World!</p>"
"""


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route("/sensors")
def get_sensors():
    return "<p>Sensors page</p>"


@app.route("/sensors/<int:sensor_id>")
def get_sensor(sensor_id):
    return f"<p>Sensor {sensor_id}</p>"


@app.route("/sensors", methods=['POST'])
def post_sensor():
    data = request.json
    print(data)
    return "example"
