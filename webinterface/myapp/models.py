from django.db import models


class Tasks(models.Model):
    taskID = models.AutoField(primary_key=True)
    priority = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    time = models.CharField(max_length=100)

    class Meta:
        app_label = 'myapp'
        db_table = 'tasks'

    def __str__(self):
        return self.taskID, self.priority, self.difficulty, self.time


class Employees(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    task_id = models.CharField(max_length=100)

    class Meta:
        app_label = 'myapp'
        db_table = 'employees'

    def __str__(self):
        return f"{self.id}, {self.name}, {self.task_id}."
