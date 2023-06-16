from django.db import models
from djongo.models import ObjectIdField
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Users(models.Model):
    _id = ObjectIdField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    isManager = models.BooleanField(default=False)
    loggedIn = models.BooleanField(default=False)

    class Meta:
        app_label = 'myapp'
        db_table = 'Users'

    @property
    def id(self):
        return self._id

    def __str__(self):
        return f"{self._id}, {self.username}, {self.password}, {self.isManager}, {self.loggedIn}"

    objects = models.Manager()  # Define a default manager


@receiver(post_migrate)
def update_logged_in_values(sender, **kwargs):
    Users.objects.update(loggedIn=False)


class Tasks(models.Model):
    _id = ObjectIdField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    estimated_hours = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    class Meta:
        app_label = 'myapp'
        db_table = 'Task'

    @property
    def id(self):
        return self._id

    def __str__(self):
        return f"{self._id}, {self.title}, {self.description}, {self.difficulty}, {self.estimated_hours}, " \
               f"{self.start_time}, {self.end_time}, {self.status}"


class AssignedTasks(models.Model):
    _id = ObjectIdField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    estimated_hours = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    class Meta:
        app_label = 'myapp'
        db_table = 'AssignedTasks'

    @property
    def id(self):
        return self._id

    def __str__(self):
        return f"{self._id}, {self.title}, {self.description}, {self.difficulty}, {self.estimated_hours}, " \
               f"{self.start_time}, {self.end_time}, {self.status}, {self.user}"
