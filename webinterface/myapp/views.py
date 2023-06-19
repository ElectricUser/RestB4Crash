import json

from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from datetime import datetime
from myapp.models import Tasks, Users, AssignedTasks, TaskPause
from django.utils import timezone


# Login page view request.
def login_page(request):
    # Set loggedIn field of all users to False when opening the login page.
    Users.objects.all().filter(loggedIn__in=[True]).update(loggedIn=False)

    # Retrieve all users, managers, and employees.
    users = Users.objects.all()
    managers = Users.objects.filter(isManager__in=[True])
    employees = Users.objects.filter(isManager__in=[False])

    context = {
        'users': users,
        'managers': managers,
        'employees': employees
    }

    # Render the login page with the retrieved data.
    return render(request, 'login.html', context)


# Navbar view request.
def navbar(request):
    # Render the navbar template.
    return render(request, 'navbar.html')


# Contact view request.
def contact(request):
    # Render the contact page.
    return render(request, 'contact.html')


# Employee page view request.
def employee_page(request):
    # Get the current logged-in user.
    logged_in_user = Users.objects.get(loggedIn__in=[True])
    username = logged_in_user.username

    # Get the assigned tasks to the logged-in user.
    assigned_tasks = AssignedTasks.objects.filter(user=username)

    # Get all the users.
    users = Users.objects.all()

    tasks_json = []
    for task in assigned_tasks:
        new_task = model_to_dict(task)
        new_task['_id'] = str(new_task['_id'])
        new_task['start_time'] = new_task['start_time'].isoformat() if new_task['start_time'] is not None else None
        new_task['end_time'] = new_task['end_time'].isoformat() if new_task['end_time'] is not None else None
        tasks_json.append(new_task)

    assigned_tasks = AssignedTasks.objects.filter(user=username)
    task_ids = assigned_tasks.values_list('_id', flat=True)  # Get the IDs of the assigned tasks
    pauses = [];
    for task_id in task_ids:
        task_pauses = TaskPause.objects.filter(task_id=task_id)
        pauses.extend(task_pauses)

    pauses_json = []
    for pause in pauses:
        new_pause = model_to_dict(pause)
        new_pause['_id'] = str(new_pause['_id'])
        new_pause['pause_start'] = new_pause['pause_start'].isoformat() if new_pause[
                                                                               'pause_start'] is not None else None
        new_pause['pause_end'] = new_pause['pause_end'].isoformat() if new_pause['pause_end'] is not None else None
        pauses_json.append(new_pause)

    context = {
        'assignedTasks': assigned_tasks,
        'users': users,
        'assignedTasksJson': json.dumps(tasks_json),
        'taskPausesJson': json.dumps(pauses_json)
    }

    # Render the employee page with the assigned tasks and users.
    return render(request, 'employee_page.html', context)


# Manager page view request.
def manager_page(request):
    # Get all tasks, assigned tasks and all users
    assigned_tasks = AssignedTasks.objects.all()
    tasks = Tasks.objects.all()
    users = Users.objects.all()

    combined_list = list(assigned_tasks)

    # Format the usernames to not show the email part.
    for task in combined_list:
        task.user = task.user.split("@")[0].capitalize()

    for task in tasks:
        if not any(task.title == combined_task.title for combined_task in combined_list):
            task.user = "Not Assigned"
            combined_list.append(task)

    context = {
        'tasks': combined_list,
        'users': users
    }

    # Render the manager page with the combined list of tasks and users.
    return render(request, 'manager_page.html', context)


# Login view request.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = Users.objects.get(username=username)

            # Set the loggedIn field of the user to True.
            user.loggedIn = True
            user.save()

            return JsonResponse({'success': True})
        except Tasks.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


# Logout view request.
def logout(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = Users.objects.get(username=username)

            # Set the loggedIn field of the user to False.
            user.loggedIn = False
            user.save()

            return JsonResponse({'success': True})
        except Tasks.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'}), redirect(request, '/login/')


# Start task view request.
def start_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        try:
            task = AssignedTasks.objects.get(_id=ObjectId(task_id))

            # Update the task status to 'doing' and set the start time.
            task.status = 'doing'
            current_time = timezone.now().astimezone(timezone.get_current_timezone())
            task.start_time = current_time
            task.save()

            # Assuming task is the model instance containing an ObjectId field
            task_dict = model_to_dict(task)

            # Convert the ObjectId field to a string representation
            task_dict['_id'] = str(task_dict['_id'])

            return JsonResponse({'success': True, 'task': task_dict})
        except Tasks.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


# Finish task view request.
@csrf_exempt
def finish_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        try:
            task = AssignedTasks.objects.get(_id=ObjectId(task_id))

            if task.status == 'doing':
                # Update the task status to 'done' and set the end time
                task.status = 'done'
                current_time = timezone.now().astimezone(timezone.get_current_timezone())
                task.end_time = current_time
                duration = task.end_time - task.start_time
                task.duration = duration.seconds
                task.save()

                # Assuming task is the model instance containing an ObjectId field
                task_dict = model_to_dict(task)

                # Convert the ObjectId field to a string representation
                task_dict['_id'] = str(task_dict['_id'])

                # Return the updated task object as JSON response.
                return JsonResponse({'success': True, 'task': task_dict})
            else:
                return HttpResponse(status=400)  # Task is not in 'doing' status
        except Tasks.DoesNotExist:
            return HttpResponse(status=404)  # Task not found
    else:
        return HttpResponse(status=405)  # Invalid request method


def update_task_duration(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        duration = request.POST.get('duration')

        task = AssignedTasks.objects.get(_id=ObjectId(task_id))

        # Update the task status to 'doing' and set the start time.
        task.pause_duration = duration
        task.save()

        # Return a JSON response indicating success or failure
        response_data = {'status': 'success'}
        return JsonResponse(response_data)

    # Return an error response if the request method is not POST
    response_data = {'status': 'error', 'message': 'Invalid request method'}
    return JsonResponse(response_data, status=400)


def pause_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(AssignedTasks, _id=ObjectId(task_id))

        if task.status != 'doing':
            return JsonResponse({'message': 'Task is not in progress.'}, status=400)

        # Create a new pause entry with the current time as the start time
        current_time = timezone.now().astimezone(timezone.get_current_timezone())
        pause = TaskPause.objects.create(task_id=task.id, pause_start=current_time)
        task.status = 'paused'
        task.save()

        # Assuming task is the model instance containing an ObjectId field
        task_dict = model_to_dict(task)
        # Convert the ObjectId field to a string representation
        task_dict['_id'] = str(task_dict['_id'])

        # Assuming task is the model instance containing an ObjectId field
        task_pause_dict = model_to_dict(pause)
        # Convert the ObjectId field to a string representation
        task_pause_dict['_id'] = str(task_pause_dict['_id'])
        task_pause_dict['task_id'] = str(task_pause_dict['task_id'])

        # Return the task and task pause objects in the JSON response
        return JsonResponse({'message': 'Task paused successfully.', 'task': task_dict, 'pause': task_pause_dict},
                            status=200)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


def continue_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(AssignedTasks, _id=ObjectId(task_id))

        if task.status != 'paused':
            return JsonResponse({'message': 'Task is not paused.'}, status=400)

        # Retrieve the most recent pause for the task
        pause = TaskPause.objects.filter(task_id=task.id).order_by('-pause_start').first()

        if pause:
            # Set the end time for the pause to resume the task
            pause.pause_end = timezone.now().astimezone(timezone.get_current_timezone())
            pause.duration = (pause.pause_end - pause.pause_start).seconds
            pause.save()
            task.status = 'doing'
            task.save()

            # Assuming task is the model instance containing an ObjectId field
            task_dict = model_to_dict(task)
            # Convert the ObjectId field to a string representation
            task_dict['_id'] = str(task_dict['_id'])

            # Assuming task is the model instance containing an ObjectId field
            task_pause_dict = model_to_dict(pause)
            # Convert the ObjectId field to a string representation
            task_pause_dict['_id'] = str(task_pause_dict['_id'])

            # Return the task and pause objects in the JSON response
            return JsonResponse({'message': 'Task resumed successfully.', 'task': task_dict, 'pause': task_pause_dict},
                                status=200)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)
