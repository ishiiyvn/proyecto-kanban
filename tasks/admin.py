from django.contrib import admin
from .models import Task, Workspace, Board, Card, CardList, ChecklistItem

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    filter_horizontal = ('members',)

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name','workspace')


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'card_list', 'assigned_to')
    search_fields = ('name', 'description')
    list_filter = ('card_list', 'assigned_to', 'created')


class CardListAdmin(admin.ModelAdmin):
    list_display = ('name', 'board')
    search_fields = ('name',)
    list_filter = ('board',)
    
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'card')  # Show relevant fields
    search_fields = ('description',)
    list_filter = ('is_completed', 'card')  # Filter by completion status and card


# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(CardList, CardListAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)