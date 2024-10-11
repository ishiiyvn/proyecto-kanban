from django.contrib import admin
from .models import Task, Workspace, Board

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    filter_horizontal = ('members',)

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name','workspace')


# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(Board, BoardAdmin)