from django.shortcuts import render, get_list_or_404
from django.db import models
from .models import ForumThread

def index(request):
    #Get threads from DB
    # data = ForumThread.objects.all()
    data = get_list_or_404(ForumThread)
    context = {
        'data': data
    }
    return render(request, 'forum/index.html', context)


def login(request):
    pass