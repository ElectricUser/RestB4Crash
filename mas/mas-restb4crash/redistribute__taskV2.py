import math

from config.database_config import *


async def get_data():
    # Getting task with a status 'todo'.
    tasks_list = [task for task in TASKS.find() if task['status'] == "todo"]

    # Getting tasks assigned to users
    assigned_task_list = [task for task in ASSIGNED_TASKS.find()]

    # Getting users
    users = {}
    for task in assigned_task_list:
        if task['user'] not in users:
            users[task['user']] = [task]
        else:
            users[task['user']].append(task)

    return tasks_list, assigned_task_list, users


async def calculate_user_today_work(users):
    removed_tasks = []

    for user in users:
        task_done = []
        task_todo = []

        for count, task in enumerate(users[user]):
            if task['status'] == "done":
                task_done.append(task)
                users[user].remove(task)
                removed_tasks.append(task)
            else:
                task_todo.append(task)

    return users, removed_tasks


async def calculate_user_tomorrow_work(users):
    users_task_info = {}
    for count, user in enumerate(users):
        today_task = users[user]
        hours_todo, difficulty_todo, n_pauses, n_stress = 0, 0, 0, 0

        for task in today_task:
            hours_todo += int(task['estimated_hours'])
            difficulty_todo += int(task['difficulty'])

            # Check if task has pauses and stress.
            try:
                n_pauses += int(task['n_pauses'])
            except ValueError:
                pass
            try:
                n_stress += int(task['n_stress'])
            except ValueError:
                pass

        users_task_info[user] = ({
            "user": user,
            "hours_todo": hours_todo,
            "difficulty_todo": difficulty_todo,
            "hours_todo_tomorrow": 8 - hours_todo if 8 - hours_todo > 0 else 0,
            "difficulty_todo_tomorrow": 15 - difficulty_todo - get_conversion(n_stress, n_pauses)
            if 15 - difficulty_todo - get_conversion(n_stress, n_pauses) > 0 else 0
        })

    return users_task_info


def get_conversion(n_stress, n_pauses):
    x = n_stress - n_pauses  # Compute the difference between stress and pauses.
    sigmoid_value = 1 / (1 + math.exp(-x))  # Apply sigmoid function.

    # Scale the sigmoid value to the range -2 to 2.
    scaled_value = round(sigmoid_value * 4) - 2

    return scaled_value


def sort_users(users, users_task_info, debug=False):
    # USERS.
    if debug:
        print("\n Users before sort\n")
        for count, user in enumerate(users):
            print(f"\tUser {count}: {user}")

    users = sorted(users, key=lambda usr: users_task_info.get(usr)[
                                              'hours_todo_tomorrow'] + users_task_info.get(usr)[
                                              'difficulty_todo_tomorrow'] / 2, reverse=True)

    if debug:
        print("\n Users after sort\n")
        for count, user in enumerate(users):
            print(f"\tUser {count}: {user}")

    return users


def sort_task(tasks, debug=False):
    # TASKS.
    if debug:
        print("\n Tasks before sort\n")
        for count, task in enumerate(tasks):
            print(f"\tTask {count}: {task['title']}")

    tasks = sorted(tasks, key=lambda x: x['difficulty'] / 2 + x['estimated_hours'], reverse=True)

    if debug:
        print("\n Tasks after sort\n")
        for count, task in enumerate(tasks):
            print(f"\tTask {count}: {task['title']} - {task['difficulty']} - {task['estimated_hours']}")

    return tasks


def show_user_agenda(user_task_info, user):
    if user_task_info['hours_todo_tomorrow'] == 0 or user_task_info['difficulty_todo_tomorrow'] == 0:
        print(f"User {user} has an full agenda for tomorrow")
        return

    print(f"User {user} has {user_task_info['hours_todo_tomorrow']} hours available")


async def distribute_task_tomorrow(users, users_task_info, tasks, debug=False):
    # Sorts users based of how much free time they have tomorrow.
    users = sort_users(users, users_task_info)

    # Sort task based on difficulty and hours.
    tasks = sort_task(tasks)

    # Distribute task_algorithm.
    task_added = {}

    for user in users:
        user_task_info = users_task_info.get(user)

        if debug:
            print("\n\nPrinting Agenda\n")
            show_user_agenda(user_task_info, user)

        if user_task_info['hours_todo_tomorrow'] == 0 or user_task_info['difficulty_todo_tomorrow'] == 0:
            # Full agenda
            continue

        task_added[user] = []

        for task in tasks:
            if (user_task_info['hours_todo_tomorrow'] >= int(task['estimated_hours']) and
                    user_task_info['difficulty_todo_tomorrow'] >= int(task['difficulty'])):
                # Add task to the list.
                task_added[user].append(task)

                # Update user Task Info.
                user_task_info['hours_todo_tomorrow'] -= int(task['estimated_hours'])
                user_task_info['difficulty_todo_tomorrow'] -= int(task['difficulty'])

                tasks.remove(task)

        # Update the dictionary entry for the user.
        users_task_info[user] = user_task_info

    return task_added, tasks, users_task_info


async def store_historic_task(tasks):
    for task in tasks:
        HIST_TASKS.insert_one(task)

    # Delete tasks from DB.
    # Deleting the collection the tasks are in.
    for task in tasks:
        ASSIGNED_TASKS.delete_one(task)


async def store_assigned_task(tasks):
    # Dup data
    for document in ASSIGNED_TASKS.find():
        NEXT_DAY_TASKS.insert_one(document)

    # End dup data
    for task in tasks:
        NEXT_DAY_TASKS.insert_one(task)

    # Delete tasks from DB
    # Deleting the collection the tasks are in
    for task in tasks:
        TASKS.delete_one({"title": task['title']})

    # Delete assigned task
    ASSIGNED_TASKS.delete_many({})


def format_added_task(task_added):
    task_added_copy = []

    for user in task_added:
        user_task = task_added[user]

        for task in user_task:
            # copy task to task added 2 and add user
            task['user'] = user
            task_added_copy.append(task)

    return task_added_copy


async def dup_data():
    # Copy a collection to another collection to simulate a move.
    for document in ASSIGNED_TASKS.find():
        RBA_AssignTask.insert_one(document)

    # Copy a collection to another collection to simulate a move
    for document in TASKS.find():
        RBA_Task.insert_one(document)


async def distribute_task():
    tasks, assigned_task, users = await get_data()

    # Gets the users.
    # Remove this task and store in the DB as "Historic Task".
    users, task2_remove = await calculate_user_today_work(users)

    # Gets User availability for tomorrow.
    users_task_info = await calculate_user_tomorrow_work(users)

    # These are task in the queue that were assigned to the user.
    # 1. Remove the task from DB "Task".
    # 2. Update Assigned task with these "Task".
    task_added, tasks, users_task_info = await distribute_task_tomorrow(users, users_task_info, tasks)

    # Delete and create a record in "Historic Task".
    await store_historic_task(task2_remove)

    # Delete and create a record in "Assigned Task".
    await store_assigned_task(format_added_task(task_added))

    if len(task_added) == 0:
        return False
    else:
        return True
