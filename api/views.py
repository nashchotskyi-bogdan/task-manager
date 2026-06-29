from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
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
from django.utils import timezone
from datetime import timedelta
import re


# auth

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


# admin_api

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_stats(request):
    """Статистика для адмін-панелі"""
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    # "Logged in" = last_login within last 15 minutes
    recent_threshold = timezone.now() - timedelta(minutes=15)
    logged_in_users = User.objects.filter(last_login__gte=recent_threshold).count()

    return Response({
        "total_users": total_users,
        "active_users": active_users,
        "logged_in_users": logged_in_users,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_users_list(request):
    """Список користувачів з пошуком та сортуванням"""
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")

    search = request.query_params.get("search", "").strip()
    sort_by = request.query_params.get("sort", "username")
    order = request.query_params.get("order", "asc")
    users = User.objects.all()
    # Пошук по username, email, first_name, last_name
    if search:
        users = users.filter(
            models.Q(username__icontains=search) |
            models.Q(email__icontains=search) |
            models.Q(first_name__icontains=search) |
            models.Q(last_name__icontains=search)
        )

    # Сортування
    allowed_sorts = ["username", "email", "date_joined", "last_login", "is_active"]
    if sort_by not in allowed_sorts:
        sort_by = "username"
    if order == "desc":
        sort_by = f"-{sort_by}"
    users = users.order_by(sort_by)
    data = []
    for u in users:
        data.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "is_active": u.is_active,
            "is_staff": u.is_staff,
            "date_joined": u.date_joined.isoformat(),
            "last_login": u.last_login.isoformat() if u.last_login else None,
        })

    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def admin_user_delete(request, user_id):
    """Видалення користувача (тільки POST)"""
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    # Заборона видаляти самого себе
    if user == request.user:
        return Response({"detail": "Cannot delete yourself"}, status=400)

    username = user.username
    user.delete()
    return Response({"detail": f"User '{username}' deleted"})

class BaseAuthViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ProjectViewSet(BaseAuthViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryViewSet(BaseAuthViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(BaseAuthViewSet):
    serializer_class = TaskSerializer

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


class CommentViewSet(BaseAuthViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            task__project__owner=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save()