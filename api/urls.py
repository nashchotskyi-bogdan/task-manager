from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ProjectViewSet, CategoryViewSet, CommentViewSet
router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"comments", CommentViewSet, basename="comments")
urlpatterns = router.urls