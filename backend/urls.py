from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# pages
def login_page(request):
    return render(request, "login.html")

def app_page(request):
    return render(request, "index.html")


urlpatterns = [
    # pages
    path("", login_page, name="login"),
    path("app/", app_page, name="app"),

    # admin
    path("admin/", admin.site.urls),

    # api
    path("api/", include("api.urls")),

    # jwt auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # google/apple auth
    path("accounts/", include("allauth.urls")),
]