import pprint
import json
from asyncio import wait_for

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://grupo3meia:Grupo3isbest@grupo3meia.twv654h.mongodb.net/?retryWrites=true&w=majority"

# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def get_db():
    mydb = client['grupo3meia']
    return mydb


my_db = get_db()


def get_tasks(db):
    col = db['Task']
    return col


mycol = get_tasks(my_db)


def fetch_n_tasks_for_8h():
    hours_sum = 0
    tasks = list()
    try:
        for task in mycol.find():
            print(task)
            if hours_sum + task['estimated_hours'] <= 8:
                tasks.append(task)
                hours_sum += task['estimated_hours']

        pprint.pprint(tasks)
    except Exception as e:
        print("There was an error fetching tasks from db ", e)
    return tasks


def assign_tasks_day(agent_jid, tasks: list):
    for t in tasks:
        t['user'] = agent_jid

    return tasks


def delete_task_documents(tasks_to_delete, col):
    for task in tasks_to_delete:
        print("Task to delete: ", task)
        try:
            col.delete_one({"title": task['title']})
        except Exception as e:
            print("There was an error deleting tasks ", e)


# Insert tasks to db
def add_tasks_to_db(tasks, col):
    try:
        col.insert_many(tasks)
        return True
    except Exception as e:
        print("There was an error inserting tasks into DB ", e)


def ask_tasks(agent_jid):
    try:
        # Fetch tasks that make 8h total
        tasks_fetched = fetch_n_tasks_for_8h()

        # Assign tasks to agent
        new_tasks = assign_tasks_day(agent_jid, tasks_fetched)

        assign_tasks_col = my_db['AssignedTasks']

        # Add tasks to assign tasks table
        add_tasks_to_db(new_tasks, assign_tasks_col)

        # Delete Tasks from old general tasks table
        delete_task_documents(tasks_fetched, mycol)
        return new_tasks
    except Exception as e:
        print("there was an error ", e)
        return False


# ask_tasks("meiaagen3@lightwitch.org")


# UTILs
# Delete all tasks from tables
def clean_db():
    my_db['AssignedTasks'].delete_many({})
    mycol.delete_many({})

# clean_db()
