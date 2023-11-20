from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('create', views.create, name='create'),
    path('delete/', views.delete,name='delete'),
    path('extend_validity', views.extend_validity, name='extend_validity'),
    path('<str:pk>', views.go, name='go'),
]