from django.urls import path
from . import views

# app_name = 'forum' #Add namespace
urlpatterns = [
    # localhost:8000/ || localhost:8000/index
    path('', views.index, name='forum-index'),

    # localhost:8000/forum/createthread || localhost:8000/createthread
    path('createthread/', views.create_thread, name='forum-createthread'),

    # localhost:8000/forum/id || localhost:8000/forum/thread/id???
    path('thread/<int:forum_thread_id>/', views.view_thread, name='forum-viewthread'),

    # localhost:8000/forum/allthreads
    path('allthreads/', views.view_all_threads, name='forum-viewallthreads'), #, views.ThreadsList.as_view()

    # localhost:8000/forum/editthread || localhost:8000/editthread
    path('editthread/<int:forum_thread_id>', views.edit_thread, name='forum-editthread'),

    path('viewownthreads/', views.view_own_threads, name='forum-viewownthreads'),
]