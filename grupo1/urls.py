"""
URL configuration for grupo1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('workspaces/', views.workspaces, name='workspaces'),
    path('workspaces/create/', views.create_workspace, name='create_workspace'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/update/', views.update_workspace, name='update_workspace'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/delete/', views.delete_workspace, name='delete_workspace'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/', views.boards, name='boards'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/create', views.create_board, name='create_board'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/<int:board_id>/update/', views.update_board, name='update_board'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/<int:board_id>/delete/', views.delete_board, name='delete_board'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/<int:board_id>/', views.view_board, name='view_board'), 
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/<int:board_id>/stats', views.stats, name='stats'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/<int:board_id>/cardlists/create/', views.create_cardlist, name='create_cardlist'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/<int:board_id>/cardlists/<int:cardlist_id>/', views.update_cardlist, name='update_cardlist'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/<int:board_id>/cardlists/<int:cardlist_id>/delete/', views.delete_cardlist, name='delete_cardlist'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/<int:board_id>/cards/<int:card_id>/update/', views.update_card, name='update_card'),
    path('workspaces/<int:owner_id>/<int:workspace_id>/boards/<int:board_id>/cards/<int:card_id>/delete/', views.delete_card, name='delete_card'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('tags/', views.tags, name='tags'),  # Ruta para listar todas las etiquetas
    path('tags/create/', views.create_tag, name='create_tag'),  # Ruta para crear una etiqueta
    path('tags/<int:tag_id>/', views.filter_by_tag, name='filter_by_tag'),  # Ruta para filtrar tarjetas por etiqueta
    path('update_card_position/<int:card_id>/cardlist/<int:cardlist_id>/', views.update_card_position, name='update_card_position'),
    
]
