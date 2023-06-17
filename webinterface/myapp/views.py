from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from django.utils import timezone
from myapp.models import Tasks, Users, AssignedTasks


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

    context = {
        'assignedTasks': assigned_tasks,
        'users': users
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
            task.start_time = timezone.now()
            task.save()

            return JsonResponse({'success': True})
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
                task.end_time = timezone.now()
                task.save()

                return HttpResponse(status=200)  # Task status updated successfully
            else:
                return HttpResponse(status=400)  # Task is not in 'doing' status
        except Tasks.DoesNotExist:
            return HttpResponse(status=404)  # Task not found
    else:
        return HttpResponse(status=405)  # Invalid request method
