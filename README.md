# Challenge 4

This document shows some of the configurations needed so that the application can work

## Database

The database used in this challenge is MySQL. To use the database, you need to:

1. Install MySQL: https://dev.mysql.com/downloads/mysql/
2. Turn on MySQL
    1. For MacOS users: Go to System Preferences, open MySQL, click on Initialize Database, then create a password for
       the "root" user
    2. For Windows users: When installing MySQL, create a password for the "root" user
3. (Optional) Install MySQL Workbench to manage the database: https://www.mysql.com/products/workbench/
4. Go to Database.ipynb and run all the cells to create the database, tables and populate all the tables

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