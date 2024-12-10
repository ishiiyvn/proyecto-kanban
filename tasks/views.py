from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, WorkspaceForm, BoardForm, CardForm, CardlistForm
from .models import Board, ChecklistItem, Task, Workspace, CardList, Card, Tag
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
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
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('workspaces')


def signout(request):
    logout(request)
    return redirect('home')


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    tags = Tag.objects.all()  # Obtener todas las etiquetas
    return render(request, 'tasks.html', {'tasks': tasks, 'tags': tags})


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
    workspaces = Workspace.objects.filter(Q(members=request.user) | Q(owner=request.user)).distinct()
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
    # Verificar que el usuario actual tiene permisos
    if request.user.id != owner_id:
        return HttpResponseForbidden('You are not allowed to edit this workspace.')
    
    # Obtener el workspace o retornar 404 si no existe
    workspace = get_object_or_404(Workspace, pk=workspace_id, owner=request.user)
    
    # Obtener los usuarios disponibles (que no están ya en el workspace)
    available_members = User.objects.exclude(id__in=workspace.members.values_list('id', flat=True))
    
    if request.method == 'GET':
        # Mostrar el formulario de edición con datos existentes
        form = WorkspaceForm(instance=workspace)
        return render(request, 'update_workspace.html', {
            'form': form,
            'workspace': workspace,
            'available_members': available_members
        })
    else:
        try:
            # Crear el formulario con los datos enviados
            form = WorkspaceForm(request.POST, instance=workspace)
            
            if form.is_valid():
                # Guardar los datos básicos del workspace
                workspace = form.save()

                # Obtener los IDs de los miembros seleccionados en el formulario
                selected_members_ids = request.POST.getlist('members')

                # Actualizar los miembros del workspace (remplaza todos los anteriores)
                workspace.members.set(selected_members_ids)
                
                # Redirigir al listado de workspaces
                return redirect('workspaces')
            else:
                # Si los datos no son válidos, mostrar errores
                return render(request, 'update_workspace.html', {
                    'form': form,
                    'workspace': workspace,
                    'available_members': available_members,
                    'error': 'Please provide valid data.'
                })
        except Exception as e:
            # Manejo de errores inesperados
            return render(request, 'update_workspace.html', {
                'form': form,
                'workspace': workspace,
                'available_members': available_members,
                'error': f'An unexpected error occurred: {e}'
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
    #if request.user.id != owner_id:
     #   return HttpResponseForbidden('You are not allowed to edit this workspace.')
    
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
    get_time = timezone.now()
    tags = Tag.objects.all()

    if request.method == 'POST':
        # Capturar datos del formulario
        form = CardForm(request.POST)
        card_list_id = request.POST.get('card_list_id')  # Capturar el ID de la lista a la que se asignará la tarjeta
        card_list = get_object_or_404(CardList, pk=card_list_id)

        if form.is_valid():
            # Si el formulario es válido, crear la tarjeta
            new_card = form.save(commit=False)
            new_card.card_list = card_list
            new_card.due_date = form.cleaned_data.get('due_date')
            new_card.assigned_to = form.cleaned_data.get('assigned_to')
            new_card.save()
            form.save_m2m()  # Guardar las etiquetas (tags)
            
            # Incrementar el contador de tarjetas de la lista
            card_list.increse_amount()
            card_list.save()
            
            return redirect('view_board', owner_id=owner_id, workspace_id=workspace_id, board_id=board.id)
        else:
            print(form.errors)  # Mostrar errores si el formulario no es válido (para depuración)

    else:
        form = CardForm(workspace=workspace)

    # Filtrar tarjetas si hay filtros activos
    filter_tag = request.GET.get('filter_tag')
    assigned_user = request.GET.get('assigned_user')

    for card_list in card_lists:
        cards = card_list.cards.all()
        if filter_tag:
            cards = cards.filter(tags__id=filter_tag)
        if assigned_user:
            cards = cards.filter(assigned_to__id=assigned_user)
        card_list.filtered_cards = cards

    return render(request, 'view_board.html', {
        'board': board,
        'card_lists': card_lists,
        'form': form,
        'tags': tags,
        'owner_id': owner_id,
        'workspace_id': workspace_id,
        'get_time': get_time
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
        print(form)
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
        card_list = get_object_or_404(CardList, pk=card.get_card_list())
        card.delete()
        card_list.decrease_amount()
        card_list.save()
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
        print(form)
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

def update_cardlist(request, owner_id, workspace_id, board_id, card_id, cardlist_id):
    card = get_object_or_404(Card, pk=card_id)
    cardlist = get_object_or_404(CardList, pk=cardlist_id)
    if request.method == 'POST':
        card.card_list = cardlist
        card.save()
        return redirect('view_board', owner_id=owner_id, workspace_id=workspace_id, board_id=board_id)

@login_required
def delete_card(request, owner_id, workspace_id, board_id, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == 'POST':
        card_list = get_object_or_404(CardList, pk=card.get_card_list())
        card.delete()
        card_list.decrease_amount()
        card_list.save()
        return redirect('view_board', owner_id=owner_id, workspace_id=workspace_id, board_id=board_id)

    return render(request, 'delete_card.html', {
        'card': card,
        'owner_id': owner_id,
        'workspace_id': workspace_id,
        'board_id': board_id
    })

@login_required
def stats(request,owner_id,workspace_id, board_id):
    board = get_object_or_404(Board, pk=board_id)

    card_lists= board.card_lists.all()
    card_lists_amounts=[]
    card_lists_names=[]
    get_time=timezone.now()
    overdue_cards_amount=[]
    members=get_object_or_404(Workspace,pk=workspace_id).members.all()
    member_amounts={"Any":0}

    for member in members:
        member_amounts[str(member)]=0

    for card_list in card_lists:
        card_lists_names.append(card_list.name)
        card_lists_amounts.append(card_list.amount_cards)
        aux=0
        for card in card_list.cards.all():
            if card.due_date<get_time:
                aux+=1
            if card.assigned_to:
                member_amounts[str(card.assigned_to)]+=1
            else:
                member_amounts['Any']+=1
            
        overdue_cards_amount.append(aux)

    return render(request,'stats.html',{
        'card_list_names':card_lists_names,
        'card_list_amounts':card_lists_amounts,
        'overdue_cards_amount':overdue_cards_amount,
        'members':list(member_amounts.keys()),
        'member_amounts':list(member_amounts.values())
    })

# Vista para filtrar tarjetas por etiqueta
@login_required
def filter_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    cards = tag.cards.all()
    return render(request, 'filter_by_tag.html', {'tag': tag, 'cards': cards})

# Vista para crear etiquetas
@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tags')  # Redirige a una lista de etiquetas
    else:
        form = TagForm()
    return render(request, 'create_tag.html', {'form': form})

# Vista para listar etiquetas
@login_required
def tags(request):
    tags = Tag.objects.all()
    return render(request, 'tags.html', {'tags': tags})


import logging

logger = logging.getLogger(__name__)



@login_required
def update_card_position(request, card_id, cardlist_id):
    if request.method == 'POST':
        try:
            card = get_object_or_404(Card, pk=card_id)
            cardlist = get_object_or_404(CardList, pk=cardlist_id)
            
            # Actualizar la lista de la tarjeta
            card.card_list = cardlist
            card.save()

            return JsonResponse({'success': True, 'message': 'Card position updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
