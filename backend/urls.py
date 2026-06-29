from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# pages

def login_page(request):
    return render(request, "login.html")

def app_page(request):
    return render(request, "index.html")

# admin_pages

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff_user, login_url='/')
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@user_passes_test(is_staff_user, login_url='/')
def admin_users_page(request):
    return render(request, "admin_users.html")

# url_patterns

urlpatterns = [
    # pages
    path("", login_page, name="login"),
    path("app/", app_page, name="app"),

    # django_admin 
    path("django-admin/", admin.site.urls),

    # custom_admin_panel
    path("admin/", admin_dashboard, name="admin_dashboard"),
    path("admin/users/", admin_users_page, name="admin_users"),

    # API
    path("api/", include("api.urls")),

    # JWT_auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Google/Apple_auth
    path("accounts/", include("allauth.urls")),
]