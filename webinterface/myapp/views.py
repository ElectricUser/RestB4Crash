from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from django.utils import timezone
from myapp.models import Tasks, Users, AssignedTasks


def login_page(request):
    Users.objects.all().filter(loggedIn__in=[True]).update(loggedIn=False)
    users = Users.objects.all()
    managers = Users.objects.filter(isManager__in=[True])
    employees = Users.objects.filter(isManager__in=[False])

    context = {
        'users': users,
        'managers': managers,
        'employees': employees
    }
    return render(request, 'login.html', context)


def navbar(request):
    return render(request, 'navbar.html')


def contact(request):
    return render(request, 'contact.html')


def employee_page(request):
    logged_in_user = Users.objects.get(loggedIn__in=[True])
    username = logged_in_user.username
    assigned_tasks = AssignedTasks.objects.filter(user=username)

    users = Users.objects.all()

    context = {
        'assignedTasks': assigned_tasks,
        'users': users
    }

    return render(request, 'employee_page.html', context)


def manager_page(request):
    assigned_tasks = AssignedTasks.objects.all()
    tasks = Tasks.objects.all()
    users = Users.objects.all()

    combined_list = list(assigned_tasks)

    # Format the user names
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

    return render(request, 'manager_page.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = Users.objects.get(username=username)

            user.loggedIn = True
            user.save()

            return JsonResponse({'success': True})
        except Tasks.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def logout(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = Users.objects.get(username=username)

            user.loggedIn = False
            user.save()

            return JsonResponse({'success': True})
        except Tasks.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'}), redirect(request, '/login/')


def start_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        try:
            task = AssignedTasks.objects.get(_id=ObjectId(task_id))

            task.status = 'doing'
            task.start_time = timezone.now()
            task.save()
            return JsonResponse({'success': True})
        except Tasks.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt
def finish_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')

        try:
            task = AssignedTasks.objects.get(_id=ObjectId(task_id))

            if task.status == 'doing':
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
