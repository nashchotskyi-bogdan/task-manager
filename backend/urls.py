from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.shortcuts import render

def login_page(request):
    return render(request, "login.html")

def app_page(request):
    return render(request, "index.html")

urlpatterns = [
    path('', login_page),
    path('app/', app_page),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]