from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# логін сторінка
def home(request):
    return render(request, "login.html")
# сторінка після логіну 
def index(request):
    return render(request, "index.html")

urlpatterns = [
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]