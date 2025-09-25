from django.contrib import admin
from django.urls import path
from . import views

app_name = 'aplicacion'

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login_view, name='login'),
]