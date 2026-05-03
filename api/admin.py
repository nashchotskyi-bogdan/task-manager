from django.contrib import admin
from .models import Task, Project, Category, Comment

admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Comment)