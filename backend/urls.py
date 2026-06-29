from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet,
    ProjectViewSet,
    CategoryViewSet,
    CommentViewSet,
    register,
    admin_stats,
    admin_users_list,
    admin_user_delete,
)

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = router.urls + [
    path("register/", register),
    
    # Admin API endpoints
    path("admin/stats/", admin_stats, name="admin_stats"),
    path("admin/users/", admin_users_list, name="admin_users_list"),
    path("admin/users/<int:user_id>/delete/", admin_user_delete, name="admin_user_delete"),
]

handler404 = "your_app.views.custom_404"