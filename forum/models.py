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

    # def add_ratings_count(self):
    #     thread_ratings = Rating.objects.filter(thread=self)
    #     thread_ratings_count_positive = sum(i.thumps_up == 1 for i in thread_ratings)
    #     thread_ratings_count_negative = sum(i.thumps_up == 0 for i in thread_ratings)
    #
    #     # Attributes are added to the ForumThread model, no viewmodel is needed
    #     self.thread_ratings_count_positive = thread_ratings_count_positive
    #     self.thread_ratings_count_negative = thread_ratings_count_negative
    #     return self

#Viewmodel is needed to help display ratings when many ForumThreads has to be displayed(for example in allthreads.html)
# class ForumThreadViewModel:
#     def __init__(self, topic, title, owner, datetime_created, views_count, likes_count, dislikes_count):
#         self.topic = topic
#         self.title = title
#         self.owner = owner
#         self.datetime_created = datetime_created
#         self.views_count = views_count
#         self.likes_count = likes_count
#         self.dislikes_count = dislikes_count


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


class Rating(models.Model):
    # likes = models.IntegerField()
    # dislikes = models.IntegerField()
    thumps_up = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.thread.title + str(self.thumps_up)
