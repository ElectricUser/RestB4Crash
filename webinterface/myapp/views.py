from django.shortcuts import render
from myapp.models import Tasks, Employees


def homepage(request):
    return render(request, 'myapp/homepage.html')


def contact(request):
    return render(request, 'myapp/contact.html')


def navbar(request):
    return render(request, 'myapp/navbar.html')


def employee_task_table(request):
    tasks = Tasks.objects.all()
    employees = Employees.objects.all()

    context = {
        'tasks': tasks,
        'employees': employees
    }

    return render(request, 'myapp/employee_task_table.html', context)
