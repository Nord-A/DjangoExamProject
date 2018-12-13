from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, render_to_response
from django.db import models
from .models import ForumThread, Comment, Rating
from .forms import ThreadForm, CommentForm
from django.http import HttpResponseRedirect
from django.utils import timezone
from users.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponseForbidden
from django.views.generic.list import ListView


def index(request):
    # Get threads from DB
    data = ForumThread.objects.order_by("-datetime_created")[:10]  # Get 10 newest threads, sort by date descending

    context = {
        'data': data
    }
    return render(request, 'forum/index.html', context)


def create_thread(request):
    current_user = request.user  # Get current logged in user

    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            #Trying to save with logged in user
            new_thread = form.save(commit=False)  # returns object, does not save
            new_thread.owner = current_user
            new_thread.save()  # Save to DB

            return HttpResponseRedirect('/thread/{}'.format(new_thread.id))  # Make successpage?
    if current_user.is_authenticated:
        form = ThreadForm()
        return render(request, 'forum/newthread.html', {'form': form})
    else:
        return redirect('login')


def edit_thread(request, forum_thread_id):
    if request.method == 'POST':
        old_thread = ForumThread.objects.get(pk=forum_thread_id)  # Get ForumThread from DB
        # old_thread.datetime_edited = timezone.now()
        updated_thread = ThreadForm(request.POST, instance=old_thread)
        if updated_thread.is_valid():
            # First approach
            # updated_thread.save()  # Update ForumThread in DB. Overload save method for this approach to work?

            # Alternative to updating datetime_edited
            updated_thread_withdate = updated_thread.save(commit=False)  # returns object, does not save
            updated_thread_withdate.datetime_edited = timezone.now()
            updated_thread_withdate.save()
        return HttpResponseRedirect('/thread/{}'.format(updated_thread_withdate.id))  # Make successpage?
    else:
        thread = get_object_or_404(ForumThread, pk=forum_thread_id)
        # form = ThreadForm()
        form = ThreadForm(initial=model_to_dict(thread))  # Model is converted to dict and passed to form?

        current_user = request.user  # Get current logged in user
        if current_user.is_authenticated:
            if current_user == thread.owner:
                return render(request, 'forum/newthread.html', {'form': form})  # Reuse HTML page or make new one?
            else:
                return HttpResponseForbidden()
        else:
            return redirect('login')


def view_thread(request, forum_thread_id):
    # Get currentuser here instead and if current_user.is_authenticated: to shorten code.
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
                # find_rating = Rating.objects.get(user=current_user, thread=thread)
                # Rewrite as method in rating model because of almost duplicate code?
                # To ensure a user can only like or dislike a thread once.
                if len(find_rating) == 0:  # If user has no rating on the thread
                    the_rating.user = current_user
                    the_rating.thread = thread
                    the_rating.save()
                else:
                    old_rating = find_rating[0]  # find_rating is a list?? with only one item, so index 0 is that item.
                    if old_rating.thumps_up != the_rating.thumps_up: #prevents unnecessary save()
                        old_rating.thumps_up = the_rating.thumps_up
                        old_rating.save()

            elif 'comment_rating_like' in request.POST or 'comment_rating_dislike' in request.POST:
                the_rating = Rating()
                if 'comment_rating_like' in request.POST:
                    the_rating.thumps_up = True
                else:
                    the_rating.thumps_up = False

                clicked_comment = Comment.objects.get(id=request.POST.__getitem__('comment_id'))  # Get comment from DB
                find_rating = Rating.objects.filter(user=current_user, comment=clicked_comment)  # Get rating from DB
                # find_rating = Rating.objects.get(user=current_user, comment=clicked_comment)  # Get rating from DB
                # Rewrite as method in rating model because of almost duplicate code?
                # To ensure a user can only like or dislike a comment once.
                if len(find_rating) == 0:  # If user has no rating on the comment
                    the_rating.user = current_user
                    the_rating.comment = clicked_comment
                    the_rating.save()
                else:
                    old_rating = find_rating[0]  # find_rating is a list?? with only one item, so index 0 is that item.
                    if old_rating.thumps_up != the_rating.thumps_up:  # prevents unnecessary save()
                        old_rating.thumps_up = the_rating.thumps_up
                        old_rating.save()

        else:  # If user is not logged in, redirect to login page
            return redirect('login')
    thread = get_object_or_404(ForumThread, pk=forum_thread_id)  # Get thread from DB
    thread.views_count += 1
    thread.save()

    comments = Comment.objects.order_by("datetime_created").filter(thread=thread)  # Get comments from DB
    # To get the total amount of likes/dislikes for all comments on the current thread
    for c in comments:
        c.sum_count_ratings()  # Using method to add attributes to the object

        # To show if user has clicked on like or dislike button (comments)
        current_user = request.user
        if current_user.is_authenticated:
            find_rating = Rating.objects.filter(user=current_user, comment=c)  # length is 0 or 1. use get instead?
            # find_rating = Rating.objects.get(user=current_user, comment=c)
            c.current_comment_rating = 'none'
            if len(find_rating) != 0:  # Rewrite as method in rating model because of almost duplicate code?
                if find_rating[0].thumps_up:
                    c.current_comment_rating = 'positive'
                else:
                    c.current_comment_rating = 'negative'

    # # To get the total amount of likes/dislikes for the current thread
    thread.sum_count_ratings()  # Using method to add attributes to the object

    # To show if user has clicked on like or dislike button (forumthreads)
    current_thread_rating = 'none'
    current_user = request.user  # Get current logged in user
    if current_user.is_authenticated:
        find_rating = Rating.objects.filter(user=current_user, thread=thread)
        if len(find_rating) != 0:  # Rewrite as method in rating model because of almost duplicate code?
            if find_rating[0].thumps_up:
                current_thread_rating = 'positive'
            else:
                current_thread_rating = 'negative'

    # context = make the dictionary here and pass to render method instead?
    form = CommentForm()
    return render(request, 'forum/thread.html', {'thread': thread, 'comments': comments,
                                                 'form': form, 'current_thread_rating': current_thread_rating})


def view_all_threads(request):
    data = get_list_or_404(ForumThread)  # Get threads from DB

    # This is for displaying the ratings
    for thread in data:
        thread.sum_count_ratings()  # Using method to add attributes to the object

    context = {
        'data': data
    }
    return render(request, 'forum/allthreads.html', context)


def view_own_threads(request):
    current_user = request.user  # Get current logged in user
    if current_user.is_authenticated:
        data = ForumThread.objects.filter(owner=current_user)  # Get threads from DB

        # This is for displaying the ratings
        for thread in data:
            thread.sum_count_ratings()  # Using method to add attributes to the object

        context = {
            'data': data
        }
        return render(request, 'forum/ownthreads.html', context)
    else:
        return redirect('login')


# Example of ListView. This requires forumthread_list.html and the model ForumThread. Method is not used
class ThreadsList(ListView):
    model = ForumThread
    # paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# Example of error handler
# def handler404(request, exception, template_name="forum/404.html"):
#     response = render_to_response("forum/404.html")
#     response.status_code = 404
#     return response

