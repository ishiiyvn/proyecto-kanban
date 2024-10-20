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

    
class CardList(models.Model):
    name = models.CharField(max_length=25)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='card_lists')
    
    def __str__(self):
        return self.name
    

class Card(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)  # New field for due date
    created = models.DateTimeField(auto_now_add=True)
    card_list = models.ForeignKey(CardList, on_delete=models.CASCADE, related_name='cards')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cards')    

    def __str__(self):
        return self.name
    

class ChecklistItem(models.Model):
    card = models.ForeignKey(Card, related_name='checklist_items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description


