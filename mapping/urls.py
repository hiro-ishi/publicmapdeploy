from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map_mainview/', views.map_mainview, name='map_mainview'),
    path('help/', views.map_help, name='map_help'),
    path('post/add/', views.post_add, name='post_add'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
]
