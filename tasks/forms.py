from django import forms
from django.contrib.auth.models import User
from .models import Task, Workspace, Board



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

class WorkspaceForm(forms.ModelForm):
    class Meta:
        members = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.SelectMultiple(attrs={'class' : 'formcontrol'}),
            required=False
        )
        
        model = Workspace
        fields = ['name', 'members']


class BoardForm(forms.ModelForm):
    class Meta: 
        model = Board
        fields = ['name']