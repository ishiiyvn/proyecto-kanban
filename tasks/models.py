from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Workspace(models.Model):
    name = models.CharField(max_length=25)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='workspaces')

    def __str__(self):
        return self.name

    
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by ' + self.user.username

class Board(models.Model):
    name = models.CharField(max_length=25)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


