from django.urls import path
from knox import views as knox_views

from user import views

urlpatterns = [
    path('', views.api_root),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
]
