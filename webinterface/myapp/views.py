from django.shortcuts import render
from myapp.models import Tasks, Employees


def employee_task_table(request):
    tasks = Tasks.objects.all()
    employees = Employees.objects.all()

    context = {
        'tasks': tasks,
        'employees': employees
    }

    return render(request, 'myapp/employee_task_table.html', context)
