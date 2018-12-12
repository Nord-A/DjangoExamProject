from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ForumThread(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # owner = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=2000) #Limit?
    datetime_created = models.DateTimeField(default=timezone.now, editable=False)
    datetime_edited = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    #Likes/dislikes?

    def __str__(self):
        return self.title
    # Overload save method. copy pasted
    # def save(self, *args, **kwargs):
    #     # if not self.id:
    #     #     self.datetime_created = timezone
    #     self.datetime_edited = timezone.now()
    #     return super(ForumThread, self).save(*args, **kwargs)

    # Adds new attributes to model: thread_ratings_count_positive, thread_ratings_count_negative
    def sum_count_ratings(self):
        thread_ratings = Rating.objects.filter(thread=self)
        self.thread_ratings_count_positive = sum(i.thumps_up == 1 for i in thread_ratings)
        self.thread_ratings_count_negative = sum(i.thumps_up == 0 for i in thread_ratings)

        # Attributes are added to the ForumThread model, no viewmodel is needed
        # self.thread_ratings_count_positive = thread_ratings_count_positive
        # self.thread_ratings_count_negative = thread_ratings_count_negative
        # return self  # Do not return anything?


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

    # Adds new attributes to model: comment_ratings_count_positive, comment_ratings_count_negative
    def sum_count_ratings(self):
        comment_ratings = Rating.objects.filter(comment=self)
        self.comment_ratings_count_positive = sum(i.thumps_up == 1 for i in comment_ratings)
        self.comment_ratings_count_negative = sum(i.thumps_up == 0 for i in comment_ratings)


class Rating(models.Model):
    # likes = models.IntegerField()
    # dislikes = models.IntegerField()
    thumps_up = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.thread.title + str(self.thumps_up)
