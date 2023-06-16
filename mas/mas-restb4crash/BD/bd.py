import asyncio

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://grupo3meia:Grupo3isbest@grupo3meia.twv654h.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))
"""
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
"""

DB = client['grupo3meia']
TASKS = DB['Task']
ASSIGNED_TASKS = DB['AssignedTasks']


async def fetch_n_tasks_for_8h():
    hours_sum = 0
    tasks = list()
    try:
        for task in TASKS.find():
            if hours_sum + task['estimated_hours'] <= 8:
                tasks.append(task)
                hours_sum += task['estimated_hours']
    except Exception as e:
        print("There was an error: ", e)
    return tasks


def assign_tasks_to_user(agent_jid, tasks: list):
    for t in tasks:
        t['user'] = agent_jid

    return tasks


# Insert tasks to db
async def add_tasks_to_db(tasks, col):
    try:
        col.insert_many(tasks)
        return True
    except Exception as e:
        print("There was an error: ", e)


async def delete_task_documents(tasks_to_delete, col):
    for task in tasks_to_delete:
        try:
            col.delete_one({"title": task['title']})
        except Exception as e:
            print("There was an error: ", e)


async def ask_tasks(agent_jid):
    try:
        # Fetch tasks that estimated time makes 8h total
        tasks_fetched = await fetch_n_tasks_for_8h()

        # Assign tasks to agent
        new_tasks = assign_tasks_to_user(agent_jid, tasks_fetched)

        assign_tasks_col = DB['AssignedTasks']

        # Add tasks to AssignedTasks table
        await add_tasks_to_db(new_tasks, assign_tasks_col)

        # Delete AssignedTasks from Tasks table
        await delete_task_documents(tasks_fetched, TASKS)
        return new_tasks
    except Exception as e:
        print("there was an error ", e)
        return False


# final_example = asyncio.run(ask_tasks("meiaagent1@lightwitch.org"))

# Delete all tasks from db
def clean_db():
    DB['AssignedTasks'].delete_many({})
    TASKS.delete_many({})


# clean_db()


async def add_stress(agent_jid):
    # find task ebing done at the moment
    doing_task = ASSIGNED_TASKS.find_one({"user": agent_jid, "status": "doing"})

    # check if task has n_stress attribute
    n_field_task = ASSIGNED_TASKS.find_one({"user": agent_jid, "status": "doing", "n_stress": { "$exists": "true" }})

    if n_field_task:
        n_stress = n_field_task['n_stress']
        n_stress += 1
        ASSIGNED_TASKS.update_one(doing_task, {"$set": {"n_stress": n_stress}})
    else:
        ASSIGNED_TASKS.update_one(doing_task, {"$set": {"n_stress": 1}})

# example = asyncio.run(add_stress("meiaagent@lightwitch.org"))
