from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ForumThread(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Make a many to many relationship for multiple topics
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=2000) #Limit?
    datetime_created = models.DateTimeField(default=timezone.now, editable=False)
    datetime_edited = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    # Adds new attributes to model
    def sum_count_ratings(self):
        thread_ratings = Rating.objects.filter(thread=self)
        self.thread_ratings_count_positive = sum(i.thumps_up == 1 for i in thread_ratings)  # 1 is true
        self.thread_ratings_count_negative = sum(i.thumps_up == 0 for i in thread_ratings)  # 0 is false


class Comment(models.Model):
    content = models.TextField(max_length=2000) #Limit?
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, null=True)
    datetime_created = models.DateTimeField(default=timezone.now, editable=False)
    datetime_edited = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None) #Remove default?
    #Can a comment be commented on?
    # File upload PDF, other

    def __str__(self):
        return self.content

    # Adds new attributes to model
    def sum_count_ratings(self):
        comment_ratings = Rating.objects.filter(comment=self)
        self.comment_ratings_count_positive = sum(i.thumps_up == 1 for i in comment_ratings)
        self.comment_ratings_count_negative = sum(i.thumps_up == 0 for i in comment_ratings)


class Rating(models.Model):
    # likes = models.IntegerField()  # Alternative to thumps_up
    # dislikes = models.IntegerField()  # Alternative to thumps_up
    thumps_up = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, null=True)  # thread or comment can be rated
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)  # thread or comment can be rated

    def __str__(self):
        return str(self.thumps_up)

    # Method is not used, but the intention was to make code shorter and move code away from views
    def make_rating(self, current_user, clicked_comment_or_thread, the_type):
        find_rating = None
        if the_type == 'comment':
            find_rating = Rating.objects.filter(user=current_user,
                                                comment=clicked_comment_or_thread)  # Get rating from DB
        elif the_type == 'thread':
            find_rating = Rating.objects.filter(user=current_user,
                                                thread=clicked_comment_or_thread)  # Get rating from DB

        if len(find_rating) == 0:  # To ensure a user can only like or dislike a comment once.
            self.user = current_user
            if the_type == 'comment':
                self.comment = clicked_comment_or_thread
            elif the_type == 'thread':
                self.thread = clicked_comment_or_thread
            self.save()
        else:
            old_rating = find_rating[0]  # find_rating is a list?? with only one item, so index 0 is that item.
            if old_rating.thumps_up != self.thumps_up:  # NEW prevents unnecessary save()
                old_rating.thumps_up = self.thumps_up
                old_rating.save()