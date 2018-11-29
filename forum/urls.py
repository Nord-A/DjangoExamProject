from django.urls import path
from . import views

# app_name = 'forum' #Add namespace
urlpatterns = [
    path('', views.index, name='forum-index'),
    path('login/', views.login, name='forum-login'),
]