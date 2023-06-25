# Challenge 4

This document shows some of the configurations needed so that the application can work

## Database

The database used in this challenge is MongoDB. To use the database, you need to:

1. Install MongoDB Compass: https://www.mongodb.com/try/download/compass
2. Make a connection with the database
    1. String connection: mongodb+srv://grupo3meia:
       Grupo3isbest@grupo3meia.twv654h.mongodb.net/?retryWrites=true&w=majority

## Agents

For the Agents to work there is a specific version of python (3.9.13) that needs to be used.

The easiest approach to this is using a conda environment, following the next steps:

1. Open a conda terminal and run the following commands:
    1. ```conda create --name "envname" python=3.9.13```
    2. ```conda activate "envname"``` (This command needs to be run everytime a new session is started to activate the
       environment).
2. Navigate to the code folder and install the following dependencies:
    1. ```python3.9 -m pip install spade```
    2. ```python3.9 -m pip install pytz```
3. To run the code use the following command:
    1. ```python3.9 main.py```

## Web Interface

To run the djando web interface, install the following dependencies:

1. ```pip install django```
2. ```pip install myapp```
3. ```pip install djongo pymongo```

To start the web interface run the following command inside the webinterface directory:

1. ```python manage.py runserver```

To be able to reassign tasks it is required to start the reassignTasksEndpoint. For that the following dependencies are
needed:

1. ```pip install Flask```
2. ```pip install flask-cors```
3. ```pip install requests ```

## Initial Measures

To be able to run the MeasureInitialValues.py file, you have to install pymongo, so that the data can be updated in the
database

1. ```pip install pymongo```