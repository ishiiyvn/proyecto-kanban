from django.contrib import admin
from .models import Task, Workspace

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    filter_horizontal = ('members',)

# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Workspace, WorkspaceAdmin)