from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<str:pk>', views.go, name='go'),
    path('delete/', views.delete,name='delete')
]