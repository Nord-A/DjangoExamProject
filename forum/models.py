from django.db import models
from django.utils import timezone


class ForumUser(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    # email = models.CharField(max_length=30)
    email = models.EmailField()
    datetime_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    # image = models.ImageField()

    def __str__(self):
        return self.username


class Topic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ForumThread(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    question = models.TextField(max_length=2000) #Limit?
    datetime_created = models.DateField()
    datetime_edited = models.DateField()
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(max_length=2000) #Limit?
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, null=True)
    datetime_created = models.DateTimeField(default=timezone.now)
    datetime_edited = models.DateTimeField(default=timezone.now)
    #Can a comment be commented on?

    def __str__(self):
        return self.content


class Rating(models.Model):
    thumps_up = models.BooleanField()
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.thumps_up
