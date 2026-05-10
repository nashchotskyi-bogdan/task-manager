from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task, Project, Category, Comment
from .serializers import TaskSerializer, ProjectSerializer, CategorySerializer, CommentSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    if not username or not email or not password:
        return Response({"detail": "All fields are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"detail": "Username already exists"}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({"detail": "Email already exists"}, status=400)
    user = User.objects.create_user(username=username, email=email, password=password)
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
        return Task.objects.filter(project__owner=self.request.user)
    def perform_create(self, serializer):
        project = serializer.validated_data.get("project")
        category = serializer.validated_data.get("category")
        if project and project.owner != self.request.user:
            raise PermissionError("Invalid project")
        if category and category.owner != self.request.user:
            raise PermissionError("Invalid category")
        serializer.save()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Comment.objects.filter(task__project__owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save()