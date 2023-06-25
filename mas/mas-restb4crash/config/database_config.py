from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://grupo3meia:Grupo3isbest@grupo3meia.twv654h.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

DB = client['grupo3meia']
TASKS = DB['Task']
ASSIGNED_TASKS = DB['AssignedTasks']
USERS = DB['Users']
NEXT_DAY_TASKS = DB['NextDayTasks']
HIST_TASKS = DB['Historic_Task']
RBA_AssignTask = DB['RBA_AssignTask']
RBA_Task = DB['RBA_Task']
