from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    text = models.CharField(max_length=300)
    is_done = models.BooleanField(default=False)
    priority = models.IntegerField()
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Task {self.pk}'

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return f'Project "{self.name}"'