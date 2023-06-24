"""
Created on Wed Jun 21 17:52:37 2023

@author: renat
"""

import asyncio

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import math
"""
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
"""

def getData():
    uri = "mongodb+srv://grupo3meia:Grupo3isbest@grupo3meia.twv654h.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))

    DB = client['grupo3meia']
    TASKS = DB['Task']
    ASSIGNED_TASKS = DB['AssignedTasks']
    
    # getting task whit "todo"
    tasks_list = [task for task in TASKS.find() if task['status'] == "todo" ]
    
    # getting tasks assigned to users
    assignedTask_list = [task for task in ASSIGNED_TASKS.find() ]
    
    # getting users
    users = {}
    for task in assignedTask_list:
        if task['user'] not in users:
            users[task['user']] = [task]
        else:
            users[task['user']].append(task)
            
    return tasks_list, assignedTask_list, users

def calculateUserTodaysWork(users):
    removed_tasks = []
    for user in users:
        # print("User: ", user)
        task_done = []
        task_todo = []
        for count, task in enumerate(users[user]):
            # print(f"Task {count} : {task}")
            if (task['status'] == "done"):
                task_done.append(task)
                users[user].remove(task)
                removed_tasks.append(task)
            else:
                task_todo.append(task)
                            
        # """ User Stats
        """
        print("\nUser Stats:\n")
        print(f"\t -> Task today: {len(users[user])}")
        print(f"\t -> Task Done number: {len(task_done)}")
        print(f"\t -> Task To Do number: {len(task_todo)}")
        print("\n")
        """
        # """
    return users, removed_tasks

def calculateUserTommorrowWork (users):
    usersTaskInfo = {}
    for count, user in enumerate(users):
        # print("User: ", user)
                
        todays_task = users[user]
        
        hours_todo, difficulty_todo, n_pauses, n_stress = 0, 0, 0, 0
        for task in todays_task:
            hours_todo      += int(task['estimated_hours'])
            difficulty_todo += int(task['difficulty'])
            # check if task has pauses and stress
            try:
                n_pauses        += int(task['n_pauses'])
            except:
                pass
            try:
                n_stress        += int(task['n_stress'])
            except:
                pass

        usersTaskInfo[user] = ({
            "user": user,
            "hours_todo": hours_todo,
            "difficulty_todo": difficulty_todo,
            "hours_todo_tommorrow": 8 - hours_todo if 8 - hours_todo > 0 else 0,
            "difficulty_todo_tommorrow" : 15 - difficulty_todo - getConversion(n_stress, n_pauses) if 15 - difficulty_todo - getConversion(n_stress, n_pauses) > 0 else 0
        })
        
        # """ Tommorrow Stats
        """
        print("\nUser Tommorrow Stats:\n")
        print(f"\t -> Hours to do tommorrow from todays task: {hours_todo}")
        print(f"\t -> Difficulty to do tommorrow from todays task: {difficulty_todo}")
        print(f"\t -> Free hours tommorrow: {usersTaskInfo[user]['hours_todo_tommorrow']}")
        print(f"\t -> Free Difficulty tommorrow: {usersTaskInfo[user]['difficulty_todo_tommorrow']}")
        print("\n")
        """
        # """
    return usersTaskInfo

def getConversion(n_stress, n_pauses):
    x = n_stress - n_pauses  # Compute the difference between stress and pauses
    sigmoid_value = 1 / (1 + math.exp(-x))  # Apply sigmoid function

    # Scale the sigmoid value to the range -2 to 2
    scaled_value = round(sigmoid_value * 4) - 2

    return scaled_value

def sortUsers(users, usersTaskInfo, debug = False):
    """
    USERS
    """
    if (debug):
        print("\n Users before sort\n")
        for count, user in enumerate(users):
            print(f"\tUser {count}: {user}")
    
    users = sorted(users, key=lambda user: usersTaskInfo.get(user)[
                   'hours_todo_tommorrow'] + usersTaskInfo.get(user)['difficulty_todo_tommorrow']/2, reverse=True)
    
    if (debug):
        print("\n Users after sort\n")
        for count, user in enumerate(users):
            print(f"\tUser {count}: {user}")
    return users

def sortTask(tasks, debug = False):
    """
    TASKS
    """
    if (debug):
        print("\n Tasks before sort\n")
        for count, task in enumerate(tasks):
            print(f"\tTask {count}: {task['title']}")
    
    tasks = sorted(tasks, key=lambda x: x['difficulty']/2 + x['estimated_hours'], reverse=True)
    
    if (debug):
        print("\n Tasks after sort\n")
        for count, task in enumerate(tasks):
            print(f"\tTask {count}: {task['title']} - {task['difficulty']} - {task['estimated_hours']}")
        
    return tasks

def showUserAgenda(userTaskInfo, user):
    if (userTaskInfo['hours_todo_tommorrow'] == 0 or userTaskInfo['difficulty_todo_tommorrow'] == 0):
        print(f"User {user} has an full agenda for tommorrow")
        return 
    print(f"User {user} has {userTaskInfo['hours_todo_tommorrow']} hours available")

def distributeTaskTommorrow (users, usersTaskInfo, tasks, debug = False):
    # sorts users based of how much free time they have tommorow
    users = sortUsers(users, usersTaskInfo)
    
    # sort task based on difficulty and hours
    tasks = sortTask(tasks)
    
    """
    distribut task_alg
    """
    task_added = {}
    
    for user in users:
        userTaskInfo = usersTaskInfo.get(user)

        if (debug):
            print("\n\nPriting Agenda\n")
            showUserAgenda(userTaskInfo, user)
        
        if (userTaskInfo['hours_todo_tommorrow'] == 0 or userTaskInfo['difficulty_todo_tommorrow'] == 0):
            # Full agenda
            continue 
        
        task_added[user] = []

        for task in tasks:
           if (userTaskInfo['hours_todo_tommorrow'] >= int(task['estimated_hours']) and
               userTaskInfo['difficulty_todo_tommorrow'] >= int(task['difficulty'])):
               
               # Add task to the list
               task_added[user].append(task)
               
               # Update user Task Info
               userTaskInfo['hours_todo_tommorrow'] -= int(task['estimated_hours'])
               userTaskInfo['difficulty_todo_tommorrow'] -= int(task['difficulty'])

               tasks.remove(task)

        # Update the dictionary entry for the user
        usersTaskInfo[user] = userTaskInfo  
        
    return task_added, tasks, usersTaskInfo

def storeHistoricTask (tasks):
    uri = "mongodb+srv://grupo3meia:Grupo3isbest@grupo3meia.twv654h.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))

    DB = client['grupo3meia']

    collection = DB['Historic_Task']

    for task in tasks:
        collection.insert_one(task)

    # Delete tasks from DB
    # Deleting the collection the tasks are in
    collection = DB['AssignedTasks']
    for task in tasks:
        collection.delete_one(task)
        

def storeAssignedTask (tasks):
    uri = "mongodb+srv://grupo3meia:Grupo3isbest@grupo3meia.twv654h.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))

    DB = client['grupo3meia']
 
    collection = DB['NextDayTasks']
    """ Dup data """
    collection2 = DB['AssignedTasks']

    for document in collection2.find():
        collection.insert_one(document)
    
    """ End dup data """

    for task in tasks:
        collection.insert_one(task)
    
    # Delete tasks from DB
    # Deleting the collection the tasks are in
    collection = DB['Task']

    for task in tasks:
        collection.delete_one(task)
        
    ## delete assigned task
    collection = DB['AssignedTasks']        
    collection.delete_many({})
    

def formatAddedTask (task_added):
    task_added_copy = []
    for user in task_added: 
        user_task = task_added[user]
        for task in user_task:
            # copy task to task added 2 and add user
            task['user'] = user
            task_added_copy.append(task)
            
    return task_added_copy

def dupData():
    uri = "mongodb+srv://grupo3meia:Grupo3isbest@grupo3meia.twv654h.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))

    DB = client['grupo3meia']
    # copy a collection to another collection to simulate a move
    collection = DB['RBA_AssignTask']
    collection2 = DB['AssignedTasks']

    for document in collection2.find():
        collection.insert_one(document)

    # copy a collection to another collection to simulate a move
    collectionTask = DB['Task']
    collectionRBATask = DB['RBA_Task']

    for document in collectionTask.find():
        collectionRBATask.insert_one(document)
    
def distributeTask():
    tasks, assignedTask, users = getData()
    
    # Gets the users
    # Remove this task and Store in the DB as "Historic Task"
    users, task2Remove = calculateUserTodaysWork(users)
    
    # Gets User availably for tommorrow
    usersTaskInfo = calculateUserTommorrowWork(users)
    
    # These are task in the queu that were assigned to the user
    # 1. Remove the task from DB "Task"
    # 2. Update Assigned task whit these "Task"
    task_added, tasks, usersTaskInfo = distributeTaskTommorrow(users, usersTaskInfo, tasks)
            
    """ Mongo DB Operations """
    # dupData()

    # # Delete and create a record in "Historic Task"
    storeHistoricTask(task2Remove)
    
    # # Delete and create a record in "Assigned Task"
    storeAssignedTask(formatAddedTask(task_added))

if __name__ == "__main__":
    distributeTask()
    # tasks, assignedTask, users = getData()
    
    # # Gets the users
    # # Remove this task and Store in the DB as "Historic Task"
    # users, task2Remove = calculateUserTodaysWork(users)
    
    # # Gets User availably for tommorrow
    # usersTaskInfo = calculateUserTommorrowWork(users)
    
    # # These are task in the queu that were assigned to the user
    # # 1. Remove the task from DB "Task"
    # # 2. Update Assigned task whit these "Task"
    # task_added, tasks, usersTaskInfo = distributeTaskTommorrow(users, usersTaskInfo, tasks)

    """ Mongo DB Operations """
    # dupData()

    # # Delete and create a record in "Historic Task"
    # storeHistoricTask(task2Remove)
    
    # # Delete and create a record in "Assigned Task"
    # storeAssignedTask(formatAddedTask(task_added))
































