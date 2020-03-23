from django.contrib import admin
from .models import Project, Task


class ProjectTasksInline(admin.TabularInline):
    model = Project.tasks.through
    verbose_name = 'task'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    exclude = ['tasks']
    inlines = [ProjectTasksInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass