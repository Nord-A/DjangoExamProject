from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.db import models
from .models import ForumThread, Comment, Rating #, ForumUser
from .forms import ThreadForm, CommentForm
from django.http import HttpResponseRedirect
from django.utils import timezone
from users.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.views.generic.list import ListView


def index(request):
    #Get threads from DB
    data = ForumThread.objects.order_by("-datetime_created")[:10]  # Get 10 newest threads, sort by date descending
    # data = get_list_or_404(ForumThread)
    context = {
        'data': data
    }
    return render(request, 'forum/index.html', context)


#Look into class based views?
def create_thread(request):
    current_user = request.user  # Get current logged in user

    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            # clean_form = form.cleaned_data
            # new_thread = form.save()  # Save to DB

            #Trying to save with logged in user
            new_thread = form.save(commit=False)  # returns object, does not save
            new_thread.owner = current_user
            new_thread.save()  # Save to DB
        return HttpResponseRedirect('/thread/{}'.format(new_thread.id))  # Make successpage?
    else:
        if current_user.is_authenticated:
            form = ThreadForm()
            return render(request, 'forum/newthread.html', {'form': form})
        else:
            return redirect('login')


def edit_thread(request, forum_thread_id):
    if request.method == 'POST':
        old_thread = ForumThread.objects.get(pk=forum_thread_id)  # Get ForumThread from DB
        old_thread.datetime_edited = timezone.now()  # remove or keep?
        updated_thread = ThreadForm(request.POST, instance=old_thread)  # Reuse ThreadForm or make new one?
        if updated_thread.is_valid():
            # updated_thread.save()  # Update ForumThread in DB. Overload save method for this approach to work?

            # Alternative to updating datetime_edited
            updated_thread_withdate = updated_thread.save(commit=False)  # returns object, does not save
            updated_thread_withdate.datetime_edited = timezone.now()
            updated_thread_withdate.save()
        return HttpResponseRedirect('/thread/{}'.format(updated_thread_withdate.id))  # Make successpage?
    else:
        thread = get_object_or_404(ForumThread, pk=forum_thread_id)
        # form = ThreadForm()
        form = ThreadForm(initial=model_to_dict(thread)) #Remove model_to_dict?

        current_user = request.user  # Get current logged in user
        if current_user.is_authenticated:
            if current_user == thread.owner:
                return render(request, 'forum/newthread.html', {'form': form})  # Reuse HTML page or make new one?
            else:
                return HttpResponseForbidden()
        else:
            return redirect('login')


def view_thread(request, forum_thread_id):
    #Get currentuser here instead and if current_user.is_authenticated: to shorten code.
    if request.method == 'POST':
        current_user = request.user  # Get current logged in user
        if current_user.is_authenticated:
            thread = get_object_or_404(ForumThread, pk=forum_thread_id)  # Get thread from DB

            if 'comment_submit' in request.POST:
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.owner = current_user
                    comment.thread = thread
                    comment.save()
            elif 'thread_rating_like' in request.POST or 'thread_rating_dislike' in request.POST:
                the_rating = Rating()
                if 'thread_rating_like' in request.POST:
                    the_rating.thumps_up = True
                else:
                    the_rating.thumps_up = False
                find_rating = Rating.objects.filter(user=current_user, thread=thread)
                if len(find_rating) == 0:  # To ensure a user can only like or dislike a thread once.
                    the_rating.user = current_user
                    the_rating.thread = thread
                    the_rating.save()
                else:
                    old_rating = find_rating[0]
                    old_rating.thumps_up = the_rating.thumps_up
                    old_rating.save()

            #Make elif here if ratings on comments is implemented?
        else:  # If user is not logged in, redirect to login page
            return redirect('login')
        # if 'comment_submit' in request.POST:
        #     form = CommentForm(request.POST)
        #     if form.is_valid():
        #         thread = get_object_or_404(ForumThread, pk=forum_thread_id)
        #         current_user = request.user  # Get current logged in user
        #         if current_user.is_authenticated:
        #             comment = form.save(commit=False)
        #             comment.owner = current_user
        #             comment.thread = thread
        #             comment.save()
        #         else:
        #             return redirect('login')
        # elif 'thread_rating_like' in request.POST or 'thread_rating_dislike' in request.POST:
        #     the_rating = Rating()
        #     if 'thread_rating_like' in request.POST:
        #         the_rating.thumps_up = True
        #     else:
        #         the_rating.thumps_up = False
        #     current_user = request.user  # Get current logged in user
        #     if current_user.is_authenticated:
        #         #NEW
        #         thread = get_object_or_404(ForumThread, pk=forum_thread_id)
        #         find_rating = Rating.objects.filter(user=current_user, thread=thread)
        #         if find_rating == None:  # To ensure a user can only like or dislike a thread once.
        #             the_rating.user = current_user
        #             the_rating.thread = thread
        #             the_rating.save()
        #     else:
        #         return redirect('login')
    # else:
    thread = get_object_or_404(ForumThread, pk=forum_thread_id)  # Get thread from DB
    thread.views_count += 1
    thread.save()
    comments = Comment.objects.order_by("datetime_created").filter(thread=thread)  # Get comments from DB

    thread_ratings = Rating.objects.filter(thread=thread)  # Get ratings from DB
    thread_ratings_count_positive = sum(i.thumps_up == 1 for i in thread_ratings)
    thread_ratings_count_negative = sum(i.thumps_up == 0 for i in thread_ratings)

    #NEW
    #This is to show if user has clicked on like or dislike button
    current_thread_rating = 'none'
    current_user = request.user  # Get current logged in user
    if current_user.is_authenticated:
        find_rating = Rating.objects.filter(user=current_user, thread=thread)
        if len(find_rating) != 0:
            if find_rating[0].thumps_up:
                current_thread_rating = 'positive'
            else:
                current_thread_rating = 'negative'

    #Ratings on comments missing

    # comment_ratings = Rating.objects.filter(comment=)
    # context = make the dictionary here and pass to render method instead?
    form = CommentForm()
    return render(request, 'forum/thread.html', {'thread': thread, 'comments': comments,
                                                 'thread_ratings_count_positive': thread_ratings_count_positive,
                                                 'thread_ratings_count_negative': thread_ratings_count_negative,
                                                 'form': form, 'current_thread_rating': current_thread_rating})


def view_all_threads(request):
    data = get_list_or_404(ForumThread)  # Get threads from DB

    # Complex task to get all ratings and display with the threads?
    # thread_ratings = Rating.objects.filter(thread=data)
    # thread_ratings_count_positive = sum(i.thumps_up == 1 for i in thread_ratings)
    # thread_ratings_count_negative = sum(i.thumps_up == 0 for i in thread_ratings)

    context = {
        'data': data,
        # 'thread_ratings_count_positive': thread_ratings_count_positive,
        # 'thread_ratings_count_negative': thread_ratings_count_negative,
    }
    return render(request, 'forum/allthreads.html', context)


def view_own_threads(request):
    current_user = request.user  # Get current logged in user
    if current_user.is_authenticated:
        data = ForumThread.objects.filter(owner=current_user)  # Get threads from DB
        context = {
            'data': data
        }
        return render(request, 'forum/ownthreads.html', context)
    else:
        return redirect('login')


#Example of ListView. This requires forumthread_list.html and the model ForumThread. Method is not used
class ThreadsList(ListView):
    model = ForumThread
    # paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context