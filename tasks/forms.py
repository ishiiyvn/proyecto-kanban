from django import forms
from django.contrib.auth.models import User
from .models import ChecklistItem, Task, Workspace, Board, Card, CardList



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
        
        

class CardForm(forms.ModelForm):
    checklist = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Card
        fields = ['name', 'description', 'due_date', 'checklist', 'assigned_to']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        workspace = kwargs.pop('workspace', None)
        super(CardForm, self).__init__(*args, **kwargs)
        if workspace:
            # Filter the queryset for the assigned_to field
            self.fields['assigned_to'].queryset = workspace.members.all()
    

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['description', 'is_completed']
        

class CardlistForm(forms.ModelForm):
    class Meta:
        model = CardList
        fields = ['name', 'max_cards']  # Include any other fields as necessary


