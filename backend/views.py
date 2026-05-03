from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task, Project, Category, Comment
from .serializers import (
    TaskSerializer,
    ProjectSerializer,
    CategorySerializer,
    CommentSerializer
)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(project__owner=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Comment.objects.filter(task__project__owner=self.request.user)