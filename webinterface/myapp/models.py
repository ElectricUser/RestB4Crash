from django.db import models
from djongo.models import ObjectIdField


# The database Users model.
class Users(models.Model):
    _id = ObjectIdField()  # Field for storing the unique identifier (_id).
    username = models.CharField(max_length=100)  # Field for storing the username (email).
    password = models.CharField(max_length=100)  # Field for storing the password.
    isManager = models.BooleanField(default=False)  # Field for indicating whether the user is a manager.
    loggedIn = models.BooleanField(default=False)  # Field for indicating whether the user is currently logged in.

    class Meta:
        app_label = 'myapp'
        db_table = 'Users'  # Name of the database table for this model.

    @property
    def id(self):
        return self._id  # Property to access the _id field

    def __str__(self):
        return f"{self._id}, {self.username}, {self.password}, {self.isManager}, {self.loggedIn}"


# The database Tasks model.
class Tasks(models.Model):
    _id = ObjectIdField()  # Field for storing the unique identifier (_id).
    title = models.CharField(max_length=100)  # Field for storing the title of the task.
    description = models.IntegerField()  # Field for storing the description of the task.
    difficulty = models.IntegerField()  # Field for storing the difficulty level of the task.
    estimated_hours = models.CharField(max_length=100)  # Field for storing the estimated hours for task completion.
    start_time = models.CharField(max_length=100)  # Field for storing the start time of the task.
    end_time = models.CharField(max_length=100)  # Field for storing the end time of the task.
    status = models.CharField(max_length=100)  # Field for storing the status of the task.

    class Meta:
        app_label = 'myapp'
        db_table = 'Task'  # Name of the database table for this model.

    @property
    def id(self):
        return self._id  # Property to access the _id field.

    def __str__(self):
        return f"{self._id}, {self.title}, {self.description}, {self.difficulty}, {self.estimated_hours}, " \
               f"{self.start_time}, {self.end_time}, {self.status}"


# The database TaskPause model.
class TaskPause(models.Model):
    _id = ObjectIdField()  # Field for storing the unique identifier (_id).
    task_id = models.CharField(max_length=100)  # Field for storing the id of the task.
    pause_start = models.DateTimeField()  # Field for storing the start time of the pause.
    pause_end = models.DateTimeField()  # Field for storing the end time of the pause.
    duration = models.IntegerField()  # Field for storing the total time of the pause.

    class Meta:
        app_label = 'myapp'
        db_table = 'TaskPause'  # Name of the database table for this model.

    @property
    def id(self):
        return self._id  # Property to access the _id field.

    def __str__(self):
        return f"{self._id}, {self.task_id}, {self.pause_start}, {self.pause_end}, {self.duration}"


# The database AssignedTasks model.
class AssignedTasks(models.Model):
    _id = ObjectIdField()  # Field for storing the unique identifier (_id).
    title = models.CharField(max_length=100)  # Field for storing the title of the task.
    description = models.CharField(max_length=100)  # Field for storing the description of the task.
    difficulty = models.IntegerField()  # Field for storing the difficulty level of the task.
    estimated_hours = models.IntegerField()  # Field for storing the estimated hours for task completion.
    start_time = models.DateTimeField()  # Field for storing the start time of the task
    end_time = models.DateTimeField()  # Field for storing the end time of the task
    status = models.CharField(max_length=100)  # Field for storing the status of the task
    user = models.CharField(max_length=100)  # Field for storing the assigned user to the task.
    duration = models.IntegerField()  # Field for storing the duration of completions of the task.
    n_pauses = models.IntegerField()  # Field for storing the number of pauses of the task.
    n_stress = models.IntegerField()  # Field for storing the number of stress moments of the task.
    pause_duration = models.IntegerField()  # Field for storing the total pause duration of the task.

    class Meta:
        app_label = 'myapp'
        db_table = 'AssignedTasks'  # Name of the database table for this model

    @property
    def id(self):
        return self._id  # Property to access the _id field

    def __str__(self):
        return f"{self._id}, {self.title}, {self.description}, {self.difficulty}, {self.estimated_hours}, " \
               f"{self.start_time}, {self.end_time}, {self.status}, {self.user}, {self.duration}"
