from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, WorkspaceForm, BoardForm, CardForm, CardlistForm
from .models import Board, ChecklistItem, Task, Workspace, CardList, Card
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })
       

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html', {
            'form': AuthenticationForm
        })
    else:
        print(request)
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('workspaces')


def signout(request):
    logout(request)
    return redirect('home')


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks' : tasks})


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'tasks.html', {'tasks' : tasks})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form' : TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form' : TaskForm,
                'error' : 'Please provide valid data'
            })
            

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task' : task, 'form' : form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task' : task,
                'form' : form,
                'error' : "Error updating task"
            })
        

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    

@login_required            
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def workspaces(request):
    workspaces = Workspace.objects.filter(owner=request.user)
    return render(request, 'workspaces.html', {'workspaces' : workspaces})


@login_required
def create_workspace(request):
    if request.method == 'GET':
        return render(request, 'create_workspace.html', {
            'form' : WorkspaceForm
        })
    else:
        try:
            form = WorkspaceForm(request.POST)
            new_workspace = form.save(commit=False)
            new_workspace.owner = request.user
            new_workspace.save()
            form.save_m2m()
            print(new_workspace)
            return redirect('workspaces')
        except ValueError:
            return render(request, 'create_workspace.html', {
                'form' : WorkspaceForm,
                'error' : 'Please provide valid data'
            })


@login_required
def update_workspace(request, owner_id, workspace_id):
    if request.user.id != owner_id:
        return HttpResponseForbidden('You are not allowed to edit this workspace.')
    
    workspace = get_object_or_404(Workspace, pk=workspace_id, owner=request.user)
    
    if request.method == 'GET':
        form = WorkspaceForm(instance=workspace)
        return render(request, 'update_workspace.html', {
            'form': form,
            'workspace': workspace
        })
    else:
        try:
            form = WorkspaceForm(request.POST, instance=workspace)
            form.save()
            return redirect('workspaces')
        except ValueError:
            return render(request, 'update_workspace.html', {
                'form': form,
                'workspace': workspace,
                'error': 'Please provide valid data'
            })


@login_required
def delete_workspace(request, owner_id, workspace_id):
    # Ensure the logged-in user matches the owner_id
    if request.user.id != owner_id:
        return HttpResponseForbidden('You are not allowed to delete this workspace.')

    workspace = get_object_or_404(Workspace, pk=workspace_id, owner_id=owner_id)

    if request.method == 'POST':
        workspace.delete()
        return redirect('workspaces')

    return render(request, 'delete_workspace.html', {
        'workspace': workspace
    })


@login_required
def boards(request, owner_id, workspace_id):
    if request.user.id != owner_id:
        return HttpResponseForbidden('You are not allowed to edit this workspace.')
    
    workspace = get_object_or_404(Workspace, pk=workspace_id)
    
    boards = Board.objects.filter(workspace=workspace)
    
    return render(request, 'boards.html', {
        'boards' : boards,
        'workspace' : workspace
    })


@login_required
def view_board(request, owner_id, workspace_id, board_id):
    board = get_object_or_404(Board, pk=board_id)

    card_lists = board.card_lists.all()
    workspace = board.workspace

    if request.method == 'POST':
        form = CardForm(request.POST)
        card_list_id = request.POST.get('card_list_id')
        card_list = get_object_or_404(CardList, pk=card_list_id)
        
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.card_list = card_list
            new_card.due_date = form.cleaned_data.get('due_date')  # Assign the due date
            new_card.assigned_to = form.cleaned_data.get('assigned_to')  # Assign the user based on form data
            new_card.save()
            new_checklist_item_description = request.POST.get('new_checklist_item')
            if new_checklist_item_description:
                ChecklistItem.objects.create(card=new_card, description=new_checklist_item_description)
            print(f"Card created with due date: {new_card.due_date}")  # Debugging line
            return redirect('view_board', owner_id=owner_id, workspace_id=workspace_id, board_id=board.id)    
    else:
        form = CardForm(workspace=workspace)
        
    return render(request, 'view_board.html', {
        'board': board,
        'card_lists': card_lists,
        'form': form,
        'owner_id': owner_id,
        'workspace_id': workspace_id
    })


@login_required
def create_board(request, owner_id, workspace_id):

    workspace = get_object_or_404(Workspace, pk=workspace_id)

    if request.method == 'GET':
        return render(request, 'create_board.html', {
            'form' : BoardForm,
            'owner_id' : owner_id,
            'workspace_id':workspace_id
        })
    else:
        try:
            form = BoardForm(request.POST)
            new_board = form.save(commit=False)
            new_board.workspace=workspace
            new_board.save()
            
            default_card_lists = ["TODO", "DOING", "READY"]
            for list_name in default_card_lists:
                CardList.objects.create(name=list_name, board=new_board)
                
            print(new_board)
            return redirect('boards', owner_id=workspace.owner.id, workspace_id=workspace.id)
        except ValueError:
            return render(request, 'create_board.html', {
                'form' : BoardForm,
                'error' : 'Please provide valid data'
            })


@login_required
def update_board(request, owner_id, workspace_id, board_id):
    workspace = get_object_or_404(Workspace, pk=workspace_id, owner_id=owner_id)
    board = get_object_or_404(Board, pk=board_id, workspace=workspace)

    if request.method == 'GET':
        form = BoardForm(instance=board)
        return render(request, 'update_board.html', {
            'form': form,
            'owner_id': owner_id,
            'workspace_id': workspace_id,
            'board_id': board_id
        })
    else:
        try:
            form = BoardForm(request.POST, instance=board)
            form.save()
            return redirect('view_board', owner_id=owner_id, workspace_id=workspace_id, board_id=board_id)
        except ValueError:
            return render(request, 'update_board.html', {
                'form': form,
                'error': 'Please provide valid data',
                'owner_id': owner_id,
                'workspace_id': workspace_id,
                'board_id': board_id
            })


@login_required
def delete_board(request, owner_id, workspace_id, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        board.delete()
        return redirect('boards', owner_id=owner_id, workspace_id=workspace_id)

    return render(request, 'delete_board.html', {'board': board})


@login_required
def create_cardlist(request, owner_id, workspace_id, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        form = CardlistForm(request.POST)
        if form.is_valid():
            card_list = form.save(commit=False)
            card_list.board = board  # Set the board for the new card list
            card_list.save()
            return redirect('view_board', owner_id=owner_id, workspace_id=workspace_id, board_id=board_id)

    # Handle the case where the form is not valid, you can add error messages as needed
    return redirect('view_board', owner_id=owner_id, workspace_id=workspace_id, board_id=board_id)



@login_required
def update_card(request, owner_id, workspace_id, board_id, card_id):
    card = get_object_or_404(Card, pk=card_id)
    workspace = card.card_list.board.workspace  # Get the workspace associated with the board
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            updated_card = form.save()

            # Handle checklist items
            checklist_item_ids = request.POST.getlist('checklist_item_ids')  # IDs of the items being updated
            for item_id in card.checklist_items.values_list('id', flat=True):
                # Get the new description from the form
                new_description = request.POST.get(f'checklist_item_{item_id}')
                checklist_item = ChecklistItem.objects.get(id=item_id)
                checklist_item.is_completed = str(item_id) in checklist_item_ids
                checklist_item.description = new_description  # Update the description
                checklist_item.save()

            # Handle new checklist item addition
            new_checklist_item_descriptions = request.POST.getlist('checklist_item_new')  # Get new checklist items
            for new_description in new_checklist_item_descriptions:
                if new_description:  # Only create if the description is not empty
                    ChecklistItem.objects.create(card=updated_card, description=new_description)

            return redirect('view_board', owner_id=owner_id, workspace_id=workspace_id, board_id=board_id)

    else:
        form = CardForm(instance=card, workspace=workspace)

    return render(request, 'update_card.html', {
        'form': form,
        'card': card,
        'checklist_items': card.checklist_items.all(),  # Pass existing checklist items to the template
        'owner_id': owner_id,
        'workspace_id': workspace_id,
        'board_id': board_id
    })


@login_required
def delete_card(request, owner_id, workspace_id, board_id, card_id):
    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'POST':
        card.delete()  # Delete the card
        return redirect('view_board', owner_id=owner_id, workspace_id=workspace_id, board_id=board_id)

    return render(request, 'delete_card.html', {
        'card': card,
        'owner_id': owner_id,
        'workspace_id': workspace_id,
        'board_id': board_id
    })






@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form' : TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form' : TaskForm,
                'error' : 'Please provide valid data'
            })
 