from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from .models import Task, Project, Category, Comment
from .serializers import (
    TaskSerializer,
    ProjectSerializer,
    CategorySerializer,
    CommentSerializer
)
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    if not username or not email or not password:
        return Response({"detail": "All fields required"}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return Response(
            {"detail": "Це не є пошта. Введіть наново свою пошту."},
            status=400
        )
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
    if not re.match(password_regex, password):
        return Response(
            {"detail": "Придумайте складніший пароль."},
            status=400
        )
    if User.objects.filter(username=username).exists():
        return Response({"detail": "Username exists"}, status=400)
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Task.objects.filter(
            models.Q(project__owner=self.request.user) |
            models.Q(category__owner=self.request.user)
        )
    def get_serializer_context(self):
        return {"request": self.request}
    def perform_create(self, serializer):
        project = serializer.validated_data.get("project")
        category = serializer.validated_data.get("category")
        if project and project.owner != self.request.user:
            raise PermissionDenied("Invalid project")
        if category and category.owner != self.request.user:
            raise PermissionDenied("Invalid category")
        serializer.save()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Comment.objects.filter(task__project__owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save()