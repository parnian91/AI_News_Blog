from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('register/', views.custom_register, name='custom_register'),
    path('profile/', views.profile, name='profile'),
]