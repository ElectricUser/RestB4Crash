from flask import Flask
from flask import render_template
from flask import request

# Create a Flask app instance.
app = Flask(__name__)

# Define a list to store users.
users = list()

"""@app.route("/")
def main():
    return "<p>Hello, World!</p>"
"""


# Define a function to handle 404 errors.
@app.errorhandler(404)
def page_not_found(error):
    # Render a custom HTML template for the 404 error page.
    return render_template('page_not_found.html'), 404


# Define a route for the "/sensors" endpoint.
@app.route("/sensors")
def get_sensors():
    return "<p>Sensors page</p>"


# Define a route for the "/sensors/<sensor_id>" endpoint.
@app.route("/sensors/<int:sensor_id>")
def get_sensor(sensor_id):
    return f"<p>Sensor {sensor_id}</p>"


# Define a route for the "/sensors" endpoint with the POST method.
@app.route("/sensors", methods=['POST'])
def post_sensor():
    data = request.json
    print(data)
    return "example"


if __name__ == "__main__":
    app.run()
