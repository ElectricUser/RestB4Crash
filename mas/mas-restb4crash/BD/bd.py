import asyncio

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from redistribue__taskV2 import distributeTask

uri = "mongodb+srv://grupo3meia:Grupo3isbest@grupo3meia.twv654h.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

DB = client['grupo3meia']
TASKS = DB['Task']
ASSIGNED_TASKS = DB['AssignedTasks']
USERS = DB['Users']
NEXT_DAY_TASKS = DB['NextDayTasks']
HIST_TASKS = DB['Historic_Task']


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


# Delete all tasks from db
def clean_db():
    DB['AssignedTasks'].delete_many({})
    TASKS.delete_many({})
    NEXT_DAY_TASKS.delete_many({})
    DB['Historic_Task'].delete_many({})


async def add_stress(agent_jid):
    # find task being done at the moment
    doing_task = ASSIGNED_TASKS.find_one({"user": agent_jid, "status": "doing"})

    if doing_task:
        n_stress = doing_task['n_stress']
        n_stress += 1
        ASSIGNED_TASKS.update_one(doing_task, {"$set": {"n_stress": n_stress}})
    else:
        return


async def add_pause(agent_jid):
    # find task being done at the moment
    doing_task = ASSIGNED_TASKS.find_one({"user": agent_jid, "status": "doing"})

    if doing_task:
        n_pauses = doing_task['n_pauses']
        n_pauses += 1
        ASSIGNED_TASKS.update_one(doing_task, {"$set": {"n_pauses": n_pauses}})
    else:
        return


async def get_user_avg_force(agent_jid):
    try:
        usr = USERS.find_one({"username": agent_jid})
        usr_avg_force = usr['avg_force']
    except Exception as e:
        print("There was an error: ", e)
        return False
    return usr_avg_force


async def assigned_tasks():
    try:
        task_exists = ASSIGNED_TASKS.find_one({})
    except Exception as e:
        print("There was an error: ", e)
        return False
    if task_exists:
        return True
    else:
        return False


# Distributes tasks using the algorithm and moves them to the assigned tasks table
async def assign_next_day_tasks():
    try:
        # Task Scheduling Algorithm
        dist_tasks = await distributeTask()
        if dist_tasks:
            try:
                next_day_tasks = NEXT_DAY_TASKS.find({})
                assign_tasks_col = DB['AssignedTasks']

                # Add tasks to AssignedTasks table
                await add_tasks_to_db(next_day_tasks, assign_tasks_col)
                DB['NextDayTasks'].delete_many({})
            except Exception as e:
                print("There was an error: ", e)
    except Exception as e:
        print("There was an error: ", e)


async def is_history_tasks_empty():
    task_exists = False
    try:
        task_exists = HIST_TASKS.find_one({})
    except Exception as e:
        print("There was an error: ", e)
    if task_exists:
        return True
    else:
        return False


# clean_db()
