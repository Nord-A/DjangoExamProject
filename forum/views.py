from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db import models
from .models import ForumThread #, ForumUser
from .forms import ThreadForm
from django.http import HttpResponseRedirect
from django.utils import timezone
from users.models import User
from django.forms.models import model_to_dict


def index(request):
    #Get threads from DB
    data = ForumThread.objects.order_by("-datetime_created")[:10]  # Get 10 newest posts, sort by date descending
    # data = get_list_or_404(ForumThread)
    context = {
        'data': data
    }
    return render(request, 'forum/index.html', context)


# def login(request):
#     pass


#Look into class based views?
# def create_thread_get(request):
#     form = ThreadForm()
#     return render(request, 'forum/newthread.html', {'form': form})
#
#
# def create_thread_post(request):
#     form = ThreadForm(request.POST)
#     if form.is_valid():
#         text = form.cleaned_data
#         print(text)
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            # clean_form = form.cleaned_data
            # new_thread = form.save()  # Save to DB

            #Trying to save with logged in user
            # current_user = request.user  # Get current logged in user
            # if current_user.is_authenticated():
            # current_user = ForumUser.objects.all()[0]  # Test user, remove after django user has been implemented
            current_user = User.objects.all()[0]  # Test user, remove after django user has been implemented
            # Attempt 1
            new_thread = form.save(commit=False)  # returns object, does not save
            new_thread.owner = current_user
            new_thread.save()  # Save to DB

            # Attempt 2
            # form.instance.user = request.user
            # form.save()
        return HttpResponseRedirect('/index')  # Make successpage? FIX Redirect path. redirect to the thread page?
    else:
        form = ThreadForm()
        return render(request, 'forum/newthread.html', {'form': form})


def edit_thread(request, forum_thread_id):
    if request.method == 'POST':
        old_thread = ForumThread.objects.get(pk=forum_thread_id)  # Get ForumThread from DB
        old_thread.datetime_edited = timezone.now()  # remove or keep?
        updated_thread = ThreadForm(request.POST, instance=old_thread)  # Reuse ThreadForm or make new one?
        if updated_thread.is_valid():
            # updated_thread.save()  # Update ForumThread in DB

            # Alternative to updating datetime_edited
            updated_thread_withdate = updated_thread.save(commit=False)  # returns object, does not save
            updated_thread_withdate.datetime_edited = timezone.now()
            updated_thread_withdate.save()

            # Alternative to updating datetime_edited
            # title = updated_thread.cleaned_data['title']
            # topic = updated_thread.cleaned_data['topic']
            # question = updated_thread.cleaned_data['question']
            # the_thread = ForumThread(title=title, topic=topic, question=question, datetime_edited=timezone.now())
            # the_thread.save()
        return HttpResponseRedirect('index')  # Make successpage? FIX Redirect path
    else:
        thread = get_object_or_404(ForumThread, pk=forum_thread_id)
        # form = ThreadForm()
        form = ThreadForm(initial=model_to_dict(thread)) #Remove model_to_dict?
        return render(request, 'forum/newthread.html', {'form': form})  # Reuse HTML page or make new one?


def view_thread(request, forum_thread_id):
    thread = get_object_or_404(ForumThread, pk=forum_thread_id)
    thread.views_count += 1
    thread.save()
    return render(request, 'forum/thread.html', {'thread': thread})


def view_all_threads(request):
    # Get threads from DB
    data = get_list_or_404(ForumThread)
    context = {
        'data': data
    }
    return render(request, 'forum/allthreads.html', context)