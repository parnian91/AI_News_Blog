from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('<int:pk>/edit/', views.edit_news, name='edit_news'),
    path('<int:pk>/delete/', views.delete_news, name='delete_news'),
    path('add/', views.add_news, name='add_news'),
]